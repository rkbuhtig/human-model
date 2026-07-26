# Current Research Terminology Intake — Extraction Map

> 이 지도는 현재 README, RFC, notes, checkpoints가 실제 설명을 위해 요구하는 후보 책임과 관계를 나타낸다. 현재 termbase의 개념체계나 인간 ontology가 아니다.

후보 설명의 단일 권위는 이 파일이다. `basic-term-list.md`는 조사 명칭에서 아래 추출 항목으로 들어오는 색인만 제공한다.

## A. 가능성·선택·행동 수행

### X-CURR-001 — 여러 행동 후보 가운데 이후 행동 경로가 선택됨

- 현재 근거: 루트 README의 가능성→선택→실제 수행 흐름; RFC 0001의 Candidate 경계
- 함께 구분할 후보: X-CURR-002, X-CURR-003
- Chapter 02 대조: X-CH02-001
- 주의: 후보 생성기나 평가 점수와 같은 엔진 구현 단계를 인간 내부 단계로 자동 승인하지 않는다.

### X-CURR-002 — 의도·시도·수행이 서로 다른 상태나 과정으로 취급됨

- 현재 근거: RFC 0001의 `Candidate ≠ Intent ≠ Attempt ≠ Performance`
- 함께 구분할 후보: X-CURR-001, X-CURR-003
- Chapter 02 대조: Commit의 선택·표현·발생 혼합
- 다음 확인: 이 분리가 인간 설명에 필요한 경계인지 계약·trace 구조의 세분인지

### X-CURR-003 — 수행이 실제 행동 발생으로 이어짐

- 현재 근거: RFC 0001의 `Performance ≠ ActionOccurrence`
- 함께 구분할 후보: X-CURR-002, X-CURR-004, X-CURR-005
- Chapter 02 대조: X-CH02-003
- 다음 확인: 수행 과정과 완료된 발생 사실의 경계

### X-CURR-004 — 행동 이후 세계에 별도 결과가 생김

- 현재 근거: RFC 0001의 `ActionOccurrence ≠ WorldOutcome`; 루트 README의 행동 결과와 피드백
- 함께 구분할 후보: X-CURR-003, X-CURR-018
- Chapter 02 대조: Event가 위치·경로를 연다는 역할
- 다음 확인: 결과 자체와 그 결과의 자기평가·관계 효과를 분리할지

## B. 발생·전달·접근·시간

### X-CURR-005 — 원천 occurrence가 고유 동일성과 발생 시각을 가짐

- 현재 근거: RFC 0002의 `occurrence_id`, `occurred_at`
- 함께 구분할 후보: X-CURR-003, X-CURR-006, X-CURR-007
- Chapter 02 대조: Event의 실제 발생·timepoint 혼합
- 주의: protocol occurrence 타입이 곧 인간이 경험한 사건 단위라는 뜻은 아니다.

### X-CURR-006 — 같은 원천이 전달·재노출·현재 접근으로 다시 모델에 도달함

- 현재 근거: RFC 0002의 delivery/reexposure; RFC 0004의 CurrentAccessOccurrence
- 함께 구분할 후보: X-CURR-005, X-CURR-007, X-CURR-009
- Chapter 02 대조: 기록됨·기억됨·현재 표면에 나타남의 혼합
- 다음 확인: transport redelivery, psychological reexposure, memory access의 별도 concept 필요성

### X-CURR-007 — 모델이나 엔진이 occurrence를 실제 처리함

- 현재 근거: RFC 0002의 `processed_at`; RFC 0003의 per-processed-occurrence checkpoint
- 함께 구분할 후보: X-CURR-005, X-CURR-006, X-CURR-008
- Chapter 02 대조: Event phase/timepoint와 JOT cycle
- 주의: 처리됨은 정신적으로 유효한 전이나 인간적 의미 형성과 동일하지 않다.

### X-CURR-008 — 처리 결과가 판정 정책 아래 유효한 상태 전이로 계수됨

- 현재 근거: RFC 0003의 Qualified Mental Transition과 qualification receipt
- 함께 구분할 후보: X-CURR-007, X-CURR-019
- Chapter 02 대조: Event hardening·Commit·Quench 경계
- 주의: 현재 Q-v1은 simulation measurement policy이며 인간 전이의 검증이 아니다.

## C. 접수·해석·판정·편입

### X-CURR-009 — 현재 접근이 주관적 encounter 형태의 descriptive proxy를 만듦

- 현재 근거: RFC 0004의 SubjectiveEncounterFormProxy
- 함께 구분할 후보: X-CURR-005, X-CURR-006, X-CURR-010, X-CURR-015
- Chapter 02 대조: Φ surface/readout 후보
- 주의: actual qualia, first-person report, evidence, external occurrence와 동일하지 않다.

### X-CURR-010 — 접근·행동·결과·private trace가 조립과 독립된 material reference로 보존됨

- 현재 근거: RFC 0004의 EpisodeMaterialReference
- 함께 구분할 후보: X-CURR-009, X-CURR-011, X-CURR-014, X-CURR-016
- Chapter 02 대조: JOT store, SSOT, 기록과 상태
- 다음 확인: reference, stored trace, persistent memory의 경계

### X-CURR-011 — 여러 material reference가 아직 통합되지 않은 Episode 조립 후보를 이룸

- 현재 근거: RFC 0004의 EpisodeAssemblyCandidate와 membership candidate
- 함께 구분할 후보: X-CURR-010, X-CURR-012, X-CURR-014
- Chapter 02 대조: CandidatePack과 결론, Episode buffer/write
- 주의: assembly candidate는 이미 통합된 Episode나 Narrative가 아니다.

### X-CURR-012 — 하나의 일시적 해석 후보가 탐색됨

- 현재 근거: RFC 0004의 InterpretiveBindingCandidate; Ghost candidate
- 함께 구분할 후보: X-CURR-011, X-CURR-013, X-CURR-017
- Chapter 02 대조: Potential·Σ·JOT court
- 주의: Ghost 후보와 현재 인간 내부 탐색 메커니즘을 자동 동일시하지 않는다.

### X-CURR-013 — scoped adjudicator가 해석 후보에 판정을 내림

- 현재 근거: RFC 0004의 BindingAdjudicationReceipt; `Ghost candidate ≠ Editor/JOT.court 판정`
- 함께 구분할 후보: X-CURR-012, X-CURR-014
- Chapter 02 대조: X-CH02-012
- 다음 확인: 판정 receipt와 인간의 판단 과정, 승인·지지의 경계

### X-CURR-014 — 판정된 후보가 더 지속적인 Episode·Narrative 수준에 편입되거나 write 후보가 됨

- 현재 근거: RFC 0004의 EpisodeIntegrationReceipt와 authored Episode→Narrative candidate path
- 함께 구분할 후보: X-CURR-010, X-CURR-011, X-CURR-013, X-CURR-017, X-CURR-019
- Chapter 02 대조: Commit의 기억 고착·자기 역사 편입, SSOT·Quench
- 주의: RFC 0004는 durable writer와 canonical Narrative object를 확정하지 않는다.

## D. 사실·믿음·기록·권한

### X-CURR-015 — 주관적 믿음과 증거 평가가 서로 다른 상태로 유지됨

- 현재 근거: RFC 0001의 `SubjectiveBelief ≠ EvidenceAssessment`; RFC 0004의 encounter/evidence/world occurrence 분리
- 함께 구분할 후보: X-CURR-005, X-CURR-009, X-CURR-016
- Chapter 02 대조: “일어난 일, 믿게 된 일, 적용 권한을 얻은 일은 다르다”
- 다음 확인: 사실 근거, 정당화, 현재 믿음, 상태 write 권한의 분리

### X-CURR-016 — record·provenance·receipt가 상태 변화와 별도로 사실과 계보를 보존함

- 현재 근거: RFC 0001의 certification/provenance/lineage; RFC 0002의 occurrence/delivery identity; RFC 0003의 read-only receipt ledger
- 함께 구분할 후보: X-CURR-005, X-CURR-010, X-CURR-015, X-CURR-017
- Chapter 02 대조: X-CH02-007, `Record/JOT ≠ State`
- 주의: 기록 존재가 기록 내용의 진실이나 인간 상태 편입을 자동 보장하지 않는다.

### X-CURR-017 — 현재 readout·surface와 persistent writable state가 분리됨

- 현재 근거: RFC 0004의 readout, material, integration, Narrative write 분리; notes의 `Readout ≠ Writable State`
- 함께 구분할 후보: X-CURR-009, X-CURR-012, X-CURR-014, X-CURR-016
- Chapter 02 대조: Φ/SSOT/Quench와 X-CH02-025
- 다음 확인: current readout, durable trace, write authority의 독립 경계

## E. 결과·자기평가·장기 경로

### X-CURR-018 — 자신의 행동과 결과를 현재 다시 평가하고 지지·책임·수리 방향을 바꿈

- 현재 근거: 루트 README와 models README의 후회·책임 수용·사과 이후 행동 변화·재저자화
- 함께 구분할 후보: X-CURR-004, X-CURR-014, X-CURR-019
- Chapter 02 대조: Commit의 의미 확정·자기 역사 편입·Ledger 정산
- 다음 확인: 현재 지지, 책임 수용, 사과, 수리, 자기 역사 편입을 분리해야 함

### X-CURR-019 — 여러 사건과 전이 뒤 지속 잔여와 장기 경로 변화가 형성됨

- 현재 근거: 루트 README의 Episode 잔여·Narrative 변화; RFC 0003의 persistent state trajectory; RFC 0004의 slow Narrative 후보
- 함께 구분할 후보: X-CURR-008, X-CURR-014, X-CURR-018
- Chapter 02 대조: 신체 흔적·기억 고착·Λ·SSOT
- 다음 확인: residue, stored trace, trajectory, Narrative를 후속 Chapter와 조화

## F. 네 우선 조사 명칭의 현재 지위

### X-CURR-020 — `Commit`은 현재 연구에서 단일 인간 개념보다 구현·계보·일반 Git 의미로 남아 있음

- 현재 확인: RFC 0003의 reducer proposal–commit instrumentation과 `committed_delta`; notes/checkpoints의 역사 계보; 저장소의 Git commit 표현
- Chapter 02 대조: Commit 과적재 전체
- 다음 확인: 각 기술 use를 해당 책임으로 분류하되 현재 인간 용어로 자동 유지하지 않음

### X-CURR-021 — `Event`는 일반 사건 표현과 protocol/type/phase 언어에 넓게 사용됨

- 현재 확인: README의 일반 사건, RFC 0002의 event jump·event count, RFC 0003의 처리 occurrence, RFC 0004의 event property 금지
- Chapter 02 대조: Event occurrence/position/phase/timepoint/hardening
- 다음 확인: 일반 자연어, protocol occurrence, 상태 전이, 기록 경계를 분리

### X-CURR-022 — `JOT`은 현재 새 정본 개념보다 역사적 충돌을 언급하는 명칭으로 남아 있음

- 현재 확인: RFC 0004가 JOT의 court-cycle·sketch stream·store 충돌을 명시하고 canonical object로 승격하지 않음
- Chapter 02 대조: X-CH02-012, X-CH02-013
- 다음 확인: 현재 인간 용어로 유지할 근거가 있는지

### X-CURR-023 — `Quench`는 현행 `research/`의 직접 설명어로 확인되지 않음

- 현재 확인: 검색 결과는 Chapter 계보에 집중됨
- Chapter 02 대조: X-CH02-008, X-CH02-009, X-CH02-010
- 다음 확인: 현재 부재는 ENGINE-ONLY 판정이 아니라 후속 자료 대기다.

## G. 첫 concept 분석 전 대조점

첫 C-ID는 Chapter 02 후보와 현재 연구 후보가 교차할 때만 연다. 우선 비교 대상은 다음이다.

- X-CH02-001 ↔ X-CURR-001/X-CURR-002
- X-CH02-003 ↔ X-CURR-003/X-CURR-005
- X-CH02-007 ↔ X-CURR-016
- X-CH02-012 ↔ X-CURR-013/X-CURR-022
- X-CH02-015/X-CH02-017 ↔ X-CURR-010/X-CURR-014/X-CURR-019
- X-CH02-019/X-CH02-025 ↔ X-CURR-009/X-CURR-017
- X-CH02-018/X-CH02-023 ↔ X-CURR-018

이 대조는 concept 승인표가 아니다. 어떤 후보를 하나로 묶거나 나눌지 다음 단계에서 검토하기 위한 입력이다.
