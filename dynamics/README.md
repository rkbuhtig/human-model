# Human Model Dynamics v0.1

Chapter 01–11의 권한 척추와 분리 원칙을 보존하면서, 인간 내부 상태에 관한 `BRIDGE`를 실행 가능한 가설로 명시해 시험한다.

이 패키지는 실제 인간의 감정값이나 행동을 예측하도록 보정되지 않았다. 퀄리아의 존재를 증명하지도 않는다. 현재 검증 대상은 다음 세 가지다.

```text
개념 간 전이가 타입을 보존하는가
부하 아래에서도 권한 경계가 유지되는가
경로 의존적 변화와 비리셋 회복을 표현할 수 있는가
```

이 구현의 연구 지위와 후속 범위는 다음 문서에서 관리한다.

- [Human Model Research Program](../research/README.md)
- [Research Architecture](../research/architecture.md)
- [Research Roadmap](../research/roadmap.md)

## 핵심 분리

```text
숨은 세계 정답
≠ 인간에게 도달한 관측

후보 salience
≠ evidence strength

Candidate
≠ Intent
≠ Attempt
≠ PerformedAction
≠ ActionOccurrence
≠ WorldOutcome
≠ ObservedOutcome
```

시나리오의 `hidden_worlds`는 테스트 오라클만 보유한다. `DynamicsEngine.run()`은 `HumanState`와 관측 가능한 `ScenarioEvent`만 받으므로 숨은 상대 의도나 실제 원인을 읽을 수 없다. 테스트는 두 세계가 같은 관측열을 내는 구간과 서로 다른 관측이 나타난 이후를 별도 실행한다.

## 구조

```text
dynamics/
├─ spec/                 상태·전이·불변식 계약
├─ scenarios/            versioned JSON 시나리오
├─ tests/                HARD·counterfactual·stress 테스트
├─ types.py              residence별 타입
├─ epistemics.py         EvidenceLink와 claim별 판단
├─ routing.py            비권위적 후보 재가중
├─ engine.py             이벤트 스케줄러와 전이 엔진
├─ scenario.py           JSON 로더와 기준 실행 CLI
└─ stress.py             다축 부하 생성기와 soak 측정
```

외부 패키지는 사용하지 않는다. Python 3.11 이상이면 실행할 수 있다.

### Evidence signal schema

외부 `supports / contradicts` 항목에는 `rule_id`가 필수다.

```json
{
  "claim_id": "C1_platform_displayed_online",
  "strength": 0.88,
  "rule_id": "observe-platform-online",
  "scope": "scenario"
}
```

`epistemics.GROUNDING_RULES`는 다음 조합을 allowlist로 검사한다.

```text
event kind
× claim
× support/contradiction relation
× provenance kind
× maximum strength
```

시나리오가 `supports`라고 선언했다는 이유만으로 임의 관측을 임의 claim에 연결할 수 없다. claim 집계 키는 `(claim_id, scope)`다.

## 기준 시나리오

```bash
python -m dynamics.scenario dynamics/scenarios/delayed_reply.json
```

`delayed_reply`는 다음 claim을 분리한다.

```text
답장이 관찰되지 않음
플랫폼이 온라인 상태를 표시함
상대가 의도적으로 피함
관계 자체를 거절함
친구가 “피하는 것 같다”고 말함
상대가 바빴다고 설명함
일정 충돌이 실제로 존재했음
바쁨이 실제 원인이었음
```

앞선 두 관측이나 친구의 추측이 상대의 의도·관계 거절을 자동 확정하지 못한다. 내부 거절 시뮬레이션은 routing과 느린 상태에 영향을 줄 수 있지만 EvidenceLink를 만들지 못한다.

## 테스트

```bash
python -m unittest discover -s dynamics/tests -v
```

테스트는 정확한 감정값 대신 다음 관계를 확인한다.

- 숨은 세계가 달라도 관측열이 같으면 궤적이 같다.
- Stake와 과거 접근 경사는 routing을 바꿀 수 있지만 evidence digest는 바꾸지 않는다.
- 같은 `independence_key`로 선언된 반복은 독립 근거로 누적되지 않는다.
- 행동 채널만 막으면 prior route는 같고 PerformanceReceipt와 downstream ActionOccurrence가 사라진다.
- 반증·설명은 기존 증거와 행동 역사를 삭제하지 않는다.
- 중복 `event_id`는 한 번만 적용된다.
- 같은 ID의 다른 payload는 duplicate가 아니라 HARD collision이다.
- 입력 손실은 `processed / dropped / unresolved`로 회계된다.

### Canonical semantic baseline

원격 revision `9b731b7f92700227de1fae8adc79e1d8e687d25f`의 `delayed_reply` 의미적 실행을 [baseline-v0.1](reports/baseline-v0.1.md)으로 동결했다.

```bash
python -m dynamics.baseline
python -m unittest dynamics.tests.test_baseline -v
```

이 baseline은 클래스명·모듈 경로·성능값이 아니라 Evidence digest, claim 전이, routing, 행동 계보, 느린 상태 궤적과 입력 회계를 비교한다. 인간 예측 정확도의 기준선은 아니다.

## 부하 실행

```bash
python -m dynamics.stress --preset all --seed 20260712
python -m dynamics.stress --preset soak --seed 20260712
```

부하는 하나의 점수가 아니다.

```text
InputRate
CandidateFanout
Ambiguity
EvidenceConflict
RelationalStake
BodyLoad
MemoryInterference
TimePressure
Adversariality
Duration
```

보고서는 의미적 안전성과 계산 성능을 분리한다.

- `hard_pass`: authority leak, phantom action, provenance loss, 수치·회계 오류가 없음
- `recovery_status`: 회복 자극 도달 여부와 비리셋 이완을 별도 판정
- `processed_events_per_second`, `peak_memory_mib`: 사건 생성 비용을 제외한 engine-only 성능 측정

성능 수치는 인간 이론의 경험적 근거가 아니다.

현재 `authority_leaks`는 구현된 내부 인식 권한 경계의 위반을 센다. 여기에는 EvidenceLink 없는 factual stance 채택뿐 아니라 등록되지 않은 grounding rule, 잘못된 ground 집합·강도·scope 같은 위반도 포함된다. 외부 `Warrant / AuthorityGrant / AppliedRecord` 전이는 아직 구현하지 않았으므로, 값이 0이라고 전체 권한 체계가 검증된 것은 아니다.

첫 실행 결과와 발견된 실패는 [reports/stress-v0.1.md](reports/stress-v0.1.md)에 기록했다.
