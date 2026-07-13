# MORPH-001B — Reducer Proposal / Declared Envelope Comparison

## Status and claim boundary

`MORPH-001B` tests whether the ordered reducer proposals captured by
`MORPH-001A` can be compared reproducibly with an explicit, versioned,
experimenter-declared simulation band.

```text
ReducerProposal
+ declared reducer-write simulation band
→ ReducerProposalEnvelopeComparison
→ ordered proxy-excess profile
```

The band is a measurement-policy parameter. It is not an estimate of human
accommodation capacity. The result is not an independently identified demand,
residual strain, morphic load, qualia, or subjective-time quantity.

```text
ReducerProposalEnvelopePolicy
≠ measured human AccommodationEnvelope / CapacityProfile

ReducerProposalEnvelopeComparison
≠ DeformationDemand
≠ ExcessDemand
≠ ResidualStrain
≠ MorphicLoadProfile
≠ qualia
≠ subjective / mental time
```

## Preregistered v1 policy

Measurement identity:

```text
reducer-proposal-envelope-comparison@1.0.0
```

Comparison operator:

```text
componentwise-signed-exceedance@1.0.0
```

The policy declares exactly one signed band for every field used by the
versioned reducer proposal schema. Every band is in
`normalized_simulation_unit` and contains zero. The two directions may have
different limits.

The built-in `synthetic-asymmetric-reducer-write-envelope@1.0.0` profile is an
author-chosen test fixture. Its values exercise direction and magnitude
dissociations; no value is calibrated from human data.

```text
aggregation window       = reducer_write
capacity depletion       = not modeled
cross-write redistribution = not modeled
```

The same field may be written more than once in one occurrence. Every ordered
write is compared separately against the declared field band. The writes are
not summed into an occurrence net delta and do not consume a shared capacity.

The snapshot is bound to the source proposal receipt and its fixed pre-update
processing-checkpoint state-projection digest. The v1 bands are constant policy parameters; binding the
pre-update digest supplies provenance, not state-dependent human
calibration.

## Componentwise calculation

For one ordered proposal write:

```text
r = proposal.requested_delta
a = clip(r, lower_delta, upper_delta)
signed_proxy_excess = r - a
```

`committed_delta` remains present as a source quantity but does not define the
band or the proxy excess. In particular:

```text
storage clamp loss = requested_delta - committed_delta
≠ signed_proxy_excess
```

An envelope upper limit may be wider than the remaining distance to the
`[0, 1]` storage bound. A proposal can therefore lose displacement to storage
clamping while producing zero proxy excess, or commit no change while two
different proposal magnitudes produce different proxy excess.

## Competing definitions held for later comparison

Only the componentwise signed result is implemented in this slice. The
following remain preregistered competitors, not adopted load measures:

```text
C0 componentwise signed exceedance     # implemented reference output
C1 directional normalized exceedance   # unimplemented
C2 occurrence maximum                  # unimplemented
C3 occurrence L1 aggregate             # unimplemented
C4 occurrence L2 aggregate             # unimplemented
```

No scalar `total_load`, mental-time value, or phenomenal score is emitted.
Aggregation may be proposed only after a separately specified outcome
comparison can discriminate alternatives without using the same data to choose
and confirm the operator.

## Structural probes

The implementation must satisfy all of the following.

1. The same source proposal under two declared bands can yield different proxy
   excess, while the source proposal receipt remains identical.
2. Two saturated proposals can have the same committed delta and different
   requested deltas and proxy excess.
3. Two runs can have the same qualified mental-transition count and different
   ordered proxy-excess profiles.
4. Equal-magnitude positive and negative proposals can yield different results
   under an asymmetric band.
5. The `[0, 1]` state-storage constraint or clamp gap cannot be reused as an
   envelope band or proxy excess.
6. Every proposal receipt maps to exactly one comparison receipt, and every
   ordered proposal maps to exactly one ordered comparison component.
7. Repeated writes to one field remain separate; saturation and cancellation
   cannot delete a component.
8. Transport redelivery creates no additional comparison. Explicit current
   reexposure retains source provenance in a new processed-occurrence receipt.
9. Policy changes alter only the derived comparison policy, receipt identity,
   and output. State, trace, evidence, routing, action, Q-v1, and source proposal
   ledgers remain unchanged.
10. Appending later events cannot rewrite an identical comparison prefix.
11. Component arithmetic, policy ranges, source receipt identity, proposal
   order, temporal lineage, and pre-update state-projection digest are content-bound and
    validated against the source ledger.
12. Finite invalid initial state continues through the existing invariant audit
    path rather than becoming a comparison exception.

The digests and validators provide internal schema integrity. They are not
cryptographic authentication and do not certify that a directly constructed,
self-consistent synthetic record describes an external fact.

## Interpretation of a passing run

A passing run establishes only this simulation result:

> A versioned proposal trace can be compared reproducibly with a declared,
> asymmetric reducer-write band without changing the generating execution.

It does not support `HM-DYN-002`. The synthetic bands are not empirical human
capacity estimates, and the current reducer proposal is still confounded by
model-specific drivers.

## Next slice

`MORPH-001C` must preregister outcomes and competing models before introducing
any load claim. It must ask whether a proposal/envelope relation adds held-out
discrimination for recovery, residual behavior, or retention beyond transition
count and simpler proposal-magnitude alternatives. Until then,
`MorphicLoadProfile`, `ResidualStrain`, the phenomenal bridge, and mental-time
interpretation remain `UNIMPLEMENTED / HOLD`.
