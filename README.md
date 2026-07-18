# Human Model

인간이 경험하고, 사실을 받아들이고, 기억하고, 판단하고, 행동하며, 그 결과를 다시 자기 변화로 받아들이는 과정을 모델링하려는 연구 기록이다.

이 저장소는 완성된 단일 이론을 선언하지 않는다. 역사 복원, 현재 합성, 구현된 계약, 실행 결과와 인간 경험적 근거를 서로 다른 권위로 관리한다.

```text
Assessment ≠ Adoption ≠ Implementation ≠ Run ≠ Evaluation ≠ Human-Empirical Evidence
```

## Current research direction

현재 연구는 사람을 하나의 결정적 상태-출력 함수보다 다음과 같은 경로분포 시스템으로 본다.

```text
history and current occurrence
+ multiple-timescale state
+ settlement history
+ capacity and context
+ self/other models
→ constrained interpretation and action distributions
→ realized episode trajectory
→ self/social feedback
→ slow narrative and transition change
```

한 시점의 그럴듯한 내부 상태나 정확한 JSON trace가 아니라, 가능한 episode 경로의 분포와 그 분포를 장기적으로 조직하는 구조가 주된 adequacy 대상이다.

- [연구의 현재 정체성과 주장 범위](research/README.md)
- [Volume 0 minimal lineage audit](research/volume-0/README.md)
- [Multi-Clock Distributional Human Dynamics](research/syntheses/2026-07-18-multi-clock-distributional-human-dynamics.md)
- [Distributional-adequacy mainline 채택 기록](research/adoption-records/2026-07-18-distributional-adequacy-mainline.md)
- [HUMAN-DYN-ADEQ-S0 preregistration](research/benchmarks/human-dyn-adequacy-s0.md)
- [Research Architecture](research/architecture.md)
- [Research Roadmap](research/roadmap.md)
- [Claim registry](research/claims/README.md)
- [Defect–Principle Abduction Corpus](research/defects/README.md)

## Strongest invariant

```text
Local causal influence
≠ cross-domain certification authority
```

느낌, 기억, Narrative와 자기해석은 이후의 접근과 행동을 바꿀 수 있다. 그 영향만으로 과거 occurrence receipt, 외부 사실, 타인의 동의나 공적 권한을 다시 쓸 수는 없다.

현재 합성은 다음 정산도 분리한다.

```text
registered occurrence receipt
≠ action realization
≠ authorship settlement
≠ narrative adoption
≠ interpersonal or normative settlement
```

## Program status

| Artifact or lane | Status |
|---|---|
| Dynamics v0.1–v0.2 | executable historical baseline and partial typed dynamics |
| `INTERP-001D1` | executed/evaluated detached synthetic conformance |
| `INTERP-001D2a0` | frozen/unexecuted reference harness |
| `INTERP-001D2a0-EXEC0` | frozen/unexecuted reference harness |
| PR #21 `MAT0` | closed as superseded; branch preserved as a non-mainline representation-specific reference proposal |
| Volume 0 minimal audit | source-bound first slice; broader reconstruction remains open |
| `HUMAN-DYN-ADEQ-S0` | structural/predictive protocol preregistered; models and run unimplemented |
| P0-v1 elicitation instrument | frozen/unexecuted development infrastructure |
| human predictive adequacy | open |

Reference harnesses preserve useful authority, ordering and isolation tests. Their exact record layout or byte serialization is not the unique ontology of the Human Model.

The immediate order is:

```text
S0 public preregistration
→ B0/B1/B2/H implementation and model freeze
→ evaluator-side hidden source-instance freeze
→ S0 execution and evaluation
→ representation retention, revision or retirement
```

Another materialization-only contract or additional Volume 0 chapter does not substitute for S0 execution.

## S0 authority boundary

S0 has two lanes.

```text
S0-A structural distributional adequacy
S0-B non-human source-conditional predictive adequacy
```

S0-A does not establish predictive fit. S0-B uses an evaluator-held synthetic hidden process and does not provide human-empirical support.

## Volume 0

The first Volume 0 slice binds the user-provided December persona-engine archive by archive/member SHA-256 and recovers one lineage in detail:

```text
proposal / output / derived framing
≠ evidence
≠ commitment
≠ state writer
```

- [Volume 0 index](research/volume-0/README.md)
- [Minimal source manifest](research/volume-0/source-manifest.json)
- [Invariant lineage matrix](research/volume-0/invariant-lineage-matrix.md)
- [Chapter 00-A — 출력은 아직 상태변경이 아니다](research/volume-0/chapter-00-a-output-is-not-state-change.md)

This is a partial source audit, not a complete December canon and not human-empirical support.

## Volume I

현재 공개 Chapter 01–11은 2026년 1월 이론 계보의 첫 정리 경계다. Volume 0은 2025년 12월 persona-engine corpus를 복원하고 Chapter 01을 절대적 기원 대신 0101 재컴파일 경계로 재배치한다.

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

### Interchapter notes

- [자기 경계와 가역적 자아](notes/interchapter-note-03a-self-boundary-ghost-editor-episode.md)
- [흐름을 견디는 경계](notes/interchapter-note-04a-flow-boundary-decision-checkpoint.md)
- [퀄리아는 변형 가능한 생존 매질이다](notes/interchapter-note-08a-qualia-morphic-medium.md)

### Checkpoints

- [최신 TAD로 다시 본 Chapter 01–05](checkpoints/checkpoint-05a-current-tad-analysis.md)

## Reading and evidence labels

역사 문서와 현재 합성을 구분하기 위해 다음 라벨을 사용한다.

```text
RECOVERED
STRUCTURAL_PRECURSOR
CURRENT_SYNTHESIS
OPEN_HYPOTHESIS
METAPHOR
```

구조 테스트 통과, synthetic source 예측, 결정적 재생성과 그럴듯한 출력은 인간에 대한 경험적 증거가 아니다. 현재 모델은 경험적으로 보정된 인간 예측기가 아니며, 실제 human/model acquisition과 분포적 예측 비교는 아직 열려 있다.
