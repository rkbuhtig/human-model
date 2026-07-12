# Structural Ablations

> **Status:** PLANNED

구조적 분리의 기여를 시간 모델과 섞지 않고 비교한다.

```text
S0  monolithic state
S1  evidence assessment / access 분리
S2  evidence assessment / access / agency 분리
S3  subjective belief / evidence assessment까지 분리
```

유효한 비교 모델은 동일한 Contract Layer를 사용한다. 반면 `S0`처럼 의도적으로 월권을 허용하는 구조는 descriptive competitor가 아니라 Contract mutant로 별도 표기해야 한다.

구조 비교는 다음을 분리해 보고한다.

- certification contract 준수 여부
- 정상 행동을 막은 수
- 새롭게 구분한 예측
- 복잡도와 추가 자유도
- 경험 자료가 생긴 뒤의 held-out 예측 성능
