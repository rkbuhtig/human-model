# Human Model Research Program

## 정체성

Human Model은 불완전한 관측과 여러 시간척도 아래에서 인간의 경로 의존적
변화를 연구한다. 한 상태의 국소적 인과 영향이 다른 관할의 사실·의도·수행·
세계 사건을 성립시킬 권한으로 자동 승격되지 않도록 구분하고, 실제 인간에서
그 경계가 어떻게 무너지는지도 모델링하려는 typed hybrid dynamics 연구
프로그램이다.

```text
Local causal influence
≠ cross-domain certification authority
```

이 원리는 상태 간 영향을 금지하지 않는다. 느낌은 믿음을, 기억은 접근성을,
몸은 수행 가능성을 바꿀 수 있다. 그 영향만으로 타 관할을 인증하지 못한다는
뜻이다.

## 현재 상태

현재 Dynamics는 v0.1.1의 구조적 구분과 동역학적 반례에 v0.2 temporal provenance
slice, read-only mental-transition measurement, `MORPH-001A` reducer-proposal
instrumentation과 opt-in `MORPH-001B` proposal/declared-band proxy comparison을 추가한 최소 모델이다.
`Q-v1`은 processed occurrence마다 literal persistent field delta를 측정해 immutable
receipt와 count/density report를 파생한다. proposal ledger는 각 occurrence의 flat
ordered pre-clamp proposal/commit tuple을 별도 receipt로 보존한다. 어느 쪽도 인간의
정신 시간·DeformationDemand·MorphicLoad를 식별하지 않았다. `MORPH-001B`의 band도
인간 능력의 측정값이 아니라 명시적으로 선택한 synthetic simulation parameter다.
인간에 대한 경험적 예측 정확도도 아직 검증되지 않았다.

| 근거 층 | 지위 |
|---|---|
| Historical / engineering | `PARTIAL` |
| Executable / structural | `PARTIAL` |
| Human-empirical | `OPEN` |

구조 테스트 통과나 그럴듯한 출력은 인간에 대한 경험적 증거가 아니다.

## 문서 권위

```text
assessment
→ adoption record / RFC
→ implementation
→ versioned execution report
→ empirical evaluation
```

각 화살표는 자동 승격이 아니라 별도 판정 문턱이다.

- [`assessments/`](../assessments/): 외부 비동료평가·비정본 자료
- [`adoption-records/`](adoption-records/): `Adopt / Revise / Hold` 판정
- [`architecture.md`](architecture.md): 연구층과 의존 경계
- [`roadmap.md`](roadmap.md): 단계별 범위와 종료 조건
- [`rfcs/`](rfcs/): 구현 전 제안
- [`claims/`](claims/): claim의 종류·범위·근거·실패 조건
- [`defects/`](defects/): 당시 기록과 현재 해석을 분리한 결함 corpus
- [`benchmarks/`](benchmarks/): 계약 mutation, 구조 ablation, 시간 비교 계획
- [`scenarios/`](scenarios/): 현실 영역의 저자 생성 가상 scenario와 기능 관할 contrast 계약

## 목표 아키텍처

```text
Contract Layer
├─ Certification Contract
├─ Provenance / Integrity Contract
├─ Transition Lineage Contract
└─ Accounting Contract

Descriptive Dynamics
Experimental Protocol
```

v0.1 baseline은 [원격 source revision과 semantic golden](../dynamics/reports/baseline-v0.1.md)으로 동결했다. v0.1.1 package 경계는 구현되었고, 기존 queue→Access
결합은 명명된 legacy bridge로 남아 있다. v0.2 temporal provenance와 read-only
mental-transition type/measurement surface는 구현되었다. 그 위에
[`MORPH-001A`](benchmarks/morph-001-demand-commit.md)가 pre-constraint reducer
proposal과 committed target을 분리하는 instrumentation을 구현했다. 이 proposal은
independently identified `DeformationDemand`가 아니다. 이어
[`MORPH-001B`](benchmarks/morph-001b-proposal-envelope-comparison.md)는 proposal을
실험자가 선언한 asymmetric reducer-write band와 비교하는 read-only surface를
구현했다. 이는 measured human `AccommodationEnvelope`나 `MorphicLoad`가 아니다.
`MORPH-001C` outcome/load comparison은 해석·회복 outcome을 성급히 선형화하지 않도록
`DEFERRED`한다. 먼저 [`INTERP-001`](benchmarks/interp-001-subjective-encounter-binding.md)이
subjective encounter, current access, Episode candidate, interpretive adjudication과
object-scoped target-form readout의 타입·시간·권한 경계를 문서화한다.
`INTERP-001A2`는 reception→access와 reception→candidate-coherence를 다루는 첫 M1
execution/evaluation contract를 동결했고, [`INTERP-001B`](benchmarks/interp-001b-m1-conformance.md)가
manifest에 고정된 assembly/adjudication phase까지 포함해 detached conformance를
실행했다. [`INTERP-001D1`](benchmarks/interp-001d1-target-form-ghost-ablation.md)은
outcome-blind `TF0–TF2` source compiler, supplied TargetForm/Reception formation
intervention과 exact-access Ghost path를 서로 다른 세 block으로 분리한 88-cell
execution/evaluation contract로 동결했고,
[`D1 conformance run`](benchmarks/interp-001d1-v1-conformance.md)이 88/88 signature와
91/91 non-retirement assertion을 통과했다. 상태는
`EXECUTED / EVALUATED SYNTHETIC CONFORMANCE`다. source compiler 성공, supplied-input
sensitivity와 Ghost-path distinction은 서로 다른 격리 판정이며 block 사이에 output을
전달하는 end-to-end pipeline이 아니다. development/sealed도 evaluator-only synthetic
분리이지 예측 partition이 아니다. durable TargetForm writer, later-access feedback, 전체
EF manifest와 Dynamics runtime behavior는 여전히 `OPEN`이다. residual·load와
INTERP/MORPH 접합은 detached lab 판별 뒤에 남아 있다.
`FlowUpdate/EventJump`·no-event flow·burst/spaced와
`HM-DYN-001` predictive comparison은 독립적인 planned temporal-comparison 축이며
`MORPH-001`의 선행 blocker가 아니다. `affect → SubjectiveBelief`는 독립 v0.3 축이고,
`WarrantState`, 독립 주관 시계, 퀄리아–부하 대응식, 다른 기억 오귀속은 `HOLD`다.

D1과 recursive D2 사이에는
[`INTERP-DIALOGUE-001A`](adoption-records/2026-07-13-functional-jurisdiction-scenarios.md)
기능 관할 gate를 둔다. 관찰·보고된 현상군을 기능 residence의 정답으로 취급하지 않고,
관계·업무·위험이라는 현실 영역의 저자 생성 가상 scenario에서 한 declared factor만
바꾸는 contrast를 등록한다. factor별 contract는 조작 source lane, public-record effect,
고정 factor, `registered_candidate_probe_domains`, must-remain-equal 항목과 열린
discriminator를 구분한다. 후보 domain은 비배타적 관측 목록이므로 목록 밖 효과는 fixture
위반이 아니라 현재 기능 분해의 scope failure 또는 열린 결과다.

[`INTERP-DIALOGUE-001B`](adoption-records/2026-07-13-functional-jurisdiction-trace-oracle.md)는
23개 exact trace field, prefix/initial/one-future ordinal horizon, 9개 factor별 38개 competing placement hypothesis,
동일 future option 비교, REL initial×later mood 2×2와 명시적 out-of-model lane을 결과 전에
동결했다. 이 oracle은 mental ground truth가 아니라 hypothesis-conditional conformance
contract다. natural contrast는 association signature만 주며 direct edge는 D2a-only
node clamp로 남는다. observed equality는 alias가 아니고, durable state와 slow cache는
현재 one-future-access horizon에서 `NOT_IDENTIFIABLE_UNDER_HORIZON`이다. 단순 challenger는 표현력 순위표가
아니라 alias·degeneracy control이다.

후속 [`INTERP-DIALOGUE-001P0-v0`](scenarios/interp-dialogue-001/elicitation/README.md)는
[`development elicitation adoption`](adoption-records/2026-07-13-development-elicitation-instrument.md)에
따라 24개 presentation, generic immediate/later prompt, matched future option과 scripted
replay provenance를 동결했다. observation coordinate와 prompt/response schedule을 분리하며,
current runner는 `SCRIPTED_ADVERSARIAL_RESPONSE`만 replay record로 materialize한다. 그
record는 실제 delivery/response occurrence가 아니며 mapping·`OUT_OF_MODEL`·defect·placement를
발행하지 않는다. author walkthrough와 language inspection은 evaluator-side source다. 상태는
`FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY`다. 이후 순서는 P1-v0 immutable
scripted replay와 defect/revision proposal → 별도 P0-v1 revision decision/freeze →
source-specific acquisition·human·latent·D2a protocol 동결 → 독립 실행 → cross-source
audit(C)다. P1은 수정된 instrument를 채택하거나 실행할 수 없다. 현재 freeze는 actual
participant/model occurrence, human support, LLM latent 측정, D2a runtime, durable TargetForm
또는 Narrative writer를 구현하지 않는다.

```text
implemented Q-v1 receipt/count/density types
≠ transition density predicts human trajectories
≠ mental time unit identified
≠ MorphicLoad or qualia measured

ReducerProposal ≠ DeformationDemand ≠ AccommodationEnvelope ≠ MorphicLoad

declared simulation envelope comparison ≠ measured human capacity or load
```

상세 범위는 [roadmap](roadmap.md), 기존 세 RFC와
[RFC 0004](rfcs/0004-subjective-encounter-interpretive-reorganization.md)를 따른다.
