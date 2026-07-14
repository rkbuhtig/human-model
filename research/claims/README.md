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
`INTERP-001D1`은 source compiler, supplied encounter-formation intervention와
exact-access Ghost ablation을 세 block으로 동결한 뒤 detached runner/evaluator에서
88/88 signature와 91/91 non-retirement assertion까지 실행·판정했다. 그러나 세 block은
end-to-end pipeline이 아니고 later-access feedback, writer/retention 또는 human prediction을
검사하지 않으므로 `HM-INV-013`과 `HM-DYN-004`는 계속 `UNIMPLEMENTED`, structural support는
empty로 둔다.
`HM-MEAS-005`의 complete comparable receipt, TargetForm/Ghost variation, runtime
integration, calibration과 human measurement는 구현되지 않았다.
이 등록은 역사적 Episode ontology의 정본화, mood-congruent ignition의 인간 법칙,
Narrative writer, actual qualia 또는 predictive support를 만들지 않는다.

`INTERP-DIALOGUE-001A`는 D1과 recursive D2 사이에 real-world-domain, author-origin
hypothetical functional-jurisdiction scenario contract를 등록한다. factor별 contrast는
조작 source lane, public-record effect, 고정 factor, `registered_candidate_probe_domains`,
must-remain-equal 항목과 열린 discriminator reference를 구조화한다. 후보 domain은
비배타적 관측 목록이며, 목록 밖 효과는 fixture 위반이 아니라 현재 분해의 scope failure
또는 열린 결과다.

`INTERP-DIALOGUE-001B`는 exact trace field, prefix/initial/one-future ordinal horizon,
factor별 competing signature, 동일 future-option 비교, REL initial×later mood 2×2,
3개 D2a-only selective challenge와 명시적 out-of-model lane을 동결했다. hypothesis relation,
future observation과 adjudication vocabulary는 서로 다른 권한을 가진다. 이 freeze는
claim evaluation run이 아니며, 자연 contrast의 최초 차이도 direct causal residence를
인증하지 않는다. observed equality는 operational alias가 아니고, 현재 one-future-access
horizon은 durable TargetForm과 slow cache를 식별하지 못한다. A/B validator가 통과해도
contract 구조만 검사할 뿐 인간 자료, LLM activation, D2a runtime trace 또는 mechanism
support를 만들지 않는다. 따라서 `HM-INV-013`과 `HM-DYN-004`는 계속 `UNIMPLEMENTED`,
structural support empty로 남는다.

`INTERP-DIALOGUE-001P0-v0`는 24개 presentation과 prompt/response schedule, scripted raw
payload provenance, materializer/scanner/analyst 권한을 동결하는 development elicitation
contract다. current runner는 `SCRIPTED_ADVERSARIAL_RESPONSE`-only replay materializer이고
actual delivery/response occurrence를 발행하지 않는다. author walkthrough와 language
inspection도 evaluator-side defect source다. internal trace를 측정하지 않으며, P0 validator
통과는 pilot result나 claim evaluation이 아니므로 support 배열을 추가하지 않는다.

P1-v0는 exact P0-v0의 immutable scripted replay와 evaluator-side inspection을 실행해
9 confirmed/4 deferred/1 rejected defect receipt와 8개의
`PROPOSED_NOT_ADOPTED / UNEXECUTED` revision proposal을 발행했다. 다음 순서는 별도 P0-v1
revision decision/freeze → source-specific acquisition/human/latent/D2a protocol freeze →
독립 실행 → cross-source audit(C)다. P1은 actual acquisition 또는 수정 instrument를
실행하거나 채택하지 않았으며 claim support도 추가하지 않는다. `HM-INV-013`과
`HM-DYN-004`는 계속 `UNIMPLEMENTED`, structural/empirical support empty로 남고,
`HM-MEAS-005`도 P0 elicitation으로 human-comparable measurement가 완성되지 않는다.
