# Temporal Model Comparison

> **Status:** Slice-A identity prerequisites implemented; T0–T3 comparison planned

시간 모델은 구조적 ablation과 독립된 축으로 비교한다.

```text
T0  persistent state 없음
T1  현재 자극에만 반응
T2  사건 횟수 기반 update — v0.1 계열
T3  canonical time 위의 flow + event jump
```

v0.2는 하나의 단조 증가 `sim_time`을 사용한다.

```text
occurred_at   세계 사건이 발생한 시각
available_at  protocol이 모델에 접근 가능하게 한 시각
processed_at  모델이 실제로 처리한 시각
dt            저장하지 않고 기준 시각의 차이로 계산
```

`occurrence_id`와 `delivery_id`를 분리해 전송 중복과 실제 반복·재접근을 구별한다.

필수 대조:

- 동일 occurrence의 전송 중복은 evidence·world ledger에 멱등적이다.
- 동일 semantic dose의 transport partition은 규정된 집계 아래 과도한 차이를 만들지 않는다.
- 실제 시간 간격을 둔 반복 경험은 burst와 다른 궤적을 가질 수 있다.
- 과거 occurrence의 시각은 현재로 다시 쓰지 않지만 현재 reexposure는 현재 activation을 만들 수 있다.
- 무입력·동일 환경 flow는 step-size 변화에 수렴해야 한다.

주관적 시간과 생물학적 시간은 이 버전의 기준 시계가 아니라 후속 `DYNAMICAL_HYPOTHESIS`다.
