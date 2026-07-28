# Chapter 05 Terminology Intake — Basic Term List

이 문서는 Chapter 05의 역사적 명칭과 기호에서 `extraction-map.md`의 후보 항목으로 들어가는 색인이다. 후보의 정의나 설명을 복제하지 않는다.

| 역사적 명칭 | 관찰된 역할 | 추출 항목 | concept ID | 다음 확인 |
|---|---|---|---|---|
| Spine | 충돌 문서의 해석·적용 우선순위 | X-CH05-001 | 미할당 | canon adoption·execution participation과 구분 |
| module priority | 누수 봉인 역할에 따른 적용 순서 | X-CH05-001 | 미할당 | 최신 날짜순과 구분 |
| 9U | readout same-tick 권한 금지 헌법 | X-CH05-001 / X-CH05-005 | 미할당 | Chapter 04 영향 경계와 대조 |
| append-only | 과거 문장을 삭제하지 않고 보존 | X-CH05-002 / X-CH05-006 | 미할당 | 현재 실행 권한과 구분 |
| textual persistence | 문서 안에 계속 남아 있음 | X-CH05-002 | 미할당 | interpretive priority·executable authority와 구분 |
| reference/comment | registry 밖 본문의 비실행 지위 | X-CH05-002 / X-CH05-003 | 미할당 | historical reference와 adoption 구분 |
| Registry-First | 본문 삽입 전 실행 참여 항목 등록 | X-CH05-003 | 미할당 | registration·linking·adoption 구분 |
| Module Registry | 실행 참여 module 목록 | X-CH05-003 | 미할당 | self-boundary로 승격 금지 |
| registered | registry에 등재된 상태 | X-CH05-003 | 미할당 | read·decision·write 권한 자동 승인 금지 |
| Skeleton | 경계·timebase·interface 조립틀 | X-CH05-004 / X-CH05-007 | 미할당 | 인간 구조와 자동 동일시 금지 |
| Interface Sheet | module read/output/no-touch/write 계약 | X-CH05-004 | 미할당 | 내용 설명과 실행 능력 구분 |
| MIM | module interface manifest | X-CH05-004 | 미할당 | Full Spec·Core와 직접 승계 별도 확인 |
| read-set | module이 읽을 수 있는 입력 | X-CH05-004 / X-CH05-009 | 미할당 | decision use·write 권한과 구분 |
| output | module이 산출할 수 있는 값 | X-CH05-004 | 미할당 | persistent write와 구분 |
| no-touch | 명시적으로 금지된 접근·우회 | X-CH05-005 | 미할당 | default deny·absent capability 구분 |
| write-set | module이 쓸 수 있는 대상 | X-CH05-004 / X-CH05-009 | 미할당 | output·record와 구분 |
| effective manifest | append source 중 실제 실행 계약 | X-CH05-006 | 미할당 | historical text·migration record와 구분 |
| TYPE RESIDUE | 의미 교정 뒤 낡은 field/schema 잔존 | X-CH05-006 / X-CH05-027 | 미할당 | 재압축 이력과 관계 확인 |
| `t_eng` | 탐색·비교·canonical 계산 timebase | X-CH05-007 | 미할당 | transition lane과 구분 |
| `t_bio` | LPF·리듬·열 적분 timebase | X-CH05-007 / X-CH05-008 | 미할당 | hidden writer 방지 확인 |
| `t_commit` | SSOT 확정 timebase | X-CH05-007 / X-CH05-020 | 미할당 | commit transaction과 구분 |
| `S_t` snapshot | tick 시작의 current state 입력 경계 | X-CH05-007 | 미할당 | cache·mid-tick state와 구분 |
| Shadow SSOT | registry 밖 지속값이 숨은 writer가 되는 문제 | X-CH05-008 | 미할당 | cache·derived readout과 구분 |
| cache equivalence | cache hit/miss가 결과를 바꾸지 않음 | X-CH05-008 / X-CH05-034 | 미할당 | Gate D 동음 충돌 확인 |
| Gate D | cache equivalence 또는 Shadow SSOT 검사 | X-CH05-008 / X-CH05-034 | 미할당 | 판본별 역할 분리 |
| SSOT Key Registry | key의 class·writer·rate·scope 등록 | X-CH05-009 | 미할당 | label·type·authority 구분 |
| SKR | runtime key registry | X-CH05-009 / X-CH05-010 | 미할당 | version·migration 잔차 확인 |
| KeyRec | key 이름과 scope를 결박한 record | X-CH05-009 / X-CH05-013 | 미할당 | concept identity와 구분 |
| LEDGER | registry label 또는 원장 key class | X-CH05-010 | 미할당 | state residence·authority와 구분 |
| STATE | registry label 또는 active pointer residence | X-CH05-010 / X-CH05-018 / X-CH05-019 | 미할당 | persistent human state와 자동 동일시 금지 |
| VIEW | 비권위 입력·surface registry label | X-CH05-010 / X-CH05-028 | 미할당 | phenomenal surface C0005와 자동 통합 금지 |
| META | audit·metadata registry label | X-CH05-010 / X-CH05-026 | 미할당 | record 권한과 구분 |
| Closure Table | socket별 allow/deny 표 | X-CH05-011 | 미할당 | epistemic closure와 구분 |
| default deny | 표·SKR에 없는 연결 거절 | X-CH05-011 | 미할당 | warrant 승인과 구분 |
| Gate A–D | authority·discount·determinism·snapshot 검사 | X-CH05-011 / X-CH05-034 | 미할당 | 동일 문자 gate의 판본별 역할 확인 |
| IS-CANON | canonical summary socket | X-CH05-012 | 미할당 | policy input 범위 확인 |
| IS-CANDGEN | 다음 candidate manifest 생성 socket | X-CH05-012 / X-CH05-021 | 미할당 | Ghost와 자동 동일시 금지 |
| IS-SELECT | active candidate·policy에서 ID 선택 | X-CH05-012 | 미할당 | selection C0001과 구현 operation 구분 |
| IS-POLICY | next policy ref 생성 socket | X-CH05-012 / X-CH05-018 | 미할당 | C0006과 자동 동일시 금지 |
| IS-COMMIT-DECISION | decision delta 계산 socket | X-CH05-012 / X-CH05-024 | 미할당 | record·rotation parameter 구분 |
| IS-COMMIT-RECORD | audit·next ref 기록 socket | X-CH05-012 / X-CH05-024 / X-CH05-026 | 미할당 | C0004·C0009와 구분 |
| key digest | 전체 KeyRec의 identity digest | X-CH05-013 | 미할당 | content digest와 구분 |
| SerializeNorm_v1 | canonical serialization 규약 | X-CH05-014 | 미할당 | semantic equivalence와 구분 |
| FloatPolicy | 숫자 정규화 규약 | X-CH05-014 | 미할당 | 인간 자원 concept와 무관 |
| HashFn_v1 | normalized payload digest 함수 | X-CH05-015 | 미할당 | concrete algorithm 판본 확인 |
| SHA-256 | Full Spec의 고정 digest 알고리즘 | X-CH05-015 | 미할당 | evidence로 승격 금지 |
| PackRef | immutable payload를 가리키는 digest ref | X-CH05-015 / X-CH05-016 | 미할당 | record·evidence와 구분 |
| PackStore | ref payload 저장·재검증 책임 | X-CH05-016 | 미할당 | STG 실행 stage 누락 확인 |
| verified load | schema/version/rehash 뒤 입력 승인 | X-CH05-016 | 미할당 | source authenticity와 구분 |
| No-RNG | 같은 입력의 실행 재현성 규율 | X-CH05-017 | 미할당 | 세계의 확률성 부정으로 해석 금지 |
| perm-invariant | 입력 순서 변화에 대한 결정론 규율 | X-CH05-017 | 미할당 | truth·legitimacy와 구분 |
| determinism | 동일 입력의 동일 결과 | X-CH05-017 | 미할당 | warrant·legitimate choice와 구분 |
| `policy_act_ref` | 현재 실행이 읽는 active policy pointer | X-CH05-018 | 미할당 | next proposal과 구분 |
| `policy_next_ref` | 같은 tick에 생성되는 next policy pointer | X-CH05-018 / X-CH05-020 / X-CH05-025 | 미할당 | current decision input 금지 확인 |
| `Policy_t` | 현재 active policy | X-CH05-018 | 미할당 | Chapter 04 Policy knob와 경계 |
| `Policy_{t+1}` | 다음 tick용 policy 또는 모호한 미래 이름 | X-CH05-018 / X-CH05-023 | 미할당 | 실제 activation timing 확인 |
| `candidate_manifest_ref` | 현재 Select가 읽는 active candidate pack | X-CH05-019 | 미할당 | candidate 자체와 구분 |
| `candidate_manifest_ref_next` | CandidateGen이 만든 next candidate pack | X-CH05-019 / X-CH05-020 | 미할당 | same-tick activation 금지 확인 |
| CandidateManifestPack | candidate set의 immutable pack | X-CH05-019 / X-CH05-021 | 미할당 | candidate provenance 범위 확인 |
| NextWire | next ref를 commit 뒤 active로 교대하는 경로 | X-CH05-020 | 미할당 | Chapter 04 직접 승계로 단정 금지 |
| rotation assignment | `act_{t+1} := next_t` pointer 교대 | X-CH05-020 / X-CH05-025 | 미할당 | substantive state delta와 구분 |
| CandidateGen | 미래 candidate space를 만드는 operation | X-CH05-021 | 미할당 | C0006·Ghost와 자동 동일시 금지 |
| candidate route | candidate 생성·활성화 경로 | X-CH05-021 / X-CH05-022 | 미할당 | selection authority와 구분 |
| Candidate provenance | ref·route·activation tick 추적 | X-CH05-022 | 미할당 | producer·authorship provenance와 구분 |
| manifest ref | candidate route integrity reference | X-CH05-022 | 미할당 | evidence·source snapshot과 구분 |
| `Cand_t` | STG의 same-tick candidate set | X-CH05-023 | 미할당 | Core active/next route와 비교 |
| ProposeFn | STG candidate 생성 함수 | X-CH05-023 | 미할당 | Story·CandidateGen 승계 미확정 |
| SelectFn | STG same-tick candidate 선택 함수 | X-CH05-023 | 미할당 | SelectIn 옆문 확인 |
| CommitDecisionIn | 선택·canonical impulse·spend 기반 decision input | X-CH05-024 / X-CH05-027 | 미할당 | next ref·audit residue 구분 |
| CommitRecordIn | policy/candidate next·audit record input | X-CH05-024 / X-CH05-026 | 미할당 | decision evidence로 사용 금지 |
| rotation ref | next pointer 복사용 parameter | X-CH05-025 / X-CH05-027 | 미할당 | delta input과 구분 |
| audit_ref | 감사·재현용 참조 | X-CH05-026 / X-CH05-027 | 미할당 | C0004·C0009·evidence와 구분 |
| CommitRecord | commit transaction의 비결정 기록 | X-CH05-026 | 미할당 | occurrence record와 구분 |
| record-only | 결정·ledger delta를 바꾸지 않는 역할 | X-CH05-026 | 미할당 | schema read-cap 실제 봉인 확인 |
| ExternalIn | 외부 text·sensor·marker input | X-CH05-028 / X-CH05-030 | 미할당 | observation·evidence 구분 |
| VIEW_KEYS | 외부 입력의 기본 registry 분류 | X-CH05-028 | 미할당 | canonical grounds over-closure 확인 |
| TR | 외부 입력을 policy-shaped PercIn으로 변환 | X-CH05-029 | 미할당 | transduction·evidence type 구분 |
| PercIn | STG의 policy-shaped perceptual input | X-CH05-029 | 미할당 | external occurrence·C0005와 구분 |
| PhysSig | PercIn에서 파생되는 phys signal | X-CH05-029 | 미할당 | policy-independent grounds 여부 확인 |
| `ΔQ⊥` | policy와 PercIn을 읽는 residual | X-CH05-029 | 미할당 | Chapter 03·04 동명 역할 대조 |
| input admission | 내부 계산 참여 경로가 열림 | X-CH05-030 | 미할당 | evidence·warrant와 구분 |
| evidence gap | 입력과 판정 근거 사이 type 부재 | X-CH05-030 / X-CH05-031 | 미할당 | Chapter 06으로 소급 금지 |
| evidence port | policy-independent attestable grounds 입력 경로 | X-CH05-031 | 미할당 | Chapter 05에는 부재한 요구 |
| grounds starvation | 강한 closure가 정당한 외부 근거도 막는 위험 | X-CH05-031 | 미할당 | over-closure와 구분 |
| OVER-CLOSURE | 합법적 입력·영향까지 함께 차단한 폐쇄 실패 | X-CH05-028 / X-CH05-031 | 미할당 | security rule과 failure mode 구분 |
| STG | 통합 실행 알고리즘 초안 | X-CH05-023 / X-CH05-028~036 | 미할당 | Core 직접 후속·승계로 단정 금지 |
| CommitFn | STG state update 함수 | X-CH05-032 / X-CH05-024 | 미할당 | Record·policy-next read-cap 확인 |
| Decision_t | STG가 commit하는 결정 | X-CH05-033 | C0001 역할 연결 | C0001 synonymy가 아니라 해당 선택 역할만 연결 |
| ActionOut_t | 외부로 내보내는 action output | X-CH05-033 | ENGINE-ONLY | C0002 실제 occurrence를 보증하지 않음 |
| Gate_Action | ActionOut 계산의 실행 gate | X-CH05-033 | ENGINE-ONLY | body authorization·actual occurrence와 구분 |
| action receipt | 실제 행동 occurrence 결박 기록 | X-CH05-033 | 보류 | C0004 NARROWER 후보; configuration Receipt·work/spend record와 구분 |
| outcome receipt | world response 결박 기록 | X-CH05-033 | 보류 | C0003·observation artifact·evidence와 후속 분석 |
| SEALED | 원문이 열거한 특정 우회 경로 봉인 | X-CH05-034 | 미할당 | 전체 이론·구현 완성으로 확장 금지 |
| Gate checklist | spec 수준 검사 항목 | X-CH05-034 | 미할당 | 실행 결과·test evidence와 구분 |
| spec closure | 검사 가능한 계약이 문서에 존재 | X-CH05-034 | 미할당 | verified implementation closure와 구분 |
| Narrative binding | STG Memory/Cache 안의 서사 결박 | X-CH05-035 | 미할당 | writer·scope·Narrative gate 미폐쇄 |
| Memory/Cache | cache·coverage·narrative binding 저장 영역 | X-CH05-035 | 미할당 | autobiographical memory와 자동 동일시 금지 |
| phys authority | STG가 Memory/Cache에 부여한 authority 표현 | X-CH05-035 | 미할당 | epistemic·social authority와 구분 |
| Gate C1 | verified PackRef만 허용한다는 STG 요구 | X-CH05-036 | 미할당 | 실제 verifier stage 존재 확인 |
| verified PackRef | 검증됐다고 선언된 pack reference | X-CH05-036 | 미할당 | declarative requirement와 execution 구분 |
| load stage | ref schema·digest 재검증 책임 stage | X-CH05-016 / X-CH05-036 | 미할당 | STG F 내부 부재 확인 |

## 사용 규칙

- 후보 설명을 바꾸려면 `extraction-map.md`만 수정한다.
- 같은 철자가 여러 역사적 역할을 맡으면 여러 추출 ID를 연결한다.
- Core와 STG에 같은 기능명이 나타나도 직접 승계·동일 schema를 보증하지 않는다.
- registry·socket·key·PackRef는 현재 인간 ontology의 concept 이름으로 자동 승격하지 않는다.
- `registered`, `linked`, `executable`, `writable`, `warranted`를 같은 상태로 합치지 않는다.
- C-ID 연결과 synonymy는 다르다. generic·partitive·associative 관계 후보는 `보류`와 다음 확인을 기록한다.
