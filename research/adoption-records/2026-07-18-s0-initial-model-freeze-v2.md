# Adoption — S0 initial model freeze v2

| Artifact | Status |
|---|---|
| `INITIAL-001` | `FROZEN HISTORICAL / SUPERSEDED BEFORE SOURCE INSTANCE` |
| `INITIAL-002` | `IMPLEMENTED / FROZEN / UNEXECUTED` |
| Source seed | `UNRESOLVED` |
| Corpus/result | `ABSENT` |

`INITIAL-001` exposed a lossy B2 representation, full-history H replay,
model-specific base logits and positional scoring. No source instance existed,
so this adoption supersedes it without contaminating a target or result.

`INITIAL-002` adopts:

- order/count-preserving B2 counted features,
- incremental H state with full and state-only modes,
- typed receipt compatibility before transition,
- predictive-state and authority-probe separation,
- a shared predictive learner without model-specific base logits,
- identity-joined trajectory scoring and hierarchical bootstrap,
- actual state-to-state directional diagnostics outside the leaderboard.

The next gate may resolve the future randomness beacon only after this freeze is
merged and bound. No source instance or corpus is authorized by the branch alone.
