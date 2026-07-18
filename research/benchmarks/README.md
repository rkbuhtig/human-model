# Research Benchmarks

이 디렉터리는 구조적 건전성과 인간 설명력을 같은 점수로 합치지 않는다.

```text
Contract mutation
: 테스트가 월권을 검출할 수 있는가

Structural ablation
: 어떤 residence 분리가 독립적으로 필요한가

Temporal comparison
: 같은 구조 아래 어떤 시간 가설이 다른 예측을 내는가

Measurement preregistration
: 파생량을 계산하기 전에 관측 단위·정보 경계·정상 통제·실패 조건을 고정한다
```

Contract mutant는 인간 모델 후보가 아니다. 반대로 descriptive model이 Contract를 통과했다는 사실은 그 모델이 인간을 더 잘 설명한다는 증거가 아니다.

구조 축 `S*`와 시간 축 `T*`는 따로 바꾸고, 장기적으로 `S3T2`와 `S3T3`처럼 한 축만 다른 대조를 만든다.

현재 측정 사전 등록:

- [`MORPH-001A` reducer proposal–commit instrumentation](morph-001-demand-commit.md):
  현재 reducer의 pre-constraint proposal과 실제 commit을 먼저 분리한다. 이는 아직
  `DeformationDemand`가 아니며 envelope·load·퀄리아·정신 시간도 계산하지 않는다.
- [`MORPH-001B` proposal / declared-band proxy comparison](morph-001b-proposal-envelope-comparison.md):
  `MORPH-001A`의 ordered proposal을 실험자가 선언한 asymmetric simulation band와
  componentwise로 비교한다. 출력은 read-only proxy profile이며 인간의 수용 능력,
  `ExcessDemand`, residual, load, 퀄리아 또는 정신 시간 측정값이 아니다.
- [`HUMAN-DYN-ADEQ-S0`](human-dyn-adequacy-s0.md):
  구조적 분포 능력과 비인간 hidden source 예측을 분리한다. 후속
  [`AMEND-001`](human-dyn-adequacy-s0-amendment-001.md)은 단일 수동 source 대신
  public generator/hyperprior와 미래 beacon으로 결정되는 16개 source instance family를
  채택하고, predictive leaderboard·state sufficiency·online compression의 판정 권한을
  분리한다. `INITIAL-001` 모델 freeze는 source 생성 권한이 없으며 `INITIAL-002`가
  merge되기 전에는 beacon·instance·corpus를 만들 수 없다.

- [`INTERP-001` subjective encounter / delayed assembly / adjudication](interp-001-subjective-encounter-binding.md):
  외부 occurrence·Evidence, current access, experimenter-defined subjective encounter
  proxy, Episode candidate, adjudication과 target-form readout을 분리한다. `INTERP-001A2`
  M1은 R0–R3 reception access/coherence의 schema, execution/evaluation manifest와
  64-cell expectation을 동결했고, [`INTERP-001B`](interp-001b-m1-conformance.md)가
  이를 64-cell/88-step detached run과 독립 conformance evaluation으로 실행했다.
  [`INTERP-001D1`](interp-001d1-target-form-ghost-ablation.md)은 source compiler
  `TF0–TF2`, supplied encounter-formation intervention `E0/ER/ET/ERT`와 exact-access
  Ghost ablation `G0/GT/GP/GTP`를 세 개의 격리된 block, 88개 cell과 evaluator-only
  development/sealed split으로 동결했다.
  [`D1 conformance run`](interp-001d1-v1-conformance.md)은 88/88 signature와 91/91
  non-retirement assertion을 통과해 `EXECUTED / EVALUATED SYNTHETIC CONFORMANCE` 상태다.
  세 block은 end-to-end pipeline이 아니며 development/sealed는 예측 partition이 아니다.
  이는 durable TargetForm, Episode/Narrative writer, predictive validation이나 인간
  mood·memory·qualia evidence가 아니다.
  후속 [`INTERP-001D2a0`](../scenarios/interp-dialogue-001/d2a0/README.md)는 이 detached
  경계를 유지한 채 current access에서 future-effective interpretation까지의 최소 spine,
  독립 T/P/H 전략 축, trace schema와 synthetic distinguishing witness를 실행 전에 동결한다.
  상태는 `FROZEN / UNEXECUTED`이며 runner/evaluator/result 또는 `HumanState` write는 없다.
  [`EXEC0 closure`](../scenarios/interp-dialogue-001/d2a0/exec0/README.md)는 predecessor를
  수정하지 않고 exact operator/lifecycle, 추가 fixture, 46개 explicit execution unit과 typed
  assertion selector를 추가 동결한다. golden과 evaluator-only artifact는 future runner 입력이
  아니며, EXEC0 자체에도 실행 결과는 없다.
