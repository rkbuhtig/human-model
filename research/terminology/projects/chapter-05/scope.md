# Chapter 05 Terminology Intake — Scope

## 1. 조사 질문

Chapter 04가 `Influence ≠ Authority`를 유지한 채 다음 tick의 탐색·비교·작업에 닿는 경로를 만들었다면, Chapter 05는 그 규율을 **문서와 모듈이 실제 실행에 참여하는 계약**으로 바꾸는 과정을 추출한다.

이 배치는 다음 연속성을 중심으로 읽는다.

```text
Chapter 04
readout은 현재 선택·원장·persistent writer를 직접 행사하지 못함
→ 다음 tick의 탐색·비교·후보 편성에는 제한된 영향 가능

→ Chapter 05
문장이 존재한다고 실행되는 것은 아님
→ registry·interface·socket·closure를 통과한 연결만 실행 참여
→ current/next pointer와 candidate route를 commit에서 교대
→ decision과 record를 같은 transaction 안에서도 분리
```

핵심 질문은 다음과 같다.

```text
보존되어 있음
≠ 현재 정본으로 채택됨
≠ 실행 graph에 연결됨
≠ 상태 전이 권한을 가짐

등록되어 있음
≠ 모든 함수가 읽을 수 있음
≠ 결정 입력으로 사용할 수 있음
≠ 상태를 쓸 수 있음

재현 가능함
≠ source가 authentic함
≠ claim이 참임
≠ 결정이 정당함

결정이 commit됨
≠ 행동이 실제 세계에서 발생함
≠ 세계 결과가 성립함
```

## 2. 연대기 독해 원칙

Chapter 05는 2026년 1월 17일 한 날짜 안에서 빠르게 이어진 여러 factory 판본과 후기 병렬 branch를 복원한다. 필요한 명칭만 개별적으로 뽑지 않고, 앞선 판본의 실제 누수를 뒤 판본이 어떻게 표·socket·key·pointer로 좁혔는지 상대 순서대로 읽는다.

```text
SP17    Spine v0.2.3
→ SK17  Skeleton v0.3b
→ MIM17 Module Interface Manifest v0.1
→ SS17  Spine+Skeleton v0.3c
→ C04B17 Executable Canon v0.4b
→ MF17  Build Step v0.4c
→ FS17  Full Spec v0.4d + Addendum A
→ SOC17 Core Socket Contract v1.0
→ CL17  Closure Tables v1.1
→ CORE17 Core v1.2 + v1.2a-SEAL

후기 병렬 branch:
STG17 Executable Canon v0.5-STG
```

다음 관계를 자동 승계로 읽지 않는다.

- `STG17`은 `CORE17`을 자신의 명시 source set으로 선언하지 않는다.
- Core branch의 socket·closure 봉인과 STG branch의 single-transition `F`는 기능적으로 비교하지만 textual descendant 관계를 확정하지 않는다.
- 같은 날짜와 같은 9U 규율을 공유한다는 사실만으로 모든 타입·socket·gate가 승계됐다고 보지 않는다.
- `fornext`, `FUULL`처럼 byte-identical 결합된 합본은 새 개념의 최초 출처로 중복 계상하지 않는다.
- 후대 Chapter 06의 Witness·Grounds·Receipt·Bill을 Chapter 05의 숨은 완성형으로 소급하지 않는다.

## 3. 선행 입력

이 프로젝트는 최신 `main`의 다음 terminology 결과를 전제한다.

- `projects/chapter-02/`
- `projects/chapter-03/`
- `projects/chapter-04/`
- `projects/current-research/`
- `termbase/concepts/C0001.md` — 행동 경로 선택
- `termbase/concepts/C0002.md` — 외부 occurrence
- `termbase/concepts/C0003.md` — 세계 결과 상태
- `termbase/concepts/C0004.md` — occurrence record
- `termbase/concepts/C0005.md` — 현재 체험 표면
- `termbase/concepts/C0006.md` — 비권위적 미래 편성 영향
- `termbase/concepts/C0007.md` — 실제 탐색·비교 노동
- `termbase/concepts/C0008.md` — 실제 자원 지출
- `termbase/concepts/C0009.md` — 수행·지출 회계 기록 (`ENGINE-ONLY`)

Chapter 05 후보는 이 concept들의 경계를 비출 수 있지만, 이번 입력 배치에서 concept 파일을 자동 수정하거나 새 C-ID를 열지 않는다.

## 4. 주 입력

- `chapters/chapter-05-document-runtime-factory-0117.md`

Chapter가 구분한 다음 지층을 따른다.

```text
Spine
  해석·적용 우선순위와 9U 헌법

Skeleton
  timebase·snapshot·module read/output/no-touch/write 계약

Manifest / Full Spec
  Registry-First, key registry, serialization, empty socket, Addendum

Socket / Closure
  key·pack ref·socket별 allow/deny, active/next 교정

Core
  CandidateGen, NextWire, Commit-Decision / Commit-Record, v1.2a-SEAL

STG
  같은 문제군을 single-transition F로 다시 접은 후기 병렬 branch
```

역사 본문과 연구 후기를 구분한다. 연구 후기가 제시한 `Preservation ≠ Adoption ≠ Executable participation`, `Authority at transition`, 계보 등급은 Chapter 내부 지층을 대조한 합성이지 각 원문이 그대로 선언한 단일 공식이 아니다.

## 5. 보조 입력

다음 파일은 선행 후보·concept와의 경계를 확인하는 데만 사용한다.

- `research/terminology/projects/chapter-04/extraction-map.md`
- `research/terminology/projects/chapter-04/basic-term-list.md`
- `research/terminology/projects/chapter-04/touched-concepts.md`
- `research/terminology/projects/chapter-03/extraction-map.md`
- `research/terminology/projects/current-research/extraction-map.md`
- `research/terminology/termbase/concepts/C0004.md`
- `research/terminology/termbase/concepts/C0006.md`
- `research/terminology/termbase/concepts/C0009.md`
- `notes/interchapter-note-04a-flow-boundary-decision-checkpoint.md`

Chapter 06 이후 문서는 Chapter 05의 공백을 소급해서 닫는 정답으로 사용하지 않는다.

## 6. 출처별 주장 권한

| 출처 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| Chapter 05 역사 본문 | 당시 문서·key·module·socket·pointer가 어떤 실행 참여 역할과 금지 경로를 가졌는가 | 그 구조가 인간 정신의 독립 메커니즘임 |
| Chapter 05 연구 후기 | 판본 간 교정·비채택·재발 누수·현행 구조와의 기능 계보 | 원문이 현행 Witness·Evidence·Authority ontology를 이미 완성함 |
| Chapter 03·04 배치 | readout influence, next-tick policy, work/accounting 경계의 선행 문제 | Chapter 05 factory 타입과 concept 동일성 확정 |
| current-research 배치 | 현행 record·provenance·readout·writer 구분의 현재 사용 | runtime interface를 인간 ontology로 승인 |
| C0004 | occurrence record의 현재 경계 | 모든 audit·decision·pack record를 occurrence record로 통합 |
| C0006 | 비권위적 미래 영향의 현재 경계 | CandidateGen·Policy socket을 인간 영향 concept와 동일시 |
| C0009 | 기술 회계 기록의 ENGINE-ONLY 경계 | 모든 CommitRecord·Trace를 하나의 회계 concept로 통합 |

Chapter 05는 주로 executable specification과 archive lineage를 다룬다. 인간적 surface와 사례가 등장해도 독립 인간 현상 근거나 인간 일반에 대한 경험적 검증으로 사용하지 않는다.

## 7. Core와 STG 처리 규칙

Core branch와 STG branch를 하나의 완성 schema로 합치지 않는다.

```text
CORE17
= key-level registry·socket·closure·ref 검증·NextWire를 세밀하게 봉인

STG17
= 인간 surface와 상태 변화를 single-transition F 안에 읽기 쉽게 재배열

둘의 기능 비교
≠ 직접 승계
≠ 자동 합집합
≠ 한 branch의 누락을 다른 branch가 공식 보완했다는 판정
```

다음은 `CROSS-BRANCH COMPARATIVE OMISSION`으로만 기록한다.

- STG 실행면에 Core의 candidate NextWire 대응 봉인이 보이지 않음
- STG `CommitFn`에서 Record·policy-next의 read-cap이 충분히 분리되지 않음
- STG에 PackRef 검증 책임 stage가 보이지 않음
- STG의 ActionOut과 committed Decision을 결박하는 receipt가 없음

이를 공식 rollback이나 기능 폐기로 부르지 않는다.

## 8. 우선 대조할 선행 후보와 concept

- X-CH03-023 — readout·proposal influence
- X-CH03-024 — next-tick delay
- X-CH03-026 — proposal / selection / application authority
- X-CH03-031 — provenance label
- X-CH03-032 — lane·authority sink
- X-CH03-033 — source access record
- X-CH03-034 — execution dependency trace
- X-CH03-035 — WorkEvent·Billing
- X-CH03-036 — trace와 truth evidence 혼동
- X-CH04-015 — delayed causal lane
- X-CH04-016 — next policy knob
- X-CH04-017 — candidate discovery influence
- X-CH04-018 — same-tick 역주입 금지
- X-CH04-019 — influence provenance 공백
- X-CH04-025~027 — 실패한 X/R/U/A audit와 남은 질문
- X-CH04-030 — outcome / observation / evidence record 공백
- C0004 — occurrence record와 audit·decision record의 경계
- C0006 — 미래 편성 영향과 CandidateGen·Policy operation의 경계
- C0009 — 수행·지출 회계 기록과 일반 audit/decision record의 경계

## 9. 조사 원칙

1. 문서의 보존, 정본 채택, registry 등록, socket 연결, 실행 참여, state write를 분리한다.
2. module 이름의 의미적 중요성과 interface capability를 분리한다.
3. `registered`를 모든 read·decision·write 권한의 승인으로 해석하지 않는다.
4. registry label을 type·residence·authority와 자동 동일시하지 않는다.
5. content digest와 PackRef가 보장하는 integrity·reproducibility를 source authenticity·truth와 분리한다.
6. CandidateGen을 중립 전처리로 취급하지 않고 선택 공간을 바꾸는 influence로 추출한다.
7. current active pointer와 same-tick 생성 next pointer를 분리한다.
8. commit transaction에 함께 들어간 field가 같은 결정 권한을 가진다고 보지 않는다.
9. decision input, pointer rotation parameter, audit record를 분리한다.
10. deterministic selection을 legitimate or warranted selection으로 승격하지 않는다.
11. ExternalIn을 VIEW로 닫은 봉인과 evidence port 부재를 함께 기록한다.
12. single-transition `F`를 내부 역할 분리가 끝난 완성 ontology로 취급하지 않는다.
13. `SEALED`의 범위를 원문이 열거한 우회 경로 밖으로 확장하지 않는다.
14. spec closure와 실제 구현·test closure를 분리한다.
15. 후보 설명의 단일 권위는 `extraction-map.md`다. `basic-term-list.md`는 명칭 색인만 제공한다.

## 10. 산출물

- `extraction-map.md`: Chapter 05에서 추출한 중립 후보와 관계
- `basic-term-list.md`: 역사적 명칭·기호에서 추출 ID로 들어가는 색인

이번 배치에서는 다음을 만들지 않는다.

- 새 C-ID
- 기존 C0001~C0009 정의 수정
- runtime socket을 concept file schema로 도입
- KEEP / MERGE / ENGINE-ONLY 판정
- harmonization 기록
- glossary
- 현재 문서 rename
- scenario suite·checker·status registry
- runtime/model/code 변경

## 11. 완료 조건

- textual preservation, canon adoption, registry membership, executable participation이 분리된다.
- module interface의 read/output/no-touch/write 역할이 명칭 의미와 구분된다.
- key registration, read scope, decision use, write authority가 서로 다른 판정으로 추출된다.
- normalized serialization·digest·PackRef integrity가 authenticity·truth와 구분된다.
- active/next policy와 candidate manifest의 activation lane이 추적된다.
- CandidateGen influence가 selection authority와 분리된다.
- CommitDecision, pointer rotation, CommitRecord가 같은 권한으로 합쳐지지 않는다.
- ExternalIn over-closure와 evidence port 부재가 함께 기록된다.
- Core와 STG의 비교가 직접 승계·rollback 주장으로 과장되지 않는다.
- ActionOut, actual occurrence, world outcome, outcome receipt가 구분된다.
- spec closure와 verified implementation closure가 분리된다.
- Chapter 06 개념을 Chapter 05의 숨은 정답으로 소급하지 않는다.
