# Adoption Record — S0 source-family and fairness amendment

| Field | Value |
|---|---|
| Decision ID | `ADOPT-S0-AMEND-001` |
| Date | `2026-07-18` |
| Status | `ADOPTED` |
| Scope | S0 source construction, structural predicates and adequacy claim authority |

## Decision

Adopt [`HUMAN-DYN-ADEQ-S0-AMEND-001`](../benchmarks/human-dyn-adequacy-s0-amendment-001.md) before any evaluator source seed, instance or corpus is generated.

The initial model implementation frozen through PR #25 remains a reproducible historical implementation but is not eligible to authorize source resolution.

```text
HUMAN-DYN-ADEQ-S0-MODEL-FREEZE-INITIAL-001
= FROZEN HISTORICAL IMPLEMENTATION
= UNEXECUTED
= MUST BE SUPERSEDED BEFORE SOURCE INSTANCE
```

A later record must explicitly adopt:

```text
HUMAN-DYN-ADEQ-S0-MODEL-FREEZE-INITIAL-002
```

before the future beacon round is selected.

## Adopted changes

1. Replace one manually specified hidden process with a public source-family generator and sixteen future-seeded instances.
2. Freeze a public hyperprior and forbid model-output or score-based candidate acceptance.
3. Include every generated instance; forbid post-generation selection or replacement.
4. Separate predictive leaderboard, state-sufficiency diagnostic and online-compression diagnostic.
5. Replace natural-language S0-A exceptions with exact matched-case predicates.
6. Move authority-integrity claims that lack an observable output surface into implementation tests.
7. Require identity-joined scoring and hierarchical instance/trajectory bootstrap in model freeze v2.

## Immediate hold

Until `INITIAL-002` is merged:

```text
future beacon resolution           FORBIDDEN
source instance generation         FORBIDDEN
development corpus materialization FORBIDDEN
S0 scoring                         FORBIDDEN
```

## Preserved artifacts

PRs #24 and #25 are not reverted. Their documents, code and tests remain evidence of the first executable comparison surface and of the defects found before source exposure.

The amendment supersedes only their use as the active source-generation and evaluation authority.

## Next required work

```text
B2 order/count-preserving baseline
+ H incremental state interface
+ no raw-history reread in H-STATE-ONLY
+ shared predictive readout without model-specific base logits
+ typed receipt compatibility
+ identity-joined scorer
→ INITIAL-002 freeze
```
