# HUMAN-DYN-ADEQ-S0 initial model implementation freeze

| Field | Status |
|---|---|
| Benchmark | `HUMAN-DYN-ADEQ-S0` |
| Implementation | `FROZEN` |
| Parameters | `INITIAL_UNFIT` |
| Hidden source | `ABSENT` |
| S0 execution | `UNEXECUTED` |
| Human empirical support | `NONE` |

This slice implements B0, B1, B2 and H plus a common runner, detached scorer,
development-only fitting function, model cards and information-boundary tests.

```text
shared learner
+ different feature residence
→ comparable candidate models
```

The implementation deliberately does not contain the evaluator-side
`SIM-REL-BOUNDARY-001` transition matrix, emission parameters, source seeds,
target probabilities or any development/evaluation/stability corpus.

## Model separation

- B0 reads current event and current context only.
- B1 reduces observable history to trust and valence scalars.
- B2 uses full observable-prefix event, order, action and feedback features.
- H updates an explicit candidate state and predicts from state features rather
  than adding raw history to the readout.

H separates causal attribution, control attribution, reflective ownership,
endorsement and responsibility acceptance. Consent, fault, obligation,
permission and authority remain separate fields. These are S0 candidate fields,
not a canonical human ontology.

## Execution boundary

Every prediction carries the public-prefix digest, visible field names, input
byte count, state byte count and explicit `target_visible=false` /
`reference_state_visible=false` receipts. H diagnostics require an explicit flag
and cannot be counted as leaderboard evidence.

## Scoring surface

The detached scorer implements immediate and long-horizon NLL, multiclass
Brier, fixed-bin ECE, branch-occupancy absolute error and deterministic paired
bootstrap intervals. No score or target is produced in this slice.

## Validation

```text
python -m unittest discover -s dynamics/tests -p 'test_s0_*.py' -v
18 tests passed

python -m compileall -q dynamics/s0 dynamics/tests
passed
```

The next gate is evaluator source-instance freeze, development corpus
materialization, development-only fitting and final model freeze.
