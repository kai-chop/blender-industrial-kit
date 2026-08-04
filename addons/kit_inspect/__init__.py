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

  kit.mold_check        doc 04 states the moulding grammar (draft 0.5-3 deg by process, uniform
                        1-3 mm wall, no undercuts) but nothing measured whether a model obeyed
                        it, and the extension catalogue has no draft/undercut/thickness tool at
                        all. Thresholds are doc 04's published ranges, exposed as parameters.

All three are callable from `bpy.ops` under `--background`, print machine-readable lines to
stdout, and never modify mesh data. `frame_feature` is the only one that writes anything, and
only to a camera's transform / lens.
"""

import math

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from mathutils.bvhtree import BVHTree

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


class KIT_OT_mold_check(bpy.types.Operator):
    """Draft angle, undercuts and wall thickness against a pull direction"""

    bl_idname = "kit.mold_check"
    bl_label = "Mold Check"
    bl_options = {"REGISTER"}

    prefix: bpy.props.StringProperty(name="Name prefix", default="")
    axis: bpy.props.EnumProperty(
        name="Pull axis",
        description="Direction the mold halves separate along",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")],
        default="Z",
    )
    # Defaults are the published ranges in kit doc 04, not numbers invented here:
    # draft — sand casting 1-3 deg, die casting 0.5-2, injection 0.5-2;
    # wall  — injection moulding 1-3 mm, and uniform is the point, not the absolute value.
    min_draft: bpy.props.FloatProperty(name="Minimum draft (deg)", default=1.0, min=0.0, max=45.0)
    wall_min: bpy.props.FloatProperty(name="Minimum wall (m)", default=0.001, min=0.0)
    wall_max: bpy.props.FloatProperty(name="Maximum wall (m)", default=0.003, min=0.0)

    def execute(self, context):
        targets = resolve_targets(context.scene, self.prefix)
        if not targets:
            self.report({"ERROR"}, "no mesh objects match prefix %r" % self.prefix)
            return {"CANCELLED"}

        pull = Vector((1.0 if self.axis == "X" else 0.0,
                       1.0 if self.axis == "Y" else 0.0,
                       1.0 if self.axis == "Z" else 0.0))
        depsgraph = context.evaluated_depsgraph_get()
        failures = 0
        for obj in targets:
            report = inspect_mold(obj, depsgraph, pull, self.min_draft,
                                  self.wall_min, self.wall_max)
            if report is None:
                continue
            flat, undercut, thin, thick, worst_draft, wall_lo, wall_hi = report
            bad = flat + undercut + thin + thick
            failures += bad
            print("%s mold %-16s axis=%s  under-drafted=%d  undercut=%d  wall<%.3f=%d  "
                  "wall>%.3f=%d  worst_draft=%.2fdeg  wall=[%.4f,%.4f]"
                  % (TAG, obj.name, self.axis, flat, undercut, self.wall_min, thin,
                     self.wall_max, thick, worst_draft, wall_lo, wall_hi))

        summary = "%d face(s) fail draft/undercut/wall across %d object(s)" % (
            failures, len(targets))
        print("%s mold summary: %s" % (TAG, summary))
        self.report({"WARNING"} if failures else {"INFO"}, summary)
        return {"FINISHED"}


def inspect_mold(obj, depsgraph, pull, min_draft, wall_min, wall_max):
    """Per-face mold diagnosis for one object, in world space.

    Draft is the angle between a face and the parting plane, so a face parallel to the pull
    direction has zero draft and cannot release: draft = asin(|normal . pull|).

    A face releases only if nothing else on the part sits between it and the outside along its
    own half's pull direction — that occlusion test is what separates a real undercut from a
    merely steep face, and it needs a ray, not a normal.

    Wall thickness is the distance from a face inward to the first surface it meets, which is
    what "uniform wall" in doc 04 actually constrains.
    """
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    if mesh is None or not mesh.polygons:
        if mesh is not None:
            evaluated.to_mesh_clear()
        return None

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.transform(obj.matrix_world)
    bm.faces.ensure_lookup_table()
    tree = BVHTree.FromBMesh(bm)

    # Offset ray origins off the surface so a face never reports hitting itself.
    epsilon = max(bm.calc_volume(signed=False) ** (1.0 / 3.0), 1e-4) * 1e-3
    flat = undercut = thin = thick = 0
    worst_draft = 90.0
    wall_lo, wall_hi = float("inf"), 0.0

    for face in bm.faces:
        normal = face.normal
        if normal.length_squared == 0.0:
            continue
        normal = normal.normalized()
        centre = face.calc_center_median()

        draft = math.degrees(math.asin(min(abs(normal.dot(pull)), 1.0)))
        worst_draft = min(worst_draft, draft)
        if draft < min_draft:
            flat += 1

        release = pull if normal.dot(pull) >= 0.0 else -pull
        if tree.ray_cast(centre + normal * epsilon, release)[0] is not None:
            undercut += 1

        hit, _, _, distance = tree.ray_cast(centre - normal * epsilon, -normal)
        if hit is not None:
            wall_lo = min(wall_lo, distance)
            wall_hi = max(wall_hi, distance)
            if distance < wall_min:
                thin += 1
            elif distance > wall_max:
                thick += 1

    bm.free()
    evaluated.to_mesh_clear()
    if wall_lo == float("inf"):
        wall_lo = 0.0
    return flat, undercut, thin, thick, worst_draft, wall_lo, wall_hi


CLASSES = (KIT_OT_camera_coverage, KIT_OT_frame_feature, KIT_OT_part_census, KIT_OT_mold_check)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
