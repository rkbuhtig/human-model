# RFC 0003 — Mental Transition Density and Morphic Load

| 항목 | 값 |
|---|---|
| Status | `PROPOSED` |
| Target | v0.2 이후의 read-only transition ledger, 이후 `MORPH-001` |
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

모든 tick, delivery, 함수 호출을 정신적 전이로 세지 않는다. 사전에 선언한
판정자 `Q`를 통과해 모델의 관련 상태가 `a → b`로 바뀐 경우만 read-only
ledger에 기록한다.

```text
MentalTransition_i = (
  transition_id,
  cause_ref,
  cause_occurred_at,
  became_available_at,
  transition_effective_at,
  processed_at,
  qualified_at,
  state_scope,
  aggregation_window,
  typed_delta,
  before_digest,
  after_digest,
  qualification_receipt_id
)

N_Q[τ0, τ1]
= Σ_i 1[
    τ0 ≤ transition_effective_at_i < τ1
    and Q(MentalTransition_i)
  ]

D_Q[τ0, τ1]
= N_Q[τ0, τ1] / (τ1 - τ0)

defined only when τ1 > τ0
```

`D_Q`는 기준 시간당 유효 전이 밀도다. 동일한 `Δτ`에도 `N_Q`와 `D_Q`는
달라질 수 있다. 다만 무엇을 전이로 인정하는지 `Q`를 바꾸면 값도 바뀌므로,
판정자·state scope·aggregation window·버전을 trace에 남겨야 한다. `Q`는 임의의
solver substep이나 함수 호출이 아니라 사전 선언된 semantic checkpoint 사이를
판정한다. 자격 판정 시점에 아직 관측되지 않은 후속 결과를 사용해 앞선 전이를
소급 생성해서도 안 된다.
전이 밀도의 판별력을 평가할 때 later access·recovery·retention을 outcome으로 쓴다면,
같은 평가 window의 그 값을 `Q` 입력에 다시 넣지 않는다. qualification window와
lagged outcome window를 분리한다.

`cause_occurred_at`은 외부 원인이 일어난 시각이고 `transition_effective_at`은 그
원인에 접근해 모델의 해당 전이가 유효해진 시각이다. backlog에서는 둘이 다를 수
있으며 `N_Q/D_Q`의 구간 귀속은 `transition_effective_at`을 따른다. digest는
무결성 확인용일 뿐 qualification 근거를 대신하지 않는다. 별도
`QualificationReceipt`가 typed delta, threshold와 unit, state scope, aggregation
window, qualifier version, 당시 이용 가능했던 입력을 보존해야 한다.

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

1. v0.2 canonical time과 occurrence/delivery identity를 먼저 구현한다.
2. semantic checkpoint 사이의 state projection에서 파생되는 read-only
   `MentalTransitionLedger`를 추가한다.
3. `Q`의 scope, aggregation window, minimum-change, qualification 시점,
   typed delta, threshold/unit, 이용 가능한 정보 집합을 버전 고정한다.
4. transition count/density report만 만들고 상태 update에는 사용하지 않는다.
5. `MORPH-001`에서 pre-transition `DeformationDemand`, vector
   `CapacityProfile`, `MorphicLoadProfile`, `MorphicWorkReceipt`,
   `ResidualStrain`, `TraceCandidate`를 한 최소 사례로 비교한다.
6. retention horizon 뒤 `PersistentTrace` 승격 여부를 별도 측정한다.
7. count-only 경쟁 모델보다 판별 이득이 없으면 load 가설을 기각·축소한다.
8. phenomenal bridge는 독립 실험과 측정 모델이 생길 때까지 `HOLD`한다.

## 비목표

- 물리적 시간 자체의 재정의
- 객관 시간과 독립된 주관 시계 상태의 즉시 도입
- 모든 상태 delta를 의식 episode로 간주
- 전이 수·부하·퀄리아의 단일 scalar 합성
- 슬라임 비유를 물리 법칙으로 사용
- 인간 자료 없이 “정신 시간의 실재 단위”를 확정

## 종료 조건

이 RFC의 첫 구현 단계는 다음을 모두 만족해야 한다.

1. canonical time, transition identity, count/density가 별도 타입이다.
2. ledger 추가가 v0.1.1 semantic golden을 바꾸지 않는다.
3. transport duplication이 전이 수를 늘리지 않는다.
4. solver step과 허용된 serialization 차이가 전이 수를 과도하게 바꾸지 않는다.
5. `Q`, scope, aggregation window를 바꾸지 않고 임의로 전이를 추가할 수 없다.
6. 후속 outcome이 과거 qualification에 누출되지 않는다.
   qualification 입력과 lagged evaluation outcome도 분리된다.
7. count가 load나 phenomenal intensity로 자동 cast되지 않는다.
8. demand는 pre-transition shape에서, load는 demand/capacity 관계에서 계산해
   순환과 capacity 이중계상을 피한다.
9. persistent라는 이름은 retention horizon 통과 뒤에만 부여된다.
10. 단위·정규화·결측 규칙 없이는 demand/capacity의 `벗어남`을 계산하지 않는다.
11. 경쟁 모델, 정상 통제, 폐기 조건이 report에 함께 기록된다.
