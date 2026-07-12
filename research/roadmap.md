# Human Model Research Roadmap

| 항목 | 지위 |
|---|---|
| 실행 순서 | `ADOPTED` |
| 후속 구현 | `PLANNED` |
| 인간 경험적 검증 | `OPEN` |

상태는 문서 선언이 아니라 commit, tests, trace, report로 승격한다.

## 0. Dynamics v0.1 baseline freeze

**상태: `FROZEN`**

동결한 것:

- source revision `9b731b7f92700227de1fae8adc79e1d8e687d25f`
- Python/dependency 버전과 stress seed
- 기존 25개 테스트 결과와 stress report
- machine-readable [golden trace](../dynamics/reports/baseline-v0.1.json)
- 실행 환경과 범위를 고정한 [baseline manifest](../dynamics/reports/baseline-v0.1-manifest.json)

golden trace는 Evidence digest, Claim transition, Routed candidate, Intent,
Attempt, Performance, ActionOccurrence, slow-state trajectory, 입력 회계를
포함한다.

검증 명령과 갱신 규칙은 [baseline report](../dynamics/reports/baseline-v0.1.md)에 있다. exact commit SHA가 immutable source reference이며 이후 의미 교정은 이 golden과 비교한다.

## 1. Research program documentation

**상태: `IMPLEMENTED`**

- assessment와 adoption record 분리
- 연구 정체성·근거 층·아키텍처
- claim schema + 실제 claim 1건
- defect schema + 실제 case 1건
- RFC 0001, RFC 0002

종료 조건 통과: `Assessment ≠ Adoption ≠ Implementation ≠ Run ≠ Empirical Evidence`가
문서 구조와 metadata에서 구분된다.

## 2. Dynamics v0.1.1 — 의미·모듈 경계

**상태: `PLANNED`**

```text
EpistemicState → EvidenceAssessmentState
BodyAuthorization → MotorFeasibility 또는 MotorExecutionGate
Contract / Dynamics / Protocol 분리
```

종료 조건:

- import boundary test가 의존 금지를 검사한다.
- 동일 입력·seed에서 baseline과 의미적 trace가 동등하다.
- 새 인간 행동과 `WarrantState`를 추가하지 않는다.

## 3. Dynamics v0.2 — Temporal Kernel

**상태: `PLANNED`**

```text
sim_time
occurred_at ≠ available_at ≠ processed_at
FlowUpdate(state, dt) ≠ EventJump(state, event)
occurrence_id ≠ delivery_id
PastOccurrence ≠ CurrentReexposure
```

종료 조건:

- 무입력 flow의 step-size consistency
- 중복 전달의 원장 멱등성과 payload collision 검출
- transport partition 안정성과 burst/spaced 판별
- 과거 발생 시각 보존과 현재 재노출 효과의 공존
- 시간 경과가 Evidence ledger를 수정하지 않음

몸 상세, 기억 archive, `WorldOutcome`, 주관적 시간은 범위 밖이다.

## 4. Dynamics v0.3 — 첫 descriptive transgression

**상태: `PLANNED`**

한 사례만 구현한다.

```text
AffectiveThreat → SubjectiveBelief 변화 가능
SubjectiveBelief → attention / routing / avoidance 변화 가능

EvidenceLink 불변
EvidenceAssessment 불변
WorldOccurrence 생성 없음
```

정확한 수치보다 방향성·독립성·인증 경계를 검사한다. 반복 서사, 수행 기억
오귀속, 모호 증거 과채택은 `HOLD`다.

## 5. 독립 검증군

**상태: `PLANNED`**

```text
Contract mutation suite   월권 검출력
Structural S0–S3          typed separation의 기여
Temporal T0–T3            시간 가설의 기여
```

가능하면 `S3T2`와 `S3T3`처럼 한 축만 바꾼다. 계약 통과, 복잡도, 판별력,
경험적 예측은 별도 지표다.

## 6. Volume 0 lineage reconstruction

**상태: `PLANNED`**

source manifest를 고정한 뒤 당시 진단과 현재 해석을 분리한다. Chapter 01은
필요하면 절대적 기원이 아니라 0101 재컴파일 경계로 재위치시킨다. 이 단계는
v0.2의 blocker가 아니다.

## 명시적 HOLD

- 완성된 `WarrantState`
- 주관적/생물학적 독립 시계
- 물리 은유의 측정량 승격
- 생리학 계수와 인간 일반 정확도 주장
- 몸·기억·세계·관계의 동시 확장
