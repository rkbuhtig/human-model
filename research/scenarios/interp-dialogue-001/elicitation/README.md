# INTERP-DIALOGUE-001P0-v0 — Development Elicitation Instrument

| Field | Value |
|---|---|
| Status | `FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY` |
| Bound scenarios | three `INTERP-DIALOGUE-001A` families / 24 cells |
| Bound oracle | `INTERP-DIALOGUE-001B-TRACE-ORACLE-V1` |
| Participant or model data | none |
| Measurement mapping | none |

P0 freezes the schedule that a later source-specific protocol may show, ask,
and record. The current implementation only materializes a declared scripted
adversarial replay. It does not record an actual participant or model
occurrence, and it does not measure an encounter, candidate set, TargetForm,
Ghost operation, or external fact.

```text
observation slot
!= scheduled prompt-delivery step

scripted replay record and exact payload provenance
!= actual delivery or response occurrence
!= internal mechanism observation
```

The core schedule uses its own elicitation namespace:

```text
E0 initial-vignette delivery record
E1 generic immediate-prompt delivery record
R1 scripted immediate-response record
E2 registered future-option delivery record
E3 generic later-prompt delivery record
R2 scripted later-response record

D0 / RD0 optional post-trace diagnostic pair, after R2 only
```

`R1` and `R2` are only eligible inputs to a future, separately frozen mapping
candidate for `O5/immediate_surface` and `O10/later_surface`. The materializer
emits neither an actual occurrence, mapping, nor observation. `D0/RD0` has no
oracle coordinate.

## Artifact layers

- [`instrument-v0.json`](instrument-v0.json) and
  [`instrument.schema.json`](instrument.schema.json) freeze the instrument.
- [`session-input.schema.json`](session-input.schema.json) freezes development
  script inputs.
- [`run.schema.json`](run.schema.json) permits only scripted delivery, response,
  and response-provenance records; these are not actual acquisition receipts.
- [`development-assessment.schema.json`](development-assessment.schema.json)
  defines mapping candidates, mechanical defect candidates, evaluator-side
  inspection reports, analyst defect adjudication, and revision proposals as
  separate artifact kinds.

The Python layers are also separate:

```text
ScriptedReplayMaterializer
-> immutable scripted replay / provenance artifact only
-> SCRIPTED_ADVERSARIAL_RESPONSE input only
!-> actual participant or model occurrence

MechanicalDefectScanner
-> MechanicalDefectCandidate only

Analyst adjudication
-> future explicit InstrumentDefectReceipt
```

Author cognitive walkthrough and language/comprehension inspection are
evaluator-side sources, not response records. P0 executes no pilot. P1 may bind
this exact instrument, preserve an immutable scripted replay, produce those
inspection sources, adjudicate defects, and issue `InstrumentRevisionProposal`
records. P1 cannot perform actual acquisition, adopt a proposal, or execute a
revised instrument. A later P0 version must accept, reject, or defer each
proposal and freeze the next instrument artifact.

## Executed development step

[`INTERP-DIALOGUE-001P1-v0`](p1-development-pilot-v0-report.md) is
`EXECUTED / EVALUATED — SCRIPTED DEVELOPMENT PILOT ONLY`. Its
[`preregistration`](p1-development-pilot-preregistration.md) froze the minimum
30-session coverage, adversarial response classes, evaluator inspections,
analyst adjudication states, proposal-only revision authority and merge
conditions before any pilot output existed.

The execution materialized 30 sessions as 24 run artifacts and checked in 96
generated artifacts plus their manifest. The mechanical scanner emitted zero
candidates; analyst adjudication recorded 9 confirmed, 4 deferred and 1
rejected defects. All 8 revision proposals remain
`PROPOSED_NOT_ADOPTED / UNEXECUTED`.

```text
P1 scripted execution
!= actual acquisition contract
!= prompt-reactivity identification
!= persona or latent-state study
```

The separate [`P0-v1 decision/freeze`](p0-v1/p0-v1-decision-report.md) is now
`FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY`. It atomizes the eight P1
proposals into 18 exact candidates and separate decision receipts, owns all
participant-visible realization in a closed-world surface, and freezes 37 final
delivery byte strings. It changes no 001A/001B semantic artifact and makes no
defect-resolution claim.

P1-v1 preregistration remains required before defect-resolution claims, but it
is now a non-mainline hold. The immediate research-program step is the separate
[`INTERP-001D2a0`](../d2a0/README.md) frozen contract, followed by detached D2a1
and `OBS-MAP-000`. That mapping decides whether this elicitation surface is
kept, revised or replaced; it does not pre-authorize P0-v2. Actual
delivery/response occurrences, source identity, clocks,
consent/privacy/withdrawal and acquisition lineage remain an `ACQ0` gate.
Interpreting prior-response-exposed later surfaces as natural persistence also
remains blocked on a separate prompt-reactivity study.

## Frozen raw-byte integrity

| Artifact | SHA-256 |
|---|---|
| `instrument-v0.json` | `52705bc686a69d43360eb0544eda59571c77dc1e29520ec4b156bcd60f413776` |
| `instrument.schema.json` | `0023386d724864c7890cdac14807782a347edc741ad5613a3687d68363f92c89` |
| `session-input.schema.json` | `2474709b767c4146d64999e73454b6bdfbcf6989984fc1e1596deeead94df71e` |
| `run.schema.json` | `8c5cca613f6bf53e925e60013e5958f29244fb236b06cf70520736ac5cbcc56d` |
| `development-assessment.schema.json` | `ac7cc68fb8c9618838f99e3c1ad9c120a79df313f22828c2b395300e2473b92f` |
