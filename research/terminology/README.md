# Terminology Research

`research/terminology/`는 과거 문서와 현재 연구에서 한 이름 아래 섞인 책임을 풀고, 현재 연구가 사용할 개념과 명칭을 정립하기 위한 작업 공간이다.

이 작업은 사전을 먼저 쓰지 않는다. ISO 704의 개념지향 용어작업, ISO 860의 개념·정의·용어 조화, ISO 10241-1의 용어 항목 작성 원칙, 캐나다 번역국의 전문용어 연구 절차를 이 저장소에 맞게 적용한다.

```text
범위와 출처 선정
→ 개념 후보와 관계 추출
→ 기초 용어 색인 작성
→ cluster 단위 개념 분석
→ 특성·차별 특성 확인
→ 정의 초안 gate
→ concept 관계 판정
→ C-ID 유지·개설·보류
→ 명칭 선정
→ 다른 입력 배치와 조화
→ 범위가 명시된 glossary
→ 현재 문서 개명
```

## 1. 작업 구조 지도

### 1.1 디렉터리와 소유권

```text
research/
├─ terminology/
│  ├─ README.md                                      공통 방법과 판정 규칙
│  ├─ projects/                                      입력 배치 소유
│  │  └─ <batch>/
│  │     ├─ scope.md
│  │     ├─ extraction-map.md                        후보 내용의 단일 권위
│  │     ├─ basic-term-list.md                       명칭 → 추출 ID → C-ID/상태 색인
│  │     └─ touched-concepts.md                      이번 배치가 건드린 C-ID·관계·보류
│  └─ termbase/                                      입력 배치를 넘어 살아남는 결과
│     ├─ clusters/
│     │  ├─ README.md                                cluster 산출물 규칙
│     │  └─ CLxxxx-*.md                              형제 후보 동시 비교 기록
│     ├─ concepts/
│     │  └─ Cxxxx.md                                 한 파일에 한 concept
│     ├─ harmonization/
│     │  └─ Hxxxx.md                                 실제 경계 교정·통합·분할 기록
│     └─ glossary.md                                 승인 명칭이 생길 때만 발행
└─ diary/
   └─ YYYY-MM-DD/
      └─ 부제.md                                     비권위 연구 메모
```

- `projects/`는 무엇을 읽고 무엇을 발견했는지를 소유한다.
- `clusters/`는 어떤 형제 후보를 어떤 관계 질문으로 동시에 비교했는지를 소유한다.
- `concepts/`는 입력 배치를 넘어 살아남는 단일 concept의 내포를 소유한다.
- `harmonization/`은 기존 판정의 실제 통합·분할·경계 수정과 철회를 소유한다.
- `diary/`는 직감·의심·연구 경험을 기록하지만 concept 판정 근거로 자동 승격되지 않는다.

### 1.2 자료 흐름

```text
source corpus
→ projects/<batch>/scope.md
→ projects/<batch>/extraction-map.md
→ projects/<batch>/basic-term-list.md
→ termbase/clusters/CLxxxx-*.md
→ concept 관계와 차별 특성 판정
→ HOLD 또는 기존 C-ID 갱신 또는 새 C-ID 개설
→ termbase/concepts/Cxxxx.md
→ projects/<batch>/touched-concepts.md
→ 충돌 시 harmonization
→ glossary
→ current-use rename
```

### 1.3 금지된 역류

- 현재 RFC의 아키텍처 구분을 인간 현상 근거로 되돌려 쓰지 않는다.
- 한 프로젝트의 extraction map을 termbase의 정본 개념체계로 취급하지 않는다.
- cluster 기록을 concept 정의의 대체물로 사용하지 않는다.
- diary의 직감을 차별 특성이나 `KEEP` 판정의 직접 근거로 사용하지 않는다.
- 구성 사례를 인간 현상 근거로 사용하지 않는다.
- 같은 runtime 흐름에 놓였다는 이유로 동일 concept라고 판정하지 않는다.

## 2. 문서별 권한

### `projects/<batch>/scope.md`

- 조사 질문
- 주 입력과 보조 입력
- 출처별 주장 권한
- 초기 명칭 범위
- 범위 밖 작업

### `projects/<batch>/extraction-map.md`

자료에서 추출한 후보 책임과 관계의 단일 권위다.

- 후보는 잠정 명칭이 아니라 중립 서술로 적는다.
- 후보마다 배치 내부의 안정 추출 ID를 붙인다.
- 역사적 명칭과 실제 문서 위치를 후보에 연결한다.
- 이 지도는 현재 인간 ontology나 termbase의 정본 개념체계가 아니다.

### `projects/<batch>/basic-term-list.md`

명칭에서 extraction map과 concept 또는 판정 상태로 들어가는 색인이다.

- 후보 설명을 복제하지 않는다.
- 명칭, 관찰된 역할, 추출 ID, C-ID 또는 상태, 다음 확인만 기록한다.
- C-ID 연결은 해당 역할만 연결하며 같은 철자의 모든 용법을 승인하지 않는다.
- generic·partitive·associative 관계 후보를 `MERGE`로 표기하지 않는다.

### `projects/<batch>/touched-concepts.md`

배치가 개설·갱신·보류한 C-ID와, C-ID를 열지 않은 후보의 관계·목적지를 기록한다. 정의나 명칭을 복제하지 않는다.

### `termbase/clusters/CLxxxx-*.md`

형제 후보를 동시에 비교한 판정 과정을 기록한다.

필수 내용:

- cluster 질문과 범위
- 형제 후보 전체와 출처
- 후보별 genus 후보
- 후보별 차별 특성 후보
- generic / partitive / associative 관계
- 코퍼스 확인 대비 또는 독립 관측 사례
- 정의 gate 결과
- 현재 판정과 재개 조건
- concept·harmonization·프로젝트 역참조

cluster는 concept의 임시 바구니가 아니다. 후보의 관계가 닫히지 않았을 때 그 불확실성을 보존하는 분석 기록이다.

### `termbase/concepts/Cxxxx.md`

입력 배치를 넘어 살아남는 **한 개의 concept**를 소유한다.

- 안정적인 concept ID
- 작업 설명
- 현재 판정
- 연결된 입력 후보
- 특성 목록과 특성별 provenance
- 코퍼스 확인 대비 사례
- generic·partitive·associative 관계
- 이 구분이 보존하는 설명적 차이
- 경계 재압축 이력
- 정의 초안
- 권장·허용·역사적 명칭
- 남은 불확실성

한 파일이 subject field, 과정 전체, 구현 묶음 또는 관련 기록군을 담는 선언지가 되면 concept 판정을 철회하고 cluster로 되돌린다.

### `termbase/harmonization/Hxxxx.md`

다음을 기록한다.

- synonymy 확인에 따른 ID 통합
- 하나의 C-ID에 둘 이상의 concept가 섞였음이 확인된 분할
- concept 경계·관계·판정의 수정 또는 철회
- `ENGINE-ONLY`·`HISTORICAL-ONLY` 처분 변경

과거 문서가 한 번 분리한 경계를 후속 문서에서 다시 섞은 사실은 harmonization이 아니다. 해당 concept 파일의 `경계 재압축 이력`에 기록한다.

## 3. 근거 층

```text
계보 근거
= 과거 명칭이 어떤 책임을 가리켰는가

현재 사용 근거
= 현재 연구가 어떤 구분을 사용하거나 필요로 하는가

인간 현상 근거
= 엔진과 무관한 인간 장면에서 그 구분이 실제로 필요한가
```

인간 현상 근거 안에서도 권한을 구분한다.

- **코퍼스 확인 사례:** 분석 이전부터 Chapter·notes·평가 기록에 존재한 인간 장면. 현재 연구 어휘의 구분 필요성을 지지하지만 인간 일반의 경험적 검증은 아니다.
- **독립 관측 사례:** 해당 구분을 설명하려고 구성하지 않은 관찰·평가·자료에서 확인된 장면. 실제 출처가 있을 때만 표시한다.
- **구성 사례:** 분석자가 정의의 과대·과소를 확인하려고 만든 예. 정의 교정에는 쓸 수 있지만 `KEEP`, `MERGE`, `ENGINE-ONLY`의 직접 근거로 기록하지 않는다.

차별 특성에는 형제 후보와 실제로 갈라지는 코퍼스 확인 사례 또는 독립 관측 사례를 연결한다.

- 사례가 없으면 그 특성으로 `KEEP`을 주지 않고 `HOLD`한다.
- `분리 사례를 찾지 못함`을 `분리 사례가 없음`으로 바꾸지 않는다.
- 근거 없는 하위 C-ID 발급보다 관계 후보와 `HOLD`를 우선한다.

## 4. 개념 분석

### 4.1 cluster 단위 분석

후보 하나를 고립해서 정의하지 않는다. 상위 개념과 형제 후보에 따라 차별 특성이 달라지므로 함께 비교한다.

```text
후보 추출
→ 기본 HOLD
→ 형제 후보와 genus 후보 비교
→ generic / partitive / associative 관계 기록
→ 정의 gate
→ 대비 사례 확인
→ C-ID 유지·개설 또는 계속 HOLD
```

### 4.2 특성 판정 라벨 — 닫힌 집합

특성표의 판정 라벨은 다음만 허용한다.

- **본질:** 없으면 해당 concept가 아닌 특성
- **본질·차별:** 본질 특성이면서 형제 concept와 갈라내는 특성
- **부수:** 일부 사례에서 따라오지만 concept를 구성하지 않는 특성
- **제외:** 다른 후보의 특성이거나 근거 권한이 맞지 않아 정의에서 제거한 특성
- **엔진 의존 후보:** 구현·protocol에서만 확인되어 인간 concept 특성으로 아직 사용할 수 없는 특성

`본질·범위`, `부분 본질`, `운영 본질`처럼 README에 정의되지 않은 라벨을 만들지 않는다. 외연·하위 유형·부분 단계는 특성이 아니라 관계 절에서 다룬다.

### 4.3 concept 관계

개념 관계는 다음 세 종류로 기록한다.

#### Generic relation

한 concept가 다른 concept의 종개념일 때 사용한다.

```text
BROADER  유개념
NARROWER 종개념
```

종개념은 유개념의 모든 본질 특성을 가지며 하나 이상의 추가 차별 특성을 가진다.

#### Partitive relation

한 concept가 과정·구조·집합의 전체 또는 부분일 때 사용한다.

```text
WHOLE
PART
```

“탐색 노동은 노동의 한 종류인가”와 “탐색은 노동 과정의 한 단계인가”를 같은 관계로 처리하지 않는다.

#### Associative relation

generic·partitive가 아니지만 인과·시간·기능·생산·관측 등으로 관련될 때 사용한다.

```text
RELATED
```

같은 장면이 둘 이상의 concept에 동시에 해당할 수 있다는 사실은 synonymy나 generic relation을 자동 보증하지 않는다.

### 4.4 명칭 관계와 `MERGE`

`MERGE`는 concept 관계가 아니라 **동일 concept의 명칭 관계**, 즉 synonymy가 확인됐을 때만 사용한다.

다음 조건을 모두 만족해야 한다.

- 동일한 genus
- 동일한 본질·차별 특성
- 동일한 적용 외연
- 서로 치환해도 참·거짓 판정 조건이 바뀌지 않음
- 차이가 명칭·표기·역사적 표현뿐임

차별 특성을 아직 찾지 못했다는 이유만으로 `MERGE`하지 않는다. scoped corpus에서 동일성이 확인되지 않으면 기본값은 `HOLD`다.

### 4.5 정의 초안 gate

정의는 하나의 상위 개념과 하나의 일관된 차별 구조로 작성한다.

다음 표현이 정의문이나 본질 특성에 나타나면 자동 판결하지 않고 **판정을 중단해 HOLD**한다.

- 서로 다른 표상 대상을 잇는 `및`
- 차별 특성 대신 예시를 열거하는 `~와 같은`
- 선택적 소속 조건인 `중 일부를`
- 외연을 정의 안에서 확장하는 `포함할 수 있다`

검사 순서:

```text
표현 감지
→ 단일 genus + differentia로 재작성 시도
→ 외연 문장은 관계 절로 이동
→ 재작성 뒤에도 복수 내포가 남으면 혼합 concept 후보
→ cluster 재분석
```

이 gate는 기계적 분할기가 아니다. 정상적인 복합 차별 특성까지 금지하지 않으며, 애매한 판단이 정의되지 않은 라벨을 통해 통과하는 것을 막는 중단 장치다.

### 4.6 concept 판정

- `HOLD`: 기본값. 근거·사례·관계·정의가 충분하지 않음.
- `KEEP`: 현재 인간 연구 어휘에서 독립적으로 유지할 차별 특성과 대비 사례가 확인됨.
- `ENGINE-ONLY`: 본질적 차별 특성이 구현·protocol 구조에서만 성립함.
- `HISTORICAL-ONLY`: 과거 계보를 설명하지만 현재 연구 어휘에는 독립 concept로 불필요함.
- `MERGE`: synonymy가 확인돼 대표 C-ID 하나로 통합함.

`MERGE`, generic, partitive, associative를 서로 대체하지 않는다.

### 4.7 C-ID 발급 조건

관계는 항상 기록할 수 있지만 C-ID는 기본적으로 열지 않는다.

새 C-ID를 열려면 다음이 필요하다.

- 단일 genus와 일관된 차별 구조
- 형제 후보와 갈라지는 차별 특성
- 그 차이를 보여주는 코퍼스 확인 사례 또는 독립 관측 사례
- 기존 C-ID에 synonymy로 통합되지 않음
- subject field·과정 전체·구현 목록이 아님

조건이 부족하면 다음처럼 남긴다.

```text
후보: PerformedAction
관계: NARROWER-CANDIDATE-OF C0002
상태: HOLD
재개 조건: generic occurrence와 가르는 긍정 대비 확보
```

### 4.8 공통 규칙

1. 개념은 명칭보다 먼저다.
2. 한 concept 파일에는 한 개념만 둔다.
3. C-ID는 이름과 주제를 인코딩하지 않는다.
4. historical mention과 current use를 구분한다.
5. 엔진 분리가 인간 ontology를 허가하지 않는다.
6. 근거 부족과 `ENGINE-ONLY`를 구분한다.
7. 현재 사용 근거만으로 인간 concept를 `KEEP`하지 않는다.
8. 다른 조사로 넘긴 후보의 목적지와 재개 조건을 남긴다.
9. 모든 용례를 영구 목록으로 만들지 않고 대표 근거를 연결한다.
10. 정의는 상위 개념과 차별 특성으로 작성하고 외연 관계를 정의문에 넣지 않는다.
11. 권장 명칭은 특성과 정의가 안정된 뒤 정한다.
12. 같은 흐름·파일·runtime residence는 concept 동일성 근거가 아니다.

## 5. 조화 규칙

### 통합

둘 이상의 C-ID가 synonymy 조건을 모두 만족한다고 확인되면 대표 ID 하나를 유지한다. 다른 ID는 대표 ID와 조화 기록을 가리키는 안내만 남긴다.

### 분할

하나의 C-ID가 둘 이상의 독립 내포를 섞었다고 확인되면 원본 ID를 어느 한쪽에 임의로 넘기지 않는다.

- 원본 ID의 판정을 `HOLD`로 내린다.
- 혼합된 후보를 cluster에 분리해 기록한다.
- 각 후보의 관계와 대비 사례를 다시 확인한다.
- 새 concept마다 발급 조건을 충족할 때만 새 ID를 연다.
- 분할이 확정되면 원본 ID는 분할 안내만 보존한다.
- 프로젝트 색인과 역참조를 실제 의미에 맞게 갱신한다.

### 관계 교정

`MERGE`로 잘못 기록한 generic·partitive·associative 관계는 동일성 판정을 철회하고 관계 후보와 `HOLD`로 되돌린다. 이전 판정을 숨기지 않고 harmonization에 교정 이유를 남긴다.

## 6. glossary 발행 조건

```text
관련 입력 배치
→ cluster concept 분석
→ 필요한 조화
→ 안정된 정의와 명칭
→ 범위가 명시된 glossary
→ 현재 이론의 use만 개명
```

첫 glossary는 반영한 입력 배치를 상단에 명시한다. 조사하지 않은 Chapter나 계보의 용어를 승인하거나 폐기한 것으로 간주하지 않는다.

기존 `models/<model>/prompt.md`와 평가는 정확한 모델 artifact이므로 조용히 개명하지 않는다. 새 용어를 반영하려면 기존 모델을 보존하고 새 프롬프트 모델을 만든다.

## 7. 현재 단계에서 하지 않는 것

- 권장 명칭과 glossary 확정
- 현재 문서 전면 rename
- 별도 시나리오 디렉터리·PASS/FAIL suite
- 자동 status registry
- 엔진 타입을 인간 구조로 자동 승격
- 근거가 부족한 후보의 대량 C-ID 발급
- relation 후보를 synonymy로 간주한 대량 `MERGE`

현재 단계는 기존 C0001~C0009의 concept cardinality를 감사하고, Chapter 05·06 action/outcome cluster에서 잘못 사용한 `MERGE`를 generic·partitive·associative 관계와 `HOLD`로 교정하는 것이다.