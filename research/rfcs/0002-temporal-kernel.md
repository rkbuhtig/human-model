# RFC 0002 — Canonical-Time Temporal Kernel

| 항목 | 값 |
|---|---|
| Status | `PROPOSED` |
| Target | Dynamics v0.2 |
| Kind | Dynamical hypothesis / protocol |
| Prerequisites | RFC 0001 승인, v0.1 baseline freeze (`SATISFIED`) |

## 제안

하나의 단조 증가 기준 시간과 flow/jump를 도입한다.

```text
sim_time       canonical monotonic time
occurred_at    세계 발생 시각
available_at   모델 접근 가능 시각
processed_at   engine 처리 시각
```

`dt`는 독립 상태로 저장하지 않고 시각 차이로 계산한다. 주관적·생물학적 시간은
`HOLD`다.

## 해결하려는 혼동

- 같은 사건 수의 burst와 spaced exposure
- 과거 발생과 현재 첫 접근
- 동일 occurrence의 전송 중복과 실제 반복 접근
- 무사건 시간의 감쇠·회복과 event count
- protocol queue 지연과 인간이 겪은 경과 시간

## 시간과 전이

기본 제약:

```text
occurred_at <= available_at <= processed_at <= sim_time
```

과거 기록이 늦게 들어와도 `occurred_at`을 현재로 다시 쓰지 않는다.

```text
x(t + dt-) = FlowUpdate(x(t), dt, environment)
x(t+)      = EventJump(x(t-), event)
```

같은 timestamp의 여러 event에는 명시적 aggregation/ordering 규칙이 필요하다.
우연한 배열 순서를 이론적 의미로 만들지 않는다.

## 사건 동일성

```text
occurrence_id  세계 원천 사건의 동일성
delivery_id    개별 전달의 동일성
```

동일 occurrence의 재전송은 world/evidence ledger의 독립 support를 늘리지 않는다.
심리적 재노출은 별도 현재 event로 표현한다.

```text
PastOccurrence ≠ CurrentReexposure
```

- 과거 occurrence의 `occurred_at`은 보존한다.
- 현재 reexposure는 activation과 persistent update를 만들 수 있다.
- reexposure는 원천 evidence의 독립성이나 외부 발생 수를 자동 증가시키지 않는다.

## 불변식과 가설

| ID | 종류 | 내용 |
|---|---|---|
| T-INV-01 | invariant | `sim_time`과 processing trace는 역행하지 않음 |
| T-INV-02 | invariant | 동일 occurrence/payload의 재전송은 원장에 멱등적 |
| T-INV-03 | invariant | 동일 occurrence ID의 충돌 payload는 hard failure |
| T-INV-04 | invariant | 지연·재노출이 과거 `occurred_at`을 변경하지 않음 |
| T-INV-05 | invariant | 새 관측 없는 flow가 Evidence ledger를 변경하지 않음 |
| T-HYP-01 | hypothesis | 조건부 flow composition / step-size convergence |
| T-HYP-02 | hypothesis | 단순 transport partition 안정성 |
| T-HYP-03 | hypothesis | 실제 간격이 있는 burst/spaced trajectory 구분 |

무입력·동일 환경·시간 동질적인 flow에서는 다음을 허용 오차 안에서 검사한다.

```text
Flow(Flow(x, dt1), dt2) ≈ Flow(x, dt1 + dt2)
```

비자율 환경에서는 보편 동일성이 아니라 step-size convergence를 본다.

## 필수 테스트

1. 같은 총 시간을 다른 step으로 적분한 no-event flow
2. 같은 occurrence/payload, 다른 delivery의 원장 멱등성
3. 같은 occurrence ID, 충돌 payload의 hard failure
4. 늦게 처리된 backlog의 원래 발생 시각 보존
5. 현재 reexposure의 activation 허용과 evidence independence 보존
6. event-count `T2`와 flow+jump `T3`의 burst/spaced 비교
7. 의미적 atomic bundle의 허용된 직렬화 안정성

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

1. event schema에 timestamp와 occurrence/delivery identity 추가
2. protocol scheduler를 canonical time으로 교정
3. `FlowUpdate`와 `EventJump` 분리
4. backlog/reexposure provenance 구현
5. invariant tests 후 T2/T3 comparison report 생성

## 종료 조건

1. 기준 시간과 timestamp 의미가 하나의 schema로 고정됨
2. 전송 중복과 반복 접근을 다르게 표현함
3. 과거 발생과 현재 재노출 시각을 함께 보존함
4. flow가 step size에 과도하게 의존하지 않음
5. 시간 경과가 evidence provenance를 수정하지 않음
6. burst/spaced 차이를 인간 경험적 사실로 과장하지 않음

## 열린 결정

- seconds와 추상 simulation unit 중 time unit
- 동일 timestamp event의 aggregation 정책
- v0.2에서 `observation_id`까지 필요한지 여부
- 적분법과 상태별 허용 오차
