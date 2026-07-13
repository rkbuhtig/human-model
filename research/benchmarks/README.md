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

- [`INTERP-001` subjective encounter / delayed assembly / adjudication](interp-001-subjective-encounter-binding.md):
  외부 occurrence·Evidence, current access, experimenter-defined subjective encounter
  proxy, Episode candidate, adjudication과 target-form readout을 분리한다. `INTERP-001A2`
  M1은 R0–R3 reception access/coherence의 schema, execution/evaluation manifest와
  64-cell expectation을 `FROZEN / UNEXECUTED`로 둔다. I0–I4와 TF0–TF2의 broader
  manifest는 여전히 open이며 predictive validation이나 인간 mood·memory·qualia
  evidence가 아니다.
