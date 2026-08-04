"""Kit Inspect — three headless checks that answer questions renders alone cannot.

Each operator exists because a real build shipped a defect that the existing gates passed:

  kit.camera_coverage   A model change was reported twice as "looks identical" because the part
                        that changed sat outside the camera frame: an orthographic camera was
                        left at scale 6.6 while the object had grown to 7.15 m. Nothing in the
                        render says "the thing you are looking for is off-frame" — this does.

  kit.frame_feature     A judged feature was declared "visually confirmed" while spanning a few
                        pixels. Sizing a camera by eye does not guarantee a decidable image;
                        this frames a target to a requested fill and reports the pixel span, so
                        "too small to judge" becomes a number instead of an impression.

  kit.part_census       A part count was wrong against the reference drawing for three build
                        cycles. Counting by name prefix is one command, and the count is what
                        gets compared to the drawing.

All three are callable from `bpy.ops` under `--background`, print machine-readable lines to
stdout, and never modify mesh data. `frame_feature` is the only one that writes anything, and
only to a camera's transform / lens.
"""

import math

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

TAG = "[kit-inspect]"


# --------------------------------------------------------------------------------------
# geometry helpers — pure, no operator context, so scripts can import them directly
# --------------------------------------------------------------------------------------

def world_corners(obj):
    """The eight world-space corners of an object's local bounding box."""
    return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]


def resolve_targets(scene, pattern):
    """Mesh objects whose name starts with `pattern`; empty pattern means the whole scene."""
    return [obj for obj in scene.objects
            if obj.type == "MESH" and (not pattern or obj.name.startswith(pattern))]


def coverage(scene, camera, points):
    """(inside_fraction, u_range, v_range) for `points` seen by `camera`.

    world_to_camera_view returns normalised frame coordinates: 0..1 spans the rendered image on
    each axis, z is distance in front of the camera. A point is visible when both axes are in
    0..1 and z > 0. The ranges are returned even when everything is inside, because how much of
    the frame a feature fills is the thing `frame_feature` acts on.
    """
    us, vs, inside = [], [], 0
    for point in points:
        ndc = world_to_camera_view(scene, camera, point)
        us.append(ndc.x)
        vs.append(ndc.y)
        if 0.0 <= ndc.x <= 1.0 and 0.0 <= ndc.y <= 1.0 and ndc.z > 0.0:
            inside += 1
    return inside / len(points), (min(us), max(us)), (min(vs), max(vs))


def pixel_span(scene, u_range, v_range):
    """How many rendered pixels the framed extent spans, at the scene's current resolution."""
    scale = scene.render.resolution_percentage / 100.0
    width = scene.render.resolution_x * scale
    height = scene.render.resolution_y * scale
    return (u_range[1] - u_range[0]) * width, (v_range[1] - v_range[0]) * height


# --------------------------------------------------------------------------------------
# operators
# --------------------------------------------------------------------------------------

class KIT_OT_camera_coverage(bpy.types.Operator):
    """Report, per camera, whether the target objects are actually inside the frame"""

    bl_idname = "kit.camera_coverage"
    bl_label = "Camera Coverage"
    bl_options = {"REGISTER"}

    prefix: bpy.props.StringProperty(
        name="Name prefix",
        description="Only objects whose name starts with this are checked; empty means all",
        default="",
    )
    camera: bpy.props.StringProperty(
        name="Camera",
        description="Camera to check; empty means every camera in the scene",
        default="",
    )

    def execute(self, context):
        scene = context.scene
        targets = resolve_targets(scene, self.prefix)
        if not targets:
            self.report({"ERROR"}, "no mesh objects match prefix %r" % self.prefix)
            return {"CANCELLED"}

        cameras = ([bpy.data.objects[self.camera]] if self.camera
                   else [obj for obj in scene.objects if obj.type == "CAMERA"])
        if not cameras:
            self.report({"ERROR"}, "no camera in the scene")
            return {"CANCELLED"}

        points = [corner for obj in targets for corner in world_corners(obj)]
        partial = 0
        for cam in sorted(cameras, key=lambda c: c.name):
            fraction, u_range, v_range = coverage(scene, cam, points)
            span_x, span_y = pixel_span(scene, u_range, v_range)
            verdict = "FULL" if fraction == 1.0 else ("NONE" if fraction == 0.0 else "CLIPPED")
            if fraction < 1.0:
                partial += 1
            print("%s coverage %-16s %-7s inside=%5.1f%%  u=[%.2f,%.2f] v=[%.2f,%.2f]  "
                  "span=%.0fx%.0fpx" % (TAG, cam.name, verdict, fraction * 100,
                                        u_range[0], u_range[1], v_range[0], v_range[1],
                                        span_x, span_y))
        summary = "%d of %d camera(s) do not fully contain %d object(s)" % (
            partial, len(cameras), len(targets))
        print("%s coverage summary: %s" % (TAG, summary))
        self.report({"WARNING"} if partial else {"INFO"}, summary)
        return {"FINISHED"}


class KIT_OT_frame_feature(bpy.types.Operator):
    """Aim and size a camera so a feature fills the frame enough to be judged"""

    bl_idname = "kit.frame_feature"
    bl_label = "Frame Feature"
    bl_options = {"REGISTER", "UNDO"}

    prefix: bpy.props.StringProperty(name="Name prefix", default="")
    camera: bpy.props.StringProperty(name="Camera", default="")
    fill: bpy.props.FloatProperty(
        name="Fill",
        description="Fraction of the frame's shorter axis the feature should span",
        default=0.6, min=0.05, max=1.0,
    )
    min_pixels: bpy.props.IntProperty(
        name="Minimum pixels",
        description="Report an error if the framed feature still spans fewer pixels than this",
        default=200, min=1,
    )

    def execute(self, context):
        scene = context.scene
        targets = resolve_targets(scene, self.prefix)
        if not targets:
            self.report({"ERROR"}, "no mesh objects match prefix %r" % self.prefix)
            return {"CANCELLED"}

        cam = bpy.data.objects.get(self.camera) or scene.camera
        if cam is None or cam.type != "CAMERA":
            self.report({"ERROR"}, "no usable camera (%r)" % self.camera)
            return {"CANCELLED"}

        points = [corner for obj in targets for corner in world_corners(obj)]
        centre = sum(points, Vector()) / len(points)
        radius = max((point - centre).length for point in points)
        if radius == 0.0:
            self.report({"ERROR"}, "target has no extent")
            return {"CANCELLED"}

        # Keep the camera's direction; only its distance (or ortho scale) and aim change, so a
        # deliberately chosen viewing angle survives being framed properly.
        forward = (cam.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))).normalized()
        extent = 2.0 * radius / self.fill
        if cam.data.type == "ORTHO":
            cam.data.ortho_scale = extent
            cam.location = centre - forward * max(extent, radius * 4.0)
        else:
            half_fov = cam.data.angle / 2.0
            distance = (extent / 2.0) / max(math.tan(half_fov), 1e-6)
            cam.location = centre - forward * distance
        cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
        context.view_layer.update()

        fraction, u_range, v_range = coverage(scene, cam, points)
        span_x, span_y = pixel_span(scene, u_range, v_range)
        smallest = min(span_x, span_y)
        print("%s frame %s -> %s  inside=%5.1f%%  span=%.0fx%.0fpx  (min_pixels=%d)"
              % (TAG, self.prefix or "<all>", cam.name, fraction * 100,
                 span_x, span_y, self.min_pixels))
        if smallest < self.min_pixels:
            message = "framed feature spans only %.0fpx (want >= %d) — raise resolution or fill" % (
                smallest, self.min_pixels)
            print("%s frame VERDICT too-small: %s" % (TAG, message))
            self.report({"WARNING"}, message)
        else:
            print("%s frame VERDICT ok" % TAG)
            self.report({"INFO"}, "framed %s at %.0fx%.0fpx" % (cam.name, span_x, span_y))
        return {"FINISHED"}


class KIT_OT_part_census(bpy.types.Operator):
    """Count objects by name prefix — the number to compare against the reference drawing"""

    bl_idname = "kit.part_census"
    bl_label = "Part Census"
    bl_options = {"REGISTER"}

    separator: bpy.props.StringProperty(
        name="Separator",
        description="Prefix is the part of the name before the last occurrence of this",
        default="_",
    )

    def execute(self, context):
        counts, triangles = {}, {}
        depsgraph = context.evaluated_depsgraph_get()
        for obj in context.scene.objects:
            if obj.type != "MESH":
                continue
            key = obj.name.rsplit(self.separator, 1)[0] if self.separator in obj.name else obj.name
            counts[key] = counts.get(key, 0) + 1
            triangles[key] = triangles.get(key, 0) + count_triangles(obj, depsgraph)

        for key in sorted(counts):
            print("%s census %-14s %4d  %7d tri" % (TAG, key, counts[key], triangles[key]))
        total = sum(counts.values())
        print("%s census total: %d object(s) in %d group(s), %d tri"
              % (TAG, total, len(counts), sum(triangles.values())))
        self.report({"INFO"}, "%d object(s) in %d group(s)" % (total, len(counts)))
        return {"FINISHED"}


def count_triangles(obj, depsgraph):
    """Triangle count of the evaluated mesh — modifiers included, originals untouched."""
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    if mesh is None:
        return 0
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    total = len(bm.faces)
    bm.free()
    evaluated.to_mesh_clear()
    return total


CLASSES = (KIT_OT_camera_coverage, KIT_OT_frame_feature, KIT_OT_part_census)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
