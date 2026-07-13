# Research Architecture

| 항목 | 지위 |
|---|---|
| 설계 방향 | `ADOPTED` |
| 코드 반영 | `PARTIAL — v0.1.1 boundaries + v0.2 provenance/Q-v1 + MORPH-001A instrumentation + MORPH-001B simulation proxy comparison; legacy access bridge retained` |
| 인간 경험적 지위 | `OPEN` |

v0.1.1은 다음 core import 경계를 코드와 test로 구현했다. 다만 frozen semantics를
보존하기 위해 protocol queue pressure를 descriptive AccessState에 전달하는 v0.1
bridge가 하나 남아 있다. 따라서 완전한 semantic decoupling을 주장하지 않는다.
이것은 인간에 대한 경험적 설명력이 아니라 소프트웨어·인증 관할의 구조적 성질이다.

## 기본 원리

```text
Local causal influence
≠ cross-domain certification authority
```

신체, 기억, affect, 접근성은 각자의 상태를 바꿀 수 있다. 금지되는 것은 그
국소 인과 능력이 타 관할의 사실·의도·수행·세계 사건 인증으로 승격되는 것이다.

## 세 연구층

### Contract Layer — `IMPLEMENTED / PARTIAL-SCOPE`

| 계약 | 책임 |
|---|---|
| Certification | 어떤 typed record가 무엇을 성립시킬 수 있는가 |
| Provenance / Integrity | 출처, scope, 동일성, payload, 독립성 보존 |
| Transition Lineage | 어떤 사건과 writer가 상태를 바꿨는가 |
| Accounting | ingress가 processed/dropped/unresolved 중 어디에 갔는가 |

하나의 보편적 인증 record로 관할을 다시 합치지 않는다.

```text
EvidenceAssessmentRecord
PerformanceReceipt
ActionOccurrenceRecord
WorldOutcomeRecord          # HOLD
```

### Descriptive Dynamics — `IMPLEMENTED / EXPLORATORY`

믿음, 느낌, 접근성, 지속 흔적, 후보와 수행 가능성이 실제로 변하는 방식을
기술한다. 심리적 오류는 발생할 수 있지만 인증 근거로 cast되지 않는다.

```text
BeliefUpdateRecord ≠ EvidenceAssessmentRecord
```

첫 오류 동역학 `affect → SubjectiveBelief`는 v0.3에 `PLANNED`되어 있으며 현재
구현된 기능이 아니다.

### Experimental Protocol — `IMPLEMENTED / v0.2 SLICE-A SCOPE`

사건 encoding과 ingress queue에 canonical time, occurrence/delivery identity,
backlog/current-reexposure provenance를 구현했다. `FlowUpdate/EventJump`와 일반적인
개입·측정 protocol은 아직 계획 단계다. Protocol queue는 인간 내부 Access
backlog라는 존재론적 주장이 아니다.

### Derived Measurement — `IMPLEMENTED / Q-v1 SIMULATION SCOPE`

완료된 processing trace에서 `TransitionQualificationReceipt`와 qualified
`MentalTransition` subset을 post-run에 파생한다. policy threshold·scope·digest와
count/density type은 기록하지만, 그 report를 같은 run의 `HumanState`, routing,
Evidence 또는 action pipeline에 재입력하지 않는다.

```text
completed processing trace
→ Q-v1 derived ledger
↛ generating run update
```

이는 현재 model trajectory의 재현 가능한 측정 surface다. 인간의 정신 시간 단위나
예측 타당성은 아니며, legacy queue→access confound와 same-time serialization 문제도
남아 있다.

### Reducer Instrumentation — `MORPH-001A IMPLEMENTED`

post-run before/after projection만으로는 clamp 전에 reducer가 요청했던 displacement를
복원할 수 없다. 따라서 현재 update 경로의 bound 직전에 typed proposal을 관찰하고,
실제 commit과 함께 occurrence-scoped immutable receipt로 보존하는 instrumentation
boundary를 둔다.

```text
current reducer proposal before storage bound
→ ReducerFieldProposal requested component

bounded persistent state after update - stage basis
→ ReducerFieldProposal committed component
```

instrumentation은 생성 경로를 관찰하지만 이를 제어하지 않는다. 미래 결과를 demand
입력으로 사용하거나 receipt를 state/routing/evidence/action pipeline에 재입력하지
않는다. 같은 field의 여러 reducer stage는 합산하지 않고 writer·stage identity와 함께
보존한다.

runtime의 traced reducer는 `ReducerStepResult`로 committed state와 해당 stage의
proposal을 함께 반환한다. engine은 fast/slow proposal을 write sequence 순서로 평탄화해
`TickTrace.reducer_proposals`에 보존하며, post-run projection은 occurrence-scoped
`ReducerProposalReceipt.proposals` flat tuple과 `ReducerProposalLedger`를 만든다.
ledger는 `ReducerStepResult` sequence를 저장하지 않는다. `MORPH-001A` proposal
ledger의 measurement identity는
`descriptive-reducer-preclamp-proxy@1.0.0`이다.

고정 policy는 mandatory/conditional operator order와 operator별 field·constraint·driver
identity를 digest에 결부한다. receipt는 typed before/after state projection과
proposal digest를 포함하며, 인접 receipt 사이의 descriptive-state chain을 검사한다.
`ReducerProposalContext`는 encoded soothing과 performance identity를 결부해
conditional action/soothing write와 driver가 실행 문맥과 맞는지 검사한다.

이 경계는 현재 simulation reducer의 요청과 commit을 분리할 뿐, 인간의 latent demand를
식별하지 않는다.

```text
ReducerProposal ≠ independently identified DeformationDemand ≠ MorphicLoad
```

`AccommodationEnvelope`, excess/residual, `MorphicLoadProfile`, qualia, 주관적 시간은
이 층의 출력이 아니다.

### Derived Proposal Envelope Comparison — `MORPH-001B IMPLEMENTED / SIMULATION PROXY ONLY`

완성된 `ReducerProposalLedger`를 명시적으로 선택한
`ReducerProposalEnvelopePolicy`와 post-run에 비교한다. policy는 current proposal
operator가 쓰는 field마다 signed band를 선언하며, 같은 field의 반복 write를
합산하지 않는다.

`MORPH-001B` comparison의 measurement identity는
`reducer-proposal-envelope-comparison@1.0.0`이다.

```text
ReducerProposal.requested_delta
+ experimenter-declared reducer-write band
→ ReducerProposalEnvelopeComparison
→ ordered proxy-excess profile
```

기준 operator는 componentwise clipping 하나뿐이며 occurrence aggregate나 scalar load를
만들지 않는다. snapshot은 source proposal receipt와 pre-update state-projection digest에
결부되지만, v1 band는 state에서 추정한 값이 아니라 synthetic policy parameter다.

이 projection은 opt-in이고 생성 실행이 끝난 뒤 source ledger만 읽는다. policy를
바꾸거나 끄더라도 `HumanState`, trace, Evidence, routing, action, Q-v1과
`ReducerProposalLedger`는 바뀌지 않아야 한다.

```text
ReducerProposalEnvelopePolicy ≠ measured human AccommodationEnvelope
ordered proxy-excess profile ≠ ExcessDemand / ResidualStrain / MorphicLoad
```

따라서 이 층도 qualia·주관적 시간 또는 `HM-DYN-002`의 근거가 아니다.

### Proposed Interpretive Dynamics — `INTERP-001A BOUNDARY DOCUMENTED / MANIFEST DRAFT / UNIMPLEMENTED`

Chapter 02에서 반복되는 기능 경계와 Checkpoint 05-A의 현행 synthesis를 분리한다.

```text
Recovered functional boundary:
Ghost candidate
≠ Editor / JOT.court 계열 판정
≠ Episode buffer / write
≠ Narrative Field write

Current synthesis / new candidates:
CurrentAccessOccurrence
→ SubjectiveEncounterFormProxy
→ EpisodeMaterialReference
→ EpisodeAssemblyCandidate + AssemblyMaterialMembershipCandidate[]
→ InterpretiveBindingCandidate
→ BindingAdjudicationReceipt
→ optional EpisodeIntegrationReceipt
→ later TargetFormReadoutChangeReceipt
```

두 객체열 전체를 역사적 정본으로 소급하지 않는다. `JOT`는 epoch마다
court/sketch/store 의미가 충돌했고, current main에는 위 interpretation types나
Narrative writer가 구현되어 있지 않다.

이 축은 Descriptive Dynamics의 future detached lab이다. Contract와 Protocol의
사실·identity·time 권한을 가져오지 않는다.

```text
ReceptionState / subjective encounter / Ghost / integration
→ simulated access and interpretation influence 가능

ReceptionState / subjective encounter / Ghost / integration
↛ EvidenceLink strength
↛ source or target identity certification
↛ past occurrence rewrite
↛ direct Narrative Field write
```

RFC 0002 `CurrentReexposure`는 새 access를 trigger할 수 있지만
`CurrentAccessOccurrence`와 동일 타입이 아니다. access ordinal k의 산출은 encounter
k에 되먹임되지 않고 `effective_from_access_ordinal > k`인 후속 access에서만 읽을 수
있다. candidate, adjudication과 integration은 immutable/append-only artifacts로
분리한다.

`TargetFormReadout`은 actor, interpreted-target, optional external-entity resolution,
relation/context scope를 가진 `HOLD` candidate다. source definition, writer,
retention과 revalidation이 식별되기 전에는 persistent HumanState가 아니다.

상세 용어, identity와 판별 조건은
[RFC 0004](rfcs/0004-subjective-encounter-interpretive-reorganization.md)와
[INTERP-001 preregistration](benchmarks/interp-001-subjective-encounter-binding.md)에
고정한다. 이 문서 계약은 code implementation, predictive support, 인간 mood·memory
법칙 또는 actual qualia measurement가 아니다.

### 알려진 v0.1 bridge

```text
protocol ingress pending / queue_limit
→ legacy_v01_access_pressure_bridge
→ descriptive AccessState.queue_load / interference
```

이 결합은 `queue_limit` 같은 실험 설정이 동일 처리열의 인간 궤적을 바꿀 수 있는
confound다. v0.1.1은 의미적 golden을 보존하기 위해 이름을 붙여 격리했을 뿐
정당화하지 않는다. occurrence/delivery/reexposure provenance는 v0.2 첫 slice에서
도입했지만 실제 access-demand identity는 아직 없다. protocol buffer pressure와
모델이 실제로 접근한 demand를 분리하는 competing repair는 후속 실험으로 남는다.

## 의존 경계

```text
Contract ↛ Dynamics 또는 Protocol에 의존
Dynamics ↛ Protocol queue를 직접 조회
Protocol ↛ HumanState를 직접 mutate
Protocol oracle ↛ HumanState에 주입
Engine → 세 층을 계약에 따라 조립
Engine → core 실행 완료 뒤 derived measurement를 조립
```

v0.1.1에서 import 방향을 test로 잠갔다. 위 legacy bridge 때문에
`Dynamics ↛ Protocol queue`의 의미적 독립은 아직 `PARTIAL`이다.

## 상태와 연산

| 개념 | 목표 표현 | 현재 지위 |
|---|---|---|
| World / truth | 인간 상태 밖의 사건·테스트 oracle | 부분 구현; 일반 world model `HOLD` |
| Evidence assessment | claim별 출처 제한 평가 | `EvidenceAssessmentState` 구현 |
| Subjective belief | 사람이 실제로 갖는 확신 | v0.3 `PLANNED` |
| Access | 접근·주의·처리 가능성 | 부분 구현 |
| Agency | 후보→의도→시도→수행→발생 | 부분 구현 |
| Persistent traces | 이후 경로를 기울이는 흔적 | 탐색적 부분 구현 |
| Plasticity | 경험과 시간에 따른 update kernel | 재정의 `PLANNED` |
| Qualified mental transition | post-run receipt/subset/count/density | Q-v1 simulation measurement 구현; predictive value `OPEN` |
| Reducer proposal / committed target | current reducer instrumentation precursor | `MORPH-001A` 구현; DeformationDemand/envelope/load/phenomenal interpretation 제외 |
| Proposal / declared envelope comparison | opt-in ordered post-run proxy profile | `MORPH-001B` simulation comparison 구현; human capacity/load/phenomenal interpretation 제외 |

Plasticity는 Truth/Access/Agency와 같은 종류의 인증 평면이 아니다. Persistence는
남아 있는 흔적이고 Plasticity는 그 흔적을 바꾸는 연산 가설이다.

## v0.1.1 명칭 교정

```text
EpistemicState → EvidenceAssessmentState       # 완료
BodyAuthorization → MotorFeasibility           # 완료
```

기존 이름은 v0.1 compatibility façade에서만 유지한다.
`WarrantState`는 reliability, defeater, validity, revalidation 규칙이 정의될
때까지 `HOLD`다.

## Claim과 결함의 거버넌스

claim은 `TYPE / INVARIANT / DYNAMICAL_HYPOTHESIS / MEASUREMENT_MODEL /
METAPHOR`를 구분하고 다음 필드를 가져야 한다.

```text
adoption_status, implementation_status, scope, exclusions, depends_on
support: historical_cases / structural_tests / empirical_datasets
failure_condition
```

결함 corpus는 다음을 분리한다.

```text
Contemporaneous record
≠ Retrospective interpretation
```

결함에서 원리를 찾는 일은 유일한 연역이 아니라 경쟁 수리를 가진 귀추다.
새 원리는 결함 제거, 판별 예측, 정상 사례 차단 비용, 추가 복잡도를 함께
평가받는다.

## 검증 경계

| Suite | 질문 |
|---|---|
| Contract mutation | 월권을 실제로 검출하는가 |
| Structural ablation | 어떤 typed separation이 필요한가 |
| Temporal comparison | 어떤 시간 가설이 관측을 구분하는가 |

계약 준수는 구조적 건전성이고 인간 자료 예측은 설명력이다.
