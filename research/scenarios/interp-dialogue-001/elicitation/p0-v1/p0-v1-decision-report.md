# INTERP-DIALOGUE-001P0-v1 — Revision Decision and Freeze Report

| Field | Value |
|---|---|
| Status | `FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY` |
| Merge basis | PR #17, merge commit `eb7f7e69afa8a78cdf0e5b5caf2ccad0a7574108` |
| Semantic sources | existing 001A families and 001B trace oracle, bytes unchanged |
| Base instrument | `INTERP-DIALOGUE-001P0-v0`, bytes unchanged |
| Source pilot | `INTERP-DIALOGUE-001P1-v0`, executed/evaluated scripted development pilot |
| Actual participant/model acquisition | none |
| Claim support | none |

## Decision result

P0-v1 converts the eight proposal-only P1 records into 18 exact, atomic
`RevisionResolutionCandidate` records. Each candidate has one separate
`P0DecisionReceipt`; all 18 were accepted into the new development instrument.
Acceptance means only that the exact operation is present in frozen P0-v1.
It does not claim semantic equivalence, successful execution, or defect
resolution.

```text
P1 RevisionProposal
→ exact RevisionResolutionCandidate
→ separate P0DecisionReceipt
→ frozen P0-v1 artifact

candidate != decision
accepted revision != defect resolved
```

The proposal disposition record has no proposal-level substantive decision
enum. It proves that every RP-001 … RP-008 is covered by the decision receipts
for all of its exact candidates, including proposals split across family,
level, or alternative wording boundaries.

## Authority split

P0-v1 does not modify any 001A scenario family or the 001B trace oracle. They
remain immutable semantic bases. Every participant-visible component is owned
by `participant-surface-v1.json`, and every final delivery is owned by the
derived `rendered-surface-catalog-v1.json`.

```text
001A scenario semantics
+ 001B oracle/horizon semantics
→ immutable basis only

participant-surface-v1
→ participant realization authority only

frozen renderer semantics
+ participant-surface-v1
→ 37 exact rendered delivery surfaces
```

The participant surface is closed over 3 family base surfaces, 18 factor-level
surfaces, 6 future-option surfaces, 6 family-resolved immediate/later prompts,
and 1 post-trace diagnostic prompt. The rendered catalog freezes 24 complete
initial presentations, 6 future deliveries, 6 family prompt deliveries, and 1
diagnostic delivery as exact UTF-8 bytes with length and SHA-256.

`instrument-v1.json` forbids fallback, direct participant-text reads from 001A
or 001B, and any participant-visible output absent from the rendered catalog.

## Mapping lineage

RP-008 is resolved by separating whether a mapping attempt was applicable from
the status of any candidate set it produced.

```text
MappingAttemptDisposition
- APPLIED
- NOT_APPLIED
- NOT_EVALUABLE

MappingCandidateStatus
- PROPOSED
- AMBIGUOUS
- NO_MAPPING
- OUTSIDE_VOCABULARY
```

Every eligible R1/R2 event must receive exactly one mapping-attempt receipt.
`APPLIED` requires exactly one candidate set; `NOT_APPLIED` and
`NOT_EVALUABLE` require zero. `AMBIGUOUS` requires at least two alternatives.
A `RESPONDED` disposition does not establish payload evaluability: present
zero-byte and whitespace-only payloads keep explicit lineage.

## Defect status

P0-v1 changes no P1 adjudication status and emits no resolution claim.

```text
DR-001 … DR-009   CONFIRMED / REVISION ACCEPTED / PENDING P1-v1 REPILOT
DR-010 … DR-013   DEFERRED / OPEN / ACQUISITION-SIDE EVIDENCE REQUIRED
DR-014            REJECTED / PRESERVED
```

In particular, a cleaner surface does not close the anchoring, say-or-do,
time-horizon, or retrospective-explanation questions deferred by P1-v0.

## Reproduction

```bash
python -m dynamics.labs.interp_dialogue_p0_v1_cli --write
python -m dynamics.labs.interp_dialogue_p0_v1_cli --verify
python -m unittest dynamics.tests.test_interp_dialogue_p0_v1 -v
```

The JSON manifest binds the normative P0-v1 schemas and artifacts plus the
exact frozen semantic/P0/P1 basis. This Markdown report is explanatory and is
not itself a normative authority artifact.

## Next gate

P1-v1 execution is not authorized by this freeze. The next separate PR must
preregister an exact P1-v1 protocol against the merged P0-v1 digest, with an
unchanged `CORE_REPLAY_CORPUS` and a revision-specific
`V1_DELTA_ADVERSARIAL_CORPUS`. Only a later execution PR may report whether a
confirmed defect is no longer reproduced under those registered development
inspections.

Actual acquisition remains behind ACQ0 and prompt-reactivity gates.
