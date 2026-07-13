# Reducer Proposal Envelope Comparison Contract — MORPH-001B

## Status

| Scope | Status |
|---|---|
| explicit versioned reducer-write simulation bands | `IMPLEMENTED` |
| asymmetric componentwise proposal comparison | `IMPLEMENTED` |
| source-bound post-run receipt and ledger | `IMPLEMENTED` |
| human accommodation-capacity measurement | `UNIMPLEMENTED` |
| independently identified `DeformationDemand` | `UNIMPLEMENTED` |
| residual, load, qualia, or subjective-time measurement | `UNIMPLEMENTED / HOLD` |

The measurement identity is:

```text
reducer-proposal-envelope-comparison@1.0.0
```

This module consumes the completed `ReducerProposalLedger`. It does not observe
or modify the reducer calculation path directly.

```text
completed Dynamics execution
→ ReducerProposalLedger
→ optional ReducerProposalEnvelopeLedger
↛ HumanState / routing / evidence / action update
```

The projection is opt-in through `EngineConfig.reducer_proposal_envelope_policy`.
There is no automatically applied default human-capacity profile. Constructing
`ReducerProposalEnvelopePolicy()` explicitly selects the built-in synthetic test
fixture.

## Types

```text
ReducerProposalEnvelopePolicy
└─ ordered ReducerProposalEnvelopeBand tuple

ReducerProposalEnvelopeSnapshot
├─ policy digest
├─ source ReducerProposalReceipt ID
├─ source pre-update processing-checkpoint state-projection digest
├─ evaluated_at = source processed_at
└─ exact declared field bands

ReducerProposalEnvelopeReceipt
├─ source proposal policy / receipt / proposal digests
├─ occurrence / delivery / reexposure lineage
├─ canonical timestamps and processing sequence
├─ one snapshot
└─ flat ordered ReducerProposalEnvelopeComparison tuple

ReducerProposalEnvelopeLedger
└─ one receipt per source proposal receipt
```

Every comparison component retains:

```text
write_sequence
source stage / operator / field / storage constraint
basis_before
requested_delta
committed_delta
declared lower_delta / upper_delta
band_limited_delta
signed_proxy_excess
unit
comparison operator identity
```

## Policy rules

The policy contains exactly one band for every field in the current proposal
operator schema, in a fixed order. A missing, duplicate, unknown, or reordered
field is rejected. Bands are immutable, finite, in
`normalized_simulation_unit`, contain zero, and admit at least one nonzero
direction.

Policy digest binds:

```text
policy ID / version
exact field order and signed limits
source proposal measurement identity
comparison measurement and operator identity
aggregation_window = reducer_write
input_kind = MORPH-001A reducer-proposal proxy
capacity_depletion = not_modeled
cross_write_redistribution = not_modeled
available-information declaration
```

Limits are not restricted to `[-1, 1]`. Such a restriction would silently
re-couple the declared simulation band with state-storage validity.

## Formula

For each source proposal independently:

```text
requested_delta = requested_after_unbounded - basis_before

band_limited_delta
= min(max(requested_delta, lower_delta), upper_delta)

signed_proxy_excess
= requested_delta - band_limited_delta
```

The sign is retained. No occurrence total, normalized ratio, maximum, L1, or L2
aggregate is part of v1.

```text
signed_proxy_excess
≠ ExcessDemand
≠ UncommittedResidual
≠ ResidualStrain
≠ MorphicLoadProfile
```

## Repeated writes

An occurrence can write the same field through multiple operators. Each write
uses its own source `basis_before`, retains its own sequence and operator, and
is compared separately with the same declared field band.

```text
accuse impulsivity write
→ separate component

soothing impulsivity write
→ separate later component
```

Zero committed displacement, zero proxy excess, and cancellation are not
reasons to delete a mandatory source component. V1 does not model band
depletion or cross-write redistribution.

## Source and temporal integrity

The snapshot is bound to the source receipt ID and source
`state_before_digest`. This hashes MORPH-001A's fixed descriptive-state projection and
is a pre-update processing-checkpoint provenance anchor; the constant
v1 fixture does not infer its limits from the state.

The comparison receipt copies and binds:

```text
source proposal policy digest
source receipt ID / proposal digest / pre-state digest
processing sequence
occurrence / delivery / reexposure IDs
occurred_at / available_at / processed_at
snapshot ID
ordered comparison digest
```

`validate_reducer_proposal_envelope_ledger` then compares every receipt and
component back to the exact source ledger. It rejects missing receipts,
deleted/reordered components, source splicing, relabelled operators or fields,
and lineage mismatch.

- transport duplicate or redundant delivery has no source proposal receipt and
  therefore no comparison receipt;
- explicit current reexposure has a new source proposal receipt and retains its
  source occurrence reference;
- later input cannot rewrite a content-identical derived prefix.

Digests are internal consistency devices, not signatures or external truth
certificates.

## Read-only boundary

Changing or disabling the policy must not change:

```text
HumanState
TickTrace
EvidenceLink / EvidenceAssessment
routing candidates
Intent / Attempt / Performance / ActionOccurrence
MentalTransitionLedger
ReducerProposalLedger
input accounting or invariant errors
```

Only the optional envelope-comparison ledger and its summary fields may differ.

## Interpretation boundary

```text
ReducerProposalEnvelopePolicy
≠ measured human AccommodationEnvelope / CapacityProfile

ReducerProposalEnvelopeComparison
≠ independently identified DeformationDemand

ordered proxy-excess profile
≠ MorphicLoad
≠ qualia
≠ subjective / mental time
```

Passing this contract supports a reproducible simulation comparison surface. It
does not calibrate a human quantity or support the count–load dynamical
hypothesis.
