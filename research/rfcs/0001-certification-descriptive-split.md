# RFC 0001 — Contract, Descriptive Dynamics, Protocol Split

| 항목 | 값 |
|---|---|
| Status | `ACCEPTED` |
| Target | Dynamics v0.1.1 |
| Kind | Semantic boundary correction |
| New human behavior | 없음 |
| Prerequisite | v0.1 baseline freeze — `SATISFIED` |
| Implementation | `CORE IMPORT BOUNDARY IMPLEMENTED`; legacy queue→Access bridge `OPEN` |

## 제안

현재 v0.1의 의미적 trace를 보존하면서 세 연구층을 분리한다.

```text
Contract Layer
├─ Certification
├─ Provenance / Integrity
├─ Transition Lineage
└─ Accounting

Descriptive Dynamics
Experimental Protocol
```

이 RFC는 도덕적 이상 모델을 도입하지 않는다. 어떤 typed record가 무엇을
성립시킬 수 있는지와, 사람이 실제로 믿게 된 내용을 그 인증에서 어떻게
분리할지를 명확히 한다.

## 명칭 교정

```text
EpistemicState → EvidenceAssessmentState
```

`WarrantState`는 reliability, defeater, measurement/temporal validity,
revalidation이 정의될 때까지 사용하지 않는다.

```text
BodyAuthorization → MotorFeasibility
```

writer와 소비 경로를 감사한 결과, 이 기록은 허가가 아니라 가용 capacity와
요구 capacity의 비교를 보존하므로 `MotorFeasibility`로 확정했다. 기존 두 이름은
한 compatibility window 동안 exact import alias와 read property로만 남는다.

## 계약 경계

```text
Candidate ≠ Intent ≠ Attempt ≠ Performance
Performance ≠ ActionOccurrence ≠ WorldOutcome
SubjectiveBelief ≠ EvidenceAssessment
```

- Certification은 관할별 typed record와 writer를 요구한다.
- Provenance는 scope, source, ID, payload, 독립성을 보존한다.
- 동일 ID와 다른 payload는 hard collision이다.
- Lineage는 state delta의 event와 writer를 추적한다.
- Accounting은 ingress를 processed/dropped/unresolved로 닫는다.

하나의 보편적 `CertificationRecord`로 관할을 합치지 않는다.

## 층별 책임

### Descriptive Dynamics

human reducer, routing, persistent-state update를 담당한다. 미래에는 비합리적인
belief update도 표현하지만 `SubjectiveBeliefState` 구현은 v0.3으로 미룬다.

### Experimental Protocol

scenario, event queue, canonical time, seed, intervention, hidden oracle,
measurement를 담당한다. Protocol은 HumanState를 직접 mutate하지 않으며 숨은
oracle을 모델 입력으로 주입하지 않는다.

### Engine

세 층을 조립하지만 계약을 우회하는 writer가 되지 않는다.

## 의존 방향

```text
Contract ↛ Dynamics 또는 Protocol에 의존
Dynamics ↛ Protocol queue를 직접 조회
Protocol ↛ HumanState를 직접 mutate
Protocol oracle ↛ engine model input
```

import boundary tests로 위 방향을 잠근다.

## 비목표

- 새 심리 변수·행동·계수
- `SubjectiveBeliefState` 또는 `WarrantState`
- temporal flow/jump
- `WorldOutcome`
- 인간 경험적 설명력 주장

## Migration

1. **완료:** baseline commit, 환경, seed, tests, golden trace를 고정한다.
2. **완료:** 기존 타입과 writer 역할을 감사한다.
3. **완료:** 이름과 모듈을 이동하고 import boundary tests를 추가한다.
4. **완료:** 동일 입력·seed로 semantic golden trace를 비교한다.
5. **완료:** spec과 README의 용어를 동기화한다.

비교 대상은 클래스 경로가 아니라 Evidence digest, Claim transition,
decision-window Routed candidate, Intent/Attempt/Performance, ActionOccurrence, persistent trajectory,
입력 회계다.

## 승인·종료 조건

RFC 승인은 구현 완료를 뜻하지 않는다. v0.1.1 종료에는 다음이 필요하다.

1. baseline freeze가 완료됨
2. import boundary tests 통과
3. golden trace의 허용·금지 차이가 명시됨
4. 새 인간 동역학 없이 의미적 결과가 보존됨
5. `WarrantState`나 경험적 정확도를 암시하지 않음

## 구현 판정

- `contract/`는 model·protocol·legacy facade를 import하지 않는다.
- `models/`는 protocol queue나 legacy facade를 import하지 않는다.
- `protocol/`은 HumanState를 import하거나 직접 mutate하지 않는다.
- engine은 세 canonical package를 조립하고, `types.py`, `epistemics.py`,
  `routing.py`, `invariants.py`는 v0.1 compatibility façade로만 남는다.
- v0.1 semantic golden은 exact match를 유지한다.
- accepted trace의 semantic projection은 보존된다. 새 provenance·mutation
  validator가 invalid trace에 추가 오류를 보고하는 것은 허용된 contract 강화다.
- `legacy_v01_access_pressure_bridge`는 protocol queue normalization이 descriptive
  state를 바꾸는 기존 confound를 명명해 격리하지만 해결하지는 않는다.

남은 결정은 compatibility alias 제거 버전과 queue pressure를 실제 model-facing
access demand로 대체하는 방식이다. alias는 별도 deprecation RFC 없이 v0.1
계열에서 제거하지 않는다.

Compatibility는 구형 import, constructor keyword, read property를 대상으로 하는
source-level 범위다. dataclass field identity를 유지하지 않으므로 구형 이름을 쓴
`dataclasses.replace`, `asdict`, `repr`, class `__name__`·`__module__`까지 동일하다고
주장하지 않는다.
