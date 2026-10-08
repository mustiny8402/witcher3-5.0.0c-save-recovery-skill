# CDPR reporting checklist

Lead with the observed original failure and user-confirmed recovery result. Identify source and repaired files by basename, bytes and SHA-256. Record build IDs rather than guessing a patch-to-build mapping.

Separate four evidence levels:

1. User observation: repeated saves at the same location, original could not load, recovery candidate loaded normally, progress recovered.
2. Measured files: chunk overlap, invalid LZ4 reference, final offset, exact encoding transformation, fact counts and source hashes.
3. Engineering hypothesis: repeated encoding expansion may exceed reserved table capacity; the engine call path and first triggering version are unknown.
4. Unperformed tests: clean-room gameplay reproduction, future new-save/reload stability, platform comparisons and exact donor-header semantics.

Describe observed steps separately from proposed developer reproduction. Do not invent how many times the game was reloaded, a quest name, store, cloud setting, driver version or mod history. Record JSON's numMods value separately from the user's statement about mods, trainers and console commands.

Explain every material repair assumption, including the 128-byte donor header, uncertain magic_number/runtimeGUIDCounter, derived history count, inverse-depth selection and rebuilt pointer tables. Label the result as a successful local workaround, not an official fix or canonical recovery algorithm.

Ask CDPR to check ANSI/UTF-8 conversions in facts identifier serialization, table capacity versus actual chunk count, independent block validation, original-save recovery and regression coverage for repeated save/load of older multilingual saves. These are engineering investigation requests, not proven fixes.

Suggested local evidence bundle: unmodified original A/B with matching PNG/JSON, donor when needed to reproduce header reconstruction, repaired comparison, minimal parameterized helper, analysis and manifest, English/Korean report. Do not submit externally unless authorized. Avoid personal paths in exported metadata.

Official PC support: https://support.cdprojektred.com/en/witcher-3/pc
Support forms request matching SAV/PNG files compressed as ZIP/RAR. Check the current form and size limits before actual submission; ordinary attachment limits may differ from the save-files upload control. Do not generate DxDiag or collect unrelated system data without a task need.
