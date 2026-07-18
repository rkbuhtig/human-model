# Adoption — S0 source process and PublicEventV3

Date: 2026-07-19

## Decision

Adopt `SIM-REL-BOUNDARY-FAMILY-002` and `HUMAN-DYN-ADEQ-S0-SOURCE-RUNTIME-001` before resolving any future randomness beacon.

```text
SIM-REL-BOUNDARY-FAMILY-001
→ FROZEN HISTORICAL PARAMETER GENERATOR
→ SUPERSEDED BEFORE SEED RESOLUTION

SIM-REL-BOUNDARY-FAMILY-002
→ PARAMETER + FEEDBACK + PROCESS-ADEQUACY GENERATOR FROZEN
→ SEED UNRESOLVED

INITIAL-002
→ FROZEN HISTORICAL MODEL SURFACE
→ NOT COMPATIBLE WITH PublicEventV3

PublicEventV3 / SOURCE-RUNTIME-001
→ FROZEN
→ UNMATERIALIZED
```

## Reason

The prior source freeze generated parameter matrices but left trajectory length, transition/emission order, public action and feedback timing, prediction points, terminal target timing, split streams, and corpus serialization open. It also exposed a future continuation label in the model context and separated receipts, actions, and feedback into parallel arrays.

This adoption closes the source side only. It deliberately does not patch the candidate models in the same PR, so source-process choices remain auditable separately from model compatibility choices.

## Authority

No source instance, corpus, score, or human evidence exists. Beacon resolution remains prohibited until a separate model-v3 compatibility freeze and joint activation record merge.
