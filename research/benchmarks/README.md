# Research Benchmarks

이 디렉터리는 구조적 건전성과 인간 설명력을 같은 점수로 합치지 않는다.

```text
Contract mutation
: 테스트가 월권을 검출할 수 있는가

Structural ablation
: 어떤 residence 분리가 독립적으로 필요한가

Temporal comparison
: 같은 구조 아래 어떤 시간 가설이 다른 예측을 내는가
```

Contract mutant는 인간 모델 후보가 아니다. 반대로 descriptive model이 Contract를 통과했다는 사실은 그 모델이 인간을 더 잘 설명한다는 증거가 아니다.

구조 축 `S*`와 시간 축 `T*`는 따로 바꾸고, 장기적으로 `S3T2`와 `S3T3`처럼 한 축만 다른 대조를 만든다.
