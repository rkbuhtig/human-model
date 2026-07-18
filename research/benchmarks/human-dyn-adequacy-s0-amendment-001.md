# HUMAN-DYN-ADEQ-S0 Amendment 001 — Source-Family Independence and Claim Separation

| Field | Status |
|---|---|
| Amendment | `HUMAN-DYN-ADEQ-S0-AMEND-001` |
| Status | `ADOPTED BEFORE SOURCE INSTANCE` |
| Hidden source instances | `ABSENT` |
| Future beacon | `UNRESOLVED` |
| Initial model freeze 001 | `HISTORICAL / NOT ELIGIBLE FOR SOURCE RESOLUTION` |
| Required next model freeze | `INITIAL-002` |
| Human empirical support | `NONE` |

This amendment controls whenever it conflicts with the original S0 preregistration or singular source contract.

```text
model-visible protocol
≠ evaluator-hidden instance
≠ human empirical evidence
```

## 1. Why this amendment exists

The original freeze order prevented models from reading target parameters but still allowed a reverse tailoring path:

```text
implemented B2/H
→ human source designer inspects their structure
→ source matrices chosen after that inspection
```

Multiple instances alone do not remove this risk if their hyperprior is itself selected to favor a model. This amendment therefore freezes a public generator and public hyperprior before any source seed or instance exists.

The procedure reduces source-tailoring risk. It is not a cryptographic proof of complete model independence because the source family was specified after initial candidate code existed.

## 2. Public source family

The singular source ID is replaced by:

```text
SIM-REL-BOUNDARY-FAMILY-001
├─ INSTANCE-0000
├─ INSTANCE-0001
├─ ...
└─ INSTANCE-0015
```

All sixteen instances must be included. The evaluator may not inspect model scores and then retain, replace, regenerate or discard individual instances.

Public artifacts:

- [`sources/sim-rel-boundary-family-001-public.json`](sources/sim-rel-boundary-family-001-public.json)
- [`sources/sim-rel-boundary-family-001-hyperprior.json`](sources/sim-rel-boundary-family-001-hyperprior.json)
- [`dynamics.s0.source_family`](../../dynamics/s0/source_family.py)

The generator imports no candidate model, runner or scorer module.

## 3. Intrinsic candidate acceptance only

A generated source candidate may be rejected only for public, model-independent source validity:

```text
probabilities are normalized
category probabilities remain inside frozen bounds
history conditions have a non-zero initial-distribution effect
continuation conditions have a non-zero transition effect
latent states have non-degenerate observable emissions
candidate-attempt limit is finite
```

Forbidden acceptance inputs include:

```text
model identity
model output
B2/H NLL
leaderboard result
preferred winner
representation label
human-plausibility judgment
```

A deterministic attempt counter resolves an intrinsically invalid candidate. It does not search for a model-performance outcome.

## 4. Future randomness

No family seed is included in this PR.

The source-family seed is resolved after `INITIAL-002` by the first verifiable drand quicknet round whose timestamp is at least one hour after the amendment merge commit timestamp.

```text
family_seed = SHA256(
  generator_version
  | family_id
  | amendment_merge_commit_sha
  | generator_blob_sha
  | hyperprior_blob_sha
  | beacon_randomness
)
```

The resolution receipt must record the chain hash, round, timestamp, randomness, signature and verification result. Manual seed substitution is forbidden.

## 5. Three different adequacy claims

The earlier compression language combined three different questions. They are now separated.

### S0-B-PRED — Predictive leaderboard

```text
B2-FULL
full observable prefix → prediction

H-FULL
full observable prefix → state reconstruction → prediction
```

This lane compares source-family-conditional prediction under identical observable information. It does not establish state sufficiency or online compression.

### S0-B-SUFF — State sufficiency diagnostic

```text
H-FULL
versus
H-STATE-ONLY
```

`H-STATE-ONLY` receives only the previous serialized state plus the next public delta and context. A material improvement from reintroducing full history indicates omitted predictive information.

This diagnostic does not by itself establish advantage over B2.

### S0-B-COMP — Online compression diagnostic

A compression claim requires all of the following:

```text
H-STATE-ONLY performs no raw-history reread
state bytes and update-input bytes are reported
static model bytes are reported separately
update compute is reported
registered performance tolerance is preserved
```

A state reconstructed from full history at every prediction point is a compact projection, not an online predictive-state compression result.

## 6. Structural predicates become executable

The structural contract is now machine-readable and implemented in:

- [`s0-structural-predicates-v2.json`](s0-structural-predicates-v2.json)
- [`dynamics.s0.structural`](../../dynamics/s0/structural.py)

The undefined phrase “unless the model emits a registered countervailing observable reason” is removed. Matched cases own all allowed differences.

Exact output predicates are:

```text
A-C1 history sensitivity
A-C2 repair discrimination
A-C3 repetition sensitivity
A-C4 projection selectivity
A-C5 local variation / gross-collapse detection
```

`No automatic healthy convergence` remains an interpretive non-requirement rather than a pass/fail rule.

Authority integrity moves to implementation tests because the current common prediction surface cannot express world-fact certification, consent issuance or normative authority. Absence of those outputs is not evidence that a model correctly handled those jurisdictions.

## 7. Source-family evaluation

Each source instance contributes:

```text
16 development trajectories
64 evaluation trajectories
64 stability trajectories
```

Every instance and split is balanced across the two history by four continuation grid.

Reports must include:

- per-instance scores,
- pooled scores,
- direction of B2/H difference per instance,
- hierarchical bootstrap that resamples source instances and then trajectories.

A pooled advantage driven by one or two hand-picked instances is insufficient.

## 8. Identity-joined scoring requirement

The v2 scorer must join predictions and targets by:

```text
source_instance_id
+ trajectory_id
+ step_ordinal
+ prediction_point_id
```

It must reject duplicate keys, unequal key sets and positional `zip` pairing. Losses are aggregated per trajectory before the hierarchical bootstrap.

## 9. Freeze order

```text
public amendment + generator + hyperprior
→ INITIAL-002 model freeze
→ future beacon resolution
→ all sixteen source instances
→ development corpus
→ final model freeze
→ evaluation and stability corpora
→ detached hierarchical evaluation
→ source and result reveal
```

The beacon and source instances must not be resolved from `INITIAL-001`.

## 10. Explicit non-claims

This amendment does not establish:

- complete model-independent source construction,
- human predictive adequacy,
- a canonical HumanState,
- an implemented incremental H state machine,
- a fair B2/H representation-isolation result,
- a source instance, corpus or score.
