# Publication repair note: portable atlas receipt identity

Date: 20 August 2026

Scope: receipt metadata and release-gate portability only

Mathematical status: unchanged

## Trigger

The first public-repository replay completed every structural control and all
1,152 atlas cases under ordinary and optimised Python. It reported zero
anomalies and zero missing certificates, and the two newly generated receipts
matched each other. The final frozen-receipt comparison nevertheless failed.

The failure was reproduced exactly by changing the frozen receipt's software
field from Python `3.14.6` (the reviewed machine) to Python `3.14.7` (the hosted
runner). No case record, symbolic digest, witness, summary count, or exit status
differed.

## Repair

The semantic receipt schema advances from
`cyclicity-atlas-case-records-v1` to
`cyclicity-atlas-case-records-v2`. The software identity now records the Python
major/minor compatibility series (`3.14`) rather than a volatile patch release.
The exactly pinned symbolic dependency remains recorded as SymPy `1.14.0`.

A focused regression control requires Python patch releases within one series
to share a receipt identity, while changes to the Python minor series or SymPy
version remain visible. The control runs in ordinary and optimised replay modes.

A complete local regeneration after the repair analysed all 1,152 cases in
612.8 seconds, reported zero anomalies and zero missing certificates, and
matched the frozen v2 receipt byte for byte.

## Receipt chain

| Object | SHA-256 |
|---|---|
| Confirmation-reviewed v1 atlas receipt | `d057118ff96e65665fe54d0f6cddf19cd53d963c6e5a81ec2c522855248ed438` |
| Publication-portable v2 atlas receipt | `84305a35d174394636dd7fdda7ab455425411ad7bb605e5a1fa7b229e5aa7356` |

The confirmation review is retained unchanged because it identifies the bytes
actually reviewed. This additive note and the final hosted replay identify the
bounded post-review repair. The repair does not upgrade internal model review
to independent specialist review and does not change the all-degree atlas from
conjecture to theorem.
