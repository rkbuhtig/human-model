# RFC 0003 — Mental Transition Density and Morphic Load

| 항목 | 값 |
|---|---|
| Status | read-only transition ledger, `MORPH-001A`, `MORPH-001B` declared-band proxy comparison `IMPLEMENTED`; human DeformationDemand/capacity/load prediction `PROPOSED` |
| Target | v0.2 derived mental-transition ledger, `MORPH-001A/B`, 이후 outcome/load comparison |
| Kind | Type separation / dynamical hypotheses / measurement preconditions |
| Prerequisites | RFC 0001 구현, RFC 0002 canonical time |
| Human empirical status | `OPEN` |

## 문제

동일한 객관적 간격이 모든 사람에게 동일한 정신적 시간량을 뜻한다고 볼 수는
없다. 그러나 이를 곧바로 “주관적 시계가 더 빨리 흐른다”라고 쓰면 서로 다른
세 양을 다시 합치게 된다.

```text
외부 기준 시간
≠ 정신적으로 유효한 전이 수와 밀도
≠ 전이를 감당하기 위해 요구된 형태 변형 부하
≠ 그 부하가 현상적으로 드러난 강도
```

이 RFC는 이 네 항을 먼저 타입으로 분리한다. 아직 새로운 심리 계수나 퀄리아
법칙을 구현하지 않는다.

## 1. Canonical Time `τ`

RFC 0002의 단조 증가 기준 시간이다. 사건의 발생·가용·처리 시각을 정렬하는
프로토콜 좌표이며, 그 자체가 정신적 경험량은 아니다.

```text
Δτ = τ1 - τ0
```

v0.2에서는 기준 시간을 하나만 둔다. 독립적인 “정신 시계” 상태를 바로
추가하지 않는다.

## 2. Qualified Mental Transition

모든 tick, delivery, 함수 호출을 정신적 전이로 세지 않는다. 구현된 v1 ledger는
**처리된 occurrence 하나당 qualification receipt 하나**를 post-run에 파생하고,
사전에 고정한 판정자 `Q-v1`을 통과한 receipt만 qualified transition subset에
포함한다. receipt 전체와 qualified subset을 분리하므로 “처리됨”과 “유효 전이로
계수됨”도 같은 사실이 아니다.

```text
TransitionQualificationReceipt_i = (
  receipt_id,
  cause_occurrence_id,
  cause_delivery_id,
  reexposure_of_occurrence_id,
  cause_occurred_at,
  became_available_at,
  processed_at,
  qualified_at,
  processing_sequence,
  state_scope,
  aggregation_window,
  minimum_absolute_delta,
  delta_unit,
  available_information,
  typed_deltas,
  qualifying_fields,
  before_digest,
  after_digest,
  qualified,
  qualifier_id / qualifier_version / policy_digest
)

MentalTransition_i = (
  qualified receipt ref,
  cause occurrence / delivery / reexposure provenance,
  cause_occurred_at,
  became_available_at,
  transition_effective_at = processed_at,
  typed_deltas,
  qualifier identity / policy digest
)

N_Q[τ0, τ1]
= Σ_i 1[
    τ0 ≤ transition_effective_at_i < τ1
    and Q-v1(TransitionQualificationReceipt_i)
  ]

D_Q[τ0, τ1]
= N_Q[τ0, τ1] / (τ1 - τ0)

defined only when τ1 > τ0
```

### 구현된 `Q-v1`

```text
checkpoint
= 처리된 occurrence 하나의 before-state / after-state pair

eligible scope
= HumanState의 literal persistent descriptive scalar fields
  body / access / associative / affective / habit / narrative / relationship

excluded
= HumanState.clock
  EvidenceAssessmentState와 모든 certification record
  PhenomenalActivation, routing, action receipt 같은 현재 tick readout
  protocol queue와 미래 trace

typed delta(field)
= after(field) - before(field)

Q-v1(receipt)
= eligible field 중 하나 이상에서
  abs(typed delta) >= 0.01 normalized simulation unit

transition_effective_at
= processed_at
```

`0.01`은 인간 측정에서 얻은 역치가 아니라 v1 simulation measurement policy다.
필드별 delta를 먼저 보존하고 서로 다른 field를 하나의 총 변화량으로 더하지 않는다.
qualification은 해당 checkpoint의 state pair, processing stamp, versioned policy만
읽는다. 이후 occurrence나 post-run outcome은 이미 파생된 prefix receipt를 소급
재판정할 수 없다.

ledger는 run이 끝난 뒤 기존 processing trace에서 파생되는 immutable read-only
artifact다. 다른 `Q` policy로 다시 파생하면 receipt의 qualification과 report는
달라질 수 있지만 원래 `HumanState`, evidence/action ledger, processing trace는
달라지지 않는다. count와 density report도 human update에 되먹임되지 않는다.
transport redelivery는 처리된 occurrence가 아니므로 새 receipt나 transition을 만들지
않는다.

`D_Q`는 기준 시간당 유효 전이 밀도 report다. 동일한 `Δτ`에도 `N_Q`와 `D_Q`는
달라질 수 있다. 다만 무엇을 전이로 인정하는지 `Q`를 바꾸면 값도 바뀌므로,
판정자·state scope·checkpoint policy·버전을 receipt에 남겨야 한다. `Q-v1`은
임의의 solver substep이나 함수 호출이 아니라 per-processed-occurrence checkpoint를
판정한다. 자격 판정 시점에 아직 관측되지 않은 후속 결과를 사용해 앞선 전이를
소급 생성해서도 안 된다.
전이 밀도의 판별력을 평가할 때 later access·recovery·retention을 outcome으로 쓴다면,
같은 평가 window의 그 값을 `Q` 입력에 다시 넣지 않는다. qualification window와
lagged outcome window를 분리한다.

`cause_occurred_at`은 외부 원인이 일어난 시각이고 `transition_effective_at`은 그
원인에 접근해 모델의 해당 전이가 유효해진 시각이다. backlog에서는 둘이 다를 수
있으며 `N_Q/D_Q`의 구간 귀속은 `transition_effective_at`을 따른다. digest는
무결성 확인용일 뿐 qualification 근거를 대신하지 않는다.
`TransitionQualificationReceipt`가 `typed_deltas`, threshold와 unit, state scope,
checkpoint policy, qualifier version, 당시 이용 가능했던 입력을 보존한다.

### Q-v1의 알려진 access confound

`access.attention_budget`, `access.interference`, `access.queue_load`는 실제
`HumanState`의 literal field이므로 Q-v1 scope에 포함된다. 그러나 현재 이 값들은
여전히 `legacy_v01_access_pressure_bridge`의 영향을 받는다. protocol queue 객체
자체를 Q 입력에서 제외했다는 사실만으로 그 간접 영향이 제거되지는 않는다.

따라서 ledger는 **현재 구현이 만든 trajectory**를 재현 가능하게 측정할 수 있지만,
그 결과를 인간의 transition-density 가설에 대한 지지로 사용할 수는 없다.
`HM-DYN-001`을 평가하기 전에는 queue/access semantic decoupling 또는 해당 field를
제외·통제한 ablation이 필요하다.

### Q-v1의 same-time serialization limitation

v1의 `aggregation_window`는 `processed_occurrence`다. 같은 canonical time의 semantic
bundle을 여러 occurrence로 나누거나 처리 순서를 바꾸면 before/after checkpoint와
count가 달라질 수 있다. unresolved `same_timestamp_order_debts`가 있는 실행에서 이
위험은 특히 남는다.

따라서 현재 slice는 serialization/aggregation stability를 만족했다고 주장하지
않는다. alternative ordering과 semantic bundling에 대한 안정성은 후속 비교의
failure probe이며, `HM-DYN-001`의 support가 아니다.

### 금지

- 전송 fragment 수를 전이 수로 자동 사용
- 동일 occurrence의 재전송을 새 정신 전이로 자동 사용
- 상태가 달라졌다는 이유만으로 모든 미세 수치 오차를 전이로 계수
- solver step 크기나 같은 의미 묶음의 직렬화만 바꿔 전이 수를 늘림
- 후속 outcome을 보고 과거 transition qualification을 소급 변경
- 전이 수를 곧바로 경험 강도나 변화 부하로 부름

## 3. Deformation Demand와 Capacity Profile

전이 수만으로는 전이가 요구한 변형의 크기를 알 수 없다. 변화 부하는 현재의
형태와 처리 가능 영역에서 얼마나 벗어난 재구성이 요구되는가에 상대적이다.

```text
CurrentShape_t + IncomingConstraint_i
        ↓ pre-transition deformation operator
DeformationDemand_i

DeformationDemand_i + CapacityProfile_t
        ↓ relative-load operator
MorphicLoadProfile_i
```

초기 표현은 scalar가 아니라 typed vector다.

```text
CapacityProfile = {
  affect_regulation,
  attentional_reorientation,
  action_reconfiguration,
  narrative_reintegration,
  relational_adaptation
}

DeformationDemand = {
  같은 typed dimensions의 요구량,
  source refs,
  pre-transition shape snapshot,
  deformation operator version
}

MorphicLoadProfile = {
  demand-to-capacity relation by typed dimension,
  redistribution requirements,
  pre-transition capacity snapshot,
  relative-load operator version
}
```

차원은 예시이며 경험 자료 없이 확정하지 않는다. 중요한 제약은 요구량을
`after - before`로 사후 정의하지 않는 것이다. 그렇게 하면 “많이 변했기 때문에
큰 요구였다”는 순환이 생긴다. Demand는 update 전에 선언된 입력 제약과 현재
형태에서 계산되어야 한다. Capacity는 그 Demand를 정의하는 입력이 아니라,
이미 정의된 Demand가 현재 처리 범위를 얼마나 벗어나는지 계산하는 다음 단계다.
이 순서를 지켜야 capacity를 두 번 반영하지 않는다.

### 3A. `MORPH-001A` — reducer proposal–commit instrumentation

첫 구현 조각은 capacity나 load를 계산하지 않는다. 현재 reducer가 각 stage에서
요청한 **bound 적용 전 field displacement**와 실제 persistent state에 commit된
displacement를 같은 trace에 보존한다.

```text
ReducerDriverContribution = (
  typed channel,
  label,
  contribution
)

ReducerFieldProposal = (
  write_sequence,
  stage_id / operator_id,
  field,
  basis_before,
  requested_after_unbounded,
  committed_after,
  unit,
  constraint_id,
  typed driver contributions
)

requested_delta = requested_after_unbounded - basis_before
committed_delta = committed_after - basis_before

ReducerStepResult = (
  committed stage state,
  ordered typed field proposals
)

ReducerProposalReceipt = (
  receipt_id,
  measurement identity / version / policy_digest,
  occurrence / delivery / reexposure provenance,
  occurred_at / available_at / processed_at / captured_at,
  processing_sequence / available_information,
  conditional writer context / context_digest,
  typed state_before / state_after projection + digest,
  flat occurrence-wide ordered proposals tuple / proposal_digest
)

ReducerProposalLedger = ordered ReducerProposalReceipt sequence
```

`ReducerStepResult`는 traced reducer가 계산 중 state와 proposal을 함께 engine에 넘기는
runtime wrapper다. engine은 fast/slow proposal을 write sequence 순서로 평탄화해
`TickTrace.reducer_proposals`에 저장한다. post-run receipt는 이 flat tuple을 복사·검증하며
step-result sequence 자체는 ledger schema가 아니다.
`captured_at = processed_at`이며 policy는 fast→slow stage order, normalized unit과 현재
이용 가능한 driver 집합을 version/digest로 고정한다. policy digest는 mandatory
operator prefix, 허용된 conditional suffix, operator별
stage·field·constraint·driver identity schema를 포함한다. receipt ID는
occurrence lineage·시각·proposal/state digest의 content identity에 결부된다.
action/soothing conditional suffix와 driver는 performance identity·encoded soothing을
담은 최소 context와 일치해야 한다.

한 occurrence에서 같은 field가 여러 stage 또는 write를 통과할 수 있으므로 첫 조각은
이를 성급하게 합산하지 않고 ordered stage/write-qualified proposal을 그대로 보존한다.
같은 field의 다음 `basis_before`는 앞선 committed target에서 이어져야 한다. write별
committed delta와 occurrence 최종 `after - before` net delta도 동일한 양으로 취급하지
않는다. receipt는 모든
processed occurrence에 하나씩 생기며 Q-v1을 통과한 `MentalTransition`에만 붙지 않는다.
따라서 saturation으로 commit이 0이어도 requested displacement는 존재할 수 있다.

measurement model은 `descriptive-reducer-preclamp-proxy@1.0.0`이다. 여기서 기록하는
것은 **현재 versioned simulation reducer가 요청한 pre-constraint proposal**이다.
fast/slow reducer에 이미 들어간 access pressure, update rate, phenomenal activation,
performance 같은 현재 driver의 효과를 포함할 수 있으므로, capacity-independent
`DeformationDemand`가 아니다.
typed driver contribution도 구현 수식의 algebraic provenance이지 독립 causal effect나
경험적으로 식별된 심리 요인이 아니다.

```text
ReducerProposal
≠ independently identified DeformationDemand
≠ MorphicLoad
```

따라서 첫 조각은 향후 Demand 측정의 instrumentation precursor일 뿐 인간의 실제
변형 요구량이나 latent quantity를 식별하지 않는다. 현재 입력·현재 stage state·현재
writer만 사용하며, 미래 결과나 post-run recovery에서 proposal을 역산하지 않는다.

instrumentation은 update를 관찰하기 위해 reducer boundary에서 기록되지만 생성
runtime을 제어하지 않는다.

```text
same writer inputs
→ traced reducer committed state = compatibility reducer committed state

proposal / receipt artifacts
↛ state, routing, evidence, action update inputs
```

이는 임의의 instrumentation 코드 변경이 항상 semantics-preserving이라는 주장이 아니다.

세부 사전 등록과 saturation control은
[`MORPH-001A` benchmark](../benchmarks/morph-001-demand-commit.md)에 고정한다.

### 3B. 구현된 simulation envelope comparison과 아직 구현하지 않는 human load

`MORPH-001B`는 `MORPH-001A`의 reducer-write proposal을 실험자가 선언한 signed
simulation band와 비교한다. `ReducerProposalEnvelopePolicy`와 ordered
`ReducerProposalEnvelopeComparison`은 구현됐지만, measured human
`AccommodationEnvelope / CapacityProfile`은 아니다. `[0, 1]` state bound나 bound까지
남은 거리도 storage validity constraint일 뿐 accommodation capacity가 아니다.

```text
ReducerProposal + declared simulation band
→ ordered proxy-excess profile                     # IMPLEMENTED

measured human AccommodationEnvelope               # UNIMPLEMENTED
ExcessDemand                                       # UNIMPLEMENTED
requested_delta - committed_delta                  # arithmetic gap only
UncommittedResidual / ResidualStrain                # UNIMPLEMENTED
MorphicLoadProfile                                 # PROPOSED / UNIMPLEMENTED
```

기준 comparison은 componentwise signed clipping 하나이며 normalized·max·L1·L2는
competing candidate로만 사전 등록한다. policy는 opt-in synthetic fixture이고 생성
실행에 되먹임되지 않는다. 상세 범위는
[`MORPH-001B` benchmark](../benchmarks/morph-001b-proposal-envelope-comparison.md)에
고정한다.

요청–commit 차이에는 clamp, 감쇠, stage 상호작용과 구현 artifact가 섞일 수 있다.
별도 operator와 단위 없이 이를 residual strain으로 승격하지 않는다.

## 4. Morphic Work, Residual Strain, Persistent Trace

Demand가 모두 실제 변화로 수행되는 것은 아니다.

```text
MorphicLoadProfile_i
        + response policy
        ↓
MorphicWorkReceipt_i
├─ achieved_deformation
├─ unmet_demand
├─ capacity_consumed
└─ estimated_recovery_requirement

ResidualStrain_{t+}
TraceCandidate_{t+}

TraceCandidate
        + preregistered retention horizon / revalidation
        ↓
PersistentTrace_{t+h}
```

따라서 다음은 서로 독립적으로 달라질 수 있다.

```text
같은 전이 수, 다른 Morphic Load
같은 Morphic Load, 다른 전이 수
같은 Demand, 다른 achieved deformation
같은 achieved deformation, 다른 residual strain
```

즉시 생긴 흔적은 persistence를 아직 입증하지 않으므로 `TraceCandidate`다.
사전에 정한 horizon 뒤에도 보존되고 재측정 조건을 통과한 경우에만
`PersistentTrace`로 승격한다.

`Morphic Load`는 당분간 하나의 총점이 아니다. `MorphicLoadProfile`과 receipt의
typed 관계를 통칭하는 연구 용어로만 쓴다. scalar aggregation은 측정 타당성과
판별 이득이 입증된 뒤 별도 claim으로 제안한다.

## 5. 퀄리아와의 경계

변형 부하를 곧 퀄리아라고 부르지 않는다.

```text
Morphic Load
≠ PhenomenalStrainReadout
≠ 외부 사실의 Evidence
```

미래 가설은 다음 정도로만 연다.

> 현재 형태와 처리 가능 범위를 넘어서는 변형 요구 및 잔여 strain이 특정
> 조건에서 현상적 강도에 영향을 줄 수 있다.

하지만 readout은 attention, masking, habituation, bodily state, report access에
따라 달라질 수 있다. 큰 부하가 반드시 강하게 보고되거나, 강한 느낌이 반드시
큰 구조 변화였다고 역추론되지는 않는다. `PhenomenalStrainReadout`은 구현되더라도
simulation-only descriptive output이며 EvidenceLink를 만들지 않는다.

이 RFC는 기존 interchapter note의 `QualiaMedium / QualiaMorph` 존재론을 채택하거나
폐기하지 않는다. 여기의 `PhenomenalStrainReadout`은 실제 퀄리아와 동일한 것이
아니라, 미래 실험을 위해 정의할 수 있는 simulation proxy 또는 report variable다.

## 6. 슬라임 비유의 지위

“슬라임의 모양을 얼마나 변성해야 하는가”는 다음 관계를 직관적으로 설명한다.

```text
현재 형태 + 허용 변형 범위 + 외부 요구
→ 필요한 재형성 + 남은 strain
```

지위는 `METAPHOR`다. 실제 물질의 탄성·점도·에너지 단위, 보존 법칙, 생물학적
기질을 주장하지 않는다. 이 비유는 측정 근거나 경험적 지지로 인용할 수 없다.

## 판별 실험

### A. Transition density

동일한 `Δτ`, 동일 occurrence 수에서 `Q`를 만족하는 상태 전이 수만 다르게 만든다.
elapsed-time-only 모델과 transition-ledger 모델이 이후 access/recovery를 다르게
예측하는지 비교한다. 같은 의미 update를 solver step이나 transport partition만
달리 표현했을 때 `N_Q`가 허용 오차 밖에서 바뀌면 qualification 설계를 실패로
판정한다.

현재 구현 성취는 이 실험을 실행할 immutable receipt와 count/density measurement
surface까지다. transition density가 later access/recovery를 더 잘 예측하는지는
`HM-DYN-001`로 남아 있으며 아직 구현·검증되지 않았다.

### B. Count–load dissociation

```text
조건 1: 작은 적응 30회
조건 2: 기존 capacity를 크게 벗어나는 적응 3회
```

전이 수만 쓰는 모델과 typed demand/capacity 모델을 비교한다. load 모델은
미리 등록한 residual strain, recovery time, horizon 뒤 persistent trace 중 적어도 하나에서
count-only 모델보다 판별 이득을 내야 한다.

### C. Capacity relativity

동일한 입력과 전이 수를 두 CapacityProfile에 공급한다. 차이는 Evidence나
WorldOccurrence가 아니라 work receipt와 이후 descriptive trajectory에만 나타나야
한다.

### D. Phenomenal bridge — `HOLD`

동일한 receipt에서 report access나 attention만 바꾸는 실험이 정의되기 전에는
부하와 현상 강도의 대응식을 구현하지 않는다.

위 synthetic 비교는 구현 sanity와 구조적 판별 가능성만 검사한다. dynamical
claim의 support로 승격하려면 독립 관측이나 held-out human data, 사전 등록된
measurement mapping, 복잡도 보정이 필요하다.

## 구현 순서

1. **완료:** v0.2 canonical timestamp와 occurrence/delivery/reexposure provenance를 구현한다. (`FlowUpdate/EventJump`는 별도 후속 slice.)
2. **완료:** processed occurrence checkpoint의 state projection에서 파생되는
   immutable read-only `MentalTransitionLedger`를 추가한다.
3. **완료:** `Q-v1`의 literal persistent scope, per-occurrence checkpoint,
   `0.01` threshold/unit, qualification 시점, typed delta, current-trace 정보 집합을
   버전 고정한다.
4. **완료:** transition count/density report만 만들고 상태 update에는 사용하지 않는다.
5. **완료 — `MORPH-001A`:** pre-constraint reducer proposal과 committed target을
   stage-qualified immutable receipt로 분리한다. 아직 envelope나 load를 계산하지 않는다.
6. **완료 — `MORPH-001B`:** experimenter-declared reducer-write band와
   componentwise proxy comparison을 사전 등록하고 구현한다. state bound를 band로
   재사용하거나 human capacity/load로 승격하지 않는다.
7. 이후에만 vector `MorphicLoadProfile`, residual, recovery와 count-only 경쟁 모델을
   한 최소 사례에서 비교한다.
8. retention horizon 뒤 `PersistentTrace` 승격 여부를 별도 측정한다.
9. count-only 경쟁 모델보다 판별 이득이 없으면 load 가설을 기각·축소한다.
10. phenomenal bridge는 독립 실험과 측정 모델이 생길 때까지 `HOLD`한다.

## 비목표

- 물리적 시간 자체의 재정의
- 객관 시간과 독립된 주관 시계 상태의 즉시 도입
- 모든 상태 delta를 의식 episode로 간주
- 전이 수·부하·퀄리아의 단일 scalar 합성
- 슬라임 비유를 물리 법칙으로 사용
- 인간 자료 없이 “정신 시간의 실재 단위”를 확정

## 종료 조건

### Read-only ledger slice — `SATISFIED`

1. canonical time, transition identity, count/density가 별도 타입이다.
2. ledger 추가가 v0.1.1 semantic golden을 바꾸지 않는다.
3. transport duplication이 receipt나 전이 수를 늘리지 않는다.
4. policy ablation은 derived ledger만 바꾸고 base run trace와 state를 바꾸지 않는다.
5. 미래 event가 이미 파생된 prefix qualification을 소급 변경하지 않는다.
6. 양의 window에서 count와 density가 별도 report로 계산되고 update에 재입력되지 않는다.
7. count가 load나 phenomenal intensity로 자동 cast되지 않는다.

구조 테스트:

- `test_one_receipt_per_processed_occurrence_and_qualified_subset`
- `test_transport_redelivery_does_not_create_mental_transition`
- `test_policy_ablation_changes_only_read_only_ledger`
- `test_future_events_cannot_requalify_prefix`
- `test_transition_window_keeps_count_and_density_distinct`

이 테스트는 `Q-v1` 구현과 derived-ledger 경계를 지지할 뿐, 정신 시간이나 인간
예측 타당성을 지지하지 않는다.

### `MORPH-001`와 phenomenal bridge — `OPEN / HOLD`

1. demand는 pre-transition shape에서, load는 demand/capacity 관계에서 계산해
   순환과 capacity 이중계상을 피한다.
2. persistent라는 이름은 retention horizon 통과 뒤에만 부여된다.
3. 단위·정규화·결측 규칙 없이는 demand/capacity의 `벗어남`을 계산하지 않는다.
4. 경쟁 모델, 정상 통제, 폐기 조건이 report에 함께 기록된다.

### `MORPH-001B` declared-envelope comparison — `SATISFIED / SIMULATION PROXY ONLY`

1. policy는 exact reducer field scope, signed band, unit, source measurement identity와
   componentwise operator를 digest에 고정한다.
2. 같은 proposal은 다른 declared band에서 다른 proxy excess를 만들 수 있고, source
   proposal ledger는 동일하다.
3. same committed delta 또는 same qualified-transition count가 different ordered proxy
   profile을 숨길 수 있다.
4. storage clamp gap과 declared band 밖의 양은 독립적이다.
5. 모든 source receipt/write가 하나의 derived receipt/component와 순서대로 대응하며,
   repeated write·saturation·cancellation도 component를 삭제하지 않는다.
6. policy variation은 state, trace, Evidence, routing, action, Q와 source proposal
   ledger를 바꾸지 않는다.
7. transport/reexposure/prefix와 finite-invalid-initial audit 경계를 보존한다.

이 조건은 synthetic simulation comparison의 구조적 재현성만 판정한다. human
accommodation capacity, `DeformationDemand`, `MorphicLoad`, qualia 또는 mental time의
support가 아니다.

### `MORPH-001A` instrumentation — `SATISFIED`

1. 모든 processed occurrence는 하나의 occurrence-lineage-bound,
   operator-schema-bound receipt를 갖고 transport
   redelivery는 이를 늘리지 않는다.
2. pre-constraint requested displacement와 committed displacement는 별도 값이며,
   saturation control에서 달라질 수 있다.
3. proposal receipt는 Q-qualified transition이 없어도 존재할 수 있다.
4. 미래 event는 동일 prefix의 proposal receipt를 변경하지 않는다.
5. traced reducer와 compatibility wrapper의 committed state가 같고, proposal과
   receipt가 state·evidence·routing·action update의 입력이 되지 않는다.
6. receipt는 envelope, excess, residual strain, MorphicLoad, qualia 또는 정신 시간을
   생성하지 않는다.
7. policy-bound operator/driver schema, content-bound identity, typed state projection과
   인접 receipt state chain이 내부 불일치를 거부한다.
8. finite out-of-bound initial state의 기존 invariant-audit 경로를 instrumentation
   exception으로 바꾸지 않는다.

이 조건은 instrumentation의 무결성만 판정한다. `HM-DYN-002`나 인간 경험적
타당성의 support가 아니다.
