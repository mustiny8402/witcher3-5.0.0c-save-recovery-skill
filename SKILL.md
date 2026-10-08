---
name: witcher3-save-recovery
description: Diagnose Witcher 3 Remastered PC saves and create verified recovery copies for facts string encoding expansion and LZ4 chunk table overlap. Use for corrupted or abnormally inflated .sav files, paired save comparison, or a CDPR evidence report. Repair requires a matching supported profile and a suitable donor save.
---

# Witcher 3 save recovery

Preserve the latest game state in a separate recovery candidate. Distinguish a valid file structure from an actual successful game load and later save stability.

## Diagnose before repair

Read [the format and repair profile](references/format-and-repair.md) when analyzing a save or deciding whether the bundled repair applies. Read [the confirmed case](references/confirmed-case.md) when comparing symptoms or explaining prior evidence; it is one case, not a universal corruption threshold.

The helper requires Python and `lz4`. Use an isolated environment or `uv run --with lz4`, without changing global Python packages.

```powershell
uv run --with lz4 python scripts/w3save.py analyze --source '<full save path>' --output '<new analysis JSON path>'
```

Record source SHA-256 before and after. Inspect matching JSON for build ID, saveVersion, gameVersion and recorded mod count. A mod count of zero does not establish lifetime absence of mods. Thumbnail integrity does not establish save integrity.

Check magic, declared chunk table extent, data offset, computed EOF, each independent raw LZ4 block, permitted final zero sentinel, serialization footer and indexes where bytes are available. An unavailable first block is not evidence that its decoded SAV3 header was absent. Small saves can already contain expanding identifiers.

## Create a recovery candidate

Run repair only when the user requests modification or recovery. Diagnosis alone does not authorize it. Existing authorization for an experimental recovery is sufficient; do not add a repeated confirmation step.

The bundled repair supports the observed PC saveVersion 66 / gameVersion 29 profile with 266 chunks, data offset 3084, 124 bytes of table overlap, and only chunk 0 failing. It requires a 128-byte donor prefix and a valid surviving LZ4 sequence at compressed offset 128. Other profiles need fresh analysis and an adapted procedure; the helper rejects them.

Use a donor from the same playthrough and version. Prefer the most recent structurally readable save. A donor supplies only lost header bytes, not quest, inventory or world data. Explain that the original magic_number and runtimeGUIDCounter cannot be recovered exactly from overwritten bytes. The counter copied from an earlier save may be stale; do not claim unrestricted gameplay or new-save safety from one successful load.

Choose the inverse encoding depth from exact comparisons against a readable baseline. Nine inverse transformations matched the confirmed case; never interpret this as nine gameplay saves or apply it to arbitrary strings. The helper edits only long ANSI fact identifiers and preserves each fact's values, timestamps and counts. Returning to a baseline encoding depth is a recovery workaround, not a fix to the engine or proof of canonical text.

```powershell
uv run --with lz4 python scripts/w3save.py repair --source '<large save>' --donor '<recent readable save>' --baseline '<readable comparison save>' --inverse-steps 9 --output-dir '<new empty candidate directory>'
```

Outputs include a uniquely named SAV, matching JSON/PNG if supplied beside the source, and a manifest. The output directory must be outside the original gamesaves folder. No input is overwritten and there is no automatic installation or external upload.

The helper verifies all output LZ4 blocks by decoding and independent token validation, rebases main variable/RB/footer pointers, updates affected SS sizes, validates bounds, checks fact values and unaffected major game sections, and rechecks input hashes. If any check fails, do not offer the candidate as verified. Never fix only the last end offset when the first block also fails.

Ask the user to load the candidate and report the result. Record user-reported loading separately from tool verification. A subsequent save and reload plus gameplay checks are separate tests. Do not update memories merely because the skill was used.

## Report to CDPR

Read [the reporting checklist](references/reporting.md) when requested. Produce local English/Korean reports if requested, with measured facts, the user's observed result, reproducibility limits, and repair assumptions. Do not submit or message CDPR unless explicitly authorized. Keep local personal paths out of the report; use basenames and SHA-256 identities. Include the damaged original as the primary reproducer and the recovery candidate as an experimental comparison.
