# 12 — Photo-mastered modelling: building a real product from photographs

骨格対抗案: a chronological case write-up (GT then Kink) vs a stage-ordered procedure with the two cases as evidence rows → stage-ordered (the reader is starting a third product and wants the next step, not the history; the cases become the numbers that justify each rule).

Written 2026-10-07 from two complete builds: the GT Street Performer 29 (`output/gt-performer-29/`, four versions over three days, 42 gate lines) and the Kink Gap 2023 BMX (`output/kink-gap-2023/`, one day, three modeler rounds, 20 gate lines). Every rule below carries the measurement that produced it. Stages follow the pipeline in `~/.claude/skills/blender-engineering/SKILL.md`; this doc is the domain knowledge for the case where **the requirement source is a set of photographs of an existing product**.

## 要点（日本語・10 行）
1. 最初に**最大解像度の公式写真**を取る（店の写真や画面キャプチャは最後の手段）。消えたページは Wayback で。Shopify の CDN は接尾辞なしが最大（2048）。
2. 縮尺は**ホイールの円フィット**（縁の点 16 以上・残差を記録）と**公式の既知長 1 本**で決める。目測のハブ位置で始めた v1 は全体が 7 % ずれた。
3. 写真と公式表が食い違ったら**写真を採り、食い違いを表に残す**（ユーザー裁定「裁定は写真に寄せる」）。縮尺を取り直して辻褄を合わせない。
4. ランドマークは**固定のキー名リスト**で頼み、各点に許容 px・弦は 4 倍クロップか副画素プローブ・未解決は理由つきで返させる。重ね図 PNG を人が見る。
5. 側面写真が与えないもの（横幅・バックスイープと転がりの分離・手前側のパララックス）は **[要確認] か camera-limited** と明記し、ゲートの上限を広げて通す（上限を黙って上げない＝シートに理由を書く）。
6. 斜め写真から**角度を読まない**（視線が回転軸に直交している時だけ）。レバー角 38° の誤読で 1 往復、GT では 4 往復失った。
7. シートの行は全部 **出典印**（src:photo／src:spec／src:std）。出典のない行は造形に渡さない。
8. ゲートは「写真残差（クラス別 mm）・厚み・重ね合わせ・干渉・決定性・再 import・接地原点・リグ」。緑でも**クローズアップを main が開く**（never-list は欠陥を拾い、粗さは拾わない）。
9. 委譲は 調査(opus)→ランドマーク(sonnet)→シート(main)→造形(opus)。造形 1 往復 30〜60 万 tok。往復の間に**生成物の退避**を取る。
10. 納品は FBX（接地面原点・平ら）＋ GLB（リグ階層）＋ 製図 ＋ 日本語 README/HANDOFF。CSP の実機確認は本人に 2 分テストを渡す。

## 1. Source acquisition (before any geometry)

| Rule | Evidence |
|---|---|
| Fetch the manufacturer's product page first; if it is gone, the Wayback Machine usually has it with the CDN images intact | Kink: live page 404, archived 2022-11-28 page gave 8 × 2048 px images + fork offset 32 mm (dossier §0) |
| Shopify CDN: the unsuffixed file is the largest; `_4096x4096` and `?width=` return the same 2048 | measured 2026-10-07 |
| Shop/retailer photos are a fallback (1200 px); user screenshots are the last resort | GT v1 built on a 695 px screenshot: 7 % scale error in every number (HANDOFF §7) |
| Also fetch the **part** pages (pedal, stem, saddle, bar, tyre) — they carry rulers (100 × 100 platform, Ø22.2 bore) and lateral sizes no side photo gives | GT v4 §B: pedal and stem cages solved from part photos with the part page ruler |
| Record pixel sizes with PIL and the source URL per image in `reference/README.md` or the dossier | both projects |
| Identify the colour from the official swatch, not from the lit frame | Kink: swatch (101,81,76) vs lit frame (157,149,147) |

## 2. Authority order (fix it in writing before measuring)

1. The user's words (what is wanted) — verbatim in the requirement register.
2. The photo (what the product looks like) — **wins over the catalogue** wherever they disagree. User ruling 2026-10-05 「裁定は写真に寄せる」; applied to GT tube heights, bar tilt, crank length (182 vs 170) and to Kink BB height (312 vs 294.6), effective TT (549 vs 521), crank (180 vs 170).
3. The catalogue/spec — binding only where the photo is silent (lateral sizes, tooth counts, angles the photo cannot separate).
4. Convention — tagged `[要確認]`, never promoted to a gate.

Never average a photo value with a spec value, and never re-anchor the scale to make a spec number come true. Write the misses in a `§0` of the photo-residual table.

## 3. Scale and datums

- **Circle-fit both wheels** on the rim's inner edge (and the tyre outer edge as a second fit): ≥ 16 edge points around the full circle, least squares, report centre, radius and RMS. Kink: RMS 0.4–1.1 px on 2048 px; the two rim radii agreed to 1–1.5 px. Partial arcs (< 170°) give a weak centre — use the fixed centre from the full-circle fit and take only the radius.
- **Anchor the scale on one published length between two fitted/centre-picked points** in the centre plane: GT used the wheelbase (hub to hub, 1119), Kink the chainstay (BB centre to rear wheel centre, 336.55). Then **cross-check** with two or three other published numbers (BB height, effective TT, tyre OD) and report each miss with its band; a miss outside the band is recorded, not corrected (§2).
- Both axles take the **mean fitted height** (3–5 px difference in the fits is pick noise; coplanar tyres pass the wobble gate).
- Near-side parts show **parallax**: the axle nut sat 12 px (GT 14 px) outside the fitted wheel centre. Axle datums come from the fits; nuts, hub caps, rotors and cassettes are drawn around them, never used as centres.
- Ground = axle z − tyre R; the FBX for CSP is exported with the ground at the origin (CSP drops the shadow on the plane through the origin; measured 2026-10-06), the .blend keeps the BB origin.

## 4. Landmark protocol (what to ask the measuring agent for)

- A **fixed key list** with exact names; `params.py` and the photo gate read the keys, so a free-form file costs a renaming round (GT lost a round on `dims.json` keys).
- Entry forms: point `[x, y, tol_px]` with the tolerance the picker believes; bbox `[x0, y0, x1, y1]`; chord = px perpendicular to the member unless the key says `_vchord`.
- Chords on 4× grid crops (`tools/grid_any.py`) or sub-pixel threshold probes (`tools/lineprobe.py`), never by eye on the full frame.
- `_meta` with image, size, axis convention and a notes list; `_unresolved` with a reason per key (occluded / out of frame / too small). 17 of 156 Kink keys were unresolved and said why.
- An **overlay PNG** of every pick on the master photo, read by main before anything is built.
- Curves (cables, saddle profile) as ordered point arrays; a brake cable needed 26 points to stay within 3 px.
- Count what can be counted (spokes 36/36, cross pattern 3 from spoke drift 1.2–1.9° vs 1.7° predicted).
- **Before a point is used as a position, write what it is the projection of.** Parts that extend laterally (lever blade, pedal top face, bar/grips) give only visibility or height constraints in a side photo. GT lost four ruling rounds (lever rev2 → rev5-b) to a blade-tip landmark that was an end face; the fix was a 25 mm "visibility" limit instead of a position row.

## 5. What a single side photo cannot give — and what to do instead

| Missing | Handling | Evidence |
|---|---|---|
| Lateral sizes (hub widths, rim width, Q-factor, chainline, saddle width, stem width) | `[要確認]` conventions; part photos with a ruler where they exist | both projects |
| Backsweep vs. roll of a handlebar | camera-limited rows: the two grips image 90 px (66 mm) apart vertically on a 2048 px side photo (near one higher); widen the grip rows' limit to ±(half that + pick tol) and say so in the residual table | Kink §9-rev (limit 40); GT bar rows frozen at 25 px on the 3/4 camera |
| Oval vs. round tubes | vertical chord vs. perpendicular chord ratio ≠ 1/cos(tilt) flags an oval | GT TT ovalized 36/44/42 |
| Chainstay taper | chords at 3+ stations, not two end values; the Kink stay is constant to 60 % then tapers | Kink A4 |
| Rear view of a saddle | derive the section (flat top, rolled edge R, quarter-ellipse flank with G1 at both ends, base 0.6 of the width) and label the constants `[要確認]`; user asked for exactly this derivation | GT v4 §D/§D2-rev |
| 3/4 form | DLT camera on the official 3/4 photo, ≥ 10 points **including 3–4 known points off the centre plane**, keep the skew term (dropping it cost 45 px) | GT `camera_34.json` RMS 7.6–8.9 px; v4 §F failed for a sibling model with no off-plane points |
| Lifestyle / wide-angle photos | do not use for metrics: the DLT skew solution degenerates and known lengths are not reproduced | GT v4 §A (saddle 261 / crank 182 not recovered) |
| Two-circle wheel calibration from a user screenshot | only when **both wheels are fully in frame**; the radius-equality control detects a cut wheel in one step | GT R17 (diameter ratio 2.09 → rejected) |
| Close-range small screenshots (130–250 px parts) | weak-perspective models fail; two rulers disagreeing 2.7× is the detector | GT R15 |
| Tread, knurl, logos' fine print | texture / Tier B; large lettering as text-object meshes wrapped on the tube (arialbd, 12° shear) | Kink Decal_DT |

## 6. Angles from photographs

Read an angle only when the viewing direction is perpendicular to the rotation axis of that angle. The Kink lever: a product photo taken from above-behind showed a blade chord of ~38° in the image; the modeler measured ~5° in that projection and the built 38° produced a 76 mm hook. GT's lever R19 reference (user screenshot) was read the same way and took 4 rounds. Write the angle as **two offsets of the tip from a datum axis** (ahead / below the grip axis: GT 28/43, Kink 25/35) and let the plan angle be derived; a third constraint over-determines it (Kink: pivot already 42 mm ahead, so "+10° splay" was impossible).

## 7. Engineering-sheet discipline specific to photo mastering

- Every PARAMS row: value + `src:photo` (landmark key) / `src:spec` (page) / `src:std` `[要確認]`. An uncited row is not specified; it goes back as a question.
- Expectation bands on every cross-check (BB height ±8, HT angle ±1.5°…) and the sentence "a miss keeps the photo value and is logged".
- Pre-declare the gate limits per class (frame/wheel ≤ 6 mm, cockpit/seat/drivetrain/accessory ≤ 10 mm, camera-limited rows explicit).
- Known contract traps (each cost a round once, twice for the first):
  - the kit's BOM/interference prefix is `name.rsplit("_", 1)[0]`, so `Cable_RB_a` counts as `Cable_RB` — write the whitelist with the prefixes the kit will see (GT §I-rev2, Kink A7);
  - "parallel" and "4° lean" in one row; "L = R rotated 180° about y" leaves both arms on one side; a pin layout that sums to 12 under a binding "14";
  - "bit-identical matrices" is unattainable in float32 (1.49e-8 m measured) — assert ≤ 1e-6 m;
  - section laws without end-point + tangent conditions crease (GT §D first draft).
- Freeze the mesh count only after the first green build; three scripts carry it (dims, FBX re-import, rig check).

## 8. Gates that matter for a photo-mastered build (all in fresh processes, none in the generator)

1. **Photo residual gate**: model side-plane points → render px → photo px with the overlay's own mapping; Δ mm per row, class limits, `scanned=N` alive line, exit 1 on zero rows. GT 30 rows / Kink 35 rows; a typical green run reads frame ≤ 2.6 mm.
2. **Thickness audit**: model silhouette chord vs. photo chord at named stations (TT ×3, DT ×3, ST, SS, CS, fork ×3, seatpost, bar, crank, grip), ≤ 4 mm; the station must sample the model part's own axis when the camera-limited part moved (Kink A65).
3. **Overlay**: 50 % blend of the ortho side render on the master photo, hubs aligned — **read by main**. This is the one picture that shows whether the silhouette is right.
4. **Closeups** of the hand-sized parts (stem, lever+grip, brake, crank+pedal, seat, dropout) — read by main. Gates green + never-list clean still shipped a tube-lever and a box-pedal in Kink round 1; coarseness is only visible here.
5. Interference with a declared whitelist, BOM census, dims asserts, determinism (build twice, snapshot compare), FBX re-import count + bbox, FBX ground z = 0, rig check (pivots ±0.5 mm, membership, pose test, FBX flat, GLB nodes).
6. Paint check for anything browser-side: count distinct colours in a canvas downsample (the GT viewer shipped with zero render calls).

## 9. Organic and cast parts from part photos

- Sub-D cages (level 2) sized by a ruler in the part photo: scaled-orthographic axis scales from a known square (pedal platform 100 × 100 → 8.0/9.0 px/mm) or a known bore (stem Ø22.2 ellipse 182 × 100 px → 12.1/15.1/11.1 px/mm). Measure end faces for thickness: a side photo taken above the part shows its top face as a band and inflates the height.
- Saddles: side profile from the bike photo (top/bottom polylines, 10+ stations), plan from a product top/3-4 photo as **fit-by-eye with a silhouette residual** (GT §G5: BKW 49 → 23.5 px) and say "fit, not measured".
- Pedals: windows, concave faces, pins laid out from the top-face photo; bottom face mirrored `[要確認]`.
- Levers: hinged clamp ring + Bezier blade swept with width/thickness tapers, tip curl, end paddle; angle per §6.
- Keep cushions solid (user ruling 2026-10-06) — no cut-outs for polygon savings.

## 10. Delegation pattern and costs (2026-10-07, Opus 5.5 / Sonnet 5.5 subagents)

| Step | Agent | Brief carries | Returns |
|---|---|---|---|
| Dossier | blender-dossier (opus) | known facts, photo list, task list, "no invented numbers" | `DOSSIER:` path, `IMAGES:` table, `OPEN:` list — ~180k tok |
| Landmarks | implementer (sonnet) | master photo, fixed key list, method §4 | `LANDMARKS:`/`COUNT:`/`FITS:`/`OVERLAY:`/`UNRESOLVED:` — ~200k tok |
| Sheet | main | — | the contract (§7) |
| Build | blender-modeler (opus) | pointer brief: reading order, reuse rules, return labels; say whether delivery is in scope | `GATES:` verbatim, `COUNT:`, `SHA:`, `PHOTO:`, `RENDERS:` + sweep, `ASSUMPTIONS:` file, `CONTRACT_ERRORS:` file:line — 560k (round 1), 330k (round 2), 370k (round 3) tok |

- Brief length does not drive the cost; the generator (1.9–2.6k lines) re-read per turn does. Keep rounds few and rulings batched in a sheet section (§9) rather than chat.
- **Snapshot between rounds** (copy generator + renders to `round_N/`): `output/` is gitignored and round 1 of Kink was overwritten.
- A fresh agent per round was cheaper than resuming a 560k-token agent; continuing the same agent was right for a small round (lever angle).
- Agent `model=` accepts aliases only (`opus`/`sonnet`/`haiku`/`fable`).

## 11. One-page checklist

- [ ] Largest official photos found (Wayback if needed), sizes recorded, part pages fetched
- [ ] Requirement register with the user's words verbatim and the authority order written
- [ ] Wheels circle-fitted (RMS reported); scale anchored on one published length; cross-checks reported with bands
- [ ] Landmark JSON with fixed keys, tolerances, unresolved list; overlay PNG read by main
- [ ] Sheet: every row sourced; camera-limited rows named with their widened limit and reason; kit prefix rule respected in the whitelist
- [ ] Angles of lateral parts expressed as tip offsets, not degrees read off an oblique photo
- [ ] Build: gates green → main opens overlay + closeups → fidelity round with batched rulings → snapshot
- [ ] Deliver: FBX ground-origin flat + GLB with rig + drawings + README/HANDOFF (JP); sha match canon ↔ delivery; one real run from the delivery folder
- [ ] Hand the user the 2-minute CSP test (drag glb, rotate `Rig_Steer`)
