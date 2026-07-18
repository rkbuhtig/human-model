# HUMAN-DYN-ADEQ-S0 initial model freeze v2

| Field | Status |
|---|---|
| Freeze ID | `HUMAN-DYN-ADEQ-S0-MODEL-FREEZE-INITIAL-002` |
| Implementation | `FROZEN` |
| Parameters | `INITIAL_UNFIT_V2` |
| Source seed | `UNRESOLVED` |
| Source instances/corpora/results | `ABSENT` |
| Human empirical support | `NONE` |

This freeze supersedes `INITIAL-001` before any source instance exists. The old
implementation remains historical and reproducible but cannot authorize beacon
resolution or source materialization.

## Fair comparison surface

```text
B0  current public event/context
B1  trust/valence accumulator
B2  order/count-preserving direct public history
H   incremental typed predictive state
```

All four predictive candidates use the same counted multinomial learner with no
model-specific base logits. Because H still has a hand-specified update kernel,
results compare representation-and-update pipelines, not a pure isolated state
representation effect.

## H execution modes

```text
H-FULL
full public prefix → reconstruct state → predict

H-STATE-ONLY
previous serialized state + exactly one public delta → next state → predict
```

State-only execution cannot receive a full prefix. It reports state input,
update input and result-state bytes separately and marks `raw_history_read=false`.

## Scoring

Predictions and targets join by:

```text
source_instance_id
+ trajectory_id
+ step_ordinal
+ prediction_point_id
```

Duplicate keys and unequal key sets fail. Loss is aggregated by trajectory and
source instance; B2/H intervals use hierarchical instance-then-trajectory
bootstrap.
