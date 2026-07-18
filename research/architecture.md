# Research Architecture

| 항목 | 지위 |
|---|---|
| 연구 권한 아키텍처 | `ADOPTED / PARTIALLY IMPLEMENTED` |
| 인간 동역학 기능 영역 | `CURRENT SYNTHESIS / NOT CANONICAL TYPES` |
| S0 평가 아키텍처 | `PREREGISTERED PROTOCOL DIRECTION` |
| 인간 경험적 지위 | `OPEN` |

이 문서는 두 축을 분리한다.

```text
Axis A — research and software authority
Axis B — candidate human-dynamics organization
```

둘은 대체 관계가 아니다. `Contract / Dynamics / Protocol / Measurement`는 무엇이 무엇을 인증하고 읽고 쓸 수 있는지 관리한다. `Internal State / Settlement Receipts / Context / Transition Kernel / Readouts`는 현재 인간 동역학을 표현하기 위한 기능적 후보 영역이다.

## 1. Strongest boundary

```text
Local causal influence
≠ cross-domain certification authority
```

느낌, 기억, Narrative와 자기해석은 미래 접근·행동·분포를 바꿀 수 있다. 그 영향만으로 외부 사실, 과거 occurrence, 타인의 동의, fault, obligation 또는 authority를 인증하지 못한다.

## 2. Axis A — research authority layers

### 2.1 Contract Layer

책임:

- record type과 writer 권한
- provenance, identity, scope와 integrity
- certification jurisdiction
- transition lineage와 accounting

```text
proposal ≠ evidence
readout ≠ writable state
action occurrence ≠ performance certification
registered report ≠ certified world fact
```

Contract는 Dynamics나 Protocol의 심리적 의미를 발명하지 않는다.

### 2.2 Descriptive Dynamics

책임:

- 상태와 transition tendency의 실제 갱신
- 후보 생성과 제약 형상화
- action realization, self/social feedback와 slow adaptation

심리적 오류와 왜곡은 허용되지만 Evidence나 World truth로 cast되지 않는다.

### 2.3 Experimental Protocol

책임:

- 사건·history·intervention 공급
- 시간과 occurrence/delivery identity
- source split, missingness, seed visibility와 model version freeze

Protocol queue와 evaluator-only state는 HumanState가 아니다. Protocol은 HumanState를 직접 mutate하지 않는다.

### 2.4 Derived Measurement and Evaluation

책임:

- completed run에서 metrics와 receipts 파생
- proper scoring, structural predicates, complexity accounting
- evaluator-only target과 model-visible input 분리

```text
completed run → derived score
score ↛ generating run update
```

## 3. Axis B — candidate human-dynamics regions

이 영역은 functional residence 후보다. canonical class나 JSON layout이 아니다.

### 3.1 Internal State

```text
FastState
- affect, attention, salience
- present interpretation
- impulse and action readiness

EpisodeResidue
- medium-timescale unresolved effects
- recent path-dependent accessibility and hysteresis

Narrative/Self State
- slow recurrent expectations and return paths
- relationship/self organization

CapacityState
- fatigue, control capacity, time/attention/social-risk limits

SelfOtherModels
- self model
- compressed model of other agents
- bounded reciprocal modeling
```

### 3.2 Settlement Receipts

`Ledger`는 truth store가 아니라 immutable receipt collection을 뜻한다. receipt 등록은 payload의 모든 world claim을 인증하지 않는다.

#### OccurrenceReceipt

```text
OccurrenceReceipt
- source identity
- occurred/reported/registered time
- occurrence scope
- submitted or observed content
- provenance and grounds lane
```

최소 scope:

```text
REGISTERED_REPORT
- source가 그 내용을 보고했다

INTERNAL_OCCURRENCE_REPORT
- 당사자가 감정·생각·지각 발생을 보고했다

CERTIFIED_WORLD_OCCURRENCE
- 별도 evidence/grounds protocol이 외부 occurrence를 성립시켰다
```

```text
OccurrenceReceipt immutability
≠ payload world-truth certification
```

#### ActionReceipt

행동이 실제 realization됐다는 기록이다. intent, endorsement, performance와 동일하지 않다.

#### AuthorshipSettlementReceipt

저자성은 하나의 scalar가 아니다.

```text
causal_attribution
control_attribution
reflective_ownership
endorsement
responsibility_acceptance
```

예:

```text
내가 했다
≠ 충분히 통제했다
≠ 지금도 지지한다
≠ 결과 수리 책임을 거부한다
```

#### NarrativeAdoptionReceipt

어떤 occurrence/action/meaning이 durable self or relationship account에 편입됐는지 기록한다. occurrence 자체를 다시 쓰지 않는다.

#### NormativeSettlementReceipt

다음 jurisdiction을 독립 typed relation으로 보존한다.

```text
consent
fault
obligation
permission
authority
recognized remedy
```

자기서사만으로 타인의 settlement를 발급할 수 없다.

### 3.3 Context

```text
external occurrence and available information
physical and bodily conditions
role and audience
relationship configuration
actual other-agent response
```

Context가 사람을 형상화한다고 해서 사람 내부 state가 되지는 않는다. 실제 타자와 내부 other-model을 구분한다.

### 3.4 Transition Kernel

```text
candidate generation
constraint shaping
selection and action realization
surface projection
self-feedback
social feedback
retrospective authorship adjudication
slow transition adaptation
```

Narrative는 slow state와 kernel parameter 양쪽에 걸칠 수 있다. placement는 S0 이후에도 경쟁 표현으로 남는다.

### 3.5 Readouts

```text
interpretation distribution
action-function distribution
surface-expression distribution
future trajectory distribution
```

Readout은 persistent state나 evidence가 아니다. 후보 분포는 state, receipts, context와 kernel에서 파생된다.

## 4. Two-axis mapping

| Candidate model region | Contract responsibility | Dynamics responsibility | Protocol responsibility | Measurement responsibility |
|---|---|---|---|---|
| Internal State | type, writer, scope | state update | intervention visibility | state probe and compression |
| Settlement Receipts | grounds and jurisdiction | delayed re-adjudication | source registration | settlement consistency |
| Context | external/internal boundary | shaping influence | event and branch supply | condition grouping |
| Transition Kernel | allowed operators | transition execution | clamp/intervention | ablation and sensitivity |
| Readouts | non-certification boundary | distribution generation | output surface | proper scoring |

이 표는 구현 파일 배치를 동결하지 않는다.

## 5. Partial finality and multiple clocks

```text
registered occurrence can be immutable
while authorship remains revisable
while Narrative adoption remains open
while interpersonal settlement requires another agent
```

하나의 `COMMITTED / NOT_COMMITTED` bit로 합치지 않는다.

## 6. S0 information architecture

### Leaderboard lanes

B0/B1/B2/H는 동일한 observable prefix, continuation surface와 training examples만 받는다.

금지:

- H에 evaluator latent state 제공
- B2에 숨긴 source information을 H에 제공
- evaluator seed/target parameter를 generating process가 읽음
- model output을 target label로 재사용

### H-only diagnostic lanes

다음은 leaderboard score가 아니다.

```text
reference-state one-step transition
state sufficiency ablation
settlement-edge probes
history added after H-state probe
```

이는 H 내부 표현의 진단이며 B2보다 우월하다는 증거가 아니다.

## 7. Implemented reference boundaries

현재 구현은 아래 일부를 보존한다.

- EvidenceAssessment, Agency와 ActionOccurrence 분리
- occurrence/delivery/reexposure temporal provenance
- proposal versus committed reducer write
- post-run Q/MORPH measurement isolation
- INTERP candidate/adjudication/integration authority separation
- runner/evaluator visible-lane separation in frozen reference harnesses

현재 구현되지 않은 것:

- 위 receipt family의 canonical runtime
- validated Narrative topology
- human-calibrated capacity
- source-conditional predictive S0 result

## 8. Representation candidates

```text
R0 object assembly
R1 multi-timescale state
R2 predictive-state compression
R3 hybrid receipts + state + predictive topology
```

S0 결과 전에는 하나를 canonical ontology로 승격하지 않는다.

## 9. Evidence lanes

```text
historical engineering recurrence
structural executable conformance
conceptual literature adjacency
imported empirical constraint
open-dataset reanalysis
new acquisition
```

서로 자동 승격되지 않는다.

## 10. Validation boundary

| Suite | 질문 |
|---|---|
| Contract mutation | 월권과 정보 누수를 검출하는가 |
| S0-A structural | intervention이 분포를 선택적으로 움직이는가 |
| S0-B predictive | 동일 정보 아래 hidden source trajectory를 더 잘 예측하는가 |
| H diagnostic | 명시적 state가 내부적으로 충분하고 독립적으로 probe 가능한가 |
| Human empirical | 실제 사람의 분포와 시간 구조를 설명하는가 |

계약 준수는 구조적 건전성이고 source prediction은 source-conditional adequacy다. 인간 자료 예측은 별도 설명력이다.

## 11. Explicit non-claims

- `OccurrenceReceipt`가 모든 world claim을 참으로 만든다는 주장
- 하나의 Authorship 또는 Normative scalar
- canonical HumanState object model
- Narrative = attractor 또는 epsilon-machine
- synthetic source performance = human support
- clinical diagnosis taxonomy
