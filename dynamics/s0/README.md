# HUMAN-DYN-ADEQ-S0 candidate models

`dynamics.s0` is a dependency-free initial implementation of the four S0
candidate models. It is detached from the canonical Dynamics runtime.

```text
B0  current event and current context
B1  trust/valence accumulator
B2  full observable-prefix features
H   explicit multi-timescale state and typed settlement features
```

All models use the same deterministic categorical learner and the same public
input object. The differentiating variable is the feature residence rather
than a different base inference engine.

## Authority boundary

```text
public observable prefix
→ candidate model
→ probability-unit PredictionBundle

candidate model
↛ evaluator hidden state
↛ target labels
↛ source transition/emission parameters
```

Probabilities are serialized as integer millionths summing to `1_000_000`.
Floating-point values are used only inside model/scoring calculations and are
not part of prediction-bundle canonical bytes.

H diagnostics are opt-in and marked
`H_ONLY_NOT_LEADERBOARD_EVIDENCE`. The detached scorer consumes prediction
bundles and target labels; the runner does not import the scorer.

## Commands

```bash
python -m dynamics.s0.run_cli \
  --model H \
  --input prefix.json \
  --parameters research/benchmarks/models/s0/initial-parameters.json \
  --model-cards research/benchmarks/models/s0/model-cards.json \
  --output prediction.json

python -m dynamics.s0.score_cli \
  --predictions predictions.json \
  --targets evaluator-targets.json \
  --output score.json
```

This freeze contains no `SIM-REL-BOUNDARY-001` hidden source instance,
development/evaluation/stability corpus or S0 result.
