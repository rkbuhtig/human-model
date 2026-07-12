# Dynamics v0.1 — Canonical Semantic Baseline

> **지위:** refactor regression oracle  
> **원격 기준 revision:** `9b731b7f92700227de1fae8adc79e1d8e687d25f`  
> **scenario:** `delayed_reply`  
> **projection schema:** `human-model-semantic-baseline/0.1`  
> **golden SHA-256:** `5197e267606a3062c01f430f743ef222d9183c9bef4f642f0d80c39f3569f0b5`

이 baseline은 Dynamics v0.1이 인간을 정확히 예측한다는 증거가 아니다. 이후 contract, protocol, descriptive model을 서로 다른 모듈로 옮길 때 기존 실행 의미가 우연히 변하지 않았는지 확인하는 회귀 오라클이다.

## 고정한 의미

- 관측 사건에서 만들어진 claim별 Evidence digest
- 사건별 support·contradiction·confidence·stance 전이
- decision window의 candidate salience·probability·influence terms
- Intent → Attempt → Performance → ActionOccurrence의 존재와 계보
- associative·affective·habit·narrative·relationship slow-state trajectory
- raw·unique·processed 및 deferred·dropped·unresolved 입력 회계

Python 클래스명, 모듈 경로, dataclass `repr`, wall-clock 실행 시간, 처리량, peak memory는 의도적으로 포함하지 않았다. 따라서 파일 이동이나 클래스명 변경은 baseline을 깨지 않지만, 의미적 수치·전이·경로 변경은 깨뜨린다.

모든 실수는 JSON 직렬화 전에 소수점 12자리로 정규화하며, 객체 ID 대신 scenario event, claim, action, provenance, independence group 같은 도메인 필드를 사용한다. 생성된 기술 ID가 필요한 계보는 ID 문자열 자체 대신 `references_intent`, `references_attempt`, `references_performance` 관계로 투영한다.

## 재생과 검증

```bash
python -m dynamics.baseline
python -m unittest dynamics.tests.test_baseline -v
```

정본은 [baseline-v0.1.json](baseline-v0.1.json)이다. baseline 갱신은 단순 포맷 변경이 아니라 의미 변경으로 취급하며, 변경 이유와 새 기준 revision을 함께 기록해야 한다.

실행 환경·기존 stress seed·원래 테스트 수와 의도적 제외 항목은 [baseline-v0.1-manifest.json](baseline-v0.1-manifest.json)에 분리해 기록한다. 환경 메타데이터는 재현 조건이지 semantic golden의 일부가 아니다.
