# INTERP-001B — Detached M1 Phase-Complete Conformance Run

| 항목 | 값 |
|---|---|
| Status | `IMPLEMENTED — SYNTHETIC STRUCTURAL CONFORMANCE ONLY` |
| Frozen input | `INTERP-001A2-M1-EXECUTION@1.0.0` |
| Runner | `INTERP-001B-M1-PHASE-COMPLETE-RUNNER@1.0.0` |
| Evaluator | `INTERP-001B-M1-CONFORMANCE-EVALUATOR@1.0.0` |
| Matrix | 16 fixtures × 4 models = 64 isolated cells, 88 protocol steps |
| Runtime integration | 없음 |
| Human empirical status | `NOT TESTED` |

## 이번 실행이 답하는 질문

동결된 M1 contract만 입력받는 detached runner가 R0–R3의 reception-conditioned
access와 candidate-coherence factorization을 expected label 없이 실행하고, 별도
evaluator가 그 결과의 closed-world signature와 negative control을 독립적으로 판정할
수 있는가?

이것은 전체 `INTERP-001` 동역학의 실행이 아니다. M1에서 TargetForm과 Ghost는
neutral/fixed control이고 encounter formation과 topology도 frozen fixture다. 따라서
이번 결과는 다음만 다룬다.

```text
phase-complete M1 execution
= op001 encounter formation
 + op002/op003 access selection
 + op004 assembly
 + op005–op008 candidate/adjudication
 + op009 integration projection
 + op010/op011 ignition projections

phase-complete M1
≠ variable TargetForm
≠ variable Ghost exploration
≠ Narrative dynamics
≠ full human interpretation model
```

## 분리된 실행 경로

runner와 evaluator는 서로 import하지 않는다.

```text
execution manifest bytes
→ runner
→ serialized 64-cell run artifact
→ runner process 종료

execution manifest bytes
+ evaluation manifest bytes
+ result schema bytes
+ run schema bytes
+ evaluator policy bytes
+ raw run artifact bytes
→ 별도 evaluator process
→ conformance report
```

runner는 evaluation manifest, evaluator alias, expected signature와 pass/fail label을
읽을 수 없다. evaluator는 raw cell을 normalization하기 전에 result schema로 검증하고,
frozen fixture와 operator declaration에서 expected projection을 다시 계산한다.

입력 binding, integrity, raw schema 또는 predicate catalog 검사가 실패하면 evaluator는
`FrozenEvaluationInputError`로 fail closed하고 report envelope를 반환하지 않는다.
따라서 versioned conformance report의 status domain은 schema-valid 입력에 대한
`PASS | FAIL`뿐이며 `INVALID_INPUT` placeholder report를 만들지 않는다.

runner/evaluator bundle은 core와 common module뿐 아니라 각 process CLI와 shared
orchestrator까지 포함한다. policy v1이 경로 집합과 bundle SHA-256을 정확히 고정하며,
normalized source가 달라지면 같은 implementation/policy version으로 실행할 수 없다.
새 source freeze에는 implementation version과 evaluator policy version을 함께 올려야 한다.

동결된 evaluator policy와 report schema:

- [Evaluator policy v1](interp-001b-m1-evaluator-policy-v1.json)
- [Run envelope schema](interp-001b-m1-run.schema.json)
- [Conformance report schema](interp-001b-m1-conformance-report.schema.json)

생성된 deterministic artifact:

- [M1 run](interp-001-m1-v1-run.json)
- [M1 conformance report](interp-001-m1-v1-conformance.json)

artifact identity에는 clock, host path, environment 또는 randomness가 들어가지 않는다.
runner/evaluator source file SHA-256와 각 구현이 의존하는 common module을 포함한 source
bundle digest, frozen manifest/contract/schema/policy digest와 ordered result-set digest만
기록한다.

## operator capability 경계

orchestrator는 manifest key를 먼저 resolve한다. operator가 inspect하는 값은 profile,
boolean, current-access position, normalized edge와 cell-local integer relation symbol뿐이다.

```text
opaque material/source refs
→ binder의 positional pass-through
→ operator 결과 position에 provenance 재결합

opaque refs
↛ operator comparison
↛ stringification
↛ hash
↛ branch condition
```

`op010`도 raw material ID를 비교하지 않는다. binder가 cell-local lineage symbol로 바꾼
unordered source relation pair만 operator에 전달한다. manifest alias로 계산하는 내부 값은
runtime assembly identity가 아니라 detached fixture-content digest로만 취급하며 closed-world
cell result에는 노출하지 않는다. runtime artifact identity는 별도 typed ref/provenance가
생기기 전까지 구현하지 않는다.

## 고정한 실행 해석

A2 manifest가 byte-level aggregate result까지 정하지 않은 부분은 evaluator policy v1에서
공개적으로 고정했다. 기존 A2 manifest를 소급 수정하지 않는다.

| 항목 | v1 해석 |
|---|---|
| operator log | active model operator 9개만 기록; present access는 각 1회, absent access는 각 0회 |
| empty upstream | phase wrapper는 1회 실행하고 empty collection을 출력 |
| evidence projection | current access가 공급한 source material의 projection key를 첫 출현 순서로 deduplicate; absent access는 empty |
| prefix enum | 첫 present access `initial`; 새 normalized assembly source relation append `extended`; 그 외 `unchanged` |
| prefix 증명력 | evaluator 재계산과 runner-bound attestation; 독립 cryptographic history proof가 아님 |
| guard ledger | detached fixture projection의 실제 before/after digest; Dynamics runtime ledger 관측이 아님 |
| single-threshold retirement | 비교 baseline이 없으므로 `NOT_EVALUABLE / RETAIN` |

## detached guard projections

매 step에서 harness가 실행 전후에 다음 projection을 다시 canonicalize하고 SHA-256을
계산한다.

| projection | detached seed |
|---|---|
| `source_occurrences` | frozen source-occurrence declarations |
| `source_materials` | frozen material declarations |
| `source_encounters` | frozen source encounter profiles |
| `evidence_links`, `evidence_assessment` | explicit empty detached ledgers |
| `action_occurrences`, `authority_outputs` | explicit empty detached ledgers |
| `narrative_writes`, `observation_artifacts`, `world_outcomes` | explicit empty detached ledgers |

모든 guard는 `before_sha256 == after_sha256`와 `delta_count == 0`을 요구한다. 이것은
runner가 engine을 호출하지 않는다는 package/API 경계와 함께 사용한다. empty digest를
runtime 전체의 무변경 관측으로 과장하지 않는다.

## 판별 결과의 범위

frozen F1–F8은 다음 구조를 판별한다.

| fixture family | frozen distinction |
|---|---|
| F1 | weak congruent: R0–R3 모두 해당 방향 adopt |
| F2 | weak incongruent: R0 adopt, R1/R3 no selected material, R2 deferred |
| F3 | strong activation + weak edge: R0/R1 adopt, R2/R3 deferred |
| F4 | strong activation + strong edge: R0–R3 adopt |
| F5 | balanced mixed material: order와 무관하게 contested |
| F6 | source-free current access: declared neutral form, no invented content |
| F7 | reception state change만 있고 access가 없으면 exact no-op |
| F8 | transport redelivery는 no-op; 새 protocol reaccess만 새 encounter/assembly 기회 |

R3 factorization은 다음 두 relation으로 검사한다.

```text
R3.access == R1.access
R3.coherence == R2.coherence  # 같은 assembly에서
```

assembly ignition은 adjudication과 무관하게 frozen edge의 source relation이 cell prefix에
처음 나타날 때만 발생한다. binding ignition은 adopted adjudication과 실제 integration이
동시에 있을 때 발생한다. 둘은 서로 다른 projection이다.

## 해석 금지

```text
ReceptionStateSnapshot
≠ measured human mood

SubjectiveEncounterFormProxy
≠ qualia
≠ first-person report

synthetic structural conformance
≠ predictive superiority
≠ human mood-congruent processing law
≠ memory or recovery measurement
≠ TargetForm or Ghost evidence
≠ mental-time evidence
```

다음 단계는 이 결과를 Dynamics state에 넣는 작업이 아니다. M1이 고정해 둔
TargetForm/Ghost를 실제 경쟁 조건으로 열기 전에, object-scoped target-form source와
Ghost exploration path가 topology/reception만으로 환원되지 않는 새 판별을 만드는지
별도 manifest로 사전등록해야 한다.
