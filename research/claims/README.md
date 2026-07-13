# Claim Registry

`registry.json`은 연구가 말하는 문장의 종류, 채택 여부, 구현 여부, 적용 범위와 근거를 서로 다른 필드로 보존한다.

```text
program adoption
≠ implementation completion
≠ structural test support
≠ human-empirical support
```

주장 종류는 동일한 방식으로 실패하지 않는다.

| Kind | Evaluation condition |
|---|---|
| `TYPE` | 불법 객체를 생성하거나 정의가 충돌하는가 |
| `INVARIANT` | 위반하는 실행 trace가 존재하는가 |
| `DYNAMICAL_HYPOTHESIS` | 경쟁 모델과 구분되는 관측을 내지 못하는가 |
| `MEASUREMENT_MODEL` | 교정·신뢰도·식별 가능성이 실패하는가 |
| `METAPHOR` | 설명 보조를 경험적 근거처럼 사용하는가 |

`schema.json`은 종류별 `failure_condition.type`을 선언한다. repository tests는 현재 registry의 필수 키·enum·ID·scope·support 축과 failure type을 독립적으로 검사한다. `scope`와 `exclusions`는 한 구현에서 통과한 주장이 인간 일반 법칙으로 자동 확장되는 것을 막는다.

전체 Draft 2020-12 schema 검증은 다음 release check로 실행한다.

```bash
npx --yes ajv-cli validate --spec=draft2020 \
  -s research/claims/schema.json \
  -d research/claims/registry.json
```

현재 registry에는 구현된 핵심 invariant와 RFC 0003의 타입 구분·가설·측정 전제·
비유 지위를 함께 둔다. 근거가 없는 dynamical claim은 `PROPOSED` 또는 `HOLD`이며,
타입 구분을 채택했다고 그 안의 인간 가설까지 채택된 것으로 읽지 않는다.
`MORPH-001B`의 implemented claim도 experimenter-declared simulation comparison에만
적용되며 measured human accommodation, load, qualia 또는 mental-time claim으로
확장되지 않는다.

`INTERP-001A`는 subjective/current-access/Episode-candidate/adjudication/readout
경계를 type·invariant·dynamical hypothesis·measurement contract로 나눠 등록한다.
`INTERP-001A2`의 manifest는 역사적 `FROZEN / UNEXECUTED` 상태와 digest를 그대로
보존하고, `INTERP-001B`가 그 exact input을 별도 runner/evaluator로 실행했다.
`HM-INV-012`와 `HM-MEAS-005`는 frozen M1에 실제 구현된 경계만 `PARTIAL`이다.
`HM-DYN-003`도 88개 signature와 54개 non-retirement assertion의 synthetic
conformance는 얻었지만 single-threshold alias retirement rule이 baseline 부재로
`NOT_EVALUABLE`이고 TargetForm-recursion dependency가 열려 있어 `PARTIAL`이다.
`HM-MEAS-005`의 complete comparable receipt, TargetForm/Ghost variation, runtime
integration, calibration과 human measurement는 구현되지 않았다.
이 등록은 역사적 Episode ontology의 정본화, mood-congruent ignition의 인간 법칙,
Narrative writer, actual qualia 또는 predictive support를 만들지 않는다.
