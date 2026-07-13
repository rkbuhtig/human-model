# RFC 0004 — Subjective Encounter and Interpretive Reorganization

| 항목 | 값 |
|---|---|
| Status | `PROPOSED — INTERP-001A TYPE/LINEAGE BOUNDARY DOCUMENTED; EXECUTABLE MANIFEST DRAFT` |
| Target | detached interpretation lab before Dynamics integration |
| Kind | Descriptive-dynamics type, lineage and falsification boundary |
| New runtime behavior implemented in this RFC | 없음 |
| Prerequisites | RFC 0001 boundary; RFC 0002 occurrence/reexposure provenance |
| Human-empirical status | `OPEN` |

## 제안

외부 occurrence에서 persistent state update로 바로 건너뛰지 않고, 그 occurrence나
현재 access가 pre-access target/reception snapshot 아래에서 어떤 subjective
encounter proxy를 만들었는지, 그 trace가 언제 어떤 Episode candidate와 interpretation
candidate에 참여했는지를 분리한다.

```text
ExternalOccurrence / protocol CurrentReexposure / source-uncertain access
+ pre-access TargetFormReadout snapshot
+ pre-access ReceptionStateSnapshot
→ CurrentAccessOccurrence
→ SubjectiveEncounterFormProxy
→ optional private-trace role / EpisodeMaterialReference
→ EpisodeAssemblyCandidate + AssemblyMaterialMembershipCandidate[]
→ Ghost InterpretiveBindingCandidate
→ BindingAdjudicationReceipt
→ optional EpisodeIntegrationReceipt
→ optional authored Episode→Narrative candidate path
→ later TargetFormReadoutChangeReceipt
```

이 RFC는 실제 퀄리아를 측정하거나 새 `Narrative Field` writer를 구현하지 않는다.
목적은 역사 문서에서 복원된 기능 경계와 현재 synthesis candidate를 구분하면서,
subjective encounter와 상태 의존적 지연 access를 판별 가능한 새 연구축의 draft
preregistration으로 제시하는 것이다. exact operator, fixture와 expected predicate는
implementation-blocking manifest에서 별도로 동결한다.

## 복원된 기능 경계와 현행 합성의 지위

Chapter 02에서 안정적으로 복원되는 최소 경계는 다음이다.

```text
Ghost candidate
≠ Editor / JOT.court 계열의 판정
≠ Episode buffer / write
≠ Narrative Field write
```

`private experience trace / EpisodeMaterial / EpisodeAssembly / NarrativeBinding`은
Checkpoint 05-A의 현행 synthesis candidate다. 이미 구현되거나 역사 전체에서 안정된
canonical object model이 아니다. Ghost/Editor/Episode는 별도 역할과 하나 field의
G/E/T mode 사이를 오갔고, `JOT`도 court-cycle·sketch stream·store라는 충돌하는
뜻을 가졌다. 이 RFC는 새 합성을 과거 문서에 소급하지 않는다.

다만 `Episode`와 `Narrative Field`는 기존의 큰 시간·승격 단위로 예약하고 작은
임시 해석에 재사용하지 않는다.

| 용어 | 이 RFC의 지위와 의미 |
|---|---|
| `EpisodeMaterialReference` | exposure·action·body·outcome·report·private trace를 source-bound immutable handle로 가리키는 assembly-independent `PROPOSED` reference |
| `EpisodeAssemblyCandidate` | material refs, imposed/authored degree, gap과 unsettled relation을 가진 `PROPOSED` 조립 후보. 아직 Episode integration이 아님 |
| `AssemblyMaterialMembershipCandidate` | assembly candidate ID와 material ref ID를 role/order로 잇는 `PROPOSED` relation. material 자체를 mutate하지 않음 |
| `InterpretiveBindingCandidate` | Ghost가 탐색한 일시적 episode interpretation 후보. `Narrative` 명칭과 write 권한이 없음 |
| `BindingAdjudicationReceipt` | scoped adjudicator가 candidate에 adopted/rejected/contested/deferred 판정을 내린 append-only receipt |
| `EpisodeIntegrationReceipt` | manifest-frozen adopted predicate를 통과한 transition의 detached-lab Episode-level policy outcome을 기록하는 선택적 receipt. contested/rejected/deferred 판정은 이를 만들지 않음 |
| `Narrative Field` | Episode와 동일하지 않은 느린 비권위 지형. authored promotion gate 없이 자동 write되지 않음 |

최근 대화에서 사용한 `EpisodeNarrative`는 폐기한다. 작은 일시적 조립은
`EpisodeAssemblyCandidate`, 해석 후보는 `InterpretiveBindingCandidate`로 표현한다.

Checkpoint 05-A의 `ImplicitFormation`은 endorsement 없는 별도 slow-formation 경로로
남겨 둔다. ΔC / α / β는 authored Narrative write candidate의 역사적 gate이며 모든
외상·조건화·암묵 형성의 보편 writer라고 주장하지 않는다.

## 신규 후보 타입

### `SubjectiveEncounterFormProxy`

하나의 current access가 simulation 안에서 어떻게 경험 형태로 구성되었는지를
나타내는 experimenter-defined descriptive proxy다.

첫 lab policy의 최소 component:

```text
positive_direction_fit
negative_direction_fit
ambiguity
activation
```

각 component의 단위는 `declared_ordinal_simulation_component`이며 서로 더하거나
상쇄하지 않는다. missing은 `0`이 아니라 별도 missing reason이다. axis, scale,
writer, available information과 policy digest가 receipt에 결부되어야 한다.

최소 lineage:

```text
current access occurrence
optional resolved / claimed / unknown source refs
pre-access target-form readout identity
pre-access reception-state snapshot identity
context / body snapshot identity
formation policy ID / version / digest
formed components / missingness / content digest
```

```text
SubjectiveEncounterFormProxy
≠ actual qualia
≠ first-person report
≠ ObservationEvent
≠ EvidenceLink
≠ ExternalOccurrence
```

### `ReceptionStateSnapshot`

material access와 candidate felt-coherence를 기울일 수 있는 declared simulation
profile이다. human-calibrated mood measurement가 아니다.

```text
positive_direction_receptivity
negative_direction_receptivity
ambiguity_tolerance
exploration_bandwidth
```

각 component는 `declared_ordinal_simulation_component`이고 방향 성분은 동시에
높거나 낮을 수 있다. 합계·차이·단일 mood scalar를 만들지 않는다. missing은 explicit
reason, source는 experiment policy fixture, writer는 detached protocol이다.

접근성 효과와 candidate-coherence 효과를 한 파라미터에서 중복 계산하지 않는다.

```text
R0  state-independent
R1  reception changes material access only
R2  reception changes candidate coherence only
R3  access + coherence with separately declared operators
```

### `CurrentAccessOccurrence`

과거 material의 회상·연상·재접근 또는 현재 encounter를 처리하는 detached-lab access
occurrence다. RFC 0002의 implemented `CurrentReexposure`와 동일 타입이 아니다.

```text
RFC 0002 CurrentReexposure occurrence
→ CurrentAccessOccurrence의 trigger가 될 수 있음

spontaneous / invoked / associative access
→ source-uncertain CurrentAccessOccurrence가 될 수 있음
```

최소 필드는 actor/subject, `access_occurrence_id`, zero-or-more source
material/occurrence refs, source-resolution status, trigger mode,
`occurred_at / available_at / processed_at`, processing sequence와 policy digest다.
자발적 회상을 Ghost가 일으켰다고 자동 인증하지 않으며 trigger attribution은
claimed/unknown일 수 있다.

```text
source world occurrence time
≠ first accepted encounter time
≠ current access time
≠ adjudication time
≠ Narrative write time
```

상태 변화만으로 저장된 과거 전체를 자동 재평가하지 않는다.

### `TargetFormReadout`

특정 대상으로 해석되는 것이 현재 어떤 형태로 경험되는지를 나타내는 object-scoped
readout 후보다.

```text
TargetFormReadout[
  actor_id,
  interpreted_target_ref,
  external_entity_ref?,
  target_resolution_status,
  relation_scope,
  context_scope
]
```

전역적인 긍정/부정 lens, external entity identity 또는 외부 대상의 실제 속성이
아니다. 같은 interpreted target도 relation/context scope에 따라 다를 수 있다.

source definition은 아직 `HOLD`이며 다음을 경쟁시킨다.

```text
TF0  experimenter-declared synthetic NarrativeTerrainFixture
     projected from the reserved historical concept
TF1  TF0 + object-scoped adopted EpisodeIntegrationReceipt
         + contested BindingAdjudicationReceipt
TF2  TF1 + object-scoped implicit/plastic trace
         + pre-access accessibility snapshot
```

TF0/TF1으로 같은 구조 구분을 얻으면 더 복잡한 TF2를 유지하지 않는다. 이 RFC는
`TargetForm`의 durable writer, retention 또는 revalidation을 결정하지 않는다.
`NarrativeTerrainFixture`는 `HumanState.narrative`도, 구현된 Narrative Field도,
역사적 Narrative의 인증된 복원도 아니다.

## Experience fragment와 Episode material의 경계

현상적으로 말한 경험 조각을 별도 persistent store로 바로 도입하지 않는다. 첫
구현은 immutable subjective encounter backed trace, assembly-independent material
reference와 assembly-scoped membership candidate를 사용하고 다음 표현을 대조한다.

```text
EF0  SubjectiveEncounterFormProxy-backed optional private-trace role
     + assembly-independent EpisodeMaterialReference
     + AssemblyMaterialMembershipCandidate

EF1  Episode-material candidate + subjective-form sidecar reference
```

둘이 identity, provenance와 판별 결과에서 같으면 별도 `ExperienceFragment`
residence를 만들지 않는다. 어떤 표현도 material 자체에
`assembled / inaccessible / unsettled` mutable enum을 쓰지 않는다.

- accessibility는 access-ordinal-specific readout이다.
- assembly participation은 immutable membership candidate/relation이다.
- unsettled는 adjudication/settlement relation이다.
- 같은 source trace가 여러 assembly candidate에 참여할 수 있다.

## 상태 의존적 지연 결합 가설

현재 수용 상태는 같은 source trace의 사실 지위를 바꾸지 않지만, 현재 접근 가능한
material refs와 조립 가능한 interpretation 후보를 기울일 수 있다.

```text
a material ref whose immutable source encounter proxy
carried a declared positive-direction component
+ incongruent current reception
→ accessed without assembly membership 가능

later compatible reception
+ new CurrentAccessOccurrence
→ new EpisodeAssemblyCandidate 가능
→ positive-direction InterpretiveBindingCandidate 가능
```

이 표현은 material 자체의 영구 valence label이 아니다. 과거 source encounter
receipt는 보존한다. 현재 재접근은 distinct encounter proxy, access, membership와
assembly receipt를 만들 수 있지만 source occurrence나 EvidenceLink를 수정하지 않는다.

## 점화의 층

점화를 하나의 보편 event property 또는 scalar threshold로 두지 않는다.

```text
AssemblyIgnition
: 이전에 분리된 material refs가 한 EpisodeAssemblyCandidate에서
  execution 전에 manifest-frozen bridge predicate를 만족함

BindingStatusTransition
: immutable InterpretiveBindingCandidate가 append-only adjudication에서
  adopted / contested / rejected / deferred 판정을 받음

BindingIgnition
: execution 전에 manifest-frozen adopted predicate를 만족한 transition만을 뜻하며
  EpisodeIntegrationReceipt를 만듦

Authored Narrative promotion
: authored candidate가 기존 ΔC / α / β 계열 gate를 통과하는 느린 write 후보

TargetFormReadoutChange
: source-bound readout 차이. persistent revision 또는 Narrative promotion이 아님
```

한 층의 점화가 다음 층을 자동 성립시키지 않는다.

## Ghost와 scoped adjudication 권한

```text
Ghost generation / exploration
≠ candidate endorsement
≠ BindingAdjudicationReceipt
≠ EpisodeIntegrationReceipt
≠ Narrative incorporation
≠ external warrant
```

Ghost exploration은 broaden·contrast·counterfactual뿐 아니라
confirmation-only·rehearsal도 포함할 수 있다. 완화는 보편 목적함수가 아니다.
Ghost가 candidate를 스스로 integration으로 write하지 않는다.

첫 lab은 역사적으로 충돌하는 `Editor`나 `JOT`를 canonical writer로 재도입하지
않고, scope가 좁은 `BindingAdjudicatorPolicy`를 simulation fixture로 둔다.

## 시간과 재귀 규칙

각 access phase는 발생 전 snapshot만 읽는다. 순서는 wall-clock timestamp가 아니라
`processing_sequence / access_ordinal`로 고정한다.

```text
TargetFormReadout_before_k + ReceptionStateSnapshot_before_k
→ encounter at access_ordinal k
→ material / assembly / adjudication receipts_k
→ TargetFormReadoutChangeReceipt
→ effective_from_access_ordinal > k
```

같은 access ordinal에서 새 TargetForm readout을 다시 읽어 encounter를 재해석하는
fixed-point loop를 허용하지 않는다. 같은 timestamp에 있더라도 더 큰 ordinal의 새
access occurrence는 허용할 수 있다. 미래 occurrence가 과거 receipt prefix를 바꾸지도
않는다.

## 최소 identity와 persistence 계약

assembly와 membership identity는 다음 순서로만 만든다.

```text
MembershipSpec = (material_ref_id, role, order)       # ID 없는 immutable value
assembly_candidate_id
  = digest(access_ref, ordered MembershipSpec[])
membership_id
  = digest(assembly_candidate_id, MembershipSpec)
```

role/order/topology는 candidate 생성 뒤 mutate하지 않는다. assembly identity가 membership
ID에 의존하지 않으므로 순환이 없고, membership은 이미 식별된 assembly와 material을
잇는다.

| artifact | identity / scope | source refs | writer | persistence / effective time |
|---|---|---|---|---|
| `CurrentAccessOccurrence` | access ID, actor, processing sequence | zero-or-more resolved/claimed/unknown material or occurrence refs | detached access protocol | append-only; occurred/available/processed times |
| `SubjectiveEncounterFormProxy` | encounter receipt ID, actor, interpreted-target scope | access occurrence, pre-access reception/target snapshots | detached formation policy | immutable; formed at processing; no external truth authority |
| optional private-trace role / `EpisodeMaterialReference` | trace/ref ID, actor, interpreted-target scope | encounter receipt and optional claimed source | trace/material-reference writer policy | assembly-independent immutable handle |
| `EpisodeAssemblyCandidate` | candidate ID + prior-version refs | access ref and ordered `MembershipSpec[]` | Ghost exploration policy | immutable candidate; proposed at ordinal k |
| `AssemblyMaterialMembershipCandidate` | membership ID, assembly candidate ID, role/order | identified assembly candidate and material ref | assembly proposer policy | immutable candidate relation; does not mutate material |
| `InterpretiveBindingCandidate` | candidate ID + assembly version | assembly candidate and Ghost trace | Ghost exploration policy | immutable candidate; no adoption authority |
| `BindingAdjudicationReceipt` | receipt ID, candidate ID, outcome | candidate, pre-adjudication snapshot | scoped adjudicator policy | append-only; rejected/deferred is not a binding |
| `EpisodeIntegrationReceipt` | integration ID, episode scope | adopted adjudication receipt | proposed versioned EpisodeCuratorPolicy | append-only receipt; records only the versioned detached-lab policy outcome, never human Episode integration or Narrative authority |
| `AssemblyIgnitionReceipt` | receipt ID, assembly candidate ID | access receipt, ordered MembershipSpec, pre-access topology snapshot digest or manifest baseline-separation relation, manifest-frozen predicate/version | read-only ignition projection | append-only derived receipt; no adjudication, integration or Narrative authority |
| `BindingIgnitionReceipt` | receipt ID, binding candidate ID | adopted adjudication receipt, emitted EpisodeIntegrationReceipt, manifest-frozen predicate/version | read-only ignition projection | append-only derived receipt; no adjudication, integration or Narrative authority |
| `TargetFormReadoutChangeReceipt` | readout ID, actor, interpreted-target scope | exact readout sources and prior readout | versioned read-only projection | immutable; effective from access ordinal greater than source ordinal |

모든 artifact는 model/policy ID, version, digest, missingness/source-resolution status와
prior-version refs를 필요한 경우 기록한다. `world_occurrence_at`은
known/claimed/unknown일 수 있고, `encounter_formed_at`은 각 accepted encounter
receipt에 속한다. 필요한 경우 `earliest_encounter_known_as_of(snapshot_id)`를 별도
readout으로 만들며 전역적인 mutable `first_encounter_at`을 immutable lineage에 넣지
않는다. 모르는 시각을 protocol이 발명하지 않는다.

## 금지 cast와 금지 간선

```text
ExternalOccurrence
≠ ObservationEvent
≠ CurrentAccessOccurrence
≠ SubjectiveEncounterFormProxy
≠ optional PrivateExperienceTraceCandidate role (EF0 only)
≠ EpisodeMaterialReference
≠ AssemblyMaterialMembershipCandidate
≠ EpisodeAssemblyCandidate
≠ InterpretiveBindingCandidate
≠ BindingAdjudicationReceipt
≠ EpisodeIntegrationReceipt
≠ Narrative Field
≠ TargetFormReadout

ReceptionStateSnapshot ↛ source provenance / Evidence strength
SubjectiveEncounterFormProxy ↛ external fact certification
CurrentAccessOccurrence ↛ past occurrence rewrite / independent source evidence
Ghost candidate ↛ direct adjudication, integration or Narrative write
EpisodeMaterialReference ↛ automatic Episode integration
BindingAdjudicationReceipt ↛ automatic Narrative write
EpisodeIntegrationReceipt ↛ valid belief or action authority
TargetFormReadout ↛ ExternalTarget identity/property
HumanState.narrative ↛ historical Narrative Field identity
Q-v1 MentalTransitionReceipt ↛ conscious Episode
```

descriptive influence는 허용하지만 cross-domain certification authority는 생기지 않는다.

## 구현 slice

### `INTERP-001A` — 이 RFC

- 역사 기능 경계와 현재 synthesis의 non-retroactive crosswalk
- 신규 candidate type의 identity, writer, persistence와 effective-order 계약
- 금지 cast와 writer 경계
- competing model, structural capability matrix와 retirement rule의 draft preregistration
- implementation 전 exact operator/fixture/predicate manifest freeze blocker
- 코드와 HumanState 변경 없음

### `INTERP-001B` — Subjective encounter lab

- access/reexposure + pre-access snapshots → subjective-form proxy
- private-trace/material-reference 표현 대조
- historical first encounter와 current access 분리
- Evidence/World ledger 불변 negative control

### `INTERP-001C` — Reception-conditioned assembly/adjudication lab

- access-only와 coherence-only mechanism 분리
- delayed current access와 non-membership relation
- Ghost candidate trace와 scoped `BindingAdjudicationReceipt`
- AssemblyIgnition / BindingIgnition receipts
- Narrative write 없음

### `INTERP-001D` — Target-form readout and ordinal-delayed recursion

- TF0–TF2 source-definition ablation
- interpreted-target/external-entity 분리
- later-access-only feedback
- scalar lens와 단순 threshold 경쟁 모델

### Runtime / Narrative integration gate

detached lab이 manifest freeze 뒤 retuning 없이 선언된 구조 구분을 재현한 뒤에만
검토한다.
predictive superiority는 별도 hidden-oracle/held-out protocol 없이는 주장하지 않는다.
authored Episode→Narrative 경로를 우회하는 writer는 도입하지 않으며,
`ImplicitFormation` 경로도 이 lab이 폐기하지 않는다.

## 비목표

- 실제 퀄리아의 구현·측정
- 인간 mood의 보편 scalar 또는 임상 모델
- 모든 기억이 Episode/Narrative로 조직된다는 주장
- `Narrative Field`의 canonical 구현 완료 선언
- Ghost를 합리적 완화 최적화기로 정의
- 주관적 해석을 Evidence로 승격
- 현재 `MORPH-001B` proxy를 interpretive load로 재명명
- 정신 시간, 사랑, 회복 또는 관계 건강의 단일 점수
- synthetic capability matrix를 인간 또는 held-out predictive support로 사용

## 종료 조건

`INTERP-001A`는 다음을 만족하면 종료한다.

1. 기존 Episode/Narrative 예약어를 임시 단위에 재사용하지 않는다.
2. historical recovery와 current synthesis를 소급 없이 구분한다.
3. 신규 후보마다 source, writer, persistence, authority와 time/order lineage가 명시된다.
4. current state change, RFC 0002 reexposure와 detached current access를 구분한다.
5. subjective experience, external evidence, adjudication/integration, Narrative write와 TargetForm readout 사이의 금지 cast를 고정한다.
6. I0–I4, R0–R3, TF0–TF2와 폐기 조건을 구현 전에 등록한다.
7. exact executable operator/fixture/predicate manifest의 미완료를 명시하고 이를 code 착수 blocker로 둔다.
8. 이 문서가 새 HumanState writer, predictive support 또는 인간 경험적 support를 만들지 않는다.
