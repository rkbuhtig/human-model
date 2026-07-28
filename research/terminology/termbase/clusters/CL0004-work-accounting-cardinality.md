# CL0004 — 수행 노동·회계 기록 cardinality 감사

## cluster 질문

C0007과 C0009는 각각 하나의 concept인가, 상위 concept인가, 과정 전체인가, 아니면 subject field label인가?

## 입력 후보

- `C0007` — 실제 탐색·비교·재표현·수리 노동
- `C0009` — 수행·지출 회계 기록
- `X-CH03-034~035` — dependency trace·work/cost record
- `X-CH04-004`, `X-CH04-023` — 호출된 노동과 실제 scan·compare work
- `X-CH05-024~027` — decision input·rotation parameter·audit record 분리
- `X-CH06-001`, `X-CH06-019` — repair demand·actual repair·settlement 분리
- `X-CH06-018`, `X-CH06-025~026` — Bill·LedgerCore 역할 과적재

## C0007 감사

현재 정의의 `탐색·비교·재표현·수리와 같은 처리`는 differentia 대신 예시 목록을 사용한다.

분리해야 할 질문:

```text
탐색 노동은 수행 노동의 종인가?
비교 노동은 수행 노동의 종인가?
탐색과 비교는 하나의 노동 과정의 부분 단계인가?
재표현은 독립 활동인가, 수리 과정의 수단인가?
수리는 탐색·비교 결과를 사용하는 연관 활동인가?
```

현재 코퍼스는 `요구됨 ≠ 수행됨`, `수행됨 ≠ 성공함`, `수행됨 ≠ 비용` 경계를 지지한다. 그러나 탐색·비교·재표현·수리 사이의 generic/partitive 관계를 결정할 대비는 부족하다.

### 판정

- C0007의 `KEEP`을 철회한다.
- 현재 상태: `HOLD`.
- C0007 ID는 삭제하지 않고 재분석 중인 후보 경계를 보존한다.
- 새 하위 C-ID는 열지 않는다.

### 재개 조건

- 탐색·비교·재표현·수리 각각의 완료 조건
- 같은 과정 안의 부분 단계인지 독립 종개념인지 보여주는 코퍼스 대비
- 인지 노동·사회적 수리·신체 수행을 같은 genus 아래 둘 근거

## C0009 감사

현재 정의는 다음 표상 대상을 접속한다.

```text
수행됐다는 사실
수행량
금액·자원 지출
참조
의존성
귀속
```

특성표의 `중 일부를 다시 감사할 수 있게 한다`는 단일 concept의 본질이 아니라 기술 기록 주제 분야의 소속 조건이다.

### 분리 후보 inventory

| 후보 | 표상 대상 | 정확성 질문 | 현재 관계 |
|---|---|---|---|
| work-performance record | 어떤 노동이 수행됐는가 | 실제 수행과 일치하는가 | C0007 RELATED |
| work-quantity record | 수행량·처리량 | 단위와 측정 규칙이 타당한가 | HOLD |
| expenditure record | 어떤 자원이 얼마나 소비됐는가 | 실제 지출 C0008과 일치하는가 | C0008 RELATED |
| dependency trace | 어떤 실행·입력에 의존했는가 | provenance graph가 정확한가 | ENGINE 후보 |
| attribution record | 수행·비용이 누구·무엇에 귀속되는가 | attribution rule이 타당한가 | HOLD |
| occurrence record | occurrence가 성립했는가 | C0004 경계 | C0004, 별도 |
| claim evidence | 특정 claim을 무엇이 지지하는가 | evidence/warrant 경계 | evidence cluster |

이 후보들은 같은 record 계열에 연관될 수 있지만 표상 대상과 정확성 조건이 다르다.

### 판정

- C0009의 `ENGINE-ONLY` concept 판정을 철회한다.
- 현재 상태: `HOLD / SUBJECT-FIELD SPLIT`.
- C0009는 위 inventory와 분할 필요를 가리키는 임시 원본 ID로 유지한다.
- 분리 후보는 발급 조건을 충족할 때까지 새 C-ID를 받지 않는다.

### 재개 조건

- 각 record 후보의 단일 genus + differentia 정의
- 실제 구현 artifact에서 표상 대상별 독립 사용 확인
- work record와 spend record가 서로 치환되지 않는 사례
- dependency trace와 attribution record의 정확성 판정 차이

## generic / partitive / associative 질문

| 후보 쌍 | generic | partitive | associative |
|---|---|---|---|
| 수행 노동 / 탐색 노동 | 종개념 가능성 | 탐색 단계 가능성 | 노동이 탐색을 포함·호출할 수 있음 |
| 수행 노동 / 수리 노동 | 종개념 가능성 | 수리 과정의 부분 가능성 | 수리 demand와 actual work가 연관됨 |
| record / work record | 기술 record의 종 가능성 | audit package의 부분 가능성 | work occurrence가 record 발행을 촉발 |
| work record / spend record | 공통 상위 record 가능성 | 하나의 accounting package 부분 가능성 | 같은 수행 장면을 다른 축으로 표상 |
| dependency trace / attribution record | provenance record의 종 가능성 | audit bundle의 부분 가능성 | dependency가 attribution 판단에 사용될 수 있음 |

## definition gate 결과

- C0007: `~와 같은` 감지 → HOLD.
- C0009: `및`, `중 일부를`, 복수 대상 열거 감지 → subject-field split.

## 판정 요약

```text
C0007 KEEP 철회 → HOLD
C0009 ENGINE-ONLY concept 철회 → HOLD / SUBJECT-FIELD SPLIT
새 C-ID → 없음
관계 기록 → generic / partitive / associative 후보만 보존
```

## 역참조

- `../concepts/C0007.md`
- `../concepts/C0008.md`
- `../concepts/C0009.md`
- `../harmonization/H0003.md`
- `../../projects/chapter-05/touched-concepts.md`
- `../../projects/chapter-06/touched-concepts.md`
