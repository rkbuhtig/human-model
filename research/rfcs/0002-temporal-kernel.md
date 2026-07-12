# RFC 0002 — Canonical-Time Temporal Kernel

| 항목 | 값 |
|---|---|
| Status | `ACCEPTED — PARTIAL IMPLEMENTATION` |
| Target | Dynamics v0.2 |
| Kind | Dynamical hypothesis / protocol |
| Prerequisites | RFC 0001 승인, v0.1 baseline freeze (`SATISFIED`) |
| Implemented slice | canonical timestamps, occurrence/delivery identity, backlog/reexposure provenance |
| Planned slice | `FlowUpdate/EventJump`, no-event flow, burst/spaced comparison |
| Human empirical status | `OPEN` |

## 제안

하나의 단조 증가 기준 시간과 명시적인 사건 동일성을 먼저 도입한다. v0.2는
한 번에 완성하지 않고 두 구현 slice로 나눈다.

```text
Slice A — IMPLEMENTED
canonical timestamp envelope
+ occurrence / delivery identity
+ backlog / current-reexposure provenance

Slice B — PLANNED
FlowUpdate / EventJump
+ no-event flow
+ burst / spaced comparison
```

첫 slice는 사건이 언제 일어났고, 언제 접근 가능해졌으며, 엔진이 언제 실제로
처리했는지를 보존하는 protocol·trace 계약이다. 이것만으로 시간 경과에 따른
인간 상태 변화나 주관적 시간을 구현했다고 주장하지 않는다.

```text
sim_time       canonical monotonic time
occurred_at    세계 발생 시각
available_at   모델 접근 가능 시각
processed_at   engine 처리 시각
```

`processed_at`은 입력 작성자가 미리 인증하는 값이 아니라 엔진이 실제 처리할 때
기록한다. `dt`와 time-driven state flow는 아직 구현하지 않았으며, 이후 slice에서
저장 시각의 차이로 계산한다. 주관적·생물학적 시간은 `HOLD`다.

## 해결하려는 혼동

- 같은 사건 수의 burst와 spaced exposure
- 과거 발생과 현재 첫 접근
- 동일 occurrence의 전송 중복과 실제 반복 접근
- 무사건 시간의 감쇠·회복과 event count
- protocol queue 지연과 인간이 겪은 경과 시간

## 시간 봉투 — `IMPLEMENTED`

기본 제약:

```text
occurred_at <= available_at <= processed_at <= final_sim_time
```

과거 기록이 늦게 들어와도 `occurred_at`을 현재로 다시 쓰지 않는다.

- `occurred_at`: 원천 occurrence가 발생한 시각
- `available_at`: protocol이 그 occurrence를 모델 처리 대상으로 공개한 시각
- `processed_at`: engine이 해당 delivery를 실제 처리한 시각
- `SimTime`: 모든 시각에 쓰는 canonical 좌표 타입
- `final_sim_time`: engine이 기록하는 이번 run의 마지막 processing frontier

입력은 `occurred_at`과 `available_at`을 선언할 수 있지만 `processed_at`을
선결할 수 없다. 이 분리는 backlog의 오래된 발생시각과 현재 처리 효과를 함께
보존한다.

## Flow와 event jump — `PLANNED`

```text
x(t + dt-) = FlowUpdate(x(t), dt, environment)
x(t+)      = EventJump(x(t-), event)
```

같은 timestamp의 여러 event에는 명시적 aggregation/ordering 규칙이 필요하다.
우연한 배열 순서를 이론적 의미로 만들지 않는다.

## 사건 동일성과 provenance — `IMPLEMENTED`

```text
occurrence_id  원천 사건의 동일성
delivery_id    그 사건을 운반한 개별 전달의 동일성
```

동일 occurrence와 동일 payload의 다른 delivery는 transport redelivery다. 새 원천
사건이나 새 모델 update로 세지 않는다. 동일 occurrence ID에 다른 payload가 오면
어느 쪽도 조용히 채택하지 않고 hard collision으로 기록한다.

심리적 재노출은 transport redelivery가 아니다. 별도 현재 occurrence와 delivery를
만들고 과거 원천을 가리키는 `reexposure_of` provenance를 보존한다.

```text
PastOccurrence ≠ CurrentReexposure
```

- 과거 occurrence의 `occurred_at`은 보존한다.
- 현재 reexposure는 descriptive state update를 만들 수 있다.
- reexposure는 원천 evidence의 독립성이나 외부 발생 수를 자동 증가시키지 않는다.
- source가 아직 commit되지 않았거나 source 접근보다 backdate된 reexposure는
  provenance error로 거부한다.

## 불변식과 가설

| ID | 지위 | 종류 | 내용 |
|---|---|---|---|
| T-INV-01 | `IMPLEMENTED` | invariant | `occurred_at ≤ available_at ≤ processed_at ≤ final_sim_time`; processing stamp는 engine 소유 |
| T-INV-02 | `IMPLEMENTED` | invariant | 동일 occurrence/payload의 transport redelivery는 원장과 human update에 멱등적 |
| T-INV-03 | `IMPLEMENTED` | invariant | 동일 occurrence ID의 충돌 payload는 hard failure |
| T-INV-04 | `IMPLEMENTED` | invariant | backlog 처리와 재노출이 과거 `occurred_at`을 변경하지 않음 |
| T-INV-05 | `IMPLEMENTED` | invariant | 현재 reexposure는 descriptive state를 바꿀 수 있지만 원천 evidence strength를 자동 증가시키지 않음 |
| T-INV-06 | `PLANNED` | invariant | 새 관측 없는 flow가 Evidence ledger를 변경하지 않음 |
| T-HYP-01 | `PLANNED` | hypothesis | 조건부 flow composition / step-size convergence |
| T-HYP-02 | `PLANNED` | hypothesis | 단순 transport partition 안정성 |
| T-HYP-03 | `PLANNED` | hypothesis | 실제 간격이 있는 burst/spaced trajectory 구분 |

다음 식은 아직 구현 판정이 아니라 두 번째 slice의 사전 등록 조건이다.
무입력·동일 환경·시간 동질적인 flow에서 허용 오차 안의 composition을 검사한다.

```text
Flow(Flow(x, dt1), dt2) ≈ Flow(x, dt1 + dt2)
```

비자율 환경에서는 보편 동일성이 아니라 step-size convergence를 본다.

## 구현된 첫 slice의 구조 테스트

1. `test_temporal_ordering_and_engine_owned_processing`
2. `test_transport_redelivery_is_idempotent`
3. `test_occurrence_payload_collision_is_hard_error`
4. `test_backlog_preserves_occurrence_time`
5. `test_current_reexposure_changes_state_not_evidence`

이 테스트들은 schema·identity·provenance와 구현된 writer 경계를 지지한다. 인간의
실제 시간 경험이나 예측 정확도에 대한 경험적 지지는 아니다.

## 두 번째 slice의 계획된 테스트

1. 같은 총 시간을 다른 step으로 적분한 no-event flow
2. event-count `T2`와 flow+jump `T3`의 burst/spaced 비교
3. 의미적 atomic bundle의 허용된 직렬화 안정성
4. 새 관측 없는 flow의 Evidence ledger 불변성

`T3`가 더 인간적인지는 경험 자료 없이 판정하지 않는다.

## 비목표

- subjective/biological time
- 수면을 필수 maintenance epoch로 만드는 가설
- memory archive와 source-memory reconstruction
- 세부 body physiology
- `WorldOutcome`
- affect→belief transgression
- 인간 자료에 맞춘 계수

## 구현 순서

1. **완료:** event schema에 timestamp와 occurrence/delivery identity 추가
2. **완료:** engine-owned processing stamp와 시간 순서 검증
3. **완료:** transport redelivery 멱등성과 occurrence payload collision 검출
4. **완료:** backlog/reexposure provenance와 evidence independence 구현
5. **계획:** `FlowUpdate`와 `EventJump` 분리
6. **계획:** no-event flow invariant tests
7. **계획:** T2/T3 burst/spaced comparison report 생성

## 첫 slice 종료 조건 — `SATISFIED`

1. 기준 시간과 timestamp 의미가 하나의 schema로 고정됨
2. 전송 중복과 반복 접근을 다르게 표현함
3. 과거 발생과 현재 재노출 시각을 함께 보존함
4. 동일 occurrence/payload redelivery가 human/evidence update를 중복 적용하지 않음
5. 동일 occurrence ID의 payload collision을 hard failure로 남김
6. 구현 상태를 인간 경험적 시간 모델의 검증으로 과장하지 않음

## 전체 RFC 종료 조건 — `OPEN`

1. `FlowUpdate`와 `EventJump`가 별도 연산으로 구현됨
2. flow가 step size에 과도하게 의존하지 않음
3. 새 관측 없는 시간 경과가 evidence provenance를 수정하지 않음
4. burst/spaced 비교와 transport partition 안정성 report가 생성됨
5. burst/spaced 차이를 인간 경험적 사실로 과장하지 않음

## 열린 결정

- seconds와 추상 simulation unit 중 time unit
- 동일 timestamp event의 aggregation 정책
- 적분법과 상태별 허용 오차
- `observation_id`를 delivery와 별도 관측 identity로 도입할 시점
