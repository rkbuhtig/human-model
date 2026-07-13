# MORPH-001A — Reducer Proposal–Commit Instrumentation Preregistration

> **Status:** `IMPLEMENTED`; preregistered synthetic structural evaluation passed

## Question

Can the update requested by the current model rule be recorded independently from the
bounded persistent change that the runtime actually commits?

This slice tests only that distinction.

```text
ReducerProposal
!= independently identified DeformationDemand
!= MorphicLoad
!= qualified MentalTransition
```

It does **not** test whether either quantity is a human mental-time unit, a phenomenal
intensity, or a morphic load.

## Observation unit

The observation unit is one processed occurrence. A transport redelivery is not a new
observation unit. An explicit current reexposure is a new occurrence and may therefore
receive its own record while retaining its source-occurrence reference.

During runtime, traced reducer wrappers return `ReducerStepResult` values so the engine
can preserve their proposals without recomputing them. The completed `TickTrace` and
post-run `ReducerProposalReceipt` do **not** retain step-result objects. Each receipt
stores one flat, occurrence-wide, ordered tuple of `ReducerFieldProposal` values with
their `ReducerDriverContribution` provenance:

```text
pre-constraint requested target / delta   -> ReducerProposal component
bounded committed target / delta          -> committed component
```

The measurement identity is
`descriptive-reducer-preclamp-proxy@1.0.0`. Each field proposal records stage/write
sequence, field, `basis_before`, `requested_after_unbounded`, `committed_after`, unit,
constraint identity, and typed driver contributions.

The policy digest binds a mandatory operator prefix, allowed conditional suffixes, and
each operator's stage, field, constraint, and allowed driver channel/label identities.
Receipt identity is content-bound to occurrence/delivery/reexposure lineage, times,
proposal digest, and typed before/after state projections. Adjacent receipts must preserve
the descriptive-state projection chain.

The receipt also binds the minimal conditional-writer context: encoded soothing and the
performance receipt/action identity. Optional action and soothing writes, including their
driver identity and value, must match that context exactly.

This is an internal integrity boundary, not a signature or external authentication scheme.
It rejects identity-preserving inconsistent mutation and trace splicing; it does not certify
the external truth of a newly constructed, internally self-consistent synthetic receipt.

`ReducerProposal` is the target requested by the current versioned simulation reducer
before its relevant storage bound. It is not inferred from the final state and is not
the raw event magnitude by itself. The committed component is the descriptive state
displacement that remains after the update is bounded and committed.

Crucially, the current reducer proposal already contains model-specific access pressure,
update rates, phenomenal activation, action performance, and other drivers where the
corresponding reducer uses them. It is therefore a **measurement precursor**, not an
independently identified, capacity-free `DeformationDemand`.

The typed driver contributions are an audit decomposition of the implemented formula.
They establish algebraic provenance for this reducer version, not independent causal
effects or empirical psychological factors.

Constructor validation checks structurally allowed driver identities and arithmetic sums.
The inline reducer builder is the trusted writer for evaluated contribution values; the
receipt is not an independent authentication of factual driver attribution.

Both are simulation-internal normalized field deltas. They are preserved as typed
components rather than aggregated into a scalar score.

The same field may be written more than once inside one occurrence. Ordered step/write
identity is therefore normative: each later `basis_before` must chain from the preceding
committed target for that field. A per-write committed delta is not silently replaced by
the occurrence-level final-minus-initial net delta.

```text
apply_fast_update_traced / apply_slow_update_traced
→ runtime ReducerStepResult wrappers
→ flatten proposals in write order into TickTrace.reducer_proposals
→ post-run ReducerProposalReceipt.proposals
```

## Information boundary

Reducer proposal instrumentation may use only information already available to the current
versioned update operation. It may not use:

- a later occurrence or later recovery;
- a post-run outcome;
- a future retention result;
- a phenomenal report as evidence of demand;
- an `AccommodationEnvelope` or future load policy.

The implemented boundary is read-only in two tested senses: traced and compatibility
reducers commit the same state for the same writer inputs, and proposal/receipt artifacts
are not downstream inputs to `HumanState`, routing, evidence assessment, intent,
performance, or action-occurrence updates. This does not claim that every arbitrary
change to instrumentation code is semantics-preserving.

## Explicitly deferred quantities

```text
AccommodationEnvelope
ExcessDemand
UncommittedResidual
MorphicLoadProfile
ResidualStrain
PhenomenalStrainReadout
subjective / mental time
```

At the `MORPH-001A` freeze, `AccommodationEnvelope` was deferred. `MORPH-001B` later
introduced only an experimenter-declared reducer-write simulation band; a measured human
accommodation range remains deferred. The current `[0, 1]` state bound and the distance
to that bound are storage constraints, not an accommodation envelope.

Likewise, the arithmetic difference between requested and committed displacement is not
yet `ResidualStrain`. It can contain clamp loss, ordinary update attenuation, staged
interaction, or model artifacts. Naming it residual strain requires a separate operator,
unit, and validation plan.

Because this `MORPH-001A` slice implements no envelope, neither excess nor
`MorphicLoadProfile` can be computed here. The later `MORPH-001B` proxy is a separate
derived artifact and still permits no bridge to qualia or subjective time.

## Preregistered structural probes

### P1 — one record per processed occurrence

Every processed occurrence produces exactly one `ReducerProposalReceipt` with matching temporal
and occurrence/delivery/reexposure provenance. Dropped, unresolved, rejected, or
transport-duplicate inputs do not.

### P2 — reducer request and commit dissociate under saturation

With `body.energy = 0.99` and `energy_delta = +0.25`:

```text
requested = +0.25
committed = +0.01
```

With `body.energy = 1.00` and the same delta:

```text
requested = +0.25
committed = 0.00
```

The latter can have a nonzero reducer proposal without a qualified mental transition.
If the record defines the requested proposal as `after - before`, the slice fails.

### P3 — transport and reexposure provenance

- A redundant delivery of the same occurrence adds no proposal receipt.
- An explicit current reexposure may add one receipt and must retain the source reference.
- Content changes without a matching canonical identity, dangling/self-referential
  lineage, temporal inconsistency, and discontinuous adjacent state projections are
  rejected. This is schema integrity, not cryptographic source authenticity.

### P4 — prefix causality

Appending future events must not change proposal receipts for an identical processed
prefix. Receipt identity and content are determined by the current occurrence, current
pre-update information, and versioned operator only.

### P5 — committed-runtime preservation and no downstream dependency

For the same writer inputs, the traced reducer and compatibility wrapper must produce the
same committed state. The frozen semantic golden must remain unchanged, and proposal or
receipt artifacts must not become inputs to state, routing, evidence, or action updates.

### P6 — typed immutable components

Field identity, unit, requested delta, committed delta, provenance, and operator identity
must be immutable. A record may not silently combine fields or cast a component into
transition count, evidence strength, load, or phenomenal intensity.

### P7 — existing audit path preservation

A finite but out-of-bound initial descriptive state must continue through the existing
invariant-audit path and be bounded by the reducer. Proposal capture must not turn that
pre-existing auditable case into an instrumentation exception.

## Failure conditions

The first slice is rejected or revised if any of the following occurs:

1. the reducer proposal is reconstructed from the post-update state rather than captured before the
   relevant bound;
2. requested and committed displacement cannot differ in the saturation control;
3. proposal receipts are emitted only for Q-qualified transitions;
4. a transport redelivery creates a new receipt;
5. future events rewrite an earlier receipt;
6. traced and compatibility reducers commit different states, or proposal artifacts become
   downstream update inputs;
7. receipt/operator/state content can change without changing its canonical identity,
   or schema-inconsistent lineage/operator/driver content is accepted;
8. a scalar load, qualia value, or mental-time value is emitted from this trace.
9. proposal capture converts the existing finite-invalid-state audit path into an
   exception.

Passing these probes establishes instrumentation integrity only. It does not implement
`DeformationDemand`, and it does not support the human dynamical hypothesis `HM-DYN-002`.

Executable checks for this slice:

- `test_one_reducer_proposal_receipt_per_processed_occurrence`
- `test_pre_constraint_reducer_proposal_is_distinct_from_committed_delta`
- `test_saturated_reducer_proposal_can_exist_without_mental_transition`
- `test_transport_redelivery_does_not_create_reducer_proposal_receipt`
- `test_current_reexposure_creates_new_reducer_proposal_with_source_provenance`
- `test_future_events_cannot_rewrite_reducer_proposal_prefix`
- `test_reducer_proposal_instrumentation_preserves_committed_runtime_semantics`
- `test_reducer_proposal_records_require_immutable_typed_components`
- `test_reducer_proposal_ledger_rejects_inconsistent_lineage_and_content_identity`
- `test_reducer_proposal_capture_preserves_invalid_initial_audit_path`

## Implemented next slice

[`MORPH-001B`](morph-001b-proposal-envelope-comparison.md) now compares this
proposal with an explicit experimenter-declared simulation band. It does not
retroactively rename storage-bound clipping as accommodation failure, and its
ordered proxy-excess profile is not a measured human `AccommodationEnvelope`,
`ExcessDemand`, residual strain, or morphic load. Outcome/load interpretation
remains a later `MORPH-001C` task.
