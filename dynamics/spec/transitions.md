# Transition Contract

## 두 개의 분리된 경로

```text
ObservationArtifact
→ claim-specific EvidenceLink
→ ClaimState support / contradiction
→ adopt / hold
```

```text
PhenomenalActivation
→ Candidate
→ RoutedCandidate

validated protocol decision window
→ ActionOpportunity

RoutedCandidate + ActionOpportunity
→ IntentDecision
→ MotorFeasibility
→ ActionAttempt
→ PerformanceReceipt
→ ActionOccurrence

후속 world adapter
→ WorldOutcome
→ ObservationArtifact
```

`models/routing.py`는 `EvidenceLink`를 읽지 않고 salience 성분만 출력한다.
`contract/`는 HumanState나 RoutedCandidate를 받지 않는다. 이 API 분리가
`Influence ≠ cross-domain certification authority`의 코드 수준 방화벽이다.

EvidenceLink는 scenario payload의 자유 선언이 아니다. `grounding_rule_id`를 보존하며 producer와 validator가 각각 `event kind × claim × relation × provenance × maximum strength` allowlist를 검사한다. claim state는 `(claim_id, scope)`로 분리된다.

## Tick 순서

1. delivery와 occurrence의 ID·payload를 각각 검사하고 transport redelivery와 현재 reexposure를 구분한다.
2. 입력 용량을 계산하고 초과 입력을 `deferred / dropped / unresolved`로 기록한다.
3. 처리된 입력에서 `ObservationArtifact`를 만든다.
4. 외부이며 grounding allowlist를 통과한 신호만 EvidenceLink로 연결한다.
5. claim별 support·contradiction을 갱신하고 채택·철회 히스테리시스를 적용한다.
6. 신체·접근 상태와 현재 입력으로 `PhenomenalActivation`을 계산한다.
7. 후보를 생성하고 비권위적 routing 분포를 계산한다.
8. 유효한 action window만 ActionOpportunity를 만들고, 그 record를 참조해 intent를 선택한다.
9. MotorFeasibility와 함께 ActionAttempt를 기록한다.
10. 수행 가능한 시도만 PerformanceReceipt와 ActionOccurrence를 만든다.
11. 느린 내부 상태를 갱신하고 StateDelta를 남긴다.
12. 구현된 per-tick HARD validator를 실행한다. 오라클 격리·append-only 전체 이력 등 시나리오 수준 속성은 별도 metamorphic test가 담당한다.

`ActionOccurrence`는 행동이 세계에 들어갔다는 기록일 뿐, 원하는 결과가 일어났다는 뜻이 아니다. 실제 WorldOutcome과 관찰은 후속 world adapter·ScenarioEvent가 제공해야 하며 같은 tick의 증거로 되먹임되지 않는다.

한 사건 안의 support와 contradiction은 전부 집계한 뒤 stance를 한 번만 계산한다. 같은 처리 tick의 stance hysteresis는 tick 시작 상태를 anchor로 사용해 event ID나 도착 순서만으로 채택 여부가 바뀌지 않게 한다.

## 증거 반복

각 EvidenceLink는 시나리오가 선언한 `independence_key`를 가진다. 같은 선언 그룹의 반복은 가장 강한 기여 하나만 남는다. 실제 출처 의존성을 엔진이 추론하는 기능은 아직 없다.

```text
같은 independence group의 소문을 열 번 반복
→ salience·plastic update에는 영향 가능
→ 독립 evidence mass 열 배 증가 금지
```

## 입력 회계

```text
raw_received
= unique_received
  + duplicate_delivery
  + redundant_delivery
  + identity_collision
  + dangling_reexposure
  + invalid_reexposure_time

unique_received
= processed + dropped + unresolved
```

`unique_received`는 v0.1 호환 필드명이며 현재 뜻은 queue에 받아들인 delivery 수다.
drop 뒤 같은 occurrence가 새 delivery로 재시도되면 두 admission을 각각 회계한다.
`deferred_unique`는 처리 여부와 별개로 한 번 이상 지연된 delivery 수다. 지연 후
처리된 delivery를 손실로 다시 계산하지 않는다.

### Ingress priority

기본 큐 정책은 `ingress_priority`를 사용한다. 이것은 처리 순서만 바꾸는 access knob다.

```text
IngressPriority
≠ Salience
≠ EvidenceStrength
≠ TruthProbability
```

FIFO 정책도 대조군으로 실행할 수 있다. 복합 부하에서 FIFO는 회복 자극을 오래된 모호 입력 뒤에 굶겼고, priority 정책은 같은 evidence strength를 유지한 채 회복 입력을 전달했다.

## 채택 히스테리시스

```text
adopt when confidence ≥ 0.75 and support mass ≥ 0.50
release when confidence < 0.55
```

이는 심리학적 상수가 아니라 v0.1의 시뮬레이션 정책이다. 상반 근거가 들어와 확신이 `0.75` 아래로 내려가도 `0.55` 위라면 기존 채택이 잠시 유지될 수 있다. 불변식은 이 히스테리시스와 기존 grounds를 함께 검사한다.
