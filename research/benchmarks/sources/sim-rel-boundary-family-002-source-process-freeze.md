# S0 source process freeze — Family 002 / Runtime 001

| Field | Status |
|---|---|
| Source family | `SIM-REL-BOUNDARY-FAMILY-002` |
| Parameter generator | `FROZEN` |
| Public event schema | `PublicEventV3 FROZEN` |
| Trajectory runtime | `HUMAN-DYN-ADEQ-S0-SOURCE-RUNTIME-001 FROZEN` |
| Process adequacy diagnostic | `FROZEN` |
| Model V3 compatibility | `ABSENT / REQUIRED NEXT` |
| Future beacon | `UNRESOLVED / PROHIBITED` |
| Source instances | `0` |
| Corpus trajectories | `0` |
| Scores | `0` |

This freeze closes the evaluator-side transformation:

```text
source instance parameters
+ split-domain seed
→ canonical ordered public trajectories
+ P1/P2/P3 realized targets
```

It does not generate the benchmark family seed, retain a hidden source instance, materialize a corpus, fit a model, or calculate a leaderboard result.

## Family relation

Family 002 retains independent source-instance draws from one public hyperprior. It does not use one shared prototype with sixteen perturbations. Latent names `q0..q5` remain evaluator-hidden and instance-local; no cross-instance latent semantics are claimed.

Family 001 remains historical and is superseded before beacon resolution because it lacked feedback emissions, a complete trajectory runtime, and an observable predictive-memory acceptance rule.

## PublicEventV3

Model-visible history is one ordered discriminated union:

```text
OccurrenceEvent
| ActionEvent
| FeedbackEvent
| ContextEvent
| NoEvent
```

There is no generic `public_value` string. Each event kind has an exact typed payload and actor/target compatibility. Ordinals are exactly continuous `1..N`.

One `NoEvent` means one canonical source-process tick without new public information. It is not a measured human duration.

## Hidden continuation branch

`F-REPAIR`, `F-DEFLECT`, `F-REPEAT`, and `F-PUBLIC` are evaluator-only cell metadata and transition selectors. They are absent from the model-visible prefix.

Within the same source instance, history condition, split, and cell sample:

```text
P1 observable prefix bytes
and P1 realized action target
```

are identical across all four hidden branches. Initial latent, P1 action, and P1 feedback use a branch-free matched seed. The first branch-conditioned latent transition occurs only after P1 action and feedback, and branch identity becomes inferable only through later public cue events.

## Runtime

```text
1  CURRENT_COMMITMENT_MISSED → P1 target
2  realized P1 action becomes public
3  action-conditioned feedback becomes public
   branch-conditioned latent transition
4  first branch cue → P2 target
5  realized P2 action becomes public
6  action-conditioned feedback becomes public
   branch-conditioned latent transition
7  second branch cue → P3 target
   final branch-conditioned latent transition
   terminal long-horizon emission
```

The one terminal region is the long-horizon target at P1, P2, and P3. No hidden P3 feedback is sampled because feedback does not condition the latent transition in S0.

This is an observable action-conditioned feedback sequence, not a full action–world–state closed loop. The source uses realized source action labels, not candidate-model outputs, to generate later feedback.

## Randomness

Random streams are domain-separated for:

- family / instance parameters,
- split,
- matched prebranch sampling,
- branch-specific trajectory continuation,
- each latent/action/feedback/terminal draw.

A sampling operation can be added to one domain without shifting the random sequence of another domain. Post-seed trajectory selection, deduplication, replacement, or regeneration is forbidden.

## Process adequacy

Candidate instances must pass model-independent exact filtering diagnostics. The comparator is:

```text
P(future | complete model-visible public history)
versus
P(future | last public event + current visible context)
```

The source instance ID and hidden continuation branch are excluded. The branch is marginalized until its public cue. Acceptance also bounds the Dobrushin coefficient of every continuation transition so the process is neither immediately mixed nor effectively frozen.

The calibration panel uses fixed public labels only to test generator feasibility. It retains no source parameters, uses no future beacon, and reads no candidate-model output or score.

## A-C5 correction

The same-category universal-collapse statistic is now:

```text
max_category min_point P(category | point)
```

Thus different dominant categories in different conditions are not mislabeled as one universal mode. Responsiveness uses only preregistered matched intervention pairs; an arbitrary large all-pairs distance cannot satisfy the contract.

## Claim authority

This source process is being designed after candidate model work already exists. Future results therefore support only:

```text
NON_HUMAN_CO_DESIGNED_PROCESS_CONDITIONAL_ADEQUACY
```

They cannot establish independent-environment generality, human empirical support, or superiority over all reasonable direct-history models.

## Next gate

The next PR must adapt B0/B1/B2/H and evaluation reporting to `PublicEventV3`, including action/feedback state updates, expected-repair clock correction, point-level and model-wide coverage reports, and joint compatibility tests.

Only the merge of that model-v3 activation PR may authorize future beacon resolution.
