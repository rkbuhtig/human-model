# Current Synthesis — Multi-Clock Distributional Human Dynamics

| Field | Status |
|---|---|
| Document class | current synthesis |
| Adoption status | `ADOPTED AS PROGRAM DIRECTION` |
| Runtime status | `UNIMPLEMENTED AS ONE MODEL` |
| Human-empirical status | `OPEN` |
| Canonical ontology status | `NOT FROZEN` |

This document integrates the December persona-engine lineage, the January chapters and the July typed-contract program. It does not claim that the recovered engine already modeled humans correctly.

## 1. Central object of study

The target is not one exact thought, action or trace.

```text
same person and macro-history
+ similar current occurrence
+ varying micro-context, attention and capacity
→ multiple plausible interpretations and actions
```

Local variation is constrained. Self-feedback, social response, memory access, resource limits and delayed settlement organize possible paths over time.

```text
local possibility distribution
+ path-dependent transition law
+ multiple settlement clocks
+ long-run episode/narrative organization
```

A state representation earns retention only if it improves held-out source prediction, compression, intervention selectivity or generalization over simpler alternatives.

## 2. Five functional regions

These are functional regions, not canonical classes or files.

### 2.1 Internal State

```text
FastState
- current affect, attention and salience
- present interpretation
- impulse and action readiness

EpisodeResidue
- medium-timescale unresolved relations
- recent path-dependent accessibility
- local hysteresis and after-effects

Narrative/Self State
- slow recurrent expectations and return paths
- long-run self/relationship organization

CapacityState
- fatigue and control capacity
- attentional, temporal and social-risk limits

SelfOtherModels
- current self-model
- compressed model of other agents
- bounded approximation of reciprocal modeling
```

These components need not update at the same rate.

### 2.2 Settlement Receipts

A human event can be final in one jurisdiction and unsettled in another. `Ledger` denotes an append-only collection of typed receipts, not a universal truth store.

#### OccurrenceReceiptLedger

```text
OccurrenceReceipt
- source identity and provenance
- declared scope
- occurred/reported/registered time
- submitted or observed occurrence content
- grounds lane
```

Minimum scopes:

```text
REGISTERED_REPORT
- a source reported the content

INTERNAL_OCCURRENCE_REPORT
- the subject reported a feeling, thought or perception occurrence

CERTIFIED_WORLD_OCCURRENCE
- a separate evidence/grounds protocol established an external occurrence
```

```text
receipt registration
≠ certification of every world claim in the payload
```

The immutable object is the registered receipt and its provenance. Later interpretation must not silently alter that receipt. This does not make all receipt content externally true.

#### ActionReceiptLedger

Records realized action occurrence. It does not by itself certify intent, control, quality, endorsement or outcome.

#### AuthorshipSettlementLedger

Authorship is multi-dimensional.

```text
causal_attribution
control_attribution
reflective_ownership
endorsement
responsibility_acceptance
```

These relations may diverge. A person may repudiate an action while accepting responsibility for repair.

#### NarrativeAdoptionLedger

Records current durable incorporation into a self/relationship account. Later re-adjudication may change placement without rewriting the occurrence receipt.

#### NormativeSettlementLedger

Normative settlement is not one scalar. It preserves independent typed relations:

```text
consent
fault
obligation
permission
authority
recognized remedy
```

Self-authorship or Narrative cannot issue another person's consent or authority.

### 2.3 Context

```text
external occurrence
physical environment
role and audience
relationship configuration
actual other-agent response
available information
current bodily conditions
```

Context is not part of the person merely because it shapes the person. Internal other-models remain distinct from the actual other agent.

### 2.4 Transition Kernel

```text
candidate generation
constraint shaping
selection and action realization
surface projection
self-feedback
social feedback
retrospective authorship adjudication
slow adaptation of future transition tendencies
```

Narrative may partly reside in slow state and partly parameterize this kernel. That placement remains open.

### 2.5 Readouts

```text
interpretation distribution
action-function distribution
surface-expression distribution
future trajectory distribution
```

Readouts are not automatically persistent state, evidence or settlement receipts.

## 3. Multi-clock settlement

Human dynamics does not use one universal commit boundary.

```text
an occurrence receipt may become immutable immediately
an action may be realized before reflective endorsement
authorship may be reconsidered later
Narrative adoption may require repeated episodes
normative settlement may depend on other agents or institutions
```

### 3.1 Occurrence immutability

After registration, a receipt's bytes, source, scope and provenance are immutable. The receipt may represent a report rather than a certified world fact.

```text
registered report remains fixed
≠ reported proposition is externally certified
```

### 3.2 Retrospective authorship adjudication

Later access may change the subject's current relation to a past occurrence or action.

```text
what was registered then                     fixed receipt
what I now think it meant                    revisable
whether I causally produced it               evidence-sensitive
whether I could control it                    revisable assessment
whether I endorse it                         revisable
whether I accept repair responsibility       revisable
how it belongs in my self-narrative          revisable
what rights another person has               separate settlement
```

No-backflow and retrospective re-adjudication are complementary.

### 3.3 Partial finality

A record can be final for one jurisdiction and open for another. The architecture must not collapse this into one `COMMITTED / NOT_COMMITTED` bit.

## 4. Authority topology

```text
local causal influence
≠ cross-domain certification authority
```

Examples:

```text
affect may bias attention
but does not certify an external fact

Narrative may bias future sampling
but does not rewrite a registered occurrence receipt

reflective ownership may alter future conduct
but does not issue another person's consent

a generated candidate may influence selection
but is not the action or settlement receipt
```

Candidate formalization:

```text
Authority = actor × operation × target × scope × grounds × effective clock
```

This is a current synthesis and possible contribution. Literature uniqueness remains unestablished.

## 5. Episode and Narrative

### 5.1 Episode

At the empirical surface, an episode is one realized trajectory:

```text
history and state
→ encounter
→ interpretation
→ action
→ result
→ self/social feedback
→ subsequent state
```

At the state level, `EpisodeResidue` denotes medium-timescale effects left by trajectories. RFC 0004's object-assembly representation remains one candidate, not the unique ontology.

### 5.2 Narrative

Narrative is not one exact sequence or necessarily one stable attractor point. It is a hypothesis about slow organization of possible episode trajectories:

```text
recurring regions
transition probabilities
return paths
persistent avoidance or approach loops
ignition and recovery thresholds
long-run drift or topology change
```

`attractor`, `basin`, `grammar` and `field` remain metaphors until extraction and generative rules are operationally defined.

## 6. Scarcity and costly selection

Choice occurs under partially non-convertible constraints:

```text
time
attention
physiological energy
cognitive control
emotional tolerance
social trust
risk capacity
future optionality
```

Resource changes may alter candidate width, gate passage, switching cost and hysteresis. They must not be silently relabeled as Narrative or identity change.

## 7. Recursive social dynamics

A person is not a closed single-agent system.

```text
A's model of B
A's model of B's model of A
B's model of A
```

The actual other agent remains outside those internal models. Coupled rollout is central but follows identifiable single-agent and fixed-other-policy slices.

## 8. Competing representations

```text
R0 — object assembly
R1 — multi-timescale state
R2 — predictive-state compression
R3 — hybrid receipts + state + predictive topology
```

The preferred representation must earn its place through held-out prediction, compression, intervention selectivity and complexity-adjusted comparison.

## 9. Evaluation implications

Evaluation is split.

```text
S0-A structural distributional adequacy
- directional intervention constraints
- mode collapse and unstructured randomness
- authority and information-boundary failures

S0-B source-conditional predictive adequacy
- evaluator-held hidden continuation source
- proper scoring
- identical observable information for B0/B1/B2/H
```

H-only reference-state probes are diagnostic and do not enter the B2/H leaderboard.

A model may fail through:

- mode collapse
- state-insensitive randomness
- rigidity
- over-reset
- target leakage
- receipt/world-truth collapse
- authorship dimension collapse

## 10. Evidence status

```text
historical engineering recurrence
structural executable conformance
conceptual literature adjacency
imported empirical constraint
open-dataset reanalysis
new acquisition
```

The persona-engine lineage is a hypothesis generator and historical ablation source, not human ground truth.

## 11. Relation to current artifacts

```text
Dynamics v0.1–v0.2
- historical executable baseline and typed boundaries

INTERP-001D1
- detached structural conformance result

INTERP-001D2a0 / EXEC0
- reference harnesses for ordering, authority and isolation

PR #21 MAT0
- closed unmerged representation-specific proposal

RFC 0004
- object-assembly precursor and competing representation
```

None alone establishes distributional or human adequacy.

## 12. Explicit non-claims

- canonical HumanState ontology
- universal truth-valued OccurrenceLedger
- one scalar Authorship or Normative settlement
- validated human Narrative attractor
- clinical taxonomy
- causal-state or epsilon-machine identity
- predictive superiority over B2
- calibrated human capacity metric
- human empirical support
