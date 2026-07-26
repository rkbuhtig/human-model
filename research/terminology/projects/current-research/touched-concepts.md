# Current research에서 개설하거나 갱신한 concept

이 문서는 current-research 배치가 이번 concept 분석에서 건드린 C-ID만 가리킨다. 정의와 명칭을 복제하지 않는다.

## 새로 개설

- `C0001` — `X-CURR-001`의 행동 경로 선택 요구를 Chapter 02 대비와 함께 분석함
- `C0002` — `X-CURR-003`의 ActionOccurrence 경계를 Chapter 02 외부 발생과 대조함
- `C0003` — `X-CURR-004`의 WorldOutcome을 선행 occurrence에 귀속되는 결과 상태로 분석함

## 경계 확인에 사용했지만 자동 통합하지 않은 후보

- `X-CURR-002` Intent / Attempt / Performance
  - RFC 0001의 아키텍처 계약만으로 독립 인간 concept를 열지 않았다.
- `X-CURR-005` occurrence identity와 발생 시각
  - protocol ID·timestamp는 `C0002`의 정의 특성에서 제외했다.
- `X-CURR-016` record·provenance·receipt
  - `C0004`보다 넓은 후보이므로 전체를 occurrence record와 통합하지 않았다. 판정 record와 실행 provenance는 후속 record cluster로 남긴다.
- `X-CURR-018` 결과 이후 자기평가·책임·수리
  - `C0003`의 결과 상태와 별도 후속 cluster로 유지한다.

## C0002–C0003 관계

`C0003`을 `C0002`의 하위 concept로 확정하지 않았다.

- `C0002`는 실제로 성립한 occurrence를 분류한다.
- `C0003`은 선행 occurrence에 대해 세계·관계가 어떤 결과 상태에 이르렀는지를 분류한다.
- 하나의 후속 반응은 occurrence이면서 동시에 앞선 행동의 결과를 구성할 수 있지만, 두 분류의 기준은 다르다.

## 근거 권한

README와 RFC는 현재 연구가 이 경계를 사용한다는 현재 사용 근거만 제공한다. `KEEP`의 인간 장면 대비는 Chapter 02의 코퍼스 확인 사례에서 왔으며, RFC의 타입 분리를 인간 내부 단계로 승격하지 않았다.
