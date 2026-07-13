# Human Model Dynamics v0.2 — Temporal Provenance + Read-only Measurement

Chapter 01–11의 권한 척추와 분리 원칙을 보존하면서, 인간 내부 상태에 관한 `BRIDGE`를 실행 가능한 가설로 명시해 시험한다.

이 패키지는 실제 인간의 감정값이나 행동을 예측하도록 보정되지 않았다. 퀄리아의
존재를 증명하지도 않는다. v0.1.1의 동역학 위에 v0.2가 시간·사건 provenance와
post-run read-only mental-transition measurement, current-reducer proposal
instrumentation과 opt-in declared-envelope comparison을 추가했다. 현재 검증 대상은
다음 일곱 가지다.

```text
개념 간 전이가 타입을 보존하는가
부하 아래에서도 권한 경계가 유지되는가
경로 의존적 변화와 비리셋 회복을 표현할 수 있는가
사건 발생·전달·처리 시각과 원천 occurrence·delivery가 섞이지 않는가
처리된 occurrence의 변화 receipt와 count/density report가 base run에 되먹임되지 않는가
clamp 전 reducer proposal과 실제 committed target을 순서와 provenance를 잃지 않고 분리하는가
proposal을 명시된 simulation band와 비교하는 read-only profile이 source와 실행을 보존하는가
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
≠ ActionOpportunity
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
├─ contract/             인증·근거·행동 계보 record와 validator
├─ models/               기술적 인간 상태·routing·update 가설
├─ protocol/             사건 encoding과 ingress queue
├─ adapters.py           명시적 cross-layer adapter와 legacy bridge
├─ temporal.py           canonical time과 occurrence/delivery stamp
├─ mental_transitions.py processed-occurrence Q-v1 derived ledger와 report
├─ reducer_proposals.py  ordered pre-clamp reducer proposal derived ledger
├─ reducer_envelope_comparisons.py declared-band proxy comparison ledger
├─ types.py              v0.1 compatibility re-export
├─ epistemics.py         v0.1 compatibility wrapper
├─ routing.py            v0.1 compatibility wrapper
├─ invariants.py         v0.1 compatibility validator wrapper
├─ engine.py             core 실행 + post-run measurement composition root
├─ scenario.py           JSON 로더와 기준 실행 CLI
└─ stress.py             다축 부하 생성기와 soak 측정
```

Canonical 의존 방향은 다음과 같다.

```text
contract  ← models
contract  ← protocol

engine → contract + models + protocol
mental_transitions → completed trace + models + temporal
engine → mental_transitions only after core execution
reducer_proposals → captured reducer trace + models + temporal
engine → reducer_proposals only as a read-only audit surface
reducer_envelope_comparisons → completed reducer_proposal ledger
engine → reducer_envelope_comparisons only when an explicit opt-in policy exists
```

`contract/`는 model·protocol을 import하지 않고, `models/`는 protocol queue를
import하지 않으며, `protocol/`은 HumanState를 직접 mutate하지 않는다. 이 경계는
`test_package_boundaries.py`가 검사한다.

단, v0.1 semantic golden을 보존하기 위해 protocol queue pressure를 descriptive
AccessState에 전달하는 `legacy_v01_access_pressure_bridge`가 남아 있다. 이는
인간 내부 backlog의 존재론이나 정당한 장기 설계가 아니라 v0.1의 알려진
experimental confound다.

v0.1 compatibility façade는 구형 import, constructor keyword, read property를
지원한다. 구형 dataclass field 이름을 사용한 `dataclasses.replace`·`asdict`,
`repr`, class identity까지 보존하는 binary/reflective compatibility는 아니다.
특히 정규화된 legacy event의 `event_id`나 `tick`만 `dataclasses.replace`하면 함께
복사된 temporal envelope와 불일치하므로, canonical envelope도 함께 교체하거나 새
event를 생성해야 한다.

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

`contract.GROUNDING_RULES`는 다음 조합을 allowlist로 검사한다.

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
- 동일 occurrence의 새 delivery는 인간·Evidence update를 반복하지 않는다.
- 과거 `occurred_at`과 현재 `available_at / processed_at`을 함께 보존한다.
- 현재 reexposure는 새 내부 occurrence로 처리하되 원천 Evidence를 복제하지 않는다.
- 처리된 occurrence마다 Q receipt 하나를 남기고 qualified subset만 transition으로 둔다.
- Q policy threshold/scope를 바꿔도 base state·trace·evidence/action record는 바뀌지 않는다.
- transition window의 canonical duration, qualified count, density를 별도 타입으로 둔다.
- reducer write마다 pre-clamp requested target과 bounded committed target을 분리한다.
- 같은 field의 반복 write는 occurrence net delta로 뭉개지 않고 순서대로 연결한다.
- 포화로 committed delta가 0이어도 reducer proposal receipt는 보존할 수 있다.
- 같은 proposal은 declared band에 따라 다른 proxy excess를 만들 수 있다.
- 같은 committed delta와 transition count가 서로 다른 ordered proxy profile을 숨길 수 있다.
- storage clamp gap과 declared simulation band 밖의 proxy excess를 서로 다른 값으로 보존한다.
- envelope policy를 바꿔도 생성 state·trace·Evidence·action·Q·proposal ledger는 같다.
- 입력 손실은 `processed / dropped / unresolved`로 회계된다.

시간·사건 동일성의 정확한 범위와 아직 구현하지 않은 flow는
[Temporal Envelope Contract](spec/temporal.md)에 구분했다.
`Q-v1`의 literal field scope, `0.01 normalized_simulation_unit` threshold,
per-processed-occurrence checkpoint와 read-only 경계는
[Mental Transition Measurement Contract](spec/mental-transitions.md)에 고정했다.
[Reducer Proposal Instrumentation Contract](spec/reducer-proposals.md)는 current reducer의
pre-clamp proxy와 commit을 분리하는 정확한 구현 범위를 고정한다.
[Reducer Proposal Envelope Comparison Contract](spec/reducer-envelope-comparisons.md)는
명시적으로 선택한 simulation band와 ordered proxy comparison의 범위를 고정한다.

이 ledger 구현은 measurement surface의 구조적 재현성만 보인다. transition density의
predictive value(`HM-DYN-001`), 정신 시간의 자연 단위, `MorphicLoadProfile`,
phenomenal bridge는 구현하거나 검증하지 않았다.

`ReducerProposal`도 independently identified `DeformationDemand`가 아니다. 현재
proposal에는 legacy access pressure, phenomenal/evidence coupling, update rate와 action
consequence가 포함될 수 있다. 구현된 `ReducerProposalEnvelopePolicy`는 synthetic
simulation fixture이지 measured human `AccommodationEnvelope`가 아니다. 따라서
`ExcessDemand`, residual, load와 퀄리아 대응은 여전히 미구현이다.

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
