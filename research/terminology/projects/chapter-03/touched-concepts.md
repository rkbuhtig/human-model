# Chapter 03에서 개설하거나 갱신한 concept

이 문서는 Chapter 03 배치가 concept 분석에서 경계를 확인하는 데 사용한 C-ID만 가리킨다. 정의와 명칭을 복제하지 않는다.

## 첫 occurrence cluster 경계 갱신

- `C0002`
  - `X-CH03-001` EventFire 판정
  - `X-CH03-002` perc 상태공간 변위
  - `X-CH03-003` 새로움 잔차
  - `X-CH03-004` marker·segment 경계

  위 네 후보는 외부 발생의 필수 특성이 아니라 Chapter 03에서 `Event`가 맡았던 판정·readout·시간 경계 역할로 분리했다.

- `C0004`
  - `X-CH03-010` append-only 비권위 로그
  - `X-CH03-033` source 접근 provenance 사건
  - `X-CH03-034` 실행 의존성 trace

  위 후보들은 기록 계열과 인접하지만 발생 기록보다 넓거나 다른 기능을 가지므로 `C0004`에 자동 통합하지 않았다.

## 두 번째 cluster에서 새로 개설

- `C0005`
  - `X-CH03-013` 현재의 느껴지는 표면
  - `X-CH03-030` 현재 체험 보고의 제한된 claim scope

  현재 체험 표면을 외부 원인 주장·공적 정당화·지속 상태와 분리했다. `Z`, MeaningFlux, Priority 같은 다른 readout은 자동 통합하지 않았다.

- `C0006`
  - `X-CH03-023` readout·서사의 proposal influence
  - `X-CH03-024` next-tick 영향

  현재 선택·Commit을 직접 쓰지 않으면서 이후 탐색·후보 발견에 미치는 인과 역할로 분석했다. `Policy`, `GateBias`, `k`, `ρ` 같은 운영 노브는 concept의 필수 특성으로 넣지 않았다.

- `C0008`
  - `X-CH03-042` 실제 자원 지출

  actual use를 resource stock, output envelope, derived slack, 수행 노동, 회계 기록과 분리했다.

- `C0009` — `ENGINE-ONLY`
  - `X-CH03-034` 실행 의존성 trace
  - `X-CH03-035` WorkEvent·Billing

  실제 노동·지출을 보존하는 기술 회계 기록으로 분석했다. 인간 내부의 독립 record concept를 지지하는 인간 현상 근거는 없으므로 `KEEP`하지 않았다.

## 경계 확인에 사용했지만 자동 통합하지 않은 후보

- `X-CH03-012` 현재상 `Z`
  - 장면 구성 구조와 C0005의 현재 체험 표면이 같은 concept인지 보류한다.
- `X-CH03-017` MeaningFlux
  - descriptive readout, 실행 결과량, durable state가 한 이름에 섞였는지 후속 분석한다.
- `X-CH03-021` Story candidate generation
  - C0006의 비권위적 영향보다 강한 generator capability이므로 자동 통합하지 않는다.
- `X-CH03-038~041` Budget·stock·limiter·envelope
  - C0008의 actual expenditure와 구별되는 자원 cluster로 유지한다.
- `X-CH03-036` Trace/Facts
  - C0009 execution audit와 epistemic evidence를 자동 동일시하지 않는다.

## 근거 권한

Chapter 03의 인간적 사례와 synthesis는 저장소 내부 이론 자료이므로 독립 인간 현상 근거가 아니다. C0005~C0008의 `KEEP`은 Chapter 03·04의 코퍼스 확인 대비를 함께 사용했고, C0009는 구현·감사 근거만 확인되어 `ENGINE-ONLY`로 판정했다.