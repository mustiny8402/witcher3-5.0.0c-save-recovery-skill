# Confirmed case on 2026-10-08

The user confirmed normal game loading of the recovery candidate on 2026-10-08 Asia/Seoul. No independent game automation was used. Later gameplay, a fresh save/reload and repeated-session stability were not verified.

| Item | Initial A | Damaged B | Recovery candidate |
| --- | ---: | ---: | ---: |
| SAV bytes | 1211745 | 96499170 | 1296427 |
| Chunks | 5 | 266 | 6 |
| Declared decoded bytes | 5179145 | 278715349 | 5571509 |
| LZ4 success | 5/5 | 265/266 | 6/6 |

Source build IDs: A `5.0.1041720`, B `5.0.1044392`; both saveVersion 66, gameVersion 29, PC and recorded numMods 0. Do not infer a store or Cross Progression setting from these fields.

Additional user-reported environment: Steam and Steam Cloud enabled. The issue occurred with Cross Progression enabled and disabled; it was disabled in the latest incident. No mods were used. A trainer edited gold only on this save lineage while using version 4.0.4. Console use was unspecified. The user observed no symptom through 5.0.0b, then observed it after 5.0.0c. This is not an independently verified release-to-build mapping or proof that the historic trainer edit was irrelevant.

The user associated onset with the first Crones/Ciri-story encounter in Crookback Bog, corresponding to Ladies of the Wood and Ciri's Story: Fleeing the Bog. They had a similar loss about two days earlier, restarted, and experienced recurrence after playing/saving at work and continuing at home. Quest autosaves are a suspected trigger, not an established cause. Exact triggering quest/save, clean reproduction, cloud logs and work/home environment comparisons were not established.

B's table ends at 3208 but compressed data starts at 3084: 124 bytes overlap. Its first LZ4 sequence outputs 60 bytes before demanding a backward distance of 1452. Its final end offset is 196631, instead of 96499170 or zero. Sizes still sum to EOF, so truncation was not observed.

A already has 43 ANSI fact IDs of 12288 bytes. Reconstructed B has 43 IDs of 6291456 bytes and one of 3145728 bytes, among 5121 facts. Before first-block reconstruction, 42 complete corresponding runs were byte-exact matches after nine forward Latin1-to-UTF8 expansions. Nine inverse steps were used for recovery. Neither this observation nor multiple saves at one location proves nine save/load cycles or a constant per-save growth rate.

B's facts section measured 273916121 bytes; A's measured 697659. Their difference explains 99.883839% of declared payload growth. After reconstruction, B's facts name and boundary were directly parsed rather than inferred.

The latest readable donor available in that case was `ManualSave_106591_7ea49800_33a3aa3.sav`. Only its first 128 decoded bytes were used; history count was restored to 450 from surviving target records. Its runtimeGUIDCounter was 2850378. The saved description was changed to RECOVERY TEST. Main variable table 80992 entries and 202 indexed SS lengths were checked; questSystem, community, CJournalManager, universe and idTagManager bytes were preserved.

Hashes identify this case without embedding personal save files in the skill:

- A: `f0233b7c53f0bc47ad8c5b49ecc0378ce541b45e25c572eecfa519af29ca1d0a`
- B: `3eec69ab723972506871e3bec26fb0988296be0f21976fb5c6a1c96082e88f2e`
- Recovery: `2f9a859ae2686e3d74f8f2a0b44739095ac3943ce9bd098f792596482b42ca4e`

Automatic installation into gamesaves failed in the execution environment. The candidate was delivered as a ZIP, and the user subsequently confirmed successful loading. Do not assume the same filesystem failure will recur elsewhere.
