# Adoption Record — HUMAN-DYN-ADEQ-S0 initial model freeze

| Field | Value |
|---|---|
| Decision date | 2026-07-18 |
| Decision | `ADOPT INITIAL IMPLEMENTATION FREEZE` |
| Runtime status | `IMPLEMENTED / FROZEN / UNEXECUTED ON S0 SOURCE` |
| Human-empirical authority | `NONE` |

## Decision

The initial B0, B1, B2 and H implementations, their shared public input surface,
detached runner/scorer, model cards and initial unfit parameters are adopted as
the first implementation freeze governed by `HUMAN-DYN-ADEQ-S0`.

```text
same public prefix
+ shared categorical learner
+ model-specific feature residence
→ comparable initial candidate implementations
```

The freeze is bound by
[`initial-model-freeze-manifest.json`](../benchmarks/models/s0/initial-model-freeze-manifest.json).

## Authority boundary

This decision does not adopt H as a canonical HumanState ontology and does not
establish predictive or human adequacy. It contains no hidden source instance,
development corpus, evaluation corpus, stability corpus, target probabilities,
result or representation decision.

H-only diagnostic state is explicitly excluded from B2/H leaderboard evidence.
Receipt registration does not certify a world claim; authorship and normative
settlement dimensions remain non-interchangeable.

## Next gate

```text
initial model freeze
→ evaluator-side source-instance freeze
→ development corpus materialization
→ development-only fitting
→ final model freeze
```

No evaluation or stability target may become visible before the final model
freeze.
