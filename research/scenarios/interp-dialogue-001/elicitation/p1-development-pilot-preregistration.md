# INTERP-DIALOGUE-001P1-v0 — Development Pilot Preregistration

| Field | Value |
|---|---|
| Status | `PLANNED / UNEXECUTED — SCRIPTED DEVELOPMENT PILOT ONLY` |
| Bound instrument | `INTERP-DIALOGUE-001P0-v0` |
| Bound merge commit | `05d946590a605a76e1bbe89fceab8b556c2d37cf` |
| Actual participant/model acquisition | none |
| Frozen response-to-observation mapping | none |
| Human-mechanism authority | none |
| Persona / trait authority | none |

P1 executes the exact frozen P0-v0 development instrument with scripted adversarial inputs. It
checks replayability, provenance preservation, instrument defects and revision needs. It does not
measure a participant or model, identify a latent residence, select a mechanism, execute D2a or
adopt a revised instrument.

```text
immutable scripted pilot
!= actual acquisition
!= response-to-trace mapping
!= latent-state observation
!= defect repair validation
```

## 1. Questions P1 may answer

P1 is limited to the following development questions.

1. Can the frozen v0 schedule and materializer reproduce the declared scripted sessions exactly?
2. Are raw response bytes, response disposition and missingness preserved without normalization or
   collapse?
3. Do the prompt, schedule, schemas or mapping vocabulary create mechanical, linguistic or
   comprehension defects?
4. Which instrument revisions, if any, should be proposed for a later adoption decision?

P1 does not answer:

```text
which human mechanism is correct
where a response belongs in the latent trace
whether a participant has a persona or trait
whether an O10 difference is natural persistence
whether D2a recursion is supported
whether a proposed revision fixes a defect
```

## 2. Frozen inputs and no-mutation rule

P1 binds the exact P0-v0 artifacts and source digests already frozen by PR #15.

- `instrument-v0.json`
- `instrument.schema.json`
- `session-input.schema.json`
- `run.schema.json`
- `development-assessment.schema.json`
- the three bound scenario-family files
- `INTERP-DIALOGUE-001B-TRACE-ORACLE-V1`

P1 must fail before materialization if any bound content digest differs from the P0-v0 contract.
P1 cannot modify these files in the same run or PR.

```text
P1 input = immutable P0-v0
P1 output = replay + candidates + adjudication + proposals
P1 output !-> P0-v0 mutation
```

## 3. Coverage manifest

Before replay execution, P1 freezes a machine-readable coverage manifest. The manifest must bind
session IDs to exact presentation IDs, selected registered future-option IDs, response-script IDs
and D0 inclusion.

Minimum coverage is 30 scripted sessions.

### 3.1 Presentation coverage

- all 24 presentation cells at least once
- no unregistered presentation
- each session bound to exactly one source cell

### 3.2 Future-option coverage

- all 6 registered future options at least once
- no free-form or unregistered future option
- matched comparisons use the same registered future option across the two arms

### 3.3 Matched-future coverage

Each registered matched comparison must cover both arms and both registered future options.

```text
rel-000  <-> rel-100
work-000 <-> work-100
risk-000 <-> risk-100
```

The 24 base sessions cover one future option for the six matched cells. Six additional sessions
cover the opposite future option, yielding 30 minimum sessions.

This coverage does not grant matched-future oracle authority to the other 18 cells.

### 3.4 D0 coverage

The corpus includes both:

```text
D0/RD0 omitted
D0/RD0 included after R2
```

No D0 or RD0 event may precede R2. D0 has no oracle coordinate and a retrospective report is not a
causal-process trace.

## 4. Scripted adversarial response corpus

The response corpus attacks loss, normalization, missingness collapse, authority overcast and
schema ambiguity. It is not synthetic human evidence and must not be described as a simulated
participant sample.

The corpus includes at least:

- ordinary short response
- long response
- multiline response
- explicit `RESPONDED` with empty UTF-8 payload
- explicit `RESPONDED` with whitespace-only payload
- non-ASCII and mixed Unicode payload
- payloads differing only by LF/CRLF bytes
- categorical response
- response preserving multiple possibilities
- response that questions the requested perspective
- response that refuses both speech and action while still being `RESPONDED`
- explicit `REFUSED`
- explicit `NO_RESPONSE`
- explicit `TECHNICAL_FAILURE`
- D0/RD0 present and absent variants

Exact payload bytes, byte length and SHA-256 must be retained. Empty or ambiguous text must not be
automatically converted into `NO_RESPONSE`, `REFUSED`, `OUT_OF_MODEL` or a trace value.

## 5. Immutable replay materialization

The frozen P0 materializer executes every declared scripted session and checks in the following
artifacts:

```text
P1 coverage manifest
scripted session inputs
immutable replay artifact(s)
artifact SHA-256 manifest
mechanical defect candidate set
```

Running the materializer twice from the same frozen inputs must produce byte-identical replay and
candidate artifacts with identical content digests.

P1 does not invent actual timestamps. `sequence_ordinal` is schedule order only.

```text
sequence ordinal
!= actual event time
!= response latency
!= processing time
!= recovery time
!= latent transition time
```

## 6. Response provenance and dispositions

The four P0 response dispositions remain distinct.

```text
RESPONDED
REFUSED
NO_RESPONSE
TECHNICAL_FAILURE
```

P1 must preserve each disposition without inferring it from text. A blank `RESPONDED` payload is not
`NO_RESPONSE`; refusal is not session termination; technical failure is neither refusal nor missing
motivation.

The replay record remains scripted provenance rather than actual occurrence provenance.

```text
SCRIPTED_RESPONSE_RECORD
!= ResponseSubmissionOccurrence
!= ResponseReceivedOccurrence
!= participant/model event
```

## 7. Mechanical scanner

The P0 scanner may emit `MechanicalDefectCandidate` records only. Scanner silence is not a PASS and
a candidate is not a defect receipt.

Mechanical candidates include the P0-frozen codes for literal leaks, payload mismatch, binding
mismatch, schedule/order failure, missingness collapse, provenance break and early D0 delivery.

```text
MechanicalDefectCandidate
!= InstrumentDefectReceipt
!= revision proposal
```

The scanner cannot issue `OUT_OF_MODEL`, map a raw response to O5/O10, select a functional
placement or modify claim support.

## 8. Author cognitive walkthrough

An evaluator-side author walkthrough inspects all 24 presentations and all registered future
options. Its observations are `DevelopmentInspectionCandidate` records, not response records or
confirmed defects.

The walkthrough examines the following preregistered hypotheses.

1. Is “the person” ambiguous among speaker, recipient, evaluator and evaluated actor?
2. Do relation, work and risk families invite inconsistent perspective assignment?
3. Does “say or do” force speech and action into one answer?
4. Does the explicit `Context:` factor list reveal experimental manipulation or anchor the response?
5. Does any item require attribution across multiple changing factors?
6. Can a future option overwrite or dominate the initial path?
7. Are “first thing” and “next thing” temporally underspecified?
8. Does D0 solicit a new explanation rather than recover a historical cause?
9. Does an item expose internal candidate anchors or design vocabulary semantically even when no
   literal identifier leaks?

Each candidate records exact source item IDs and text spans where possible.

## 9. Language and comprehension inspection

A separate evaluator-side artifact inspects:

- sentence naturalness
- pronoun and action-agent resolution
- family-level reading difficulty
- temporal ordering
- grammatical attachment of the future option
- overlap among factor descriptors
- translation balance between base surface and source descriptors
- semantic anchoring not detectable by literal scanners
- participant burden and answer-format ambiguity

Automated leak scanning does not certify semantic neutrality. Analyst judgment remains explicit and
source-linked.

## 10. Development mapping attempts

P1 may create development-only mapping attempts from a raw scripted response. Mapping artifacts are
separate from event rows.

```text
RawResponseReceipt
-> DevelopmentMappingAttempt
-> DevelopmentMappingCandidate
```

Allowed mapping statuses:

```text
NOT_APPLIED
PROPOSED
AMBIGUOUS
NO_MAPPING
OUTSIDE_CURRENT_VOCABULARY
NOT_EVALUABLE
```

A mapping candidate is not:

```text
an O5/O10 observation
a frozen mapping policy
an internal trace residence
an instrument defect
an OUT_OF_MODEL final adjudication
```

`OUTSIDE_CURRENT_VOCABULARY` is a limitation candidate for the current mapping vocabulary, not an
error in the response.

## 11. Analyst defect adjudication

The analyst reads both source kinds.

```text
MechanicalDefectCandidate
DevelopmentInspectionCandidate
```

Every candidate receives exactly one explicit adjudication.

```text
CONFIRMED
REJECTED
DEFERRED
NOT_EVALUABLE
```

Candidate absence, scanner silence or replay success must not be converted automatically to
`NO_DEFECT` or global PASS.

A confirmed defect must retain source lineage to the candidate records and exact instrument item or
schema path. A rejected or deferred candidate remains in the append-only assessment artifact.

## 12. Revision proposals

Only `CONFIRMED` defect receipts may directly ground a revision proposal.

Each proposal includes at least:

```text
proposal_id
defect_receipt_refs
target_json_pointer or target artifact path
proposed_change
rationale
status = PROPOSED_NOT_ADOPTED
execution_status = UNEXECUTED
```

P1 cannot:

- mutate `instrument-v0.json`
- create or adopt `instrument-v1.json`
- execute a revised instrument
- emit `DEFECT_FIXED`
- change claim adoption/support status
- select a placement winner
- implement persona, trait, Access runtime or D2a

Acceptance, rejection or deferral of proposals belongs to a later P0-version decision PR. A revised
instrument, if adopted, must be frozen as a new artifact and re-piloted before a defect can be
considered resolved.

## 13. P1 merge conditions

P1-v0 may merge only if all conditions hold.

### Frozen boundary

- P0 frozen artifacts have zero byte changes
- bound scenario and oracle digests match P0-v0
- no Dynamics runtime behavior changes
- no claim registry support/status changes

### Coverage

- 24/24 presentation coverage
- 6/6 future-option coverage
- both arms and both options for all three matched comparisons
- D0/RD0 included and omitted coverage

### Provenance

- all four response dispositions preserved
- raw UTF-8 bytes, lengths and digests preserved
- no payload normalization or missingness collapse
- optional diagnostic ordering violations: zero
- deterministic replay digests reproduced

### Authority

- raw response direct-to-trace casts: zero
- runner-issued `OUT_OF_MODEL`: zero
- scanner candidate auto-promotion to defect receipt: zero
- every adjudication retains source lineage
- every revision remains proposal-only and unexecuted
- actual acquisition artifacts: zero
- human mechanism, persona, trait or D2a claims: zero

## 14. Post-P1 decision path

```text
no confirmed defects
-> retain P0-v0
-> proceed to source-specific protocol design

confirmed defects
-> separate P0-v1 decision PR
-> ACCEPTED / REJECTED / DEFERRED per proposal
-> freeze accepted revisions as a new instrument version
-> P1-v1 re-pilot if needed
```

P1 execution does not itself authorize actual acquisition.

## 15. Gates before actual acquisition

A later `ACQ0` contract must separately define actual event provenance, source identity, protocol
version, clocks, consent, privacy, withdrawal and raw/mapping/adjudication lineage.

A later `PROMPT-REACT-001` must compare:

```text
NO_INTERMEDIATE_ELICITATION
PRIOR_FREE_RESPONSE_EXPOSURE
PRIOR_STRUCTURED_RESPONSE_EXPOSURE
```

before prior-response-exposed later surfaces are used as evidence for natural persistence or
unprompted latent paths.

## Final authority statement

P1 is a development test of a frozen elicitation instrument.

```text
successful replay
!= valid human measurement

confirmed instrument defect
!= human mechanism finding

revision proposal
!= adopted revision

adopted revision
!= defect fixed
```
