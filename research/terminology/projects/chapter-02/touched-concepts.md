# Chapter 02에서 개설하거나 갱신한 concept

이 문서는 Chapter 02 배치가 이번 concept 분석에서 건드린 C-ID만 가리킨다. 정의와 명칭은 복제하지 않는다.

## 새로 개설

- `C0001` — `X-CH02-001`의 행동 선택 후보를 분석함
- `C0002` — `X-CH02-003`의 외부 발생 후보를 분석함
- `C0003` — `X-CH02-004`의 후속 경로 후보를 선행 occurrence에 귀속되는 결과 상태로 분석함
- `C0004` — `X-CH02-007` 가운데 occurrence record 역할만 분석함

## concept ID를 열지 않은 인접 후보

- `X-CH02-002` 외부 표현
  - 외부 발생의 하위 개념인지 수행 과정인지 아직 결정할 코퍼스 확인 대비가 부족하다.
- `X-CH02-005` 단계·위상
  - 엔진 처리 단계와 인간 변화 단계의 경계가 열려 있다.
- `X-CH02-006` 검사점·시점
  - occurrence의 일반 시간 특성과 protocol checkpoint를 분리해야 한다.
- `X-CH02-007` 판정 기록 역할
  - C0004에 넣지 않고 adjudication-record cluster로 넘긴다.
- `X-CH02-008` 비가역 잠금
  - 발생의 특성이 아니라 state application·lock 후보로 남긴다.
- `X-CH02-016` 신체 흔적, `X-CH02-017` 기억 고착, `X-CH02-018` 자기 역사 편입
  - occurrence cluster와 자동 통합하지 않고 후속 지속·기억 cluster로 넘긴다.

## 이번 배치가 제공한 코퍼스 확인 대비

- Chapter 02 §3.2의 같은 `연락하지 않음` 아래 안정된 noop, 문턱 미달, 억제 상태
- Chapter 02 §4.3의 몸 인터럽트 뒤 사후 인수·거부
- Chapter 02 §4.1의 발생, 올바른 사실 기록, 학습, 렌즈 변화의 네 질문
- Chapter 02 §3.1·§3.4의 Hit/Miss/Ignore와 OPEN/SETTLED/EXPIRED

이 사례들은 분석 이전부터 저장소 내부에 존재한 인간 장면이지만, 구분을 설명하기 위해 작성된 이론 사례다. 독립 관측 자료나 인간 일반에 대한 경험적 검증 자료는 아니다.

## 후속 record cluster로 이동

- 결과 상태 기록 — C0003에 관한 표상
- 판정 기록 — X-CH02-007의 나머지 역할
- 실행 provenance — Chapter 03 source/trace 계열과 대조
