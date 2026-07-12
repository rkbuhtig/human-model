# Research Architecture

| 항목 | 지위 |
|---|---|
| 설계 방향 | `ADOPTED` |
| 코드 반영 | `PARTIAL — v0.1.1 boundaries + v0.2 temporal provenance/Q-v1 projection; legacy access bridge retained` |
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
