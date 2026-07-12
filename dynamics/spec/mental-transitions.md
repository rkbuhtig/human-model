# Mental Transition Measurement Contract — Q-v1

## 지위

| 범위 | 지위 |
|---|---|
| processed-occurrence receipt와 qualified subset | `IMPLEMENTED` |
| immutable post-run derived ledger | `IMPLEMENTED` |
| count / density window report | `IMPLEMENTED` |
| transition density의 predictive value | `PROPOSED / UNIMPLEMENTED` |
| `MorphicLoadProfile` | `PROPOSED / UNIMPLEMENTED` |
| phenomenal bridge | `HOLD` |
| 인간 경험적 검증 | `OPEN` |

이 slice는 existing run trace를 읽어 변화 receipt를 만드는 measurement surface다.
새 human-state update나 독립적인 정신 시계를 도입하지 않는다.

```text
canonical elapsed interval
≠ processed occurrence count
≠ Q-v1 qualified transition count
≠ qualified transition density
≠ MorphicLoadProfile
≠ phenomenal intensity
```

## 파생 시점과 권한

```text
DynamicsEngine run
→ completed processing trace
→ post-run Q-v1 derivation
→ MentalTransitionLedger
→ optional TransitionWindowReport
```

구현 module과 주요 타입은 다음과 같다.

```text
dynamics.mental_transitions

MentalTransitionQualificationPolicy
TransitionQualificationReceipt
MentalTransition
MentalTransitionLedger
MentalTransitionWindowReport

CanonicalWindowDuration
QualifiedTransitionCount
QualifiedTransitionDensity
```

ledger derivation은 engine의 update path 밖에서 수행된다. ledger, receipt, count,
density는 다음 run의 `HumanState`, routing, evidence assessment, action pipeline에
자동 재입력되지 않는다.

다른 qualification policy로 같은 run을 다시 읽을 수는 있다. 이때 derived
qualification만 달라질 수 있고 base state trajectory, processing trace,
EvidenceLink, action record는 달라지면 안 된다.

## Checkpoint identity

Q-v1 checkpoint는 **처리된 occurrence 하나**다.

- accepted되어 실제 처리된 occurrence마다 receipt 하나를 만든다.
- qualification에 실패한 occurrence도 unqualified receipt를 남긴다.
- qualified transition은 전체 receipt의 subset이다.
- transport duplicate와 redundant delivery는 처리된 occurrence가 아니므로 receipt를
  추가하지 않는다.
- protocol tick, solver substep, 함수 호출 횟수를 transition identity로 쓰지 않는다.

```text
processed occurrence
≠ transport delivery attempt
≠ qualified mental transition
```

## Literal persistent descriptive scope

Q-v1은 `PERSISTENT_DESCRIPTIVE_FIELDS`에 고정한 다음 literal scalar leaf만 읽는다.

```text
body.energy
body.arousal
body.action_capacity
access.attention_budget
access.interference
access.queue_load
associative.rejection_access
associative.ambiguity_sensitivity
affective.residual_distress
affective.update_rate
habit.impulsivity
habit.withdrawal_bias
narrative.rejection_story
narrative.relational_security
relationship.stake
relationship.trust
relationship.boundary_strain
```

각 값은 현재 Dynamics의 normalized `[0, 1]` simulation unit이다. 다음은 scope에서
제외한다.

- `HumanState.clock`
- `EvidenceAssessmentState`와 certification record
- `PhenomenalActivation`, candidate, routing probability
- intent, attempt, performance, action occurrence
- protocol queue의 내부 상태
- 해당 checkpoint 이후의 event, state, outcome

scope는 인간의 실제 심리 변수를 확인했다는 주장이 아니라 Q-v1의 literal code
projection이다.

### 알려진 access confound

`access.attention_budget`, `access.interference`, `access.queue_load`는 literal
`HumanState` field이므로 default scope에 들어간다. 그러나 이 값들은 현재
`legacy_v01_access_pressure_bridge`의 영향을 받는다. protocol queue 객체를 Q 입력
목록에서 제외한 것만으로 그 간접 영향이 deconfound되지는 않는다.

따라서 Q-v1은 현재 model trajectory를 재현 가능하게 측정하지만, 이 field를 포함한
결과를 인간의 transition-density 가설에 대한 근거로 사용할 수 없다.
`HM-DYN-001` 평가에는 queue/access semantic decoupling 또는 access field scope
ablation이 먼저 필요하다.

## Typed delta와 qualification

각 receipt는 동일 field의 before/after만 비교한다.

```text
delta_f = after_f - before_f

Q-v1(receipt) =
  any(abs(delta_f) >= 0.01 normalized simulation unit)
```

- threshold는 모든 eligible field에 공통으로 적용한다.
- 서로 다른 field delta를 더해 하나의 총 변화량을 만들지 않는다.
- `state_scope`는 검사한 전체 field를 보존하고, `typed_deltas`는 수치 오차 허용치
  `1e-12`를 넘는 non-zero delta만 보존한다. 그중 qualification threshold를 넘은
  field 이름은 `qualifying_fields`에 별도로 남긴다.
- threshold `0.01`은 인간 측정에서 보정된 역치가 아니라 versioned simulation
  measurement policy다.
- `transition_effective_at = processed_at`이다.
- field delta는 `typed_deltas`에 `MentalStateDelta` tuple로 보존한다.
- receipt와 qualified transition 모두 source의 `occurred_at`, `available_at`,
  `processed_at`, `reexposure_of_occurrence_id`를 provenance로 보존한다. reexposure
  reference는 더 이른 processing receipt의 occurrence를 가리켜야 하며,
  reexposure occurrence는 source가 처리되기 전으로 backdate될 수 없다.
- source의 `occurred_at`과 `available_at`은 count window의
  귀속 시각을 대신하지 않는다.

## Current-trace information only

receipt `i`의 qualification은 그 checkpoint에 이미 존재하는 before/after state,
processing stamp, Q-v1 policy만 읽는다. 미래 event나 later outcome을 읽지 않는다.

v1 `available_information`은 다음 네 literal label로 고정된다.

```text
current_observation_temporal_envelope
current_state_before
current_state_after
current_state_delta
```

따라서 같은 prefix를 가진 두 run에서 prefix processing trace가 같다면, 뒤에 붙은
future event가 prefix receipt의 delta나 qualification을 바꿀 수 없다. 이 조건은
future information leakage를 막지만 transition density의 predictive validity를
보장하지는 않는다.

## Same-time serialization limitation

Q-v1의 `aggregation_window`는 `processed_occurrence`다. 따라서 같은 canonical time의
semantic bundle을 여러 occurrence로 직렬화하거나 processing order를 바꾸면
before/after checkpoint와 count가 달라질 수 있다. 현재 engine이 기록하는
`same_timestamp_order_debts`도 이 문제가 아직 닫히지 않았음을 표시한다.

이 slice는 serialization/aggregation stability를 구현 불변식으로 주장하지 않는다.
alternative ordering과 semantic bundling에 대한 안정성은 future comparison의
failure probe다.

## Count와 density

양의 반열림 window `[start, end)`에서:

```text
count_Q
= qualified receipt 중
  start <= effective_at < end 인 receipt 수

duration
= end - start

density_Q
= count_Q / duration
```

`MentalTransitionWindowReport`는 `canonical_duration`, `qualified_count`,
`density_per_sim_time`을 각각 `CanonicalWindowDuration`,
`QualifiedTransitionCount`, `QualifiedTransitionDensity`로 보존한다. `end <= start`인
window는 정의하지 않는다. density를 count나 elapsed time에 자동 cast하지 않는다.

## 구조 테스트

- `test_one_receipt_per_processed_occurrence_and_qualified_subset`
- `test_transport_redelivery_does_not_create_mental_transition`
- `test_policy_ablation_changes_only_read_only_ledger`
- `test_future_events_cannot_requalify_prefix`
- `test_transition_window_keeps_count_and_density_distinct`

이 테스트가 통과해도 다음은 성립하지 않는다.

- Q-v1 transition이 인간 의식 episode의 자연 단위다.
- transition count나 density가 주관적 시간량이다.
- transition density가 recovery, access, retention을 예측한다.
- transition count가 변화 부하나 퀄리아 강도다.
- threshold `0.01`이 인간 집단에 일반화된다.
