# Witcher 3 save recovery skill

A Codex skill for diagnosing inflated Witcher 3 Remastered PC saves and creating a recovery copy for one verified corruption profile: expanded fact identifiers combined with an overlapping LZ4 chunk table.

위쳐 3 리마스터의 비정상적으로 커진 PC 세이브를 진단하고, 검증된 특정 손상 유형에 대해 원본을 보존한 복구 사본을 만드는 Codex 스킬입니다.

## Install in Codex

Clone or download this repository and copy its skill files into `~/.codex/skills/witcher3-save-recovery/`. `SKILL.md`, `agents/`, `references/` and `scripts/` must be directly inside that folder. On Windows, `~` denotes your user profile directory.

Invoke `$witcher3-save-recovery` and provide the save paths and desired diagnosis or recovery task. The helper requires Python and `lz4`; the examples use `uv` to supply the dependency without changing global packages.

## Command-line usage

Run from the repository or installed skill directory. Use new output paths outside the original gamesaves directory.

```powershell
uv run --with lz4 python scripts/w3save.py analyze --source '<save.sav>' --output '<new-analysis.json>'

uv run --with lz4 python scripts/w3save.py repair --source '<damaged.sav>' --donor '<readable-donor.sav>' --baseline '<readable-comparison.sav>' --inverse-steps 9 --output-dir '<new-candidate-directory>'
```

Diagnosis does not require a donor. Repair requires compatible readable saves from the same playthrough and evidence for the inverse encoding depth. Nine steps matched the documented case; do not assume that value applies to other cases.

## Scope and validation

- Implemented repair profile: PC saveVersion 66 / gameVersion 29, 266 chunks, data offset 3084, 124-byte table overlap, and only the first LZ4 chunk failing. Unsupported profiles are rejected.
- Inputs are retained unchanged. The helper produces a separate SAV, available matching sidecars and a verification manifest. It does not install the candidate into the game or upload files.
- A user confirmed normal game loading of the documented recovery candidate on 8 October 2026. Later gameplay, new-save/reload stability and Switch 2 recovery were not verified.
- Lost header values are supplied by a donor. The copied runtime GUID counter may be stale; successful loading is not proof of future ID-allocation safety.
- This is an experimental local workaround. The repository name identifies the suspected patch context; it does not establish that 5.0.0c first caused the encoding anomaly or provide an official CDPR fix.

Read [SKILL.md](SKILL.md), the [supported format and repair profile](references/format-and-repair.md), and the [confirmed case](references/confirmed-case.md) before attempting recovery. The [reporting checklist](references/reporting.md) separates measured evidence from user observations and hypotheses.

Personal save files, generated recovery files and support-report attachments are not included. The existing [MIT license](LICENSE) applies to this repository.
