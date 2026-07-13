# INTERP-001D1 — Detached Three-Block Conformance Run

| 항목 | 값 |
|---|---|
| Status | `EXECUTED / EVALUATED SYNTHETIC CONFORMANCE` |
| Frozen execution | `INTERP-001D1-V1-EXECUTION@1.0.0` |
| Frozen evaluation | `INTERP-001D1-V1-EVALUATION@1.0.0` |
| Runner | `INTERP-001D1-V1-DETACHED-RUNNER@1.0.0` |
| Evaluator | `INTERP-001D1-V1-CONFORMANCE-EVALUATOR@1.0.0` |
| Matrix | 3 isolated blocks, 88 cells |
| Runtime integration | 없음 |
| Human empirical status | `NOT TESTED` |

## 이번 실행이 답하는 질문

frozen execution manifest만 읽는 detached runner가 source compiler, supplied encounter
formation과 exact-access Ghost path의 88-cell matrix를 완전하게 실행하고, 별도 evaluator가
frozen evaluation contract에 따라 closed-world signature, assertion, challenger와
retirement condition을 판정할 수 있는가?

report의 답은 이 synthetic contract 범위에서 `PASS`다.

| 판정 | 결과 |
|---|---:|
| schema-valid cells | 88 / 88 |
| closed-world signatures | 88 / 88 |
| cell assertions | 24 / 24 |
| pair assertions | 30 / 30 |
| global assertions | 37 / 37 |
| non-retirement assertions 합계 | 91 / 91 |
| development signatures | 44 / 44 |
| sealed signatures | 44 / 44 |
| target-scoped challenger rows | 72 |
| retirement conditions | 2 triggered / 16 |

이 결과는 frozen fixture와 operator가 선언한 출력을 구현이 재현했다는 structural
conformance다. 더 복잡한 모델이 인간을 더 잘 설명하거나 해당 구조가 실제 사람에게
필요하다는 판정이 아니다.

## 세 block은 하나의 pipeline이 아니다

runner는 다음 세 matrix를 같은 artifact에 직렬화하지만 각 cell을 fresh detached
ledger에서 실행한다.

| block | models | cells | 닫힌 질문 |
|---|---|---:|---|
| `SOURCE_COMPILER` | `TF0 / TF1 / TF2` | 24 | declared historical-source fixture에서 object-scoped readout projection을 구분하는가 |
| `ENCOUNTER_FORMATION` | `E0 / ER / ET / ERT` | 32 | supplied Reception/TargetForm intervention을 서로 다른 edge로 구분하는가 |
| `GHOST_PATH` | `G0 / GT / GP / GTP` | 32 | exact accessible material 아래 supplied context/path가 candidate structure를 구분하는가 |

```text
Block A output ↛ Block B input
Block B output ↛ Block C input
```

따라서 A·B·C의 동시 통과를 source에서 encounter와 Ghost로 이어지는 end-to-end 인과
사슬의 실행이라고 부르지 않는다. 특히 supplied TargetForm에 민감한 B/C 결과는 A가
산출한 readout의 downstream necessity를 시험하지 않는다.

## 분리된 실행과 평가

orchestrator는 runner와 evaluator를 순서가 분리된 subprocess로 실행한다.

```text
execution manifest bytes
→ runner
→ serialized 88-cell run
→ runner process 종료

execution + evaluation manifests
+ result/run schemas + evaluator policy
+ serialized run
→ evaluator
→ conformance report
```

runner는 evaluation manifest, development/sealed role, expected signature, challenger 또는
pass/fail label을 받지 않는다. evaluator는 runner를 import하지 않고 raw cell을 schema로
검증한 뒤 frozen fixture와 operator declaration에서 final semantic을 독립적으로 다시
계산한다. runner/evaluator source와 dependency bundle은 evaluator policy의 digest에
고정된다.

부모 `dynamics` package의 기존 public export는 같은 API를 유지하는 lazy resolution으로
바꿨다. 따라서 D1 subprocess가 `dynamics.labs`를 import할 때 engine, models와 protocol을
부수적으로 bootstrap하지 않는다. 부모 package initializer도 양쪽 source bundle에 포함해
고정하며 subprocess probe로 이를 검사한다. 이는 package-load 경계 보정이지 Dynamics
state transition이나 새 model behavior의 통합이 아니다.

입력 binding, exact JSON, schema, implementation bundle 또는 evaluation contract가
어긋나면 evaluator는 `FrozenD1EvaluationInputError`로 fail closed하고 report를 만들지
않는다. binding은 유효하지만 semantic relation이 틀리면 versioned `FAIL` report를 만든다.

동결된 입력과 정책:

execution/evaluation manifest 내부의 `FROZEN_UNEXECUTED`는 실행 전 동결 시점의 immutable
status라 소급 수정하지 않았다. 현재 실행 상태와 결과 identity는 이 문서, evaluator policy,
run artifact와 conformance report가 기록한다.

- [Execution manifest](interp-001d1-v1-execution.json)
- [Evaluation manifest](interp-001d1-v1-evaluation.json)
- [Cell-result schema](interp-001d1-v1-result.schema.json)
- [Run schema](interp-001d1-v1-run.schema.json)
- [Evaluator policy](interp-001d1-v1-evaluator-policy.json)
- [Conformance-report schema](interp-001d1-v1-conformance-report.schema.json)

생성된 deterministic artifacts:

- [88-cell run](interp-001d1-v1-run.json)
- [Conformance report](interp-001d1-v1-conformance.json)

artifact identity에는 clock, randomness, host path 또는 environment 값을 넣지 않는다.

## development / sealed의 정확한 의미

각 block의 fixture `001–004`는 development, `005–008`은 sealed role이다. 이 membership과
expected signature는 evaluation manifest에만 있고 execution manifest에는 없다. 실제
report에서 양쪽 signature는 각각 44/44 통과했다.

그러나 `sealed`는 evaluator-only synthetic isolation이다. 연구자에게 숨겨진 human
outcome, 독립 test set 또는 외부 prediction partition이 아니다. 이 split의 통과는
generalization이나 human predictive validity를 제공하지 않는다.

## challenger와 retirement 결과

9개 challenger를 block별 8 fixture에 적용해 72개의 named common-target comparison을
기록했다. 16개 retirement condition 중 trigger된 것은 다음 둘뿐이다.

| condition | 해석 |
|---|---|
| `retire.challenger.ch_rt_congruence` | frozen formation-direction target에서 `ERT`와 RT-congruence reference가 동등 |
| `retire.challenger.ch_declared_rt_lookup` | 위 reference와 대수적으로 같은 declared lookup adapter가 alias relation을 재확인 |

이는 독립적인 단순 모델 승리 두 개가 아니다.

```text
RT-equivalence family count       = 1
RT alias-control confirmation     = 1
distinct challenger reduction     = 0
```

여섯 factor-retirement condition, 나머지 일곱 distinct-challenger reduction과
Ghost-to-access-selection reduction은 trigger되지 않았다. trigger receipt도 frozen common
target의 축소 조건을 보고할 뿐 full model, factor, rich ordinal profile 또는 source
lineage를 자동 retire하거나 mutate하지 않는다.

## observability와 guard의 한계

evaluator가 확인하는 typed dataflow는 frozen static DAG와 exact operator trace, 그리고
independently recomputed final semantic이다. cell artifact는 중간 typed-edge value와 모든
stage receipt를 직렬화하지 않는다. 따라서 이 report를 intermediate causal provenance의
완전한 관측이라고 부르지 않는다.

각 cell의 12개 named guard는 fresh empty detached ledger의 before/after digest equality다.
fixture input immutability도 별도로 검사한다. 이는 이 implementation이 해당 detached
projection을 바꾸지 않았다는 attestation이지, 실제 Dynamics runtime ledger가 관측되어
불변이었다는 뜻이 아니다.

마찬가지로 runner가 execution-only API를 쓰고 evaluator와 별도 process로 끝나는 것은
implementation-bound blinding이다. cryptographic non-access proof나 독립 감사 환경의
관측으로 승격하지 않는다.

## 해석 금지

```text
DeclaredTargetFormReadoutProfile
≠ durable human TargetForm
≠ 대상의 실제 속성

SubjectiveEncounterFormProxy
≠ qualia
≠ first-person report

Ghost-path synthetic distinction
≠ human reason or consciousness mechanism

development/sealed conformance
≠ human prediction
≠ external validity
```

D1은 `HumanState`, routing, Evidence, action, authority, WorldOutcome 또는 Narrative Field를
변경하지 않는다. 기분에 따른 점화, 인간 기억·Episode/Narrative 형성, recovery,
`MorphicLoad`와 정신 시간도 측정하거나 입증하지 않는다.

## 다음 gate

다음은 D1을 runtime에 통합하는 작업이 아니라 `INTERP-001D2` 계약이다. D2에서만 다음을
별도로 사전등록한다.

- access ordinal보다 늦게 effective한 readout change와 later-access feedback
- writer, retention, decay, revalidation과 reconsolidation
- current access가 없을 때의 no-op
- future extension에 대한 prefix stability
- outcome/retention protocol과 단순 baseline

D2가 성공하기 전에는 TargetForm을 durable state로 추가하거나 Episode/Narrative writer와
접합하지 않는다.
