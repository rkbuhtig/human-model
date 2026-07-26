# Current Research Terminology Intake — Basic Term List

이 문서는 현재 조사 명칭에서 `extraction-map.md`의 후보 항목으로 들어가는 색인이다. 후보 내용과 정의를 복제하지 않는다.

| 조사 명칭 | 현재 사용 맥락 | 추출 항목 | concept ID | 다음 확인 |
|---|---|---|---|---|
| `Commit` | reducer proposal–commit instrumentation | X-CURR-020 | 미할당 | 구현 적용과 인간 개념을 분리 |
| `committed_delta` | bound 이후 persistent state에 실제 반영된 displacement | X-CURR-020 | 미할당 | Quench/Application 계보와 대조하되 자동 동일시 금지 |
| `commit` | Git 이력·baseline commit | X-CURR-020 | 해당 없음 | 저장소 일반어로 분류 |
| `Commit` | notes/checkpoints의 역사 계보 언급 | X-CURR-020 | 미할당 | historical mention 유지 |
| `Event` | 루트 README의 일반 사건 | X-CURR-021 | 미할당 | 일반 자연어와 기술 타입 구분 |
| `event` | RFC 0002의 FlowUpdate/EventJump | X-CURR-021 | 미할당 | 상태 전이 연산과 occurrence 구분 |
| `event count` | burst/spaced 비교의 사건 수 | X-CURR-021 | 미할당 | occurrence count와 mental transition 구분 |
| `event property` | RFC 0004의 보편 점화 속성 금지 | X-CURR-021 | 미할당 | 단일 Event scalar 폐기 근거 |
| `occurrence` | 원천 발생과 동일성 | X-CURR-005 | 미할당 | Chapter Event 실제 발생과 대조 |
| `delivery` | occurrence 전달 동일성 | X-CURR-006 | 미할당 | transport redelivery와 재노출 구분 |
| `CurrentReexposure` | 현재의 별도 재노출 occurrence | X-CURR-006 | 미할당 | memory access와 경계 |
| `CurrentAccessOccurrence` | 회상·연상·현재 encounter 접근 | X-CURR-006 | 미할당 | protocol reexposure와 동일 타입 아님 |
| `processed occurrence` | 엔진이 실제 처리한 입력 | X-CURR-007 | 미할당 | qualified transition과 구분 |
| `Qualified Mental Transition` | Q 정책을 통과한 전이 | X-CURR-008 | 미할당 | 인간 전이 개념으로 승격 보류 |
| `JOT` | court-cycle·sketch stream·store의 역사 충돌 언급 | X-CURR-022 | 미할당 | 현재 권장 용어로 유지할 근거 확인 |
| `JOT.court` | 판정 계열의 역사적 명칭 | X-CURR-013 | 미할당 | BindingAdjudicationReceipt와 직접 동일시 금지 |
| `JOT store` | 미확정 재료 저장의 역사적 명칭 | X-CURR-010 | 미할당 | EpisodeMaterialReference·persistent store와 경계 |
| `Quench` | 현행 research 직접 use 미확인 | X-CURR-023 | 미할당 | Chapter 02·03·후속 자료에서만 조사 |
| `Candidate` | 행동·해석·조립 전 후보 | X-CURR-001 / X-CURR-011 / X-CURR-012 | 미할당 | 서로 다른 후보 종류를 한 concept로 묶지 않음 |
| `Intent` | 수행 이전 의도 | X-CURR-002 | 미할당 | 선택·시도·수행과 경계 |
| `Attempt` | 수행 시도 | X-CURR-002 | 미할당 | intent/performance 사이 별도 개념 필요성 |
| `Performance` | 행동 수행 과정 | X-CURR-002 / X-CURR-003 | 미할당 | ActionOccurrence와 경계 |
| `ActionOccurrence` | 행동이 실제로 발생한 사실 | X-CURR-003 | 미할당 | Chapter Commit/Event 실제 발생과 대조 |
| `WorldOutcome` | 행동 뒤 세계 결과 | X-CURR-004 | 미할당 | occurrence와 자기 피드백 구분 |
| `SubjectiveEncounterFormProxy` | 현재 접근의 descriptive encounter proxy | X-CURR-009 | 미할당 | actual qualia·evidence와 구분 |
| `EpisodeMaterialReference` | 조립 독립 material handle | X-CURR-010 | 미할당 | 기억 저장소나 Episode 자체가 아님 |
| `EpisodeAssemblyCandidate` | 아직 통합되지 않은 조립 후보 | X-CURR-011 | 미할당 | CandidatePack·Episode integration과 대조 |
| `InterpretiveBindingCandidate` | 일시적 해석 후보 | X-CURR-012 | 미할당 | Narrative write 권한 없음 |
| `BindingAdjudicationReceipt` | 해석 후보 판정 기록 | X-CURR-013 | 미할당 | 인간 판단 과정과 receipt 구분 |
| `EpisodeIntegrationReceipt` | detached-lab 통합 결과 기록 | X-CURR-014 | 미할당 | durable writer·canonical Episode 아님 |
| `SubjectiveBelief` | 현재 믿음 | X-CURR-015 | 미할당 | EvidenceAssessment와 구분 |
| `EvidenceAssessment` | 증거에 대한 평가 | X-CURR-015 | 미할당 | world truth·belief·warrant와 구분 |
| `receipt` / `record` | provenance와 판정 보존 | X-CURR-016 | 미할당 | persistent state와 write authority 구분 |
| `readout` | 현재 표면·관측 출력 | X-CURR-017 | 미할당 | writable state와 경계 |
| `Narrative write` | 느린 상태에 대한 write 후보 | X-CURR-014 / X-CURR-017 | 미할당 | 현재 readout과 자동 연결 금지 |
| `후회` / `책임 수용` / `수리` | 행동 결과 이후 자기평가와 후속 변화 | X-CURR-018 | 미할당 | 지지·책임·사과·수리·채택 분리 |
| `Episode 잔여` / `Narrative 변화` | 여러 사건 뒤 지속 경로 변화 | X-CURR-019 | 미할당 | stored trace·trajectory·Narrative 구분 |

## 사용 규칙

- 후보 설명은 `extraction-map.md`만 수정한다.
- 한 명칭이 여러 후보 종류에 쓰이면 여러 추출 ID를 연결한다.
- 현재 사용이 없다는 사실은 ENGINE-ONLY 판정이 아니다.
- concept 단계가 시작되면 같은 개념으로 확인된 여러 행만 하나의 C-ID에 연결한다.
- 구현 타입명과 인간 연구 용어가 같은 철자를 사용해도 자동 통합하지 않는다.
