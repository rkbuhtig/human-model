# State Contract

## 모델 지위

`Human Model Dynamics v0.1`은 인간 내부 상태에 관한 실행 가설이다. Chapter 01–11이 직접 도출한 완성 이론이 아니다.

| 표지 | 의미 |
|---|---|
| `DIRECT-LINEAGE` | 기존 권한 척추에서 직접 유지한 분리·금지 규칙 |
| `BRIDGE-HUMAN` | 인간 모델을 실행하기 위해 명시한 가설 |
| `SIMULATION-ONLY` | 테스트를 위한 수치·읽기값 |
| `HOLD` | 아직 구현하지 않거나 존재론적 주장을 보류한 개념 |

## Residence

| Residence | 주요 타입 | Writer | 시계 | 권한 | 지위 |
|---|---|---|---|---|---|
| Scenario oracle | `hidden_worlds` | scenario author | 외부 | 테스트만 읽음 | `SIMULATION-ONLY` |
| Persistent human | `BodyState`, `AccessState`, `AssociativeState`, `AffectivePrior`, `HabitPolicy`, `NarrativeState`, `RelationalProfile` | human reducer | 빠름·느림 혼합 | 외부 사실 쓰기 금지 | `BRIDGE-HUMAN` |
| Epistemic | `ObservationArtifact`, `EvidenceLink`, `ClaimState` | evidence linker·adjudicator | 사건 | claim별 내부 채택 | `DIRECT-LINEAGE + BRIDGE-HUMAN` |
| Momentary runtime | `PhenomenalActivation`, `Candidate`, `RoutedCandidate`, `IntentDecision` | 현재 tick 연산 | 빠름 | routing만 | `BRIDGE-HUMAN / SIMULATION-ONLY` |
| Action | `BodyAuthorization`, `ActionAttempt`, `PerformanceReceipt` | action pipeline | 사건 | 수행 범위만 | `DIRECT-LINEAGE + BRIDGE-HUMAN` |
| World-facing | `ActionOccurrence` | performed receipt를 받은 occurrence writer | 외부 접촉 | 수행된 행동 범위만 | `DIRECT-LINEAGE` |
| Audit | `EpisodeTrace`, `TickTrace`, `StateDelta` | engine logger | append-only | 인간 근거로 자동 재입력 금지 | `SIMULATION-ONLY` |

## 지속 상태를 하나의 PlasticState로 두지 않은 이유

느린 변화를 하나의 만능 상태로 합치면 어떤 원인이 어떤 경로를 바꿨는지 알 수 없다. v0.1은 최소한 다음을 분리한다.

```text
AssociativeState  기억 단서와 접근 경사
AffectivePrior    이전 활성에서 남은 정서적 잔여
HabitPolicy       반복된 행동 선택 경사
NarrativeState    자신·관계에 대한 채택된 해석
RelationalProfile Stake·trust·boundary strain
BodyState         에너지·각성·행동 가능성
```

이 값들은 모두 `0–1 simulation unit`이다. 측정된 심리량이 아니며 서로 더해 하나의 인간 점수를 만들지 않는다.

## Persistent human state로 재입력하지 않는 것

`PhenomenalActivation`과 후보 분포는 현재 tick의 readout이다. `TickTrace`에는 감사용으로 보존되지만 다음 HumanState의 지속 필드나 외부 증거로 자동 재입력되지 않는다.

```text
PhenomenalActivation
≠ 실제 퀄리아의 존재 증명
≠ EvidenceArtifact
≠ 기억 원본

CandidateSet
≠ 의도
≠ 판단
≠ 통시적 자아
```

`Ghost`와 `Editor`는 v0.1에서 독립 실체로 구현하지 않는다. Ghost는 현재 조립된 후보 활성의 해석 이름이고, Editor는 deliberation·selection 연산의 해석 이름으로만 남는다.
