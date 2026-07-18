# Human Model Research Roadmap

| 항목 | 지위 |
|---|---|
| 현재 실행 순서 | `ADOPTED — DISTRIBUTIONAL ADEQUACY MAINLINE` |
| 기존 typed-contract 구현 | `PRESERVED REFERENCE LANE` |
| 인간 경험적 검증 | `OPEN` |

상태는 문서 선언이 아니라 commit, frozen input, versioned run, evaluation report와 empirical source로 승격한다.

```text
Assessment ≠ Adoption ≠ Implementation ≠ Run ≠ Evaluation ≠ Human-Empirical Evidence
```

상세한 pre-S0 구현 연대기는 [Historical Roadmap Snapshot — through PR #23](history/roadmap-through-pr23.md)에 보존한다.

## 0. Current program order

2026-07-18 distributional-adequacy adoption이 아래 순서를 현재 mainline으로 채택했다.

| 순서 | 작업 | 상태 | 종료 조건 |
|---:|---|---|---|
| 1 | current synthesis documentation | `DONE` | 연구 정체성과 비주장을 문서화 |
| 2 | Volume 0 minimal lineage audit | `DONE — PARTIAL` | source-bound manifest, matrix, Chapter 00-A |
| 3 | `HUMAN-DYN-ADEQ-S0` exact preregistration | `CURRENT` | structural/predictive lane, source, information budget, scoring freeze |
| 4 | S0 model implementation freeze | `NEXT` | B0/B1/B2/H version과 allowed information 고정 |
| 5 | S0 execution and evaluation | `NEXT` | versioned result/report; model 수정 없이 평가 |
| 6 | representation decision | `OPEN` | retain / revise / retire 명시 |
| 7 | P1-v1 repilot | `REQUIRED BEFORE ACQUISITION` | confirmed instrument defects 재판정 |
| 8 | source-specific human/model acquisition | `OPEN` | 별도 consent, mapping, missingness, source protocol |

```text
current synthesis
→ minimal lineage audit
→ exact S0 preregistration
→ model freeze
→ S0 execution
→ representation decision
```

새로운 materialization-only contract, 추가 Volume 0 chapter 또는 새 HumanState field는 S0 실행을 자동으로 선행하지 않는다.

## 1. What S0 can and cannot establish

S0는 두 lane을 분리한다.

```text
S0-A  Structural Distributional Adequacy
- directional constraints
- intervention selectivity
- mode-collapse / unstructured-randomness detection
- authority and information-boundary checks

S0-B  Source-Conditional Predictive Adequacy
- evaluator-held non-human synthetic trajectory source
- hidden continuation prediction
- B0/B1/B2/H identical observable information
- proper scoring and complexity reporting
```

S0-A 통과는 인간 예측력이 아니다. S0-B의 synthetic source 예측 성공도 인간 경험적 support가 아니다.

## 2. Historical implementation inventory

아래 lane은 삭제되거나 실패작으로 재분류되지 않는다. 현재 adequacy mainline의 reference implementation과 failure corpus다.

### Dynamics v0.1 baseline

**상태: `FROZEN / EXECUTED HISTORICAL BASELINE`**

- source revision과 dependency/seed 고정
- semantic golden trace와 manifest
- Evidence, routing, agency, action occurrence와 slow-state trajectory 포함

정확한 golden trace는 compatibility와 mutation detection을 위한 것이며 인간 ontology가 아니다.

### Dynamics v0.1.1 boundary refactor

**상태: `IMPLEMENTED`**

```text
EpistemicState → EvidenceAssessmentState
BodyAuthorization → MotorFeasibility
Contract / Dynamics / Protocol import separation
```

legacy queue-pressure → AccessState bridge는 여전히 부분적 semantic confound다.

### Dynamics v0.2 temporal provenance

**상태: `FIRST SLICE IMPLEMENTED / BROADER DYNAMICS OPEN`**

```text
occurred_at ≠ available_at ≠ processed_at
occurrence_id ≠ delivery_id
PastOccurrence ≠ CurrentReexposure
FlowUpdate ≠ EventJump                 # broader implementation open
```

현재 구현은 temporal/provenance envelope다. 인간의 독립 정신 시계나 no-event recovery law를 확립하지 않는다.

### Q-v1 transition measurement

**상태: `IMPLEMENTED SIMULATION MEASUREMENT / PREDICTIVE VALUE OPEN`**

post-run receipt와 qualified transition subset을 생성하지만 generating run에 되먹임하지 않는다.

```text
TransitionQualificationReceipt
≠ human mental-time unit
≠ predictive support
```

### MORPH-001A/B

**상태: `IMPLEMENTED SIMULATION INSTRUMENTATION / HUMAN LOAD OPEN`**

- reducer requested write와 committed write 분리
- experimenter-declared envelope와 post-run comparison
- human capacity, phenomenal strain, morphic load로 승격 금지

### INTERP-001 lineage

**상태 요약:**

| Artifact | 지위 |
|---|---|
| `INTERP-001D1` | executed/evaluated detached synthetic conformance |
| `INTERP-001D2a0` | frozen/unexecuted reference harness |
| `INTERP-001D2a0-EXEC0` | frozen/unexecuted reference harness |
| PR #21 `MAT0` | closed unmerged representation-specific proposal |
| P0-v1 instrument | frozen/unexecuted development infrastructure |

이 lane은 authority, future-effective ordering, runner/evaluator isolation과 deterministic replay를 보존한다. exact record rank, source bundle과 canonical bytes는 Human Model의 유일한 존재론이 아니다.

## 3. Superseded immediate order

다음 순서는 2026-07-14 당시에는 채택됐지만, 2026-07-18 adoption에 의해 **immediate mainline으로서는 superseded**됐다.

```text
D2a0-EXEC0
→ D2a1 detached runner/evaluator
→ OBS-MAP-000
→ P1-v1 if warranted
```

이 순서는 `REFERENCE LANE / REACTIVATION REQUIRES NEW ADOPTION`이다. S0 결과가 해당 harness의 재사용 필요성을 보일 때만 다시 연다.

## 4. Architecture and representation decision

S0는 다음 후보를 경쟁시킨다.

```text
R0 object assembly
R1 multi-timescale state
R2 predictive-state compression
R3 source-bound ledgers + state + predictive topology
```

H representation은 다음 중 하나를 보여야 유지된다.

- B2보다 held-out predictive score 개선
- 같은 predictive performance에서 더 작은 predictive state
- intervention selectivity 개선
- long-horizon stability 또는 data efficiency 개선
- output과 독립적인 state probe 성공

그렇지 않으면 vocabulary가 설명적으로 들리더라도 축소하거나 폐기한다.

## 5. Acquisition gate

실제 human/LLM/engine source acquisition은 source별로 분리한다.

```text
synthetic hidden process
≠ persona-engine source
≠ LLM source
≠ open human dataset
≠ new human acquisition
```

P0-v1을 사용하는 actual acquisition 전에는 P1-v1 repilot이 필요하다. Synthetic S0를 P1-v1 완료의 대체물로 사용하지 않는다.

## 6. Volume 0

**상태: `MINIMAL AUDIT DONE / BROADER RECONSTRUCTION OPEN`**

현재 완료된 것은 source manifest, invariant matrix와 Chapter 00-A다. 추가 chapter는 S0 preregistration이 요구하는 역사 구분이 있을 때만 연다.

## 7. Stop rules

다음 중 하나가 발생하면 새 설계층을 추가하지 않고 현재 slice를 실행하거나 중단 판정한다.

```text
- preregistration이 모델별 expected trace를 포함하려 함
- H에 B2가 받지 못하는 observable information을 제공함
- hidden target 없이 predictive superiority를 주장함
- evaluation 결과를 본 뒤 같은 version을 수정함
- source recurrence를 human empirical support로 승격함
- 새 episode family가 S0 실행을 다시 연기함
```

## 8. Explicit holds

- canonical HumanState ontology
- validated human Episode/Narrative attractor
- clinical taxonomy
- causal-state or epsilon-machine identity
- calibrated human capacity metric
- human predictive superiority
- full world model and normative truth oracle
