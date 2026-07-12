# Temporal Envelope Contract — v0.2 Slice A

## 지위

이 문서는 v0.2의 첫 temporal slice에서 실제로 구현한 protocol·trace 계약만
기술한다.

| 범위 | 지위 |
|---|---|
| canonical timestamp와 writer ownership | `IMPLEMENTED` |
| occurrence / delivery identity | `IMPLEMENTED` |
| backlog / current-reexposure provenance | `IMPLEMENTED` |
| `FlowUpdate / EventJump` | `PLANNED` |
| no-event recovery·decay | `PLANNED` |
| burst / spaced comparison | `PLANNED` |
| 주관적·생물학적 시간 | `HOLD` |
| 인간 경험적 검증 | `OPEN` |

구조 테스트 통과는 시간과 사건 provenance가 코드에서 섞이지 않는다는 뜻이다.
사람이 실제로 시간을 어떻게 경험하는지를 검증했다는 뜻은 아니다.

## 기준 시간

`SimTime`은 non-negative integer인 canonical simulation coordinate다. `bool`,
fractional number, 음수의 묵시적 변환은 허용하지 않는다.

```text
EventTemporalEnvelope
├─ occurrence_id
├─ delivery_id
├─ occurred_at
├─ available_at
├─ reexposure_of_occurrence_id?
└─ delivery_sequence?

ProcessingStamp
├─ envelope
├─ processed_at
└─ processing_sequence
```

`human-model-scenario/0.2` JSON은 envelope의 source-owned 필드를 event object에
flat하게 기록한다. 중첩 `temporal` object와 engine-owned stamp 필드는 입력으로
받지 않는다.

각 시각은 writer와 뜻이 다르다.

| 필드 | 뜻 | Writer |
|---|---|---|
| `occurred_at` | 원천 occurrence가 발생한 시각 | scenario / protocol source |
| `available_at` | delivery가 engine ingress에 공개되는 시각 | scenario / protocol source |
| `processed_at` | engine이 실제로 처리한 시각 | engine only |
| `final_sim_time` | 이번 run의 마지막 processing frontier | engine only |

```text
occurred_at <= available_at <= processed_at <= final_sim_time
```

`processed_at`은 versioned scenario 입력 payload 필드가 아니다. production
`DynamicsEngine.run` 경로가 event를 처리할 때
`ProcessingStamp`를 만들고, observation과 processing trace가 이를 보존한다.
`processing_sequence`는 같은 canonical time에서 처리 순서를 감사하기 위한
양의 정수이지 별도 시간 단위가 아니다.

v0.1 호환 surface에서 `ScenarioEvent.tick`은 `available_at`,
`ObservationArtifact.source_tick`은 `occurred_at`, `observed_tick`은
`processed_at`의 deprecated alias다. v0.1에서는 세 시각이 같았으므로 frozen
baseline 값은 바뀌지 않는다.

Python의 record 생성자를 capability-secure하게 봉인한 것은 아니다. 직접
`ProcessingStamp`나 `ObservationArtifact`를 조립하는 코드는 unsafe test surface이며
versioned scenario writer-ownership claim의 범위 밖이다.

아직 no-event `FlowUpdate`가 없으므로 queue가 비어 있는 구간은 engine이 다음
`available_at`으로 event-driven jump한다. 이는 큰 sparse timestamp를 시간값만큼
반복하지 않기 위한 protocol 실행 최적화이며, 빈 시간 동안 인간 상태가 변하지
않는다는 경험적 가설을 채택한 것이 아니다.

## 사건과 전달의 동일성

```text
occurrence_id = 원천 사건의 동일성
delivery_id   = 그 사건을 운반한 전달의 동일성
```

ingress는 delivery projection과 occurrence projection을 별도로 canonicalize하고
digest한다.

| 입력 관계 | disposition | 의미 |
|---|---|---|
| 같은 delivery ID, 같은 delivery payload | `duplicate` | 동일 전달 재전송; 무시 |
| 같은 delivery ID, 다른 delivery payload | `delivery_collision` | hard error |
| 다른 delivery ID, 같은 occurrence ID와 occurrence payload | `redundant_delivery` | transport redelivery; 무시 |
| 같은 occurrence ID, 다른 occurrence payload | `occurrence_collision` | hard error |
| 새 occurrence와 delivery | `accepted` | 처리 후보 |

transport metadata인 availability, delivery sequence, ingress priority가 다르더라도
원천 occurrence payload가 같으면 새 원천 사건이 되지 않는다. 반대로 occurrence
payload가 충돌하면 최신 전달로 덮어쓰지 않는다.

## Backlog

event는 `available_at`에 ingress에 들어오지만 capacity에 따라 더 늦은
`processed_at`에 처리될 수 있다.

```text
PastOccurrence
occurred_at = 2
available_at = 8
processed_at = 11
```

이 경우 `2`를 `8`이나 `11`로 다시 쓰지 않는다. processing trace는 현재 처리와
과거 발생을 함께 보존한다. 아직 구현되지 않은 것은 `11 - 2`에 따라 human
state를 흘려 보내는 time-driven update다.

## Current reexposure

현재 재노출은 동일 occurrence의 transport redelivery와 다르다.

```text
source occurrence O1 at t=2

current reexposure O2 at t=11
reexposure_of_occurrence_id = O1
O2 != O1
```

현재 구현에서 reexposure는 다음 경계를 지킨다.

- 별도 현재 `occurrence_id`와 `delivery_id`를 가진다.
- 자기 자신의 occurrence를 source로 가리킬 수 없다.
- 이미 처리되어 commit된 source occurrence만 가리킬 수 있다.
- 현재 occurrence의 `occurred_at`은 source가 처음 처리된 시각보다 이를 수 없다.
- internal event여야 하며 support/contradiction signal을 실을 수 없다.
- 따라서 현재 descriptive state update는 가능하지만 원천 evidence strength를
  자동 증가시키지 않는다.

source가 아직 commit되지 않은 reexposure는 `dangling_reexposure`, source 접근보다
앞으로 backdate된 reexposure는 `invalid_reexposure_time` hard error다.
이는 일반적인 인간 기억 재구성 이론이 아니라 현재 실험 protocol의 provenance
제약이다. 여기서 hard error는 process 전체를 즉시 중단한다는 뜻이 아니라 해당
delivery를 거부하고 invariant error와 입력 회계를 남긴다는 뜻이다.

drop되거나 거부된 delivery ID도 소비된 transport identity로 남는다. 같은
occurrence를 재시도하려면 새 `delivery_id`를 사용해야 한다.

## 같은 timestamp의 순서

optional `delivery_sequence`는 같은 availability time과 priority에서 명시적인
순서를 제공한다. 순서가 필요한 묶음에 sequence가 없으면 engine은
`SimulationLedger.same_timestamp_order_debts`에 advisory를 남긴다.

이 debt 검출은 aggregation 문제를 해결했다는 뜻이 아니다. 의미적 atomic bundle,
가환 가능한 update, same-time aggregation 정책은 두 번째 slice에서도 별도 결정이
필요하다.

## 구현된 구조 테스트

- `test_temporal_ordering_and_engine_owned_processing`
- `test_transport_redelivery_is_idempotent`
- `test_occurrence_payload_collision_is_hard_error`
- `test_backlog_preserves_occurrence_time`
- `test_current_reexposure_changes_state_not_evidence`

## 아직 없는 연산

```text
FlowUpdate(state, dt)
EventJump(state, event)
```

그러므로 현재 구현만으로는 다음을 주장할 수 없다.

- 무입력 시간 동안 회복·감쇠가 일어난다.
- step size를 바꿔도 동일한 flow trajectory가 나온다.
- burst와 spaced exposure가 다른 결과를 만든다.
- canonical elapsed time이 정신적 시간량이다.
- transport partition 안정성이 flow/jump 전체에서 검증되었다.

이 항목은 RFC 0002의 second slice 종료 조건으로 남는다.
