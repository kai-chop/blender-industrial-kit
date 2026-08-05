# blender-engineering — rule registry

`SKILL.md` holds only the operative text, tagged with the IDs below. This file holds where each rule
came from. Keeping them apart is what makes the skill **editable instead of accreting**: an incident
adds a registry row, never a paragraph of story to SKILL.md.

## Status and what it licenses

| status | meaning | may be enforced as a pass/fail gate? |
|---|---|---|
| `user` | the user stated or confirmed it | **yes** |
| `claude` | an inference — a working default | **no.** Advisory only. To gate it, show it to the user and get `user` status first |
| `retired` | withdrawn or superseded | no — and its line is deleted from SKILL.md |

Two hard constraints on this file:

1. **Never write a `claude` row as though it were `user`.** Guessing a number (angle, margin,
   tolerance) and letting it reach a gate or a handoff document is the failure this registry exists
   to stop.
2. **Retiring is deletion, not annotation.** Flip the status here, delete the line from SKILL.md.
   Do not leave "formerly we did X because Y" behind — that is the rot.

Source quotes are kept in the user's own words, untranslated: a decision paraphrased is a decision
distorted.

## Registry

| id | status | rule | source | date |
|---|---|---|---|---|
| U1 | user | In requirement space the user's words and drawings are the ground truth; no measurement outranks them | 「機械の判定を理由に実測ですらないこちらの言葉を無視する」「userが作ってほしい形状の話,modで言えば望む挙動の話だ」 | 2026-08-04 |
| U2 | user | New reference material governs its whole extent; re-derive it all, demote earlier readings | 「なんで…使うパーツの具体形状まで出したのに…全部守れなかったの」 | 2026-08-04 |
| U3 | user | Conflicting references → ask, never invent a compromise | standing instruction | 2026-07 |
| U4 | user | Criticism is input to the user's decision, never licence to substitute a different shape | 「無批判な同意はこちらも望まない,適切な批判対案大いにけっこうだが,動いて欲しい挙動を無視して違う挙動を正解と言われても制作意図が無視されるのだから意味不明だ」 | 2026-08-04 |
| U5 | user | Never gate on anything the user has not confirmed; never invent values to fill a spec blank | 「こちらが正解と言ってないものを勝手にゲート化するのもやめて」 | 2026-08-04 |
| U6 | user | Gate expectations are transcribed from the requirement source with per-criterion citations | 「説明のまんまにしてね」＋ a self-certifying gate passed 65/65 while shipping 3 requirement violations | 2026-08-04 |
| U7 | user | A green gate disagreeing with the user's words means the gate is stale — fix the gate | same as U6 | 2026-08-04 |
| U8 | user | Whoever produced a render opens it before handing it over. "Exit 0" / "the file exists" is not a visual check | standing quality rule (run the real path and look at the actual object — never stop at "it started" / "non-empty") + never-list #14 | 2026-08-05 |
| C1 | claude | Write a requirement register before Stage 0 | inference from U1/U2. Never used as a gate | 2026-08-04 |
| C2 | claude | Prefer shape conditions over boolean ones (the values themselves stay U5) | inference from the 28°-slit failure | 2026-08-04 |
| C3 | claude | Render each judged feature large enough to decide before claiming visual confirmation | inference | 2026-08-04 |
| C4 | claude | Run the part census against the source image, not only the sheet | inference | 2026-08-04 |
| C5 | claude | The builder's own look is bounded to objective defects (never-list 1–6) and reports a defect list or "none found" — never "looks good", never requirement conformance | inference bounding U8 so it cannot grow into the self-certifying gate U6/U7 exist to stop | 2026-08-05 |

## Incident pointers (not rules)

Full accounts live in the operator's own ledgers, never in SKILL.md. On the origin machine:
`~/.claude/ledgers/trouble-classes.md`「要求空間の権威逆転」and `~/.claude/ledgers/user-incidents.md`
(2026-08-04, ring fittings).
