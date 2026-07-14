# INTERP-DIALOGUE-001P1-v0 — Development Pilot Report

| Field | Value |
|---|---|
| Status | `EXECUTED / EVALUATED — SCRIPTED DEVELOPMENT PILOT ONLY` |
| Bound instrument | `INTERP-DIALOGUE-001P0-v0` (bytes unchanged, still `FROZEN`) |
| Preregistration | [`p1-development-pilot-preregistration.md`](p1-development-pilot-preregistration.md) |
| Actual participant/model acquisition | none |
| Frozen response-to-observation mapping | none |
| Human-mechanism / persona / trait authority | none |
| Evaluator identity | Claude (Anthropic AI agent), declared inside each inspection artifact |

## 1. Authority statement

P1-v0 executed the exact frozen P0-v0 development elicitation instrument as an
immutable scripted adversarial replay and evaluated the instrument itself. It
produced replay artifacts, defect candidates, an analyst adjudication, and
revision proposals.

```text
successful replay            != valid human measurement
confirmed instrument defect  != human mechanism finding
revision proposal            != adopted revision
adopted revision (future)    != defect fixed
scanner silence              != PASS
```

No output of this pilot is an actual delivery/response occurrence, an O5/O10
observation, an `OUT_OF_MODEL` adjudication, a placement result, a D2a
recursion, or support for any registry claim.

## 2. Frozen inputs

`dynamics/labs/interp_dialogue_p1_runner.py` pins the SHA-256 of ten frozen
inputs (instrument, four P0 schemas, three 001A family sources, the 001B
trace oracle JSON, and `trace-oracle.md`) and fails before materialization on
any byte difference. `test_interp_dialogue_p1.py` enforces the same guard in
the test suite, so a PR that touches any frozen artifact fails.

All ten digests matched the P0-v0 / 001A / 001B freeze at execution time.
Zero bytes of the frozen artifacts were changed by this pilot.

## 3. Coverage result

The frozen [`coverage manifest`](p1/coverage-manifest-v0.json) declares, and
the replay materialized, exactly 30 sessions:

```text
24/24 presentations covered at least once
6/6 registered future options covered at least once
3/3 matched comparisons covered on both arms under both registered options
   (rel-000/rel-100, work-000/work-100, risk-000/risk-100
    x FUTURE-*-0 and FUTURE-*-1)
10 sessions with D0/RD0 collected after R2, 20 sessions with D0 omitted
30 sessions total = 24 base + 6 opposite-future-option matched sessions
```

Structural note: the frozen P0 materializer requires a matched comparison
group to close both arms inside one session input. The 30 sessions are
therefore materialized as 24 run artifacts — 6 two-session runs (one per
matched comparison group) and 18 single-session runs — rather than 30
single-session runs. Session identity, coverage accounting, and provenance
are unaffected.

Non-matched cells received future options by a declared deterministic rule
(option index = cell bit-sum mod 2), recorded in the manifest.

## 4. Replay determinism

Building every generated artifact twice from the same frozen inputs produced
byte-identical results, and the checked-in artifacts equal the deterministic
rebuild (`python -m dynamics.labs.interp_dialogue_p1_run_cli --verify`;
`test_p1_replay_is_byte_deterministic`,
`test_p1_checked_in_artifacts_match_deterministic_rebuild`).
[`artifact-manifest-v0.json`](p1/runs/artifact-manifest-v0.json) records the
SHA-256 of all 96 generated artifacts (24 session inputs, 24 runs, 24
mechanical candidate sets, 24 mapping candidate sets) plus the manifest and
corpus digests.

No timestamps were invented. `sequence_ordinal` is schedule order only and is
not an event time, latency, thinking duration, or recovery time
(`test_p1_sequence_ordinals_are_schedule_order_only`).

## 5. Payload and disposition preservation

The [`response corpus`](p1/response-corpus-v0.json) (18 scripts) attacked
recording, normalization, missingness, and authority boundaries. Verified in
the replayed artifacts:

- exact raw bytes, byte length, and SHA-256 preserved for every present
  payload, including a 0-byte `RESPONDED` payload and a whitespace-only
  payload that remained distinct from empty;
- LF and CRLF variants of the same visible sentence survived as different
  bytes; Korean, Japanese, emoji, and an NFD combining-accent word survived
  without normalization;
- all four dispositions (`RESPONDED / REFUSED / NO_RESPONSE /
  TECHNICAL_FAILURE`) appear in both immediate and later slots and remained
  distinct: no empty payload was recast as `NO_RESPONSE`, no
  refusal-describing `RESPONDED` text was recast as `REFUSED`, and absent
  payloads carry their exact declared reason;
- zero D0/RD0 ordering violations; sessions with `OMITTED` diagnostics have
  no D0/RD0 events at all;
- runner-issued `OUT_OF_MODEL`: zero; raw response direct-to-trace casts:
  zero (`test_p1_emits_no_acquisition_or_adjudication_authority_in_runs`).

## 6. Mechanical candidates

The frozen P0 scanner ran over all 24 run artifacts:
**0 `MechanicalDefectCandidate` records** ([sets](p1/assessment/mechanical/)).

Scanner silence is not a PASS. The scanner checks literal leaks, payload and
binding integrity, schedule order, missingness collapse, and provenance
links; it cannot see semantic anchoring, register defects, or referent
ambiguity. Those are exactly the classes the evaluator-side inspections found
below, which is why the two sources are kept separate.

## 7. Walkthrough candidates

The [author cognitive walkthrough](p1/assessment/author-walkthrough-v0.json)
inspected all 24 rendered presentations, 3 prompts, and 6 future options
against the nine preregistered hypotheses and filed 10
`DevelopmentInspectionCandidate` records (WT-001 … WT-010), including:

- `WT-001` — "the person" has two eligible referents in REL and WORK;
- `WT-002` — participant-facing descriptors refer to themselves as "the
  vignette";
- `WT-003` — FUTURE-REL options expose internal design vocabulary ("At a new
  access", "prior-material cue", "external target evidence");
- `WT-005` — the RISK equality bullet carries the must-remain-equal contract
  in one referent-free sentence.

## 8. Language candidates

The separate [language/comprehension inspection](p1/assessment/language-comprehension-inspection-v0.json)
filed 7 candidates (LC-001 … LC-007), including the speaker/partner identity
gap in REL (LC-002), unmatched family reading burden (LC-003), the natural-
speech vs research-register seam (LC-004), and a mechanically verifiable
mapping-vocabulary gap (LC-005): the preregistered mapping statuses
`NOT_APPLIED` / `NOT_EVALUABLE` have no counterpart in the frozen
development-assessment schema enum, and absent-payload events admit no
mapping status at all — during this pilot, mapping candidate sets silently
skip them.

## 9. Development mapping candidates

Development-only mapping attempts were recorded for every `RESPONDED`
immediate/later event ([sets](p1/assessment/mapping/); 50 candidates):

```text
PROPOSED_SURFACE_MAPPING                    30
AMBIGUOUS_SURFACE_MAPPING                   11
NO_SURFACE_MAPPING_PROPOSED                  6
OUTSIDE_CURRENT_MAPPING_VOCABULARY_CANDIDATE 3
```

These are development candidates only — not O5/O10 observations, not a
frozen mapping policy, not `OUT_OF_MODEL` adjudications. The
`OUTSIDE_CURRENT_MAPPING_VOCABULARY_CANDIDATE` cases (prompt-directed
meta-responses) indicate a narrow vocabulary, not wrong responses.

## 10. Adjudicated defects

The [analyst adjudication](p1/assessment/analyst-adjudication-v0.json) gave
every candidate exactly one status with full lineage
(`test_p1_every_candidate_is_adjudicated_exactly_once`):

```text
CONFIRMED  9   DR-001..DR-009
DEFERRED   4   DR-010..DR-013 (need acquisition-side evidence)
REJECTED   1   DR-014 (REL factor overlap is superficial)
```

Confirmed defects, in brief: prompt referent ambiguity (DR-001),
speaker/partner identity gap (DR-002), vignette self-reference (DR-003),
design-vocabulary and factor restatement in FUTURE-REL options (DR-004),
construct-label self-reports (DR-005), register seam (DR-006), RISK reading
burden (DR-007), "resolved as following" wording (DR-008), and the mapping
vocabulary gap (DR-009). Rejected and deferred candidates remain in the
append-only artifact.

## 11. Revision proposals

[`instrument-revision-proposals-v0.json`](p1/proposals/instrument-revision-proposals-v0.json)
issues 8 proposals (RP-001 … RP-008), each grounded only in `CONFIRMED`
receipts, each with a `target_json_pointer`, and all of them:

```text
status           = PROPOSED_NOT_ADOPTED
execution_status = UNEXECUTED
authority        = FUTURE_P0_VERSION_DECISION_REQUIRED
```

P1 modified no instrument byte, created no `instrument-v1.json`, adopted no
proposal, executed no revised instrument, declared no `DEFECT_FIXED`, and
changed no claim registry entry. Because confirmed defects exist, the next
registered step is a separate **P0-v1 decision PR** that adjudicates each
proposal (`ACCEPTED / REJECTED / DEFERRED`); any accepted revision must be
frozen as a new instrument version and re-piloted (P1-v1) before a defect may
be considered resolved.

## 12. Unresolved limitations

- The three RP-005-adjacent surfaces live in the frozen 001B oracle; adopting
  wording changes there requires a versioned oracle decision, not an in-place
  edit.
- Evaluator-side inspections were produced by a single AI-agent evaluator; a
  second, independent reading (especially by a human reader outside the
  project vocabulary) may find candidates this pass missed. Inspection
  candidate absence is not instrument soundness.
- The scripted corpus demonstrates that adversarial forms are *expressible*
  and survivable; it says nothing about their frequency in any real source.
- Deterministic replay verifies the recording surface, not the elicitation
  quality of the instrument.
- The mapping candidate sets inherit the DR-009 vocabulary gap: absent-payload
  events are skipped rather than recorded as explicitly unmapped.

## 13. Explicit non-claims

This pilot provides **no** human participant data, **no** LLM latent or
activation data, **no** persona/trait/mechanism finding, **no** placement
winner, **no** D2a recursion, **no** durable TargetForm or Episode/Narrative
writer, **no** `HM-INV-013` / `HM-DYN-004` support, and **no** change to any
claim's adoption or support status. The P0-v0 instrument remains `FROZEN`;
actual acquisition remains behind the separate `ACQ0` and
`PROMPT-REACT-001` gates.