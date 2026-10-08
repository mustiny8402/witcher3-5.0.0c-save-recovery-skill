# Format and supported repair

## Container

- Offsets 0..7: ASCII `SNFHFZLC` (SNFH and FZLC).
- Offset 8: little-endian uint32 chunk count.
- Offset 12: little-endian uint32 compressed data start.
- Offset 16: count records of 12 bytes each, containing compressed size, decoded size and compressed end offset.
- Blocks use independent raw LZ4. Decode a block using its declared decoded size; a zero final end offset is a permitted sentinel.
- Reject table/data overlap, bad references, size mismatches or out-of-file reads. Separately note trailing bytes rather than silently trimming them.

## Serialization

Decoded offsets in the main file include the outer header size even though the payload starts with SAV3. The last six bytes contain the absolute main variable table offset and `SE`. The variable table contains count and pairs of absolute offset/size. At variable-table offset minus ten are NM and RB pointers; MANU name strings follow NM. RB has count and uint16-size/uint32-offset records.

BS has a uint16 name index; VL has name and type indexes. SS has a uint32 inner length. In the observed facts section: BS facts, SS, SXAP and SBDF, then a uint32 fact count. Each fact has a packed string identifier, two uint16 counters, and 10 bytes per value/time record; EBDF terminates the section. Verify the section boundary rather than guessing records.

Packed strings: bit 7 of the first byte marks single-byte storage; its low six bits begin the length and bit 6 marks continuation. Subsequent bytes contribute seven length bits and use bit 7 for continuation. For non-ANSI strings, the byte width is two. Never rewrite a length without updating offsets and enclosing sizes.

## Narrow recovery profile

Only profile `pc66-chunks266-overlap124` is implemented. First decoded 128 bytes are missing from the target. A surviving complete LZ4 sequence begins at compressed offset 128 and requires a 128-byte decoded prefix. Later blocks must all decode. The donor prefix must use the same save/game versions and playthrough ID as the baseline; validate all surviving history records and derive their count.

The helper copies a donor's magic_number and runtimeGUIDCounter because the target values were overwritten. These are uncertain reconstructed header values. It preserves latest world/quest data, but a load success does not prove future GUID allocation safety. This uncertainty belongs in the manifest and user explanation.

Inverse operation on selected inflated ANSI fact IDs is `bytes.decode('utf-8').encode('latin1')`. Evidence must support the selected depth. The 2026-10-08 candidate used nine steps, retaining the baseline's already expanded representation. It did not identify the intended canonical IDs and does not prevent recurrence.

Do not transplant the baseline's facts block or world data. Rewrite only confirmed identifiers; preserve all non-identifier fact bytes and source progress data. Relocate main indexes, RB offsets, footer pointers and affected SS lengths. Preserve the original outer decoded-offset base and repack independent 1 MiB chunks so the table fits before the data start.

## Format sources

- https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/ChunkedLz4/ChunkedLz4FileHeader.cs
- https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/ChunkedLz4/ChunkedLz4FileTable.cs
- https://github.com/Atvaark/W3SavegameEditor/blob/master/W3SavegameEditor.Core/Savegame/SavegameFile.cs
- https://github.com/solusipse/witcher3-inventory-editor/blob/master/w3_decompress.c

These public parsers are not CDPR's official current 5.x specification. Their layouts must be validated against each input.
