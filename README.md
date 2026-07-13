# Human Model

인간이 경험하고, 사실을 받아들이고, 기억하고, 판단하고, 변화하면서도 자신으로 이어지는 과정을 모델링하려는 연구 기록이다.

이 저장소의 문서들은 완성된 단일 이론을 선언하지 않는다. 2026년 1월에 전개된 초기 문서들을 시간순으로 복원하고, 각 단계에서 생겨난 개념을 다음 네 범주로 다시 판정한다.

- 현재도 유지할 수 있는 구조
- 후기 이론으로 이어진 계보
- 강하게 주장되었지만 근거가 부족했던 부분
- 아직 검증이 필요한 열린 문제

## Research program

이 저장소는 역사 복원, 채택된 연구 방향, 구현된 계약, 실행 결과와 인간 경험적 근거를 같은 권위로 취급하지 않는다.

```text
Assessment ≠ Adoption ≠ Implementation ≠ Run ≠ Human-Empirical Evidence
```

- [연구의 현재 정체성과 주장 범위](research/README.md)
- [Contract / Descriptive Dynamics / Experimental Protocol 경계](research/architecture.md)
- [단계별 연구 로드맵](research/roadmap.md)
- [Claim registry](research/claims/README.md)
- [Defect–Principle Abduction Corpus](research/defects/README.md)
- [비정본 assessment 기록](assessments/2026-07-13-research-program-plan-assessment.md)

## Volume I

현재 범위는 인간 모델의 내부 구조다.

```text
생성의 자유
→ 사실과 권한의 문턱
→ 사건·증언·책임
→ 기억과 접근
→ 자아와 연속성
→ 유지와 재조정
→ 권위 없는 경험의 영향
```

| 장 | 제목 | 문서 |
|---:|---|---|
| 01 | 틀릴 자유와 사실의 문턱 | [읽기](chapters/chapter-01-ionstar-origin-0101-0103.md) |
| 02 | 사건은 아직 현실이 아니다 | [읽기](chapters/chapter-02-event-irreversibility-0104-0111.md) |
| 03 | 읽히지만 쓰지 못하는 것들 | [읽기](chapters/chapter-03-readout-authority-0111-0115.md) |
| 04 | 다음 박자에만 닿는 것들 | [읽기](chapters/chapter-04-next-tick-influence-0115-0117.md) |
| 05 | 문서는 아직 런타임이 아니다 | [읽기](chapters/chapter-05-document-runtime-factory-0117.md) |
| 06 | 증언과 빚의 탄생 | [읽기](chapters/chapter-06-witness-grounds-billing-0118.md) |
| 07 | 안개 속의 편성자 | [읽기](chapters/chapter-07-fog-reporter-compressed-self-0119.md) |
| 08 | 저장된 과거는 아직 ‘나’가 아니다 | [읽기](chapters/chapter-08-access-rehydration-continuity-0120.md) |
| 09 | 나를 계속 켜 두는 비용 | [읽기](chapters/chapter-09-runtime-self-continuity-tax-0121.md) |
| 10 | 잠을 필연으로 만들려 한 이론 | [읽기](chapters/chapter-10-maintenance-sleep-overreach-0121-0122.md) |
| 11 | 권위 없이 나를 바꾸는 것 | [읽기](chapters/chapter-11-authorityless-influence-qualia-routing-0122.md) |

## 보조 문서

### Interchapter notes

- [자기 경계와 가역적 자아](notes/interchapter-note-03a-self-boundary-ghost-editor-episode.md)
- [흐름을 견디는 경계](notes/interchapter-note-04a-flow-boundary-decision-checkpoint.md)
- [퀄리아는 변형 가능한 생존 매질이다](notes/interchapter-note-08a-qualia-morphic-medium.md)

이 문서들은 장 사이에서 생긴 강한 가설과 통합 시도를 보존한다. 본편의 최종 판정과 일치하지 않을 수 있다.

### Checkpoints

- [최신 TAD로 다시 본 Chapter 01–05](checkpoints/checkpoint-05a-current-tad-analysis.md)

Checkpoint는 당시의 현행 이론과 복원된 초기 문서를 대조한 중간 감사 기록이다.

## 읽는 법

각 장은 대체로 다음 순서를 따른다.

1. 당시 문서가 해결하려 했던 문제를 복원한다.
2. 개념과 수식의 실제 계보를 추적한다.
3. 내부 논리와 외부 연구를 분리해 감사한다.
4. `Recovered / Lineage / Residue / Bridge / Open`으로 현재 위치를 판정한다.

원문의 목소리와 실패한 시도 역시 연구사의 일부로 보존했다. 따라서 문서 안의 역사적 주장과 현재 채택된 주장을 구분해서 읽어야 한다.

## 상태

**Research draft — Volume I boundary.**

Chapter 01–11은 인간 내부 모델의 첫 번째 정리 경계다. 생명·복제·죽음, 집단·게임·문명, 우주적 일반화는 이 저장소의 현재 범위에 포함하지 않았다.

## Dynamics v0.2 — temporal provenance and read-only measurement

Chapter 01–11의 분리 원칙을 실행 가능한 가설로 시험하는 최소 동역학 모델은 [dynamics/](dynamics/README.md)에 있다.

현재 모델은 경험적으로 보정된 인간 예측기가 아니다. 관측·증거·후보·의도·시도·수행과, 수행된 행동의 세계 진입인 `ActionOccurrence`까지만 다른 타입으로 구현했다. 실제 `WorldOutcome`은 아직 구현하지 않았다. 시나리오 및 다축 부하 아래에서 권한 누수와 경로 의존성을 검사하는 simulation contract다.

리팩터링 전 v0.1의 의미적 실행은 [canonical baseline](dynamics/reports/baseline-v0.1.md)으로 동결했다. v0.1.1은 그 trace를 바꾸지 않고 Certification Contract,
Descriptive Dynamics, Experimental Protocol의 package 경계와 용어를 교정했다.
단, 기존 queue pressure→AccessState 결합은 의미 보존을 위해 명명된 legacy
bridge로 남겼으며 완전한 semantic decoupling으로 보지 않는다.

v0.2의 첫 slice는 `occurred_at / available_at / processed_at`과
`occurrence_id / delivery_id`를 분리하고, backlog·transport redelivery·현재
reexposure의 provenance를 실행 가능한 계약으로 만들었다. [Temporal Envelope
Contract](dynamics/spec/temporal.md)에 구현 범위가 있다. `FlowUpdate/EventJump`,
무입력 회복·감쇠와 burst/spaced 비교는 아직 구현되지 않았다.

그 위의 `Q-v1`은 처리된 occurrence마다 literal persistent state delta를 측정해
immutable qualification receipt와 qualified transition subset을 post-run에 만든다.
count, canonical duration, density는 별도 타입이며 base run에 되먹임되지 않는다.
[Mental Transition Measurement Contract](dynamics/spec/mental-transitions.md)에 정확한
scope와 threshold가 있다. 이 구현은 정신 시간의 자연 단위, transition density의
인간 예측력, `MorphicLoadProfile` 또는 퀄리아를 검증한 것이 아니다.

그다음 `MORPH-001A`는 current reducer가 각 write에서 계산한 clamp 전 proposal과
실제 committed target을 occurrence별 immutable receipt로 분리한다. 이는
[Reducer Proposal Instrumentation Contract](dynamics/spec/reducer-proposals.md)에
고정한 simulation proxy이며, 독립적으로 식별된 `DeformationDemand`, 인간의
`AccommodationEnvelope`, `MorphicLoad` 또는 정신 시간량은 아니다.
`MORPH-001B`는 이 proposal을 명시적으로 선택한 비대칭 simulation band와 비교해
ordered proxy-excess profile을 만드는 opt-in post-run projection을 추가했다.
[Envelope Comparison Contract](dynamics/spec/reducer-envelope-comparisons.md)에 고정된
band는 실험자가 선언한 fixture이며 인간의 수용 능력 측정값이 아니다. 출력 역시
`ExcessDemand`, `ResidualStrain`, `MorphicLoad`, 퀄리아 또는 정신 시간량이 아니다.

그 뒤의 outcome/load 작업은 `INTERP-001A` 앞에서 보류했다. 현재 새 연구 조각은
외부 occurrence, current access, experimenter-defined subjective encounter proxy,
Episode candidate, interpretive adjudication과 target-form readout을 서로 다른 후보
경계로 문서화한다. [RFC 0004](research/rfcs/0004-subjective-encounter-interpretive-reorganization.md)와
[INTERP-001 benchmark](research/benchmarks/interp-001-subjective-encounter-binding.md)에
더해 `INTERP-001A2`가 reception access/coherence M1 contract를 고정했고,
[`INTERP-001B`](research/benchmarks/interp-001b-m1-conformance.md)가 64-cell/88-step
detached run과 독립 conformance evaluation을 구현했다. 이어
[`INTERP-001D1`](research/benchmarks/interp-001d1-target-form-ghost-ablation.md)은
TargetForm source compiler, supplied Reception/TargetForm formation과 exact-access Ghost
path를 분리한 3-block/88-cell contract를 동결했다. D1은 아직 실행되지 않았고 durable
TargetForm·feedback·Narrative writer를 만들지 않는다. 이는 새 runtime behavior,
실제 퀄리아·기분 측정 또는 인간 경험적 지지를 구현하지 않는다.
