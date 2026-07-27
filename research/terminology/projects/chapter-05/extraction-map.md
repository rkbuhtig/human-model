# Chapter 05 Terminology Intake — Extraction Map

> 이 지도는 Chapter 05에서 추출된 후보 책임과 관계를 나타낸다. 현재 인간 ontology나 termbase의 정본 개념체계가 아니다.

후보 설명의 단일 권위는 이 파일이다. `basic-term-list.md`는 역사적 명칭에서 아래 추출 항목으로 들어오는 색인만 제공한다.

## A. 보존·채택·실행 참여

### X-CH05-001 — 충돌한 문장의 해석·적용 우선순위가 별도로 정해짐

- 연결된 역사적 명칭: Spine, module priority, 9U
- Chapter 근거: SP17이 최신 날짜순이 아니라 권한·closure·timebase 봉인 역할에 따라 9U→9b→7i→9a→7L→6c→7g/h 우선순위를 둠
- 선행 대조: X-CH03-037의 LAB/RATIONALE/CORE, X-CH04-028의 source set 비채택
- 함께 구분할 후보: X-CH05-002, X-CH05-003, X-CH05-006
- 다음 확인: interpretive priority, canon adoption, executable participation의 경계

### X-CH05-002 — 과거 문장의 보존과 현재 실행 권한이 분리됨

- 연결된 역사적 명칭: append-only, textual persistence, reference/comment
- Chapter 근거: 충돌한 하위 문장을 삭제하지 않되 상위 규칙 아래 authority를 무효화하거나 readout 의미로 격하함
- 선행 대조: C0004, X-CH03-010, Chapter 02의 Persistence ≠ Authority
- 함께 구분할 후보: X-CH05-001, X-CH05-003, X-CH05-006
- 다음 확인: archive preservation, historical reference, canon adoption의 분리

### X-CH05-003 — registry에 등재된 항목만 executable semantics에 참여할 수 있음

- 연결된 역사적 명칭: Registry-First, Module Registry, registered
- Chapter 근거: MF17에서 registry에 없는 본문은 참고·주석으로 존재할 수 있지만 authority·input·commit에 관여하지 못함
- 선행 대조: X-CH03-020의 계산 참여 자격, X-CH03-037의 정본 채택
- 함께 구분할 후보: X-CH05-002, X-CH05-004, X-CH05-010, X-CH05-012
- 다음 확인: registration, linking, execution participation, adoption의 경계

### X-CH05-004 — 모듈 능력이 read/output/no-touch/write 계약으로 제한됨

- 연결된 역사적 명칭: Skeleton, Interface Sheet, MIM
- Chapter 근거: 각 모듈이 본문보다 먼저 read-set, output, no-touch, write-set을 선언함
- 선행 대조: X-CH03-032의 lane·authority sink, X-CH04-025~027의 residence audit
- 함께 구분할 후보: X-CH05-003, X-CH05-005, X-CH05-009, X-CH05-012
- 다음 확인: module capability, information-flow contract, human faculty metaphor의 분리

### X-CH05-005 — 명시적으로 만질 수 없는 대상이 interface 일부가 됨

- 연결된 역사적 명칭: no-touch, forbidden path
- Chapter 근거: 무엇을 읽고 쓰는지뿐 아니라 어떤 우회 경로도 가져서는 안 되는지를 module contract로 선언함
- 선행 대조: X-CH03-032의 READOUT_ONLY, X-CH04-018의 One-Wall/Closure
- 함께 구분할 후보: X-CH05-004, X-CH05-011, X-CH05-012
- 다음 확인: no-touch, deny rule, absent capability의 차이

### X-CH05-006 — append-only source와 실제 effective manifest가 달라질 수 있음

- 연결된 역사적 명칭: effective manifest, append residue, version residue
- Chapter 근거: 후기 patch가 의미를 좁혀도 낡은 식·schema가 문서에 남고, 같은 version 아래 key·rate·field 역할이 바뀜
- 선행 대조: X-CH03-037의 정본 계층, terminology의 경계 재압축 이력
- 함께 구분할 후보: X-CH05-001, X-CH05-002, X-CH05-034
- 다음 확인: historical source, effective executable spec, migration record의 분리

## B. 시간·상태·key 경계

### X-CH05-007 — 서로 다른 timebase와 tick-start snapshot이 실행 입력 경계를 형성함

- 연결된 역사적 명칭: `t_eng`, `t_bio`, `t_commit`, `S_t snapshot`
- Chapter 근거: SK17이 엔진·신체 적분·commit 축을 분리하고 tick 시작의 S_t를 current 계산 입력으로 고정함
- 선행 대조: X-CH03-024, X-CH04-018
- 함께 구분할 후보: X-CH05-008, X-CH05-018, X-CH05-020
- 다음 확인: timebase, transition lane, activation tick의 분리

### X-CH05-008 — tick 사이 지속되거나 cache된 값이 숨은 writer가 되는 것을 금지함

- 연결된 역사적 명칭: Shadow SSOT, cache equivalence, Gate D
- Chapter 근거: 지속값은 SSOT에 기록되거나 S_t에서 순수 재구성 가능해야 하고 cache hit/miss가 결과를 바꾸면 안 됨
- 선행 대조: C0008의 persistent resource 대조, Chapter 02의 Persistence ≠ Authority
- 함께 구분할 후보: X-CH05-007, X-CH05-009, X-CH05-034
- 다음 확인: cache, derived value, persistent state, hidden writer의 경계

### X-CH05-009 — key마다 class·writer·rate·read scope·write scope가 결박됨

- 연결된 역사적 명칭: SSOT Key Registry, SKR, KeyRec
- Chapter 근거: MF17·SOC17·CORE17이 key 이름 외에 label/axis/rate/writer/read/write scope를 등록함
- 선행 대조: X-CH03-031의 AttrSet/LabelSet, X-CH04-027의 Residence/Flow/Attribution 질문
- 함께 구분할 후보: X-CH05-004, X-CH05-010, X-CH05-013
- 다음 확인: key metadata, runtime type, authority grant의 분리

### X-CH05-010 — registry label이 residence·type·authority와 동일하지 않음

- 연결된 역사적 명칭: LEDGER, STATE, VIEW, META label
- Chapter 근거: MF17의 SSOT 3분류가 FS17에서 실행기가 추적할 key label로 넓어지고 label이 type이 아니라고 제한됨
- 선행 대조: X-CH04-025~027의 X/R/U/A 실패
- 함께 구분할 후보: X-CH05-003, X-CH05-009, X-CH05-011
- 다음 확인: classification label, storage residence, transition authority의 직교성

### X-CH05-011 — 표와 registry에 없는 연결은 기본 deny됨

- 연결된 역사적 명칭: Closure Table, default deny, Gate A–D
- Chapter 근거: CL17이 table·SKR·label·PackRef 검증을 통과하지 않은 socket input을 거절함
- 선행 대조: X-CH03-032의 authority lane, X-CH04-018의 Closure
- 함께 구분할 후보: X-CH05-005, X-CH05-010, X-CH05-012
- 다음 확인: information-flow closure, authorization, epistemic warrant의 분리

### X-CH05-012 — socket 연결 가능성이 구체적인 입력 계약으로 판정됨

- 연결된 역사적 명칭: IS-CANON, IS-CANDGEN, IS-SELECT, IS-POLICY, IS-COMMIT-DECISION, IS-COMMIT-RECORD
- Chapter 근거: SOC17·CORE17이 module 설명을 tick 내부 socket input/output/no-touch 계약으로 바꿈
- 선행 대조: X-CH03-026의 proposal/selection/application authority
- 함께 구분할 후보: X-CH05-003, X-CH05-004, X-CH05-011, X-CH05-024
- 다음 확인: executable link, call permission, decision authority의 경계

### X-CH05-013 — key identity가 이름이 아니라 scope를 포함한 record digest로 판정됨

- 연결된 역사적 명칭: KeyRec digest, key identity
- Chapter 근거: CORE17이 같은 key_id 뒤 scope만 바꾸는 우회를 막기 위해 전체 KeyRec digest를 allow/deny 기준으로 사용함
- 선행 대조: X-CH03-031의 ValueId, X-CURR-005의 protocol occurrence identity
- 함께 구분할 후보: X-CH05-009, X-CH05-015
- 다음 확인: runtime identity, semantic identity, concept identity의 분리

## C. 결정론·ref·integrity

### X-CH05-014 — 정규화 직렬화가 동일 입력 표현을 고정함

- 연결된 역사적 명칭: SerializeNorm_v1, FloatPolicy
- Chapter 근거: 문자열·map 순서·배열·숫자·type tag를 고정하고 runtime 객체 표현을 금지함
- 선행 대조: X-CH03-034의 execution trace
- 함께 구분할 후보: X-CH05-015, X-CH05-017, X-CH05-034
- 다음 확인: canonical serialization, semantic equivalence, reproducibility의 경계

### X-CH05-015 — payload 대신 content digest 기반 ref가 전달됨

- 연결된 역사적 명칭: PackRef, digest, HashFn_v1, SHA-256
- Chapter 근거: candidate·policy pack을 ref로 전달하고 normalized payload를 다시 hash해 digest 일치를 확인함
- 선행 대조: C0004, X-CH03-034
- 함께 구분할 후보: X-CH05-013, X-CH05-014, X-CH05-016, X-CH05-017
- 다음 확인: content identity, reference identity, record identity의 분리

### X-CH05-016 — ref load가 schema·version·digest 재검증을 요구함

- 연결된 역사적 명칭: PackStore, verified load
- Chapter 근거: 같은 digest가 immutable payload를 가리키는지 schema/version check와 rehash 뒤에만 load함
- 선행 대조: X-CH03-033의 source access, X-CH03-034의 trace
- 함께 구분할 후보: X-CH05-015, X-CH05-017, X-CH05-033
- 다음 확인: integrity verification, source verification, execution stage responsibility의 분리

### X-CH05-017 — integrity·reproducibility가 authenticity·truth·legitimacy를 보증하지 않음

- 연결된 역사적 명칭: No-RNG, perm-invariant, digest match, determinism
- Chapter 근거: 동일 입력의 재생성과 content integrity는 강화되지만 source authenticity·claim truth·legitimate choice는 남음
- 선행 대조: X-CH03-036의 Trace/Facts 혼동, C0009
- 함께 구분할 후보: X-CH05-014, X-CH05-015, X-CH05-030, X-CH05-031
- 다음 확인: audit evidence, epistemic evidence, normative warrant의 분리

## D. current/next와 후보 공간

### X-CH05-018 — 현재 active policy와 같은 tick에 생성된 next policy가 분리됨

- 연결된 역사적 명칭: `policy_act_ref`, `policy_next_ref`, Policy_t, Policy_{t+1}
- Chapter 근거: CL17·CORE17이 현재 Select/Canon은 act만 읽고 next는 commit rotation 뒤 다음 tick에 활성화하도록 교정함
- 선행 대조: X-CH03-024, X-CH04-016, C0006
- 함께 구분할 후보: X-CH05-007, X-CH05-019, X-CH05-020, X-CH05-025
- 다음 확인: current policy state, proposed policy, activation transition의 분리

### X-CH05-019 — 현재 candidate manifest와 다음 candidate manifest가 분리됨

- 연결된 역사적 명칭: `candidate_manifest_ref`, `candidate_manifest_ref_next`, CandidateManifestPack
- Chapter 근거: CandidateGen은 next manifest만 만들고 현재 Select는 이미 S_t에 고정된 active manifest만 읽음
- 선행 대조: X-CH03-021~023, X-CH04-017, C0006
- 함께 구분할 후보: X-CH05-018, X-CH05-020, X-CH05-021, X-CH05-023
- 다음 확인: candidate set, proposal output, active choice space의 분리

### X-CH05-020 — active/next pointer 교대가 commit에서만 수행됨

- 연결된 역사적 명칭: NextWire, rotation assignment
- Chapter 근거: CORE17의 `act_{t+1} := next_t` assignment가 policy와 candidate manifest에 적용됨
- 선행 대조: X-CH04-023의 delayed update
- 함께 구분할 후보: X-CH05-018, X-CH05-019, X-CH05-025
- 다음 확인: state transition, pointer rotation, substantive decision delta의 분리

### X-CH05-021 — 후보 생성은 선택 writer가 아니지만 미래 선택 공간을 바꾸는 influence임

- 연결된 역사적 명칭: CandidateGen, ProposeFn, candidate route
- Chapter 근거: 원하는 후보만 생성하면 deterministic Select를 우회 조작할 수 있어 CandidateGen을 독립 socket과 next route로 봉인함
- 선행 대조: X-CH03-021, X-CH03-023, X-CH04-017, C0006
- 함께 구분할 후보: X-CH05-019, X-CH05-022, X-CH05-023
- 다음 확인: candidate generation, causal influence, proposal permission, selection authority의 분리

### X-CH05-022 — candidate provenance가 route·activation 추적에 한정됨

- 연결된 역사적 명칭: Candidate provenance, manifest ref
- Chapter 근거: ref·next-wire·활성 tick은 추적하지만 producer identity·source snapshot·authorship을 필수로 증명하지 않음
- 선행 대조: X-CH03-031~034, X-CH04-019
- 함께 구분할 후보: X-CH05-016, X-CH05-021, X-CH05-030
- 다음 확인: route provenance, causal provenance, authorship provenance의 분리

### X-CH05-023 — 후기 STG에서 same-tick 후보 생성→선택 경로가 다시 열림

- 연결된 역사적 명칭: `Cand_t`, `ProposeFn`, `SelectFn`, STG Candidate route
- Chapter 근거: STG17은 같은 tick에 생성한 Cand_t를 같은 tick SelectFn에 전달하며 Core NextWire 대응 봉인이 실행면에 보이지 않음
- 선행 대조: X-CH05-019~021
- 함께 구분할 후보: X-CH05-006, X-CH05-019, X-CH05-021
- 다음 확인: cross-branch omission, formal rollback, independent design difference의 경계

## E. 결정·rotation·기록

### X-CH05-024 — commit transaction 안에서 decision input과 record input이 분리됨

- 연결된 역사적 명칭: CommitDecisionIn, CommitRecordIn, IS-COMMIT-DECISION, IS-COMMIT-RECORD
- Chapter 근거: CL17·CORE17이 선택·canonical impulse·spend와 policy/candidate/audit record를 별도 역할로 가름
- 선행 대조: C0004, C0009, X-CH03-035
- 함께 구분할 후보: X-CH05-012, X-CH05-025, X-CH05-026, X-CH05-027
- 다음 확인: decision computation, transaction parameter, audit record, occurrence record의 분리

### X-CH05-025 — next pointer는 decision 근거가 아니라 rotation parameter로만 사용됨

- 연결된 역사적 명칭: rotation ref, `policy_next_ref`, candidate next ref
- Chapter 근거: v1.2a-SEAL이 CommitDecisionIn field에 남은 next ref를 delta 계산에 쓰지 못하게 하고 pointer 복사에만 제한함
- 선행 대조: X-CH05-018~020
- 함께 구분할 후보: X-CH05-020, X-CH05-024, X-CH05-027
- 다음 확인: state transition parameter와 decision evidence의 경계

### X-CH05-026 — durable audit record가 decision input이나 warrant가 아님

- 연결된 역사적 명칭: audit_ref, CommitRecord, record-only
- Chapter 근거: Core가 audit를 Decision socket에서 Record socket으로 옮기고 ledger delta·선택 변경을 금지함
- 선행 대조: C0004, C0009, X-CH03-036
- 함께 구분할 후보: X-CH05-024, X-CH05-027, X-CH05-030
- 다음 확인: audit trail, decision record, evidence, warrant의 분리

### X-CH05-027 — 의미상 분리된 field가 낡은 schema 안에 남는 type residue가 발생함

- 연결된 역사적 명칭: DecisionIn residue, audit_ref residue, rotation-ref residue
- Chapter 근거: v1.1의 audit_ref와 v1.2a의 rotation ref가 의미상 비결정 역할로 제한돼도 기존 field/schema 배치가 즉시 제거되지 않음
- 선행 대조: terminology의 경계 재압축 이력
- 함께 구분할 후보: X-CH05-006, X-CH05-024, X-CH05-025
- 다음 확인: semantic correction, schema migration, executable effective contract의 분리

## F. 외부 입력·grounds·evidence 공백

### X-CH05-028 — 외부 입력을 전부 VIEW로 제한해 직접 승격을 막음

- 연결된 역사적 명칭: ExternalIn, VIEW_KEYS, default deny
- Chapter 근거: FS17·Core branch가 외부 text·sensor·marker를 VIEW로만 등록하고 Canon·Select·Commit 입력 승격을 기본 deny함
- 선행 대조: X-CH03-027~030, X-CH04-030
- 함께 구분할 후보: X-CH05-029, X-CH05-030, X-CH05-031
- 다음 확인: stimulus input, observation, evidence, canonical grounds의 분리

### X-CH05-029 — policy-shaped perception이 phys·residual·commit 경로에 들어갈 수 있음

- 연결된 역사적 명칭: TR, PercIn, PhysSig, ΔQ⊥, policy-shaped perception
- Chapter 근거: STG17에서 policy_t가 TR/PercIn을 거쳐 phys signal·residual·CommitFn 입력에 영향을 줌
- 선행 대조: X-CH03-027·028, X-CH04-018
- 함께 구분할 후보: X-CH05-028, X-CH05-030, X-CH05-032
- 다음 확인: perception shaping, physical evidence, commit read-cap의 경계

### X-CH05-030 — 내부 계산에 입력된 것과 판정 근거가 된 것이 분리되지 않음

- 연결된 역사적 명칭: input admission, ExternalIn path, evidence gap
- Chapter 근거: Core는 외부 입력을 과도하게 봉인하고 STG는 입력 경로를 열지만 어느 field가 grounds/evidence인지 type이 없음
- 선행 대조: X-CH03-020, X-CH03-029·030, X-CH04-030
- 함께 구분할 후보: X-CH05-017, X-CH05-022, X-CH05-028, X-CH05-031
- 다음 확인: access, eligibility, evidence, warrant의 분리

### X-CH05-031 — authority wall과 별도로 policy-independent evidence port가 필요해짐

- 연결된 역사적 명칭: evidence port absence, grounds starvation, over-closure
- Chapter 근거: 권한 없는 입력을 막았지만 world trace를 attestable grounds로 받는 전용 port가 Core·STG 양쪽에 없음
- 선행 대조: X-CH03-029·030·036, X-CH04-030
- 함께 구분할 후보: X-CH05-017, X-CH05-028, X-CH05-030
- 다음 확인: Chapter 06의 Witness/Grounds와 대조하되 직접 승계는 별도 확인

## G. 단일 전이·행동·검증 closure

### X-CH05-032 — 모든 상태 갱신과 output이 하나의 외부 전이 경계 안에 배치됨

- 연결된 역사적 명칭: `F`, single transition, CommitFn
- Chapter 근거: STG17이 `(S_{t+1}, ActionOut_t, ViewOut_t)=F(S_t,X_t,Mark_x)` 밖의 SSOT write를 금지함
- 선행 대조: X-CH03-006·007, current reducer transition
- 함께 구분할 후보: X-CH05-023, X-CH05-029, X-CH05-033, X-CH05-035
- 다음 확인: transition boundary, internal stage typing, human process ontology의 분리

### X-CH05-033 — Decision·ActionOut·실제 occurrence·world outcome이 서로 다름

- 연결된 역사적 명칭: Decision_t, ActionOut_t, Gate_Action, action receipt, outcome receipt
- Chapter 근거: STG17은 Decision과 ActionOut을 별도 계산하고 world response·action/outcome receipt 없이 S_{t+1}을 만듦
- 선행 대조: C0001, C0002, C0003, C0004
- 함께 구분할 후보: X-CH05-024, X-CH05-032, X-CH05-036
- 다음 확인: selected decision, emitted command, performed action, observed outcome의 분리

### X-CH05-034 — 검사 가능한 spec closure와 검증된 구현 closure가 분리됨

- 연결된 역사적 명칭: SEALED, Gate checklist, linker spec, test report absence
- Chapter 근거: CORE17은 특정 우회 경로를 SEALED로 열거하지만 실제 linker 실행·test result는 없고 registry/version 잔차도 남음
- 선행 대조: X-CH05-006, X-CH05-014~017
- 함께 구분할 후보: X-CH05-006, X-CH05-016, X-CH05-032
- 다음 확인: specification, implementation, conformance evidence의 분리

### X-CH05-035 — authoritative state 안의 Narrative binding이 별도 writer·scope 없이 남음

- 연결된 역사적 명칭: Narrative binding, Memory/Cache, phys authority
- Chapter 근거: STG17이 서사 binding을 S_t.Memory/Cache에 넣지만 별도 residence·writer·read scope·write gate를 두지 않음
- 선행 대조: X-CURR-014·017·019, X-CH03-016
- 함께 구분할 후보: X-CH05-009, X-CH05-010, X-CH05-032
- 다음 확인: persistent trace, narrative state, canonical decision input의 분리

### X-CH05-036 — PackRef 검증 요구와 실제 검증 책임 stage가 분리됨

- 연결된 역사적 명칭: Gate C1, verified PackRef, load stage omission
- Chapter 근거: STG17은 검증된 PackRef만 받는다고 선언하지만 F 내부에 schema/digest recheck 책임 stage가 보이지 않음
- 선행 대조: X-CH05-015·016
- 함께 구분할 후보: X-CH05-016, X-CH05-032, X-CH05-034
- 다음 확인: declarative requirement, executable verifier, conformance evidence의 분리

## H. 핵심 관계 지도

```text
textual preservation
≠ interpretive priority
≠ canon adoption
≠ registry membership
≠ socket linking
≠ executable participation
≠ state write authority
```

```text
registered key
≠ universally readable
≠ decision-usable
≠ writable
≠ warranted ground
```

```text
CandidateGen influence
→ candidate_manifest_ref_next
→ commit rotation
→ active candidate space at t+1

≠ current selection authority
```

```text
decision computation input
≠ pointer rotation parameter
≠ audit record
≠ epistemic evidence
≠ warrant
```

```text
normalized payload
→ digest match
→ reproducible load

≠ authentic source
≠ true claim
≠ legitimate decision
```

```text
Decision
≠ ActionOut
≠ actual occurrence
≠ world outcome
≠ outcome record
```

## I. 선행 concept와의 대조

- `C0004`는 occurrence record다. CommitRecord, audit trail, candidate manifest, PackRef를 자동 통합하지 않는다.
- `C0006`은 비권위적 미래 편성 영향이다. CandidateGen·Policy socket은 구현 operation이며 같은 concept인지 후속 cluster에서 분석한다.
- `C0009`는 수행·지출 회계 기록이다. generic CommitRecord·audit·dependency trace 전체보다 좁다.
- `C0001~C0003`은 선택·occurrence·outcome을 분리한다. Chapter 05의 Decision·ActionOut·receipt 공백은 이 경계를 다시 확인하지만 이번 intake에서 concept를 갱신하지 않는다.

## J. 다음 concept cluster에 넘길 후보

다음 배치 전에 우선 비교할 cluster 후보는 다음과 같다.

```text
historical preservation
canon adoption
registry eligibility
executable participation
socket/link permission
state write authority
```

그리고 record 계열은 별도 비교가 필요하다.

```text
occurrence record
commit decision record
pointer rotation record
work/spend accounting record
audit/dependency trace
outcome record
```

이 목록은 C-ID 발급 계획이 아니다. Chapter 05 intake 뒤 실제 형제 대비·인간 근거·현재 사용을 확인할 작업 목록이다.
