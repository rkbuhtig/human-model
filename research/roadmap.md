# Human Model Research Roadmap

| 항목 | 지위 |
|---|---|
| 실행 순서 | `ADOPTED` |
| 후속 구현 | `PLANNED` |
| 인간 경험적 검증 | `OPEN` |

상태는 문서 선언이 아니라 commit, tests, trace, report로 승격한다.

## 0. Dynamics v0.1 baseline freeze

**상태: `FROZEN`**

동결한 것:

- source revision `9b731b7f92700227de1fae8adc79e1d8e687d25f`
- Python/dependency 버전과 stress seed
- 기존 25개 테스트 결과와 stress report
- machine-readable [golden trace](../dynamics/reports/baseline-v0.1.json)
- 실행 환경과 범위를 고정한 [baseline manifest](../dynamics/reports/baseline-v0.1-manifest.json)

golden trace는 Evidence digest, Claim transition, decision-window Routed candidate, Intent,
Attempt, Performance, ActionOccurrence, slow-state trajectory, 입력 회계를
포함한다.

검증 명령과 갱신 규칙은 [baseline report](../dynamics/reports/baseline-v0.1.md)에 있다. exact commit SHA가 immutable source reference이며 이후 의미 교정은 이 golden과 비교한다.

## 1. Research program documentation

**상태: `IMPLEMENTED — package boundary`; semantic queue/access decoupling `PARTIAL`**

- assessment와 adoption record 분리
- 연구 정체성·근거 층·아키텍처
- claim schema + typed claim registry
- defect schema + 실제 case 1건
- RFC 0001, RFC 0002, RFC 0003, RFC 0004

종료 조건 통과: `Assessment ≠ Adoption ≠ Implementation ≠ Run ≠ Empirical Evidence`가
문서 구조와 metadata에서 구분된다.

## 2. Dynamics v0.1.1 — 의미·모듈 경계

**상태: `IMPLEMENTED`**

```text
EpistemicState → EvidenceAssessmentState
BodyAuthorization → MotorFeasibility
Contract / Dynamics / Protocol 분리
```

종료 조건:

- import boundary test가 의존 금지를 검사한다.
- 동일 입력·seed에서 baseline과 의미적 trace가 동등하다.
- 새 인간 행동과 `WarrantState`를 추가하지 않는다.

종료 판정: canonical package 의존 방향과 compatibility façade를 분리했고, import
boundary suite와 v0.1 semantic golden exact match를 통과했다. 다만 frozen v0.1의
queue pressure → AccessState 결합은 `legacy_v01_access_pressure_bridge`로 격리만
했으며, v0.2 실험에서 protocol buffer와 실제 access demand를 분리해야 한다.

## 3. Dynamics v0.2 — Temporal Kernel

**상태: first provenance slice `IMPLEMENTED`; full temporal dynamics `PARTIAL / PLANNED`**

```text
sim_time
occurred_at ≠ available_at ≠ processed_at
FlowUpdate(state, dt) ≠ EventJump(state, event)
occurrence_id ≠ delivery_id
PastOccurrence ≠ CurrentReexposure
```

구현된 first slice:

- `occurred_at ≤ available_at ≤ processed_at ≤ final_sim_time`
- `processed_at`의 engine-owned stamp
- occurrence와 delivery identity 분리
- 동일 occurrence/payload transport redelivery 멱등성
- 동일 occurrence ID의 payload collision hard failure
- backlog의 원래 발생시각 보존
- 별도 현재 reexposure provenance와 evidence independence

구조 테스트:

- `test_temporal_ordering_and_engine_owned_processing`
- `test_transport_redelivery_is_idempotent`
- `test_occurrence_payload_collision_is_hard_error`
- `test_backlog_preserves_occurrence_time`
- `test_current_reexposure_changes_state_not_evidence`

아직 계획된 second slice:

- 무입력 flow의 step-size consistency
- transport partition 안정성과 burst/spaced 판별
- 시간 경과가 Evidence ledger를 수정하지 않음

이 second slice는 독립 temporal-comparison 축이다. read-only transition ledger나
`MORPH-001`을 시작하기 위한 선행 blocker가 아니다.

따라서 v0.2는 provenance-capable temporal envelope까지만 구현되었다.
`FlowUpdate/EventJump`, no-event recovery/decay, burst/spaced 결과는 아직 구현 성취가
아니며 인간의 정신 시간에 대한 경험적 지지는 전혀 없다. 구현된 타입·writer·
identity 경계는 [Temporal Envelope Contract](../dynamics/spec/temporal.md)에 고정한다.

몸 상세, 기억 archive, `WorldOutcome`, 주관적 시간은 범위 밖이다.

## 3A. Read-only Mental Transition Ledger

**상태: type/measurement slice `IMPLEMENTED`; predictive hypothesis `PROPOSED` — RFC 0003**

```text
canonical elapsed time
≠ qualified mental-transition count / density
```

구현된 `Q-v1`은 processed occurrence마다 receipt 하나를 post-run에 파생한다.
`body/access/associative/affective/habit/narrative/relationship`의 literal persistent
field 중 하나라도 `0.01 normalized_simulation_unit` 이상 변한 receipt만 qualified
transition subset에 들어간다.

```text
checkpoint                  per processed occurrence
transition_effective_at     processed_at
qualification information  current trace only
ledger                      immutable / post-run derived / read-only
report                      count ≠ canonical duration ≠ density
```

transport duplicate와 redundant delivery는 receipt를 추가하지 않는다. qualification
policy를 바꿔도 base HumanState·processing trace·evidence/action ledger는 바뀌지
않으며, count/density report는 update kernel에 재입력되지 않는다. 동일 원천을 현재
실제로 다시 접근한 경우는 별도 reexposure occurrence로 처리되므로 독립적으로
qualify할 수 있다.

구조 테스트:

- `test_one_receipt_per_processed_occurrence_and_qualified_subset`
- `test_transport_redelivery_does_not_create_mental_transition`
- `test_policy_ablation_changes_only_read_only_ledger`
- `test_future_events_cannot_requalify_prefix`
- `test_transition_window_keeps_count_and_density_distinct`

이 구현은 [Q-v1 measurement contract](../dynamics/spec/mental-transitions.md)를
실행화한다. transition density가 이후 access/recovery를 예측한다는
`HM-DYN-001`은 여전히 `PROPOSED / UNIMPLEMENTED`이며, 정신 시간의 실재 단위나
인간 경험적 타당성은 검증되지 않았다.

또한 default Q scope의 `access.*` field에는 `legacy_v01_access_pressure_bridge`의
간접 영향이 남아 있고, per-occurrence checkpoint는 unresolved same-time ordering과
semantic bundling에 안정적이라고 검증되지 않았다. queue/access decoupling 또는
scope ablation과 serialization failure probe가 `HM-DYN-001` 평가 전에 필요하다.

## 3B. `MORPH-001` — Count–Load Dissociation

**상태: `MORPH-001A` instrumentation과 `MORPH-001B` simulation proxy comparison `IMPLEMENTED`; human capacity/load comparison `PROPOSED` — RFC 0003**

```text
transition count
≠ pre-transition DeformationDemand / CapacityProfile relation
≠ MorphicLoadProfile
≠ MorphicWorkReceipt / ResidualStrain / TraceCandidate
≠ horizon-qualified PersistentTrace
```

작은 전이 다수와 큰 적응 소수를 비교한다. Demand와 Capacity는 단위·정규화가
선언된 commensurate typed vector로 시작하고, load는 둘의 preregistered
`MorphicLoadProfile` 관계로 표현한다.

count-only 경쟁 모델보다 회복·잔여·지속 흔적에서 판별 이득이 없으면 축소하거나
기각한다. synthetic comparison은 구현 sanity일 뿐 claim support가 아니며,
`PhenomenalStrainReadout` 연결은 `HOLD`다.

한 번에 전체 load stack을 만들지 않고 다음 조각으로 나눈다.

### 3B-A. Reducer proposal–commit instrumentation

**상태: `IMPLEMENTED`**

현재 reducer가 field별로 요청한 pre-constraint displacement와 실제 bounded state에
commit된 displacement를 flat ordered proposal receipt로 보존한다.

```text
ReducerProposalReceipt
├─ current occurrence temporal/provenance identity
├─ measurement policy / available-information identity
├─ conditional writer context / content digest
├─ typed before/after state projections and content-bound digests
└─ flat ordered proposals tuple
   └─ ReducerFieldProposal
      ├─ stage / operator / write sequence
      ├─ typed ReducerDriverContribution
      └─ requested pre-constraint target ≠ committed target
```

`ReducerStepResult`는 traced fast/slow reducer의 runtime wrapper다. engine이 그 안의
proposal을 write order로 평탄화한 뒤 `TickTrace`와 receipt에 보존하므로 ledger에는
step-result sequence가 없다.

receipt는 모든 processed occurrence에 하나씩 대응하고, transport redelivery에는
생기지 않으며, Q-qualified `MentalTransition`이 없는 포화 사례에도 존재할 수 있다.
traced/compatibility reducer는 같은 writer 입력에서 같은 committed state를 만들고,
proposal/receipt artifact는 state·evidence·routing·action update의 입력이 되지 않는다.

measurement model은 `descriptive-reducer-preclamp-proxy@1.0.0`이다. 현재 simulation
reducer proposal은 access pressure·update rate·phenomenal/performance driver를 이미
포함할 수 있으므로 independently identified `DeformationDemand`가 아니다.

```text
ReducerProposal ≠ DeformationDemand ≠ MorphicLoad
```

이 조각은 future demand measurement의 instrumentation precursor다. 상세 failure probe는
[`MORPH-001A` preregistration](benchmarks/morph-001-demand-commit.md)을 따른다.

### 3B-B. Declared reducer-write band와 proxy excess

**상태: `IMPLEMENTED — EXPERIMENTER-DECLARED SIMULATION PROXY ONLY`**

`MORPH-001A` proposal마다 별도 typed `ReducerProposalEnvelopePolicy`의 signed band를
적용하고 componentwise clipping 밖의 부분을 ordered proxy-excess profile로 보존한다.
이 policy는 실험자가 선언한 synthetic reducer-write fixture이며 measured human
`AccommodationEnvelope / CapacityProfile`이 아니다. `[0, 1]` state bound나 단순
`requested - committed`를 band·proxy excess·residual strain으로 재명명하지 않는다.

```text
ReducerProposal + declared simulation band
→ ReducerProposalEnvelopeComparison
≠ DeformationDemand / ExcessDemand / MorphicLoad
```

normalized·max·L1·L2 operator는 competing candidate로만 사전등록했고 구현하지 않았다.
상세 범위는 [`MORPH-001B` preregistration](benchmarks/morph-001b-proposal-envelope-comparison.md)에 있다.

### 3B-C. Load와 outcome comparison

**상태: `DEFERRED / UNIMPLEMENTED — INTERP-001 boundary first`**

independent demand/capacity measurement와 outcome protocol이 식별된 뒤에만
`MorphicLoadProfile`과 residual/recovery/retention outcome을 정의한다. 현재 synthetic
proposal/band comparison은 이 조건을 만족하지 않는다. 회복을 선형 exposure count나
단일 threshold로 성급히 고정하지 않도록 subjective encounter, delayed current
access와 interpretive integration 경계를 먼저 분리한다. 그 전에는
퀄리아·주관적 시간·정신 시간량을 출력하지 않는다.

## 3C. `INTERP-001` — Subjective Encounter and Interpretive Reorganization

**상태: `INTERP-001A BOUNDARY DOCUMENTED; INTERP-001A2 M1 CONTRACT FROZEN; INTERP-001B DETACHED CONFORMANCE IMPLEMENTED; BROADER DYNAMICS OPEN` — RFC 0004**

```text
ExternalOccurrence / CurrentAccessOccurrence
≠ SubjectiveEncounterFormProxy
≠ EpisodeMaterialReference
≠ AssemblyMaterialMembershipCandidate
≠ EpisodeAssemblyCandidate
≠ InterpretiveBindingCandidate
≠ BindingAdjudicationReceipt
≠ EpisodeIntegrationReceipt
≠ Narrative Field write
≠ TargetFormReadout
```

현재 boundary slice는 역사적 기능 경계와 현행 synthesis를 구분하고, 신규 candidate의
identity·writer·persistence·effective order와 금지 cast를 문서로 고정한다.
`INTERP-001A2`는 그중 reception→access와 reception→candidate-coherence를 R0–R3,
16 mirrored fixtures, 64 cells와 별도 execution/evaluation manifest로 동결했다.
`INTERP-001B`는 manifest에 함께 고정된 encounter→assembly→adjudication phase를 포함한
64-cell/88-step M1을 detached runner로 실행하고 독립 evaluator로 conformance를 판정한다.
Dynamics code, HumanState, Narrative writer와 새 runtime behavior는 변경하지 않는다.

후속 detached lab은 다음 순서로만 연다.

1. `INTERP-001B` (`IMPLEMENTED`): frozen M1 phase-complete runner + independent evaluator
2. `INTERP-001C` (`M1 MECHANICAL SLICE EXECUTED`): RFC 0004의 reception-conditioned
   assembly/adjudication 범위는 B report 안에서 판정하되, 이를 variable Ghost 또는 durable
   receipt 구현으로 승격하지 않음
3. `INTERP-001D1`: object-scoped TargetForm source와 Ghost-path ablation의 competing manifest
4. `INTERP-001D2`: later-access-only target-form feedback와 outcome/retention protocol
5. 단순 합·threshold와 다른 구조 구분을 재현한 뒤에만 runtime/Narrative integration 검토

synthetic capability matrix는 predictive support나 인간의 기분·기억·퀄리아 법칙을
지지하지 않는다. `MORPH-001C`와의 접합도 별도 measurement mapping 전에는 금지한다.

## 4. Dynamics v0.3 — 첫 descriptive transgression

**상태: `PLANNED`; INTERP detached-lab integration은 별도 gate**

한 사례만 구현한다.

```text
AffectiveThreat → SubjectiveBelief 변화 가능
SubjectiveBelief → attention / routing / avoidance 변화 가능

EvidenceLink 불변
EvidenceAssessment 불변
WorldOccurrence 생성 없음
```

정확한 수치보다 방향성·독립성·인증 경계를 검사한다. 반복 서사, 수행 기억
오귀속, 모호 증거 과채택은 `HOLD`다.

## 5. 독립 검증군

**상태: `PLANNED`**

```text
Contract mutation suite   월권 검출력
Structural S0–S3          typed separation의 기여
Temporal T0–T3            시간 가설의 기여
```

가능하면 `S3T2`와 `S3T3`처럼 한 축만 바꾼다. 계약 통과, 복잡도, 판별력,
경험적 예측은 별도 지표다.

## 6. Volume 0 lineage reconstruction

**상태: `PLANNED`**

source manifest를 고정한 뒤 당시 진단과 현재 해석을 분리한다. Chapter 01은
필요하면 절대적 기원이 아니라 0101 재컴파일 경계로 재위치시킨다. 이 단계는
v0.2의 blocker가 아니다.

## 명시적 HOLD

- 완성된 `WarrantState`
- 주관적/생물학적 독립 시계 상태
- 물리 은유의 측정량 승격
- 생리학 계수와 인간 일반 정확도 주장
- 몸·기억·세계·관계의 동시 확장
