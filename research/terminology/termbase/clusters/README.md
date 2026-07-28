# Termbase Clusters

`clusters/`는 extraction 후보를 형제 집합으로 동시에 비교한 분석 과정을 보존한다.

concept 파일은 판정 결과와 단일 내포를 소유한다. cluster 파일은 그 결과에 도달하기 전의 비교 공간, 관계 후보, 보류 이유와 재개 조건을 소유한다.

## 파일명

```text
CLxxxx-짧은-주제.md
```

CL 번호는 분석 순서를 추적하기 위한 안정 ID다. concept 수, 중요도 또는 ontology 층을 인코딩하지 않는다.

## 필수 항목

1. cluster 질문
2. 입력 후보와 출처
3. 형제 후보 전체
4. 후보별 genus 후보
5. 차별 특성 후보
6. concept 관계
   - generic: BROADER / NARROWER
   - partitive: WHOLE / PART
   - associative: RELATED
7. definition gate 결과
8. 코퍼스 확인 대비 또는 독립 관측 사례
9. 판정
   - HOLD가 기본
   - KEEP / ENGINE-ONLY / HISTORICAL-ONLY
   - synonymy가 확인된 경우에만 MERGE
10. 재개 조건
11. concept·harmonization·프로젝트 역참조

## 관계 표기

```text
A BROADER-THAN B
B NARROWER-CANDIDATE-OF A
A WHOLE-OF B
B PART-CANDIDATE-OF A
A RELATED-TO B
```

`CANDIDATE`가 붙은 관계는 아직 concept 관계가 확정되지 않았다는 뜻이다. 관계 후보를 기록하기 위해 B의 C-ID를 먼저 열지 않는다.

## 금지

- 같은 실행 사슬에 있다는 이유로 MERGE하지 않는다.
- 상위 개념이 여러 종개념을 가진다는 이유로 혼합 concept라고 판정하지 않는다.
- 여러 내포가 섞였다는 이유만으로 즉시 새 C-ID를 대량 발급하지 않는다.
- 정의문에서 외연을 늘린 뒤 그 문장을 본질 특성으로 사용하지 않는다.
- cluster의 직관을 인간 현상 근거로 승격하지 않는다.

## 완료 조건

cluster가 끝났다는 것은 모든 후보가 C-ID를 받았다는 뜻이 아니다. 다음 중 하나의 목적지를 가질 때 완료된다.

- 기존 C-ID와 synonymy 확인 후 MERGE
- 기존 C-ID와 generic·partitive·associative 관계 확정
- KEEP 또는 새 C-ID 발급 조건 충족
- ENGINE-ONLY
- HISTORICAL-ONLY
- HOLD와 구체적 재개 조건
