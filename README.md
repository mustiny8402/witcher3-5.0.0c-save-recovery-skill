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

Personal save files, generated recovery files and binary support-report attachments are not included. The latest report text is embedded below. The existing [MIT license](LICENSE) applies to this repository.

## Latest reports

**Report origin: 7 October 2026 (2026-10-07). Current revision: 8 October 2026 (2026-10-08), Asia/Seoul.** The reports were generated for the 7 October save-corruption and recovery case and subsequently supplemented with the confirmed game-load result and additional incident history. The report date in the current text identifies the supplemented revision.

**2026년 10월 7일 생성 리포트 · 최신 보완일 2026년 10월 8일 · Asia/Seoul 기준.** 10월 7일 저장 손상 및 복구 사례의 리포트이며, 아래 최신 본문에는 10월 8일 정상 로딩 확인과 추가 발생 경과를 반영했습니다. 본문의 작성일은 보완본 기준입니다.

Both current reports are displayed in full below. Private save files and the separate CDPR support evidence archive mentioned in the reports are not published here. No report has been submitted automatically.

최신 영문·한글 보고서 전체를 아래에 표시합니다. 본문에 언급한 개인 세이브와 별도 CDPR 제출용 자료 묶음은 이 저장소에 공개하지 않습니다.

## English report

### Witcher 3 Remastered Save Corruption Report

Fact identifier expansion and LZ4 table overlap

To CD PROJEKT RED Technical Support and Save System Engineering
Report date 8 October 2026   Time zone Asia/Seoul

I was at risk of losing several hours of progress because of a corrupted save. A local recovery candidate was generated from the affected save, and I confirmed that it loads normally in the game on 8 October 2026. Please investigate the original save and the serialization issues documented below.

The file analysis found large encoding expansion in fact identifiers, overlapping chunk metadata and compressed data, and a malformed first LZ4 block. The successful recovery is a local workaround. It does not establish an official fix or future save stability.

#### Environment and affected files

| Field | Recorded value |
| --- | --- |
| Game | The Witcher 3 Remastered 5.0 |
| Platform | PC; save metadata records PC |
| Affected build | 5.0.1044392   P4CL 13360103 |
| Earlier build | 5.0.1041720   P4CL 13312615 |
| Serialization versions | saveVersion 66; gameVersion 29; buildPatch 0 |
| Mods and external tools | No mods, as reported; numMods 0. A trainer changed gold only while using version 4.0.4. Console-command history not specified. |
| Store and cloud settings | Steam; Steam Cloud enabled. CDPR cloud saving for Cross Progression was disabled before the latest recurrence. These are separate cloud systems. |

The original investigation referred to release 5.00c. The exact build IDs above are taken from the files; the mapping of these IDs to the named hotfix was not independently established.

A is the earlier comparison save, B is the damaged later save, and R is the recovery candidate. File names and SHA-256 identities are listed in the File identities and evidence attachments section below.

#### Observed history and reproduction limits

The following chronology is my reported experience, not an independently reproduced patch regression. I did not observe this symptom through version 5.0.0b; I observed it in saves made after 5.0.0c. The historic gold-only trainer edit was already present in version 4.0.4. A causal contribution from that edit has not been established or excluded.

More specifically, I observed no symptom in saves dated 30 September 2026 or earlier, but observed it in saves from 1 October onward. CDPR’s official 5.00c PC announcement is dated 1 October 2026. This date alignment makes a 5.00c regression an important investigation candidate, but does not establish when the internal encoding expansion first began. The measured 30 September comparison A already contains oversized fact identifiers.

[Official 5.00c PC announcement, 1 October 2026](https://www.thewitcher.com/us/en/news/52073/hotfix-5-00c-out-now-for-the-witcher-3-wild-hunt-remastered-on-pc)

I did not observe the symptom in saves before the first encounter with the three Crones in Crookback Bog where they recount Ciri’s story; it appeared after that point. This description corresponds to Ladies of the Wood and the related Ciri’s Story: Fleeing the Bog sequence. Quest-name identification is based on the described scene and published quest guides, not a verified quest-state comparison in the saves.

I had already lost progress to the same symptom approximately two days before this report, restarted, and encountered it again. In the latest sequence I played briefly at work, saved, continued at home, played further and saved before the symptom appeared. Both computers and the Steam Cloud transfers are possible investigation variables; their hardware, OS details and synchronization logs have not been collected.

On 7 October at lunchtime, my work-PC save still loaded on PC after 5.0.0c, but Switch 2 reported that the save file was corrupted. I then disabled CDPR cloud saving used for Cross Progression, continued playing and saved again; the issue recurred in that later save. Steam Cloud remained in use. These are my observed platform outcomes, not a controlled test of identical file bytes on both platforms; the lunchtime save has not been mapped to an attachment by hash.

The latest recurrence shows that active CDPR cloud saving is not required for a failure to appear in this already affected save lineage. It does not exclude earlier cross-platform processing or prove that cloud-off play can independently create the issue in a pristine save. PC loading of an earlier affected save is not proof that its serialized data was healthy.

I suspect an autosave after certain quests may trigger or accelerate the issue. This is an unconfirmed hypothesis. The exact quest transition, first expanding save and corresponding autosave are not isolated; no autosave file has been established as the trigger.

I saved several times at the same in-game point as a precaution. This does not establish growth on every save or a trigger count. The original PC error text was not recorded. The Switch 2 corruption-message wording above is my recollection; no screenshot or complete UI text is attached.

For a file-based reproduction, use unmodified B with its matching PNG/JSON and attempt to load it on the affected build. Compare with R. The expected behavior is a successful load of the original game state. A clean gameplay sequence that produces the corruption from a fresh save has not yet been established.

#### Measured container and serialization findings

| Measurement | Earlier A | Damaged B | Recovery R |
| --- | --- | --- | --- |
| SAV bytes | 1,211,745 | 96,499,170 | 1,296,427 |
| Raw LZ4 chunks | 5 | 266 | 6 |
| Declared payload bytes | 5,179,145 | 278,715,349 | 5,571,509 |
| Successfully decoded chunks | 5 of 5 | 265 of 266 | 6 of 6 |
| Data start offset | 3,084 | 3,084 | 3,084 |
| Chunk table end | 76 | 3,208 | 88 |
| Main variable entries | 76,364 | 80,992 | 80,992 |

All three containers begin with SNFHFZLC. The 12-byte chunk records contain compressed size, decoded size and end offset. B requires 16 + 266 × 12 = 3,208 bytes for the table, but declares compressed data at offset 3,084. The two regions overlap by 124 bytes.

B chunk 0 declares 363,551 compressed bytes and 1,048,576 decoded bytes. The library decoder fails. An independent token validator finds that the first sequence outputs 60 bytes, then requires a backward reference of 1,452 bytes at compressed offset 62. That reference precedes the start of the output buffer.

B chunk 265 starts at offset 96,052,737 and has 446,433 compressed bytes. Its computed end is 96,499,170, but the table records 196,631. That value is neither the correct end nor the permitted zero sentinel. The sum of compressed sizes still matches EOF; file truncation was not observed.

#### Fact identifier expansion

A contains 43 oversized ANSI fact identifiers of 12,288 bytes each. After reconstructing B’s first block, its 5,121 facts contain 43 identifiers of 6,291,456 bytes and one of 3,145,728 bytes. Forty-two complete corresponding runs were compared before header reconstruction: applying Latin1 decoding followed by UTF-8 encoding nine times to A produced byte-exact matches to B, a 512-fold expansion.

Forward operation: value.decode('latin1').encode('utf-8')

The indexed facts region grows from 697,659 bytes in A to 273,916,121 in B. This accounts for 99.883839% of the declared payload growth. A already contains the same expansion pattern despite its valid container; it is not a proven pristine baseline.

#### Recovery procedure and confirmed result

The recovery used the damaged later save as the source of game progress. The originals were retained unchanged. The generated R file has SHA-256 2f9a859ae2686e3d74f8f2a0b44739095ac3943ce9bd098f792596482b42ca4e.

1. Reconstruct the lost first 128 decoded bytes using a more recent readable save from the same playthrough. Resume decoding the surviving LZ4 sequence at compressed offset 128. Later blocks are decoded from B.

2. Restore the history count to 450, supported by surviving compressed bytes and 450 parsed history records. Set the description to RECOVERY TEST so the candidate can be identified.

3. Apply nine inverse UTF-8-to-Latin1 transformations only to the 44 oversized ANSI fact identifiers. This returns them to the earlier comparison’s encoding depth. It does not establish their intended canonical text.

4. Preserve all 5,121 facts and their non-identifier value, time and count bytes. Rebase affected main indexes, RB offsets and footer pointers; update enclosing SS lengths.

5. Repack six independent 1 MiB LZ4 chunks, with a shorter final chunk, a table that fits before the data and a valid final zero sentinel.

#### Verification and remaining uncertainty

All six generated chunks decoded successfully and matched the rebuilt payload exactly. Independent LZ4 token validation also passed. All 80,992 main variable entries and 202 indexed SS lengths were checked. The questSystem, community, CJournalManager, universe and idTagManager regions remained byte-identical to B after relocation. Original SAV/PNG/JSON hashes did not change.

I confirmed normal game loading of R on 8 October 2026 and recovered my progress. This is a user-observed result, distinct from the file checks. Extended gameplay, a newly created save and reload, and repeated-session stability have not been verified.

The donor header supplied magic_number and runtimeGUIDCounter because their exact B values were overwritten. The copied counter is 2,850,378 and may be older than B’s original value. These are reconstruction assumptions, not an exact restoration of the lost header. Header semantics and future ID allocation need developer review.

#### Engineering investigation requested

Please examine fact identifier conversions during save/load, reserved chunk-table capacity, block boundaries and final offsets. Please compare 5.0.0b and 5.0.0c with this legacy save lineage, test manual saves and quest autosaves around Ladies of the Wood, and assess Steam Cloud transfers and Cross Progression enabled/disabled cases. Please assess an official recovery path. The engine call path, first triggering version and quest/autosave causality remain unconfirmed.

#### File identities and evidence attachments

These identities distinguish the unmodified originals, donor and experimental recovery. File-system modified times of A and B were 30 September 2026 21:03:45 and 7 October 2026 23:19:07 Asia/Seoul. They are not asserted to be embedded game timestamps.

A   ManualSave_51d43_7ea47400_543b466.sav

`SHA-256 f0233b7c53f0bc47ad8c5b49ecc0378ce541b45e25c572eecfa519af29ca1d0a`

B   ManualSave_52584_7ea49800_5d31dfd.sav

`SHA-256 3eec69ab723972506871e3bec26fb0988296be0f21976fb5c6a1c96082e88f2e`

Donor   ManualSave_106591_7ea49800_33a3aa3.sav

`SHA-256 a3ccb2b369ed15cbe4dc948dd0adec3f033b3383b46e4ff1adea5564fc874091`

R   ManualSave_52584_7ea49800_5d31dfe.sav

`SHA-256 2f9a859ae2686e3d74f8f2a0b44739095ac3943ce9bd098f792596482b42ca4e`

#### Evidence package contents

A separately prepared support archive, not published in this repository, contains original A/B and their matching PNG/JSON, the donor and matching sidecars where available, R, the repair manifest, measured analysis, the parameterized recovery helper, and both language reports. R is supplied for comparison, not as a replacement for the damaged original reproducer.

DxDiag for the work/home computers, the exact original error screenshot, cloud synchronization logs, the historic trainer tool/version and an isolated triggering autosave are not included. Store/cloud settings above are user-reported. No report has been submitted automatically.

#### Technical reference and requested support route

The container and footer layouts were compared against public save parser source code and then checked against the supplied files. These older parsers are not treated as CDPR’s official current 5.x specification.

[W3SavegameEditor chunk table reader](https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/ChunkedLz4/ChunkedLz4FileTable.cs)

[W3SavegameEditor serialization reader](https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/Savegame/SavegameFile.cs)

[Independent raw LZ4 save decompressor](https://github.com/solusipse/witcher3-inventory-editor/blob/master/w3_decompress.c)

[CD PROJEKT RED PC support](https://support.cdprojektred.com/en/witcher-3/pc)

[Quest identification: Ladies of the Wood walkthrough](https://www.gamebanshee.com/thewitcher3/walkthrough/ladiesofthewood.php)

CDPR support forms request the affected SAV and matching PNG compressed as ZIP/RAR. Please use the current support form and its save-file upload control; attachment limits can differ by control.

## 한글 보고서

### 위쳐 3 리마스터 저장 데이터 손상 보고서

팩트 식별자 인코딩 팽창과 LZ4 블록 표 충돌

수신 CD PROJEKT RED 기술 지원 및 저장 시스템 개발 담당자
작성일 2026년 10월 8일   기준 시간대 Asia/Seoul

저장 데이터 손상으로 수 시간의 진행 내용을 잃을 위험이 있었습니다. 손상된 세이브를 기반으로 로컬 복구 사본을 만들었으며, 2026년 10월 8일 게임에서 정상 로딩됨을 확인했습니다. 아래 원본 파일과 직렬화 오류의 원인을 조사해 주시기 바랍니다.

파일 분석에서 팩트 식별자의 대규모 인코딩 팽창, 압축 블록 표와 본문의 영역 충돌, 첫 LZ4 블록의 구조 오류를 확인했습니다. 복구 성공은 로컬 우회 조치의 결과이며, 공식 수정이나 향후 저장 안정성을 입증하지는 않습니다.

#### 실행 환경과 대상 파일

| 항목 | 기록된 값 |
| --- | --- |
| 게임 | The Witcher 3 Remastered 5.0 |
| 플랫폼 | PC   세이브 메타데이터에 PC로 기록 |
| 손상 파일 빌드 | 5.0.1044392   P4CL 13360103 |
| 초기 비교 파일 빌드 | 5.0.1041720   P4CL 13312615 |
| 직렬화 버전 | saveVersion 66   gameVersion 29   buildPatch 0 |
| 모드와 외부 도구 | 사용자 모드 미사용 진술 및 numMods 0. 4.0.4 당시 트레이너로 골드만 수정한 이력 있음. 콘솔 명령 사용 여부 미확인. |
| 스토어와 클라우드 설정 | Steam 및 Steam Cloud 사용. 최종 재발 전 Cross Progression용 CDPR 클라우드 저장을 끔. 두 클라우드 기능은 별개. |

최초 조사에서는 5.00c를 언급했습니다. 위 빌드 ID는 파일에서 직접 확인한 값이며, 해당 ID와 명명된 핫픽스의 대응 관계는 독립적으로 확인하지 않았습니다.

A는 초기 비교 세이브, B는 후기 손상 세이브, R은 복구 사본입니다. 파일 이름과 SHA-256 식별값은 아래 파일 식별값과 첨부 근거 절에 기재했습니다.

#### 사용 중 관찰 내용과 재현 범위

아래는 사용자 관찰이며 독립 재현한 패치 회귀 결과는 아닙니다. 5.0.0b까지 증상이 없었고 5.0.0c 이후 확인했습니다. 4.0.4에서 골드만 수정한 트레이너 이력의 원인 기여 여부는 미확인입니다.

구체적으로 2026년 9월 30일까지의 저장에서는 증상이 없었고 10월 1일 저장부터 관찰했습니다. CDPR의 공식 PC 5.00c 발표일도 10월 1일입니다. 날짜 일치는 5.00c 회귀를 우선 조사할 근거이나 내부 인코딩 팽창의 최초 발생 시점을 확정하지는 않습니다. 실측한 9월 30일 비교 파일 A에도 과대 팩트 식별자가 이미 있습니다.

[공식 PC 5.00c 발표: 2026년 10월 1일](https://www.thewitcher.com/us/en/news/52073/hotfix-5-00c-out-now-for-the-witcher-3-wild-hunt-remastered-on-pc)

늪지대에서 마녀 세 명을 처음 만나 시리의 이야기를 듣는 지점 이전 저장에서는 증상을 관찰하지 않았고 이후에 발생했습니다. 설명한 장면은 숲의 여인들(Ladies of the Wood) 및 연결된 시리의 이야기: 늪지 탈출(Ciri’s Story: Fleeing the Bog)에 해당합니다. 퀘스트명은 장면 설명과 공개 공략에 따른 식별이며 파일 내 퀘스트 상태 대조로 확정한 경계는 아닙니다.

약 이틀 전에도 동일 증상으로 진행 내용을 잃고 다시 진행한 뒤 재발했습니다. 회사에서 저장하고 집에서 이어 플레이한 경로도 조사 대상이며 두 PC의 사양, OS 및 Steam Cloud 동기화 로그는 미수집입니다.

10월 7일 점심시간 회사에서 만든 저장은 5.0.0c 이후에도 PC에서 로딩되었지만 Switch 2에서는 저장 파일이 손상되었다는 메시지가 나왔습니다. 이후 Cross Progression용 CDPR 클라우드 저장을 끄고 계속 플레이한 뒤 저장한 파일에서 다시 문제가 발생했습니다. Steam Cloud는 사용 중이었습니다. 이는 사용자 관찰이며 두 플랫폼에서 동일 바이트의 파일을 검사한 통제 실험은 아닙니다. 점심시간 파일과 첨부 파일의 대응 해시는 아직 확정하지 않았습니다.

최종 재발은 이미 영향을 받은 세이브 계보에서 오류가 나타나는 데 CDPR 클라우드의 현재 활성화가 필수는 아님을 보여 줍니다. 과거 크로스플랫폼 처리의 영향을 배제하거나 깨끗한 저장에서 클라우드를 꺼도 독립적으로 발생함을 입증하지는 않습니다. 이전 파일이 PC에서 로딩되었다는 사실도 내부 저장 구조의 완전한 정상성을 보장하지 않습니다.

일부 퀘스트의 자동 저장 이후 문제가 유발되거나 가속되는지 의심합니다. 이는 미확인 가설입니다. 정확한 퀘스트 전환, 최초 팽창 저장, 대응 자동 저장은 분리하지 못했으며 특정 자동 저장 파일을 원인으로 확정하지 않았습니다.

같은 지점에서 여러 번 저장했지만 매 저장마다 팽창했는지나 유발 횟수는 확정하지 못했습니다. 원본 PC 오류 문구는 기록하지 않았습니다. 위 Switch 2 손상 메시지는 사용자 기억이며 화면 캡처와 전체 UI 문구는 첨부하지 않았습니다.

파일 재현은 수정하지 않은 B와 대응 PNG 및 JSON을 해당 빌드에서 로드하여 R과 비교하는 방식입니다. 기대 동작은 원래 진행 상태의 정상 로드이며, 새 세이브부터 손상을 만드는 플레이 재현 절차는 미확립입니다.

#### 컨테이너와 직렬화 구조 실측

| 측정 항목 | 초기 A | 손상 B | 복구 R |
| --- | --- | --- | --- |
| SAV 크기 바이트 | 1,211,745 | 96,499,170 | 1,296,427 |
| raw LZ4 블록 수 | 5 | 266 | 6 |
| 선언 해제 크기 바이트 | 5,179,145 | 278,715,349 | 5,571,509 |
| 해제 성공 블록 | 5 / 5 | 265 / 266 | 6 / 6 |
| 압축 데이터 시작 위치 | 3,084 | 3,084 | 3,084 |
| 블록 표 끝 위치 | 76 | 3,208 | 88 |
| 메인 변수 색인 수 | 76,364 | 80,992 | 80,992 |

세 파일의 매직은 SNFHFZLC입니다. 각 12바이트 블록 레코드는 압축 크기, 해제 크기, 끝 위치를 담습니다. B의 표에는 16 + 266 × 12 = 3,208바이트가 필요하지만 데이터 시작은 3,084로 지정되어 두 영역이 124바이트 겹칩니다.

B의 첫 블록은 압축 363,551바이트와 해제 1,048,576바이트를 선언합니다. 라이브러리 해제가 실패하며, 별도 토큰 검사에서도 첫 시퀀스가 60바이트를 출력한 뒤 압축 위치 62에서 1,452바이트 역참조를 요구합니다. 출력 버퍼 시작 이전을 참조하는 오류입니다.

마지막 블록 265는 96,052,737에서 시작하며 압축 크기는 446,433바이트입니다. 계산한 끝은 96,499,170인데 표의 값은 196,631로 실제 끝도 허용되는 0 센티널도 아닙니다. 압축 크기 합은 EOF와 일치하여 파일 잘림은 관찰되지 않았습니다.

#### 팩트 식별자 인코딩 팽창

A에는 각각 12,288바이트인 과대 ANSI 팩트 식별자 43개가 있습니다. B의 첫 블록을 보완한 후 확인한 팩트 5,121개에는 6,291,456바이트 식별자 43개와 3,145,728바이트 식별자 1개가 포함됩니다. 헤더 보완 전 비교 가능한 완전한 대응 패턴 42개에 대해 A에 Latin1 읽기와 UTF-8 기록 변환을 9회 적용하면 B와 바이트 단위로 동일했으며, 팽창률은 512배입니다.

정방향 변환   value.decode('latin1').encode('utf-8')

팩트 영역은 A의 697,659바이트에서 B의 273,916,121바이트로 증가하여 선언된 해제 데이터 증가의 99.883839%를 설명합니다. A도 이미 같은 팽창 패턴을 포함하므로, 압축 구조가 정상이라는 이유로 완전히 깨끗한 기준 파일로 보지는 않습니다.

#### 복구 절차와 확인 결과

후기 손상 파일의 진행 데이터를 사용하고 원본은 보존했습니다. 생성한 R의 SHA-256은 2f9a859ae2686e3d74f8f2a0b44739095ac3943ce9bd098f792596482b42ca4e입니다.

1. 같은 플레이스루의 더 최근 읽을 수 있는 세이브로 손실된 해제 헤더 128바이트를 보완했습니다. 압축 위치 128의 살아 있는 LZ4 시퀀스부터 해제를 재개하고 이후 블록은 B에서 가져왔습니다.

2. 남아 있는 압축 바이트와 이력 레코드 450개에 근거해 이력 개수를 450으로 복원했습니다. 사본을 구분하도록 설명을 RECOVERY TEST로 지정했습니다.

3. 과대 ANSI 팩트 식별자 44개에만 UTF-8에서 Latin1로 되돌리는 변환을 9회 적용했습니다. 초기 비교 파일의 인코딩 깊이로 되돌린 것으로, 의도된 원래 식별자 문자열을 확정한 것은 아닙니다.

4. 팩트 5,121개의 수치 시간 개수 등 식별자 외 바이트를 보존했습니다. 메인 색인 RB 위치 footer 포인터를 재배치하고 영향을 받는 SS 길이를 수정했습니다.

5. 마지막 블록만 짧은 독립적인 1 MiB LZ4 블록 6개로 다시 압축했습니다. 표가 본문 시작 전에 들어가도록 하고 마지막 0 센티널을 정상 기록했습니다.

#### 검증 범위와 남은 불확실성

생성한 블록 6개를 모두 다시 해제하여 재구성 payload와 바이트 단위로 일치함을 확인했고, 별도 LZ4 토큰 검사도 통과했습니다. 메인 색인 80,992개와 색인에 등록된 SS 길이 202개를 검사했습니다. questSystem community CJournalManager universe idTagManager 영역은 재배치 후에도 B와 동일했으며 원본 SAV PNG JSON의 해시는 변하지 않았습니다.

2026년 10월 8일 R의 정상 게임 로딩을 직접 확인하여 진행 내용을 복구했습니다. 이는 사용자가 확인한 결과이며 파일 구조 검사와 구분됩니다. 장시간 플레이 새 저장 후 재로드 반복 세션 안정성은 아직 검증하지 않았습니다.

B의 정확한 magic_number와 runtimeGUIDCounter 값은 덮어써져 donor 헤더의 값을 사용했습니다. 복사한 카운터는 2,850,378이며 B의 원래 값보다 오래된 값일 수 있습니다. 이 부분은 완전 복원이 아닌 보완 가정이므로 헤더 의미와 이후 ID 생성 동작의 개발자 검토가 필요합니다.

#### 개발 담당자에게 요청하는 조사

팩트 식별자 인코딩 변환, 블록 표 예약 용량, 블록 경계와 마지막 위치 검증을 확인해 주시기 바랍니다. 이 기존 세이브 계보로 5.0.0b와 5.0.0c를 비교하고, 숲의 여인들 전후 수동 및 자동 저장, Steam Cloud 전달과 Cross Progression 사용 및 미사용을 검증해 주십시오. 공식 복구 경로도 요청합니다. 엔진 코드 경로, 최초 유발 버전, 퀘스트 및 자동 저장 인과관계는 아직 미확인입니다.

#### 파일 식별값과 첨부 근거

아래 식별값으로 수정하지 않은 원본 donor 복구 사본을 구분할 수 있습니다. A와 B의 파일시스템 수정 시각은 Asia/Seoul 기준 2026년 9월 30일 21시 03분 45초와 10월 7일 23시 19분 07초입니다. 내부 게임 저장 시각으로 단정하지 않습니다.

A   ManualSave_51d43_7ea47400_543b466.sav

`SHA-256 f0233b7c53f0bc47ad8c5b49ecc0378ce541b45e25c572eecfa519af29ca1d0a`

B   ManualSave_52584_7ea49800_5d31dfd.sav

`SHA-256 3eec69ab723972506871e3bec26fb0988296be0f21976fb5c6a1c96082e88f2e`

Donor   ManualSave_106591_7ea49800_33a3aa3.sav

`SHA-256 a3ccb2b369ed15cbe4dc948dd0adec3f033b3383b46e4ff1adea5564fc874091`

R   ManualSave_52584_7ea49800_5d31dfe.sav

`SHA-256 2f9a859ae2686e3d74f8f2a0b44739095ac3943ce9bd098f792596482b42ca4e`

#### 근거 자료 묶음

이 저장소에 공개하지 않은 별도 지원용 ZIP에는 원본 A B와 대응 PNG JSON, donor와 존재하는 대응 파일, R, 복구 manifest, 실측 분석, 매개변수형 복구 도구, 영문 및 한글 보고서를 담았습니다. R은 비교용 실험 사본이며 손상 원본을 대체하는 재현 자료가 아닙니다.

회사와 집 PC의 DxDiag, 원본 오류 화면, 클라우드 동기화 로그, 과거 트레이너 이름과 버전, 분리된 유발 자동 저장 파일은 포함하지 않았습니다. 위 스토어 및 클라우드 설정은 사용자 진술입니다. 보고서는 자동 제출하지 않았습니다.

#### 형식 참고 자료와 지원 경로

컨테이너와 footer 구조는 공개 세이브 파서 소스와 대조한 뒤 대상 파일에서 직접 검사했습니다. 이 오래된 파서들은 CDPR의 현재 5.x 공식 저장 스펙으로 취급하지 않았습니다.

[W3SavegameEditor 블록 표 파서](https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/ChunkedLz4/ChunkedLz4FileTable.cs)

[W3SavegameEditor 직렬화 파서](https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/Savegame/SavegameFile.cs)

[독립 raw LZ4 세이브 해제 도구](https://github.com/solusipse/witcher3-inventory-editor/blob/master/w3_decompress.c)

[CD PROJEKT RED PC 기술 지원](https://support.cdprojektred.com/en/witcher-3/pc)

[퀘스트 식별 참고: Ladies of the Wood 공략](https://www.gamebanshee.com/thewitcher3/walkthrough/ladiesofthewood.php)

CDPR 지원 양식은 대상 SAV와 대응 PNG를 ZIP 또는 RAR로 압축해 제공하도록 안내합니다. 실제 제출 시 현재 양식의 세이브 첨부 항목과 용량 제한을 확인해야 하며, 일반 첨부 항목과 제한이 다를 수 있습니다.

## Historical reports

The latest report remains embedded in this README. When a revision is superseded, its report files will be added to the repository and linked in this section. No historical report files are currently published.

최신 리포트는 README 본문에 유지합니다. 과거 리포트는 파일로 보관하고 이 절에 링크를 추가할 예정입니다. 현재 공개된 과거 리포트 파일은 없습니다.
