# Current Synthesis — Multi-Clock Distributional Human Dynamics

| Field | Status |
|---|---|
| Document class | current synthesis |
| Adoption status | `ADOPTED AS PROGRAM DIRECTION` |
| Runtime status | `UNIMPLEMENTED AS ONE MODEL` |
| Human-empirical status | `OPEN` |
| Canonical ontology status | `NOT FROZEN` |

This document states the current research synthesis after comparing the December persona-engine lineage, the January chapters and the July typed-contract program. It is not a claim that the recovered engine already modeled humans correctly.

## 1. Central object of study

The model target is not one exact next thought, one exact action or one exact trace.

```text
same person and macro-history
+ similar current event
+ varying micro-context, attention and capacity
→ multiple plausible local interpretations and actions
```

Those local variations are not unrestricted. Over time, self-feedback, social response, memory access, resource limits and repeated settlement organize them into a smaller set of recurring trajectory structures.

The target is therefore:

```text
local possibility distribution
+ path-dependent transition law
+ multiple settlement clocks
+ long-run episode/narrative organization
```

A model is adequate only if its state representation improves prediction or compression of held-out trajectory distributions over simpler alternatives.

## 2. Five architectural regions

The current synthesis separates five regions. They are functional roles, not yet canonical classes or files.

### 2.1 Internal state

```text
FastState
- current affect
- attention and salience
- present interpretation
- impulse and action readiness

EpisodeResidue
- medium-timescale unresolved relations
- recent path-dependent accessibility
- local hysteresis and after-effects

NarrativeState
- slow self/relationship topology
- recurrent expectations and return paths
- long-run constraints on what becomes plausible next

CapacityState
- fatigue and control capacity
- attentional, temporal and social-risk budget

SelfOtherModels
- current self-model
- compressed model of other agents
- approximation of how another agent models the self
```

These components need not update at the same rate. A surface action may change immediately while Episode residue, Narrative topology and transition parameters remain nearly fixed.

### 2.2 Settlement ledgers

A human event can be final in one sense and unsettled in another.

```text
OccurrenceLedger
- what occurred

ActionLedger
- what action was realized

AuthorshipLedger
- what the subject currently endorses, owns or accepts responsibility for

NarrativeAdoptionLedger
- what has been incorporated into a durable self/relationship account

NormativeSettlementLedger
- what is interpersonally or institutionally recognized as obligation, consent, fault or authority
```

These ledgers must not be collapsed.

```text
an action occurred
≠ it was fully intended
≠ it is currently endorsed
≠ it defines the person
≠ another person consented
≠ it is normatively justified
```

### 2.3 Context

Context is not part of the person merely because it shapes the person.

```text
external occurrence
physical environment
role and audience
relationship configuration
other-agent response
available information
current bodily conditions
```

The model must distinguish internal capacity from external constraint and internal other-models from the actual other agent.

### 2.4 Transition kernel

The transition kernel denotes the current rules and tendencies by which state, context and ledgers generate future distributions.

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

Narrative may partly reside in slow state and partly parameterize this kernel. That placement remains an open representation question.

### 2.5 Readouts

The following are readouts, not automatically persistent state objects:

```text
interpretation distribution
action-function distribution
surface-expression distribution
future trajectory distribution
```

A candidate distribution should be derived from state, ledgers, context and transition rules. It should not be equated with HumanState without a separate residence argument.

## 3. Multi-clock settlement

Human dynamics does not use one universal commit boundary.

```text
occurrence can settle immediately
behavior can be realized before reflective endorsement
authorship can be reconsidered later
narrative adoption can require repeated episodes
normative settlement can depend on other agents and institutions
```

The clocks interact but remain distinct.

### 3.1 Occurrence immutability

Once an occurrence is accepted into its declared ledger, later interpretation must not rewrite whether that occurrence happened.

### 3.2 Retrospective authorship adjudication

Later access may change the subject's current relation to a past event.

```text
what happened then                         fixed within the occurrence ledger
what I now think it meant                  revisable
whether I endorse or repudiate my action   revisable
how it belongs in my self-narrative         revisable
what rights another person has              not issued by self-narrative alone
```

No-backflow and retrospective re-adjudication are therefore complementary rather than contradictory.

### 3.3 Partial finality

A record can be final for one jurisdiction and open for another. The architecture must represent partial finality rather than one `COMMITTED / NOT_COMMITTED` bit.

## 4. Authority topology

The strongest recurrent invariant in the lineage is not a particular module name but a restriction on what each layer may establish.

```text
local causal influence
≠ cross-domain certification authority
```

Examples:

```text
affect may bias attention and belief
but does not by itself certify an external fact

Narrative may bias future sampling
but does not rewrite a past occurrence

self-authorship may alter future action
but does not issue another person's consent

a generated candidate may influence selection
but is not the selection receipt
```

The current candidate for formalization is a typed authority relation:

```text
Authority = actor × operation × target × scope × grounds × effective clock
```

This is a current synthesis and potential original contribution. The claim that no adjacent cognitive architecture contains a comparable structure remains unestablished until a dedicated literature audit.

## 5. Episode and Narrative

### 5.1 Episode

An Episode is not one universal stored object in the current synthesis.

At the empirical surface, an episode is one realized sample trajectory:

```text
state and history
→ encounter
→ interpretation
→ action
→ result
→ self/social feedback
→ subsequent state
```

At the state level, `EpisodeResidue` denotes the medium-timescale effects left by such trajectories.

The object-assembly representation in RFC 0004 remains one candidate representation, not the unique ontology.

### 5.2 Narrative

Narrative is not one exact sequence and not necessarily one stable attractor point.

It is the slow organization of possible episode trajectories:

```text
recurring regions
transition probabilities
return paths
persistent avoidance or approach loops
ignition and recovery thresholds
possible long-run drift or topology change
```

`attractor`, `basin`, `grammar` and `field` remain metaphors until node equivalence, transition extraction and generative rules are operationally defined.

## 6. Scarcity and costly selection

Choice is meaningful only under limited capacity and opportunity cost.

The model should not assume one conserved scalar resource. Human constraints may include partially non-convertible resources:

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

Resource changes can alter candidate width, gate passage, switching cost and hysteresis. They must not be silently relabeled as Narrative or identity change.

## 7. Recursive social dynamics

A person is not a closed single-agent system.

The constraint layer may contain compressed models of other agents and of reciprocal modeling:

```text
A's model of B
A's model of B's model of A
B's model of A
```

The actual other agent remains outside those internal models. Coupled social rollout is therefore a central future test, but it should follow identifiable single-agent and fixed-other-policy slices so that failure sources remain separable.

## 8. Competing representations

The current synthesis does not freeze one representation.

```text
R0 — object-assembly representation
EpisodeMaterialReference → Assembly → Adjudication → Integration

R1 — multi-timescale state representation
FastState → EpisodeResidue → NarrativeState

R2 — predictive-state representation
histories are equivalent when held-out future distributions are equivalent

R3 — hybrid representation
source-bound ledgers + multi-timescale state + predictive narrative topology
```

The preferred representation must earn its place through held-out prediction, compression, intervention selectivity and complexity-adjusted comparison.

## 9. Evaluation implications

The main evaluation target is a trajectory distribution, not an exact full trace.

A valid adequacy slice should distinguish:

```text
mode collapse
- one response is produced regardless of micro-context

unstructured randomness
- many responses occur without state-dependent constraint

healthy or pathological recurrence
- local variation is organized by stable but revisable long-run structure

rigidity
- structural events cannot change the topology

over-reset
- any small event erases slow state
```

It should also compare an explicit HumanState/Narrative model against a direct full-history-to-output model. If the intermediate representation does not improve prediction, compression, intervention behavior or generalization, it may be explanatory decoration rather than a useful state.

## 10. Evidence status

The following evidence lanes remain separate:

```text
historical engineering recurrence
structural executable conformance
conceptual literature adjacency
imported empirical constraint
open-dataset reanalysis
new acquisition
```

The persona-engine lineage can generate hypotheses and historical ablations. It cannot serve as human ground truth for the theory it helped produce.

## 11. Relation to current repository artifacts

```text
Dynamics v0.1–v0.2
- executable historical baseline and typed boundary implementation

INTERP-001D1
- detached structural conformance result

INTERP-001D2a0 / EXEC0
- reference harnesses for ordering, authority and isolation

INTERP-001D2a0-MAT0 draft
- representation-specific closure on non-mainline hold

RFC 0004
- object-assembly precursor and competing representation
```

None of these artifacts alone establishes distributional or human adequacy.

## 12. Lineage labels

Volume 0 and future theory documents must use the following labels explicitly:

```text
RECOVERED
- directly attested in the historical corpus

STRUCTURAL_PRECURSOR
- historical structure that supports but does not entail the current synthesis

CURRENT_SYNTHESIS
- present integration not projected backward as original canon

OPEN_HYPOTHESIS
- discriminable proposal awaiting execution or evidence

METAPHOR
- useful language without an operational mapping
```

This document is primarily `CURRENT_SYNTHESIS`, with individual boundaries inherited from recovered and implemented authority structures.