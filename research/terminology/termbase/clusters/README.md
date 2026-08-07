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

## adjudication 대칭 규율

intake가 후보의 차이를 보존하는 단계라면 adjudication은 **같음과 다름을 둘 다 판정하는 단계**다. 분리도 병합과 마찬가지로 근거를 요구한다.

형제 후보를 비교할 때 가능한 경우 다음 두 가설을 함께 둔다.

```text
H_same
A와 B는 같은 concept이고
차이는 명칭·표현·epoch·구현·역할 시점뿐이다.

H_distinct
A와 B는 서로 다른 concept이고
서로 다른 genus·differentia·identity criterion을 가진다.
```

다음은 동일성을 깨는 충분조건이 아니다.

- 명칭이 다르다.
- 기호가 다르다.
- 다른 chapter·epoch에 나온다.
- 구현 함수나 저장 위치가 다르다.
- 같은 concept를 서로 다른 과정 단계에서 기술한다.
- 하나가 source-relative 또는 result-relative role로 불린다.

반대로 공통 철자·같은 장면·같은 시간창·같은 causal chain도 synonymy의 충분조건이 아니다.

adjudication 중간 판정은 필요할 때 다음처럼 기록할 수 있다.

```text
SAME-CONCEPT
DISTINCT-ROLE
CHARACTERISTIC-OVERLAP
GENERIC-CANDIDATE
PARTITIVE-CANDIDATE
ASSOCIATIVE-CANDIDATE
UNRESOLVED
```

- `SAME-CONCEPT`: genus, 본질 특성, identity criterion과 치환 조건이 같은 경우다. 서로 독립적으로 쓰인 명칭이 확인되면 그때 `MERGE`를 검토한다.
- `DISTINCT-ROLE`: 역할 차이는 확인됐지만 각각 독립 C-ID를 요구하는 concept인지까지는 확정하지 않은 상태다.
- `CHARACTERISTIC-OVERLAP`: 여러 후보가 같은 facet을 공유하지만 그 facet이 하나의 genus를 만들지 않는 경우다.
- `UNRESOLVED`: 같음과 다름 어느 쪽도 판정할 근거가 부족한 경우다.

새 C-ID 수나 `MERGE` 수를 cluster 성공 지표로 사용하지 않는다. **새 C-ID 0, MERGE 0도 정확한 cardinality와 관계를 닫았다면 완료된 판정이다.**

## 금지

- 같은 실행 사슬에 있다는 이유로 MERGE하지 않는다.
- 상위 개념이 여러 종개념을 가진다는 이유로 혼합 concept라고 판정하지 않는다.
- 여러 내포가 섞였다는 이유만으로 즉시 새 C-ID를 대량 발급하지 않는다.
- 정의문에서 외연을 늘린 뒤 그 문장을 본질 특성으로 사용하지 않는다.
- cluster의 직관을 인간 현상 근거로 승격하지 않는다.
- 분리 규율이 익숙하다는 이유로 작은 역할 차이를 곧바로 별도 concept로 승인하지 않는다.
- `MERGE`가 필요하다는 압력 때문에 synonymy가 약한 후보를 합치지 않는다.

## 완료 조건

cluster가 끝났다는 것은 모든 후보가 C-ID를 받았다는 뜻이 아니다. 다음 중 하나의 목적지를 가질 때 완료된다.

- 기존 C-ID와 synonymy 확인 후 MERGE
- 기존 C-ID와 generic·partitive·associative 관계 확정
- KEEP 또는 새 C-ID 발급 조건 충족
- ENGINE-ONLY
- HISTORICAL-ONLY
- HOLD와 구체적 재개 조건
- 여러 후보가 하나의 genus가 아니라 characteristic intersection임을 판정
- 역할 차이는 확인했지만 별도 concept 발급은 보류하는 `DISTINCT-ROLE` 판정
