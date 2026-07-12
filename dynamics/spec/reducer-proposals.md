# Reducer Proposal Instrumentation Contract — MORPH-001A

## 지위

| 범위 | 지위 |
|---|---|
| ordered pre-clamp reducer proposal capture | `IMPLEMENTED` |
| one receipt per processed occurrence | `IMPLEMENTED` |
| requested target / bounded committed target 분리 | `IMPLEMENTED` |
| independently identified `DeformationDemand` | `UNIMPLEMENTED` |
| `AccommodationEnvelope`, excess, residual, load | `UNIMPLEMENTED` |
| qualia 또는 subjective-time bridge | `HOLD` |
| 인간 경험적 검증 | `OPEN` |

measurement identity는 다음으로 고정한다.

```text
descriptive-reducer-preclamp-proxy@1.0.0
```

이 instrumentation이 기록하는 것은 현재 simulation reducer가 각 persistent-state
write의 `[0, 1]` storage bound를 적용하기 직전에 계산한 target이다. protocol wire의
raw payload도 아니고, 독립적으로 식별된 인간의 latent demand도 아니다.

```text
ReducerProposal
≠ raw ScenarioEvent payload
≠ independently identified DeformationDemand
≠ MorphicLoad
≠ qualia / subjective time
```

## 포착 위치

proposal은 final `after - before`에서 사후 복원하지 않는다. 값을 실제로 쓰는 동일한
reducer 계산 경로에서 clamp 직전에 포착한다.

```text
current writer basis
+ evaluated driver contributions
→ requested_after_unbounded
→ clamp01
→ committed_after
```

```text
requested_delta = requested_after_unbounded - basis_before
committed_delta = committed_after - basis_before
```

두 delta는 property로 계산한다. 그 차이는 현재로서는 산술적인 constraint gap일 뿐
`ExcessDemand`, `UncommittedResidual`, `ResidualStrain`으로 부르지 않는다.

## Ordered write boundary

한 occurrence에서 같은 field가 여러 번 쓰일 수 있다.

```text
fast body.energy write
→ optional slow action-cost body.energy write

slow accuse habit.impulsivity write
→ optional slow soothing habit.impulsivity write
```

따라서 proposal을 occurrence net vector 하나로 합치지 않는다. 각
`ReducerFieldProposal`은 다음을 보존한다.

```text
write_sequence
stage_id
operator_id
field
basis_before
requested_after_unbounded
committed_after
unit
constraint_id
typed driver contributions
```

같은 field의 다음 `basis_before`는 직전 write의 `committed_after`와 같아야 한다.
write sequence는 occurrence 안에서 연속적이며 fast stage 뒤에 slow stage가 온다.

measurement policy digest는 mandatory operator prefix, 허용된 conditional suffix,
operator별 `(stage, field, constraint, driver channel/label)` schema를 포함한다.
따라서 포화로 commit이 0인 mandatory proposal을 삭제하거나, 가짜
operator·field·driver를 같은 measurement identity 아래에 넣을 수 없다.
conditional action/soothing write는 receipt의 `ReducerProposalContext`에 기록된
performance action과 encoded soothing에 정확히 맞아야 한다. 수행이 없는 trace에
no-op action write를 붙이거나 ask cost를 withdraw driver로 재라벨링할 수 없다.

`ReducerStepResult`는 compatibility wrapper가 반환하는 committed state와 해당 stage의
proposal tuple을 묶는다. occurrence receipt에는 두 stage에서 나온 proposal을 하나의
flat ordered tuple로 보존한다. step result 객체 자체를 ledger에 중복 저장하지 않는다.

## Driver contribution

현재 channel은 다음과 같다.

```text
encoded_input
endogenous_dynamics
protocol_bridge
phenomenal_coupling
evidence_assessment_coupling
action_consequence
```

각 contribution의 합은 해당 write의 `requested_delta`와 일치해야 한다. 이것은 현재
수식의 algebraic provenance다. channel을 독립적인 심리 원인이나 경험적으로 식별된
효과로 해석하지 않는다. receipt는 이미 평가된 contribution을 보존하지만,
원래 ModelInput·evidence·performance 객체 전체를 복제해 source causality를
독립적으로 재식별하는 record는 아니다.
즉 validator는 driver identity·unit·합계의 구조적 허용성을 검사하고,
실제 contribution 값은 inline reducer builder가 writer boundary에서 남긴다.
직접 새로 구성한 자체-일관 record의 factual attribution을 validator 하나로
인증하지 않는다.

특히 access proposal에는 `legacy_v01_access_pressure_bridge`가 남아 있다. slow
proposal에는 update rate, phenomenal readout, evidence-assessment coupling,
performance consequence가 포함될 수 있다. 이 confound 때문에 proposal을
capacity-independent demand로 승격할 수 없다.

## Receipt와 provenance

실제 처리된 occurrence마다 `ReducerProposalReceipt` 하나를 post-run ledger에 만든다.

```text
ReducerProposalReceipt
├─ measurement identity / policy digest
├─ occurrence / delivery / reexposure identity
├─ occurred_at / available_at / processed_at
├─ processing_sequence
├─ conditional writer context + digest
├─ typed state-before / state-after projection + digest
└─ ordered ReducerFieldProposal tuple
```

receipt ID는 occurrence/delivery/reexposure, 시각, processing sequence, policy,
proposal digest, before/after state digest의 content identity에 결부된다. 인접 receipt의
`state_after_projection`은 다음 receipt의 `state_before_projection`과 일치해야 한다.
이 digest와 ID는 불일치 mutation·splicing을 검출하는 내부 integrity 장치이며,
전자서명이나 외부 authentication은 아니다. 모든 field와 digest를 함께 새로 만든
자체-일관 synthetic receipt의 외부 진실성까지 인증하지 않는다.

- transport duplicate와 redundant delivery는 receipt를 만들지 않는다.
- explicit current reexposure는 별도 occurrence이므로 새 receipt를 만들 수 있다.
- reexposure source는 더 이른 processed receipt여야 한다.
- reexposure occurrence는 source 처리 시점보다 앞서도록 backdate될 수 없다.
- dropped, rejected, unresolved input은 processed occurrence가 아니므로 receipt가 없다.

state projection은 normalized coordinate를 쓰지만, 이미 범위를 벗어난 초기 상태도
finite하면 감사 trace에 보존한다. 그 실행의 범위 오류는 기존 invariant
ledger가 별도로 남기며 instrumentation이 기존 audit path를 예외로 바꾸지
않는다.

receipt 수는 Q-v1 qualification과 독립적이다. storage saturation 때문에
`committed_delta = 0`이고 `MentalTransition`이 없어도 non-zero reducer proposal은
존재할 수 있다.

## Read-only 경계

capture는 reducer 안에서 일어나지만 proposal은 writer를 제어하지 않는다. traced
variant와 compatibility wrapper는 동일한 committed state를 반환해야 한다.

```text
apply_fast_update(...)
= apply_fast_update_traced(...).state_after

apply_slow_update(...)
= apply_slow_update_traced(...).state_after
```

receipt와 ledger는 `HumanState`, routing, evidence assessment, intent, performance,
action occurrence에 재입력되지 않는다. later event는 동일한 processed prefix의
proposal receipt를 다시 쓸 수 없다.

## 구조 테스트

- `test_one_reducer_proposal_receipt_per_processed_occurrence`
- `test_pre_constraint_reducer_proposal_is_distinct_from_committed_delta`
- `test_saturated_reducer_proposal_can_exist_without_mental_transition`
- `test_transport_redelivery_does_not_create_reducer_proposal_receipt`
- `test_current_reexposure_creates_new_reducer_proposal_with_source_provenance`
- `test_future_events_cannot_rewrite_reducer_proposal_prefix`
- `test_reducer_proposal_instrumentation_preserves_committed_runtime_semantics`
- `test_reducer_proposal_records_require_immutable_typed_components`
- `test_reducer_proposal_ledger_rejects_inconsistent_lineage_and_content_identity`
- `test_reducer_proposal_capture_preserves_invalid_initial_audit_path`

이 테스트는 current-reducer instrumentation의 무결성만 지지한다. 인간의 실제
처리 범위, 변화 부하, 정신 시간량 또는 퀄리아에 대한 근거가 아니다.
