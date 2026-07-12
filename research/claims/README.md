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

현재 registry의 claim 수는 작게 유지한다. 실제 역사 사례, 구조 테스트 또는 경험 자료와 연결하지 못하는 문장은 먼저 `DRAFT`나 `HOLD`에 둔다.
