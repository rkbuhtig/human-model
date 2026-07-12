# Test Oracle and Invariants

## 판정 등급

| 등급 | 의미 | 예 |
|---|---|---|
| `HARD` | 계수와 행동 성향이 달라도 위반하면 안 됨 | 상상이 외부 증거가 됨 |
| `CONTRACT` | v0.1이 의도적으로 채택한 연산 방향 | body capacity 차단 시 수행만 사라짐 |
| `EXPLORATORY` | 궤적을 관찰하지만 정답을 두지 않음 | 불안할 때 어떤 행동 후보가 1위인가 |

## HARD

```text
ScenarioTruth ≠ ObservationArtifact
RoutingInfluence ≠ EvidenceLink
Stake ≠ EvidenceStrength
Candidate ≠ Intent
Intent ≠ Attempt
Attempt ≠ PerformanceReceipt
PerformanceReceipt ≠ ActionOccurrence
ActionOccurrence ≠ WorldOutcome
WorldOutcome ≠ ObservedOutcome
InternalSimulation ≠ ExternalOccurrence
Recovery ≠ HistoryDeletion
```

### H1 오라클 격리

동일한 초기 상태·관측열·실행 정책은 숨은 세계가 달라도 동일한 궤적을 만든다. 숨은 진실은 엔진 함수의 인자가 아니다.

### H2 claim별 grounds

채택된 claim은 자기 claim을 지지하는 EvidenceLink ID를 가져야 한다. 다른 claim의 강한 근거나 높은 감정 salience를 빌릴 수 없다.

### H3 행동 단계

차단된 attempt는 PerformanceReceipt와 ActionOccurrence를 만들지 못한다. coercion이 있는 수행은 현재 `agency < 1`로만 표시되며 coercer causal edge는 아직 미구현이다.

### H4 append-only

새 설명과 반증은 이전 ObservationArtifact·EvidenceLink·ActionAttempt를 삭제하지 않는다. 현재 stance만 갱신된다.

### H5 중복 멱등성

같은 `event_id`의 재전송은 한 번만 처리한다. 별도 ID를 가진 실제 반복 사건과 구분한다.

### H6 명시적 과부하

처리되지 않은 입력은 dropped 또는 unresolved로 남는다. 입력 회계가 맞지 않으면 즉시 실패다.

### H7 수치 안전성

모든 unit state는 유한한 `[0,1]` 범위에 있고 routing probability의 합은 1이다.

## Counterfactual whitelist

| 단일 변경 | 변경 가능 | 변경 금지 |
|---|---|---|
| 관계 Stake | 느낌·routing·관계 비용 | EvidenceLink 내용·strength |
| rejection access | 후보 우선순위·느린 update | 현재 외부 근거 |
| action capacity | BodyAuthorization·PerformanceReceipt | 차단 전 route·claim grounds |
| 숨은 세계 | 관측 분기 뒤 궤적 | 동일 관측 구간의 궤적 |
| 내부 상상 | 느낌·routing·associative residue, 후속 별도 decision window | 그 상상 자체의 EvidenceLink·ActionOccurrence |
| 같은 declared independence group 반복 | salience·노출 흔적 | 독립 support mass |

## 회복 판정

회복은 두 단계를 분리한다.

1. 회복 입력이 실제로 처리됐는가
2. 첫 회복 입력 직전과 마지막 회복 입력 직후의 같은 상태량이 이완됐는가
3. 회복 구간 뒤 오래된 stress backlog가 다시 처리됐는가

```text
recovery_delivery_ratio < 0.80
→ not_reached_due_to_backlog

delivery reached but distress did not relax
→ failed_to_relax

associative state remains at upper boundary
→ failed_by_plastic_lock

all plastic residue erased
→ failed_by_full_reset

relaxation + bounded residual + append-only history
→ passed_nonreset
```

`recovery_drop`은 `AffectivePrior.residual_distress`의 회복 직전·직후 차이다. PhenomenalActivation과 AffectivePrior처럼 다른 residence를 서로 빼지 않는다.

과부하로 회복 자극이 큐에 갇힌 경우를 “회복 연산이 실패했다”고 오판하지 않는다. 회복 뒤 backlog stress를 다시 처리해 최종 상태가 재상승한 경우도 `post_recovery_stress_processed`로 분리한다.
