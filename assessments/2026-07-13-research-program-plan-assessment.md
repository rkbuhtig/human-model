# Human Model 연구 프로그램 전환 계획에 대한 외부 평가

| 항목 | 값 |
|---|---|
| Document type | External non-peer assessment |
| Canonical status | **NON-CANONICAL** |
| Adoption status | 이 문서에서는 판정하지 않음 |
| Source provenance | 2026-07-13 사용자 제공 피드백의 구조화된 기록 |

> 이 문서는 외부 평가를 보존한다. 여기에 적힌 제안은 채택된 주장이나 구현
> 상태가 아니다. 채택 판정은 [별도 기록](../research/adoption-records/2026-07-13-program-plan-assessment.md)에 있다.

## 총평

평가자는 다음 네 결정을 지금까지의 다음 단계 가운데 가장 강한 계획으로 보았다.

1. 비평, 채택 판단, 구현, 실행 결과의 권위를 분리한다.
2. 계약, 인간 동역학, 실험 프로토콜을 분리한다.
3. 다른 기능보다 시간축을 먼저 구현한다.
4. 새 개념 전에 경쟁 모델과 실패 조건을 요구한다.

다만 실행 전 다음 여섯 가지 교정을 권고했다.

## 권고 1 — 인증과 기술을 분리

첫 층은 인간이 어떻게 행동해야 하는지를 말하는 `Normative Contract`보다,
“어떤 기록이 무엇을 성립했다고 주장할 수 있는가”를 다루는
`Certification Contract`가 정확하다.

```text
Certification Contract
≠ Descriptive Dynamics
≠ Experimental Protocol
```

두려움 때문에 확신이 커지는 것은 기술 가능한 인간 변화다. 그러나 그 확신이
`EvidenceLink`나 외부 사실 인증을 생성해서는 안 된다.

```text
BeliefUpdateRecord ≠ CertificationRecord
```

## 권고 2 — `WarrantState`를 유보

현재 `EpistemicState`는 claim별 EvidenceLink, scope, support/contradiction을
가진다. source reliability, defeater, measurement validity, temporal validity,
revalidation까지 갖춘 warrant로 부르기에는 이르다.

```text
EpistemicState → EvidenceAssessmentState
BodyAuthorization → MotorFeasibility 또는 MotorExecutionGate

SubjectiveBeliefState
≠ EvidenceAssessmentState
≠ WarrantState                # HOLD
```

## 권고 3 — claim 종류별 실패 조건

`TYPE / INVARIANT / DYNAMICAL_HYPOTHESIS / MEASUREMENT_MODEL / METAPHOR`는 서로
다른 방식으로 평가해야 한다.

| 종류 | 실패 조건 |
|---|---|
| `TYPE` | invalid construction |
| `INVARIANT` | counterexample trace |
| `DYNAMICAL_HYPOTHESIS` | discriminating observation |
| `MEASUREMENT_MODEL` | calibration / identifiability failure |
| `METAPHOR` | 경험적 근거로 오용됨 |

근거도 단일 서열로 합치지 말고 historical cases, structural tests, empirical
datasets를 독립적으로 기록한다. 모든 claim에는 `scope`와 `exclusions`가 필요하다.

## 권고 4 — 계약 검출력과 인간 설명력 분리

```text
Contract mutation suite
: 의도적으로 월권하는 mutant를 테스트가 잡는가

Descriptive comparison suite
: 같은 계약 아래 어느 동역학이 관측을 더 잘 설명하는가
```

구조 분리 `S0–S3`와 시간 모델 `T0–T3`도 별도 ablation 축으로 비교해야 한다.
계약 준수는 구조적 건전성이지 인간 설명력이 아니다.

## 권고 5 — 하나의 기준 시간

v0.2는 여러 독립 시계보다 하나의 단조 증가 `sim_time`에서 시작한다.

```text
occurred_at   세계 발생 시각
available_at  접근 가능 시각
processed_at  처리 시각
```

`occurrence_id`와 `delivery_id`를 분리해 전송 중복과 실제 반복 접근을 구별한다.
과거 사건의 발생 시각은 보존하되, 현재 재노출은 현재 activation과 plastic
update를 만들 수 있다.

```text
PastOccurrence ≠ CurrentReexposure
```

## 권고 6 — 첫 인간적 월권은 하나만

v0.3은 다음 한 사례만 닫는 것이 좋다.

```text
AffectiveThreat 증가
→ SubjectiveBelief 변화 가능
→ attention / routing / avoidance 변화 가능

EvidenceLink 불변
EvidenceAssessment 불변
WorldOccurrence 생성 없음
```

반복 서사, 수행 기억 오귀속, 위협에 의한 모호 증거 과채택은 각각 필요한
구조가 다르므로 이후로 미룬다.

## 저장소와 실행 순서에 대한 권고

- assessment 원문과 Adopt/Revise/Hold 판정을 다른 파일에 둔다.
- 결함 corpus는 당시 기록과 현재의 소급 해석을 분리한다.
- 새 원리는 결함 제거, 판별 예측, 정상 사례 차단 비용, 추가 복잡도로 평가한다.
- v0.1의 commit, 환경, seed, tests, golden trace를 먼저 동결한다.
- 그다음 v0.1.1 의미 경계, v0.2 시간 kernel, v0.3 affect→belief 순서로 진행한다.

## 제안된 연구 정체성

> Human Model은 불완전한 관측과 여러 시간척도 아래에서 인간의 경로 의존적
> 변화를 연구하며, 한 상태의 국소적 인과 영향이 다른 관할의 사실·의도·수행·
> 세계 사건을 성립시킬 권한으로 자동 승격되지 않도록 구분하고, 실제 인간에서
> 그 경계가 어떻게 무너지는지도 모델링하려는 typed hybrid dynamics 연구
> 프로그램이다.

현재 공개 구현은 일부 구조적 구분과 동역학적 반례를 실행화했으며, 인간에 대한
경험적 예측 정확도는 아직 검증되지 않았다는 한정을 함께 둘 것을 권고했다.

## 최종 판정

평가자는 계획의 진행을 권고했다. 핵심 기준은 다음과 같다.

```text
Assessment ≠ Adoption
Adoption ≠ Implementation
Implementation ≠ Successful Run
Successful Run ≠ Human-Empirical Evidence
```

