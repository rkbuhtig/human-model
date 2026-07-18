# HUMAN-DYN-ADEQ-S0 — Distributional Adequacy Slice 0

| Field | Status |
|---|---|
| Benchmark class | minimal distributional adequacy slice |
| Status | `DRAFT / UNEXECUTED` |
| Human-empirical status | `NO HUMAN DATA` |
| Canonical runtime status | none |
| Claim support | none |

This document defines the first comparison required by the distributional-adequacy mainline. It does not freeze a runner ABI, record ordering, exact trace bytes or a canonical HumanState schema.

## 1. Question

Does an explicit state-and-settlement representation provide a complexity-adjusted advantage over simpler models when predicting held-out episode trajectory distributions?

The benchmark does not ask whether one generated response matches one author-written answer. It asks whether the model assigns and updates possibility mass in the right directions under controlled history, intervention and feedback changes.

## 2. Single episode family

S0 uses one relationship-boundary family only.

### Initial relation

The focal person values continuation of the relationship. Two history conditions are compared:

```text
H-STABLE
- prior reliability is high
- occasional ambiguity has usually resolved safely

H-BREACH
- prior reliability has been repeatedly violated
- ambiguous delays have previously predicted real withdrawal or avoidance
```

### Current occurrence

A counterpart fails to keep an important commitment under initially ambiguous circumstances.

The initial public record is identical across history conditions. Hidden motive or internal state is not supplied as fact.

### Registered continuation branches

```text
F-REPAIR
counterpart acknowledges impact, accepts responsibility and offers a costly repair

F-DEFLECT
counterpart minimizes impact and shifts responsibility

F-REPEAT
a similar violation occurs again before repair is consolidated

F-PUBLIC
the issue must be handled under an audience or role constraint
```

S0 does not include additional episode families, diagnosis labels, treatment language or open-ended life histories.

## 3. Competing models

All models receive the same observable history and current occurrence surface.

### B0 — Current-event only

```text
current occurrence + current context
→ action-function distribution
```

No persistent state or history is available.

### B1 — Simple accumulator

```text
trust scalar
valence scalar
current occurrence
→ next-state scalars + action-function distribution
```

This baseline may accumulate but has no separate settlement ledgers, Episode residue or Narrative topology.

### B2 — Direct history model

```text
full observable history + current occurrence + context
→ action-function and future-trajectory distributions
```

B2 has no required explicit intermediate HumanState. It is the primary test of whether the proposed state representation adds value beyond direct history conditioning.

### H — State-and-settlement model

The H model may use an explicit internal representation drawn from the current synthesis:

```text
fast state
episode residue
slow narrative/self state
capacity
self/other models
occurrence/action/authorship/narrative settlement ledgers
```

S0 does not prescribe the exact internal object layout. Any submitted H representation must declare its state surface, update rules, readouts and complexity accounting before evaluation.

## 4. Output surface

Each model must emit distributions over registered functional categories, not exact wording.

### Immediate action functions

```text
SEEK_CLARIFICATION
EXPRESS_HURT
ASSERT_BOUNDARY
TEMPORARY_WITHDRAWAL
PUNITIVE_ATTACK
SUPPRESS_FOR_ROLE
REPAIR_ATTEMPT
RELATION_EXIT
```

### Next-state directional readouts

```text
trust: increase / stable / decrease
relationship-continuation motive: increase / stable / decrease
threat interpretation: increase / stable / decrease
action-control capacity: increase / stable / decrease
```

### Long-horizon region readout

```text
PARTIAL_REPAIR
GUARDED_CONTINUATION
CONFLICT_LOOP
RELATION_EXIT
UNRESOLVED_DRIFT
```

These labels are benchmark readouts. They are not asserted to be canonical human mental states.

## 5. Distributional execution

Each model is executed over multiple stochastic rollouts.

```text
development seed panel
- public; used for debugging

evaluation seed panel
- preregistered and not available to the generating process during development

stability seed panel
- used once after model selection to test sensitivity to seed-panel choice
```

Environment and model stochasticity must use distinguishable streams or receipts. Determinism means that fixed inputs, model version and seed panel reproduce the same rollout set; it does not mean every rollout is identical.

## 6. Constraint reference

S0 does not freeze exact target probabilities. It registers directional and exclusion constraints.

### C1 — History sensitivity

Under the same current occurrence:

```text
H-BREACH
must not assign less threat-oriented mass than H-STABLE
without an explicit countervailing state difference.
```

### C2 — Repair discrimination

```text
F-REPAIR
must shift more probability toward PARTIAL_REPAIR or GUARDED_CONTINUATION
than F-DEFLECT under the same prefix.
```

### C3 — Repetition sensitivity

```text
F-REPEAT
must not increase immediate full-repair probability relative to a matched no-repeat branch.
```

### C4 — Projection selectivity

```text
F-PUBLIC
may shift surface suppression and role-compatible expression,
but must not rewrite the prior occurrence or automatically restore trust.
```

### C5 — Local variation with structural constraint

The rollout set must avoid both:

```text
mode collapse
- nearly all mass on one immediate function in every micro-context

unstructured randomness
- history and continuation interventions do not reliably move the distribution
```

### C6 — No automatic healthy convergence

Repair, apology or regret must not force every rollout into a healthy basin. Defensive, avoidant or conflict-maintaining branches remain legal when supported by declared state and feedback rules.

## 7. Evaluation lanes

### 7.1 Immediate distribution fit

Evaluate whether intervention and history changes move action-function mass in registered directions.

### 7.2 One-step state transition

Provide a declared reference state surface where needed and compare one-step directional transitions without rollout error accumulation.

### 7.3 Free rollout

After the initial condition, feed each model its own previous state or history representation. Measure divergence, mode occupancy and sensitivity across continuation branches.

### 7.4 Predictive sufficiency

For H, compare:

```text
P(future | explicit H state)
versus
P(future | explicit H state + full history)
```

If adding full history materially improves held-out prediction, the explicit state may have omitted predictive information.

### 7.5 Representation benefit

Compare H against B2 under declared complexity controls.

H earns retention only if it improves at least one of:

```text
held-out predictive performance
compression at comparable performance
intervention selectivity
long-horizon stability
data efficiency
usable state-level explanation with successful probes
```

A more interpretable vocabulary without predictive or intervention benefit is not sufficient.

## 8. Failure conditions

S0 fails as an adequacy benchmark if any of the following occurs:

```text
reference constraints encode one exact author-preferred trajectory
model-specific expected traces are visible to the generating process
only surface wording is evaluated
seed choice determines the conclusion without stability analysis
H receives information unavailable to B2
a model is revised after evaluation-panel results without a new versioned run
a second episode family is added before S0 is executed
```

The H hypothesis is not supported if it provides no complexity-adjusted benefit over B2 or if its state variables cannot be probed independently of the outputs they were introduced to explain.

## 9. Required artifacts for the later preregistration PR

This draft authorizes no implementation. A later preregistration must freeze only what is needed to compare models fairly:

```text
observable episode input surface
registered branch generator
functional output vocabulary
constraint predicates
seed-panel identities and visibility lanes
model version and allowed information
complexity accounting
result and evaluation separation
```

It should not freeze internal record rank, exact record IDs, source-file counts or one canonical HumanState representation unless those details are themselves the explicit subject of a separate structural test.

## 10. Exit condition

S0 is complete only after a versioned execution and evaluation report exists for B0, B1, B2 and H.

The next episode family may be opened only after the report states:

```text
what H predicted better or worse
where state information was insufficient
which constraints were non-discriminating
whether seed-panel stability held
which representation should be retained, revised or retired
```

Contract verification without these results does not complete S0.