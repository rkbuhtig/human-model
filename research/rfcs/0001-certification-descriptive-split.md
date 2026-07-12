# RFC 0001 — Contract, Descriptive Dynamics, Protocol Split

| 항목 | 값 |
|---|---|
| Status | `PROPOSED` |
| Target | Dynamics v0.1.1 |
| Kind | Semantic boundary correction |
| New human behavior | 없음 |
| Prerequisite | v0.1 baseline freeze — `SATISFIED` |

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
BodyAuthorization
→ MotorFeasibility        # 수행 가능성 상태라면
→ MotorExecutionGate     # 수행 전 gate라면
```

최종 이름은 writer와 소비 경로를 감사한 뒤 고른다.

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
2. 기존 타입과 writer 역할을 감사한다.
3. 이름과 모듈을 이동하고 import boundary tests를 추가한다.
4. 동일 입력·seed로 semantic golden trace를 비교한다.
5. spec과 README의 용어를 동기화한다.

비교 대상은 클래스 경로가 아니라 Evidence digest, Claim transition, Routed
candidate, Intent/Attempt/Performance, ActionOccurrence, persistent trajectory,
입력 회계다.

## 승인·종료 조건

RFC 승인은 구현 완료를 뜻하지 않는다. v0.1.1 종료에는 다음이 필요하다.

1. baseline freeze가 완료됨
2. import boundary tests 통과
3. golden trace의 허용·금지 차이가 명시됨
4. 새 인간 동역학 없이 의미적 결과가 보존됨
5. `WarrantState`나 경험적 정확도를 암시하지 않음

## 열린 결정

- 신체 타입의 최종 이름
- 실제 package 경계와 순환 import 제거 방식
- compatibility alias를 유지할 기간
