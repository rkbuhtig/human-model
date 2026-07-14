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

**상태: `INTERP-001A BOUNDARY DOCUMENTED; INTERP-001A2 M1 CONTRACT FROZEN; INTERP-001B DETACHED CONFORMANCE IMPLEMENTED; INTERP-001D1 EXECUTED / EVALUATED SYNTHETIC CONFORMANCE; INTERP-DIALOGUE-001A SCENARIOS DOCUMENTED / UNEXECUTED; INTERP-DIALOGUE-001B TRACE ORACLE FROZEN / UNEXECUTED; INTERP-DIALOGUE-001P0-V0 ELICITATION CONTRACT FROZEN / UNEXECUTED; INTERP-DIALOGUE-001P1-V0 EXECUTED / EVALUATED SCRIPTED DEVELOPMENT PILOT; BROADER DYNAMICS OPEN` — RFC 0004**

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

`INTERP-001D1`은 후속 자유도를 한 run에서 섞지 않고 다음 세 block으로 동결한다.

```text
SOURCE_COMPILER     TF0 / TF1 / TF2                    8 fixtures × 3 = 24 cells
ENCOUNTER_FORMATION E0 / ER / ET / ERT                 8 fixtures × 4 = 32 cells
GHOST_PATH          G0 / GT / GP / GTP                 8 fixtures × 4 = 32 cells
```

execution manifest는 development/sealed membership과 expected signature를 갖지 않고,
별도 evaluation manifest만 block별 `001–004` development, `005–008` sealed split을
읽는다. source compiler 성공, supplied-input sensitivity와 Ghost-path distinction은 서로
다른 판정이다. [`D1 conformance run`](benchmarks/interp-001d1-v1-conformance.md)은
88/88 closed-world signature와 24/24 cell + 30/30 pair + 37/37 global assertion을
통과했다. 상태는 `EXECUTED / EVALUATED SYNTHETIC CONFORMANCE`다. 그러나 세 block은
서로 output을 전달하지 않는 독립 cell 집합이며 end-to-end pipeline이 아니다.
development/sealed도 evaluator-only synthetic isolation이지 예측 또는 외부 타당도
검증이 아니다. D1은 feedback/revision, durable TargetForm writer, Episode/Narrative write
또는 인간 claim을 구현하지 않는다.

16개 retirement condition 중 RT-congruence와 declared RT lookup만 trigger됐지만,
두 조건은 coarse projection에서 같은 대수적 equivalence family와 lookup alias control이다.
이는 Reception/TargetForm factor retirement나 두 개의 독립 challenger 승리가 아니다.
단순 합·threshold·lookup은 이후 인간 설명력의 주된 순위표가 아니라 alias, degeneracy와
불필요한 구현 자유도를 찾는 control로 사용한다.

### 3C-A. `INTERP-DIALOGUE-001A` — Functional-jurisdiction scenario gate

**상태: `DOCUMENTED / UNEXECUTED — NO HUMAN OR LATENT DATA`**

D1과 D2 사이에 관계·업무·물리적 위험이라는 현실 영역의 저자 생성 가상 기능 관할
gate를 둔다. 주된 질문은 풍부한 모델이 가난한 모델보다 더 많은 출력을 표현하는지가
아니라, declared vignette factor 하나를 선택적으로 바꿨을 때 현재 기능 분해가 예상하는
관할만 달라지는지다. 이 한-factor contrast는 원시적인 인간 원인 하나를 식별했다는
뜻이 아니다.

```text
real-world-domain author-origin hypothetical scenario family
+ one-factor vignette contrast
+ manipulated source lane
+ public-record effect
+ held factor IDs
+ registered candidate probe domains
+ must-remain-equal contract
+ open-discriminator references
+ forbidden cast
+ future discriminating probe
```

fixture는 다음 authority lane을 분리한다.

```text
normative invariant
≠ non-exclusive phenomenological expectation
≠ open functional-placement discriminator
```

같은 즉시 출력 아래 서로 다른 내부 경로를 주장하려면 적어도 하나의 사전등록된 후속
probe에서 later trace가 달라질 가능성이 있어야 한다. `001A`의
`registered_candidate_probe_domains`는 비배타적인 후보 관측 영역이다. 목록 밖 효과는
fixture 위반이 아니라 현재 기능 분해의 scope failure 또는 열린 결과로 남긴다. exact trace
field와 competing signature는 `001B`에서 별도로 동결했다.

`INTERP-DIALOGUE-001A` 자체는 scenario contract 등록과 구조 validation만 수행했다. 인간
참가자 자료, LLM activation, D2 recursive composition, durable TargetForm, Episode
integration 또는 Narrative writer를 만들지 않는다. 별도 `001B` trace oracle freeze는
아래 범위이며, A validator 통과도
`HM-INV-013`이나 `HM-DYN-004`의 support가 아니다.

### 3C-B. `INTERP-DIALOGUE-001B` — Conditional functional-placement trace oracle

**상태: `FROZEN / UNEXECUTED — NO HUMAN, LLM, OR D2A TRACE DATA`**

`001B`는 사람의 숨은 상태를 맞히는 정답 oracle을 만들지 않는다. 각 competing placement를
구현했다고 주장할 때 그 구현이 약속해야 할 조건부 trace 관계와, 현재 probe/horizon에서
어떤 배치를 판정할 수 없는지를 결과 전에 고정한다.

```text
11 ordinal observation points
+ H_PREFIX_BEFORE_K / H_INITIAL_ACCESS_K / H_REGISTERED_FUTURE_ACCESS_K_PLUS_1
+ 23 authority-scoped trace fields
+ 9 factor placement oracles / 38 conditional hypotheses
+ 3 same-future-option oracles
+ REL initial reported mood × later reported mood 2×2
+ 3 D2a-only selective challenges
+ strict operational-alias / out-of-model rules
```

가설 정의의 relation, 미래 protocol의 observation status와 adjudication result는 서로 다른
vocabulary다. `001A`의 candidate surface는 관측값이 아니며, 실제로 elicited된 surface만
observation이 될 수 있다. natural contrast에서 earliest registered difference를 찾더라도
이는 association/location signature일 뿐 direct causal residence가 아니다. direct edge는
대안 node를 고정하는 D2a-only clamp protocol을 별도로 동결한 뒤에만 도전한다.

같은 즉시 표면 아래 두 path를 비교할 때는 **동일한** registered future option을 양쪽에
적용하고 strictly later access 한 번만 연다. observed equality나 missing mapping은
operational alias가 아니다. alias는 동일 probe·projection·horizon·measurement mapping에서
두 가설의 전체 conditional signature가 같은 경우에만 허용한다. 한 번의 later access로
durable TargetForm과 slow cache를 구분하지 않으며 `NOT_IDENTIFIABLE_UNDER_HORIZON`으로
남긴다. 등록 밖 효과는 raw payload와 provenance를 보존한 `OUT_OF_MODEL` lane으로 보내고
가장 가까운 placement로 강제 cast하지 않는다.

이 작업은 trace를 실행하거나 human/LLM measurement mapping을 동결하지 않는다. Ghost,
adjudicator와 action gate도 `001A` 자연 factor의 결과로 선택하지 않고 D2a-only challenge로
남긴다. schema·semantic validator 통과는 placement winner, later-access causality,
`HM-INV-013`/`HM-DYN-004` support, durable writer 또는 인간 메커니즘 근거가 아니다.

완료된 detached lineage는 다음과 같다.

1. `INTERP-001B` (`IMPLEMENTED`): frozen M1 phase-complete runner + independent evaluator
2. `INTERP-001C` (`M1 MECHANICAL SLICE EXECUTED`): RFC 0004의 reception-conditioned
   assembly/adjudication 범위는 B report 안에서 판정하되, 이를 variable Ghost 또는 durable
   receipt 구현으로 승격하지 않음
3. `INTERP-001D1` (`EXECUTED / EVALUATED SYNTHETIC CONFORMANCE`): object-scoped source
   compiler, supplied formation intervention와 exact-access Ghost-path ablation을 격리된
   88-cell run에서 판정; runtime/human mechanism으로 승격하지 않음

후속 연구는 결과를 본 뒤 질문과 protocol을 맞추지 않도록 다음 순서로만 연다.

1. `INTERP-DIALOGUE-001A` (`DOCUMENTED / UNEXECUTED`): 현실 영역의 저자 생성 가상
   scenario family, 한-factor contrast, authority lane과 registered candidate probe domain 등록
2. `INTERP-DIALOGUE-001B` (`FROZEN / UNEXECUTED`): competing functional placement,
   선택적 intervention signature, ordinal horizon, out-of-model lane과 trace oracle 동결
3. `INTERP-DIALOGUE-001P0-v0` (`FROZEN / UNEXECUTED`): 24개 presentation,
   prompt/response schedule, scripted replay provenance, runner/scanner/analyst 경계와 P1
   proposal-only 권한 동결
4. `INTERP-DIALOGUE-001P1-v0` (`EXECUTED / EVALUATED`): exact v0의 30-session immutable
   scripted adversarial replay를 24 run으로 실행하고 evaluator-side walkthrough/inspection,
   9 confirmed/4 deferred/1 rejected defect receipt와 8개 미채택·미실행 revision proposal을
   발행; actual acquisition과 수정 instrument 채택·실행 없음
5. 필요 시 `INTERP-DIALOGUE-001P0-v1`: proposal을 `ACCEPTED / REJECTED / DEFERRED`로
   별도 판정하고 채택된 변경만 새 immutable instrument로 동결
6. source-specific acquisition, human confirmatory, cross-model latent와 `INTERP-001D2a`
   protocol을 결과 전에 각각 동결
7. human judgment, latent representation probe와 D2a recursive composition을 독립 실행
8. `INTERP-DIALOGUE-001C`: 세 source의 일치·불일치와 operational alias 범위를 교차 판정
9. 살아남은 기능 배치에 한해서만 Dynamics runtime 또는 Narrative integration을 별도 검토

synthetic capability matrix는 predictive support나 인간의 기분·기억·퀄리아 법칙을
지지하지 않는다. `MORPH-001C`와의 접합도 별도 measurement mapping 전에는 금지한다.

### 3C-P0. `INTERP-DIALOGUE-001P0-v0` — Development elicitation instrument

**상태: `FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY`**

P0는 `001B`의 observation point를 질문 slot으로 바꾸지 않는다. 세 `001A` family와
`001B` oracle을 digest로 묶고, 미래 acquisition이 따라야 할 delivery/response schedule을
별도 namespace로 동결한다.

```text
E0 initial vignette delivery
E1 generic immediate-response prompt delivery
R1 immediate response event
E2 matched future-option delivery
E3 generic later-response prompt delivery
R2 later response event
D0 / RD0 optional retrospective diagnostic, after R2 only
```

R1/R2는 미래에 별도로 동결된 mapping의 O5/O10 surface 입력 후보일 뿐 observation이
아니다. D0/RD0는 retrospective diagnostic이며 oracle coordinate가 없다. O1–O4와
O7–O9는 mapping이 없으면 `NOT_OBSERVED`로 남기고 질문을 추가해 채우지 않는다. 현재
runner가 만드는 E/R record는 이 schedule의 scripted replay이며 실제 delivery/response
occurrence가 아니다.

```text
ScriptedReplayMaterializer
→ immutable scripted replay / provenance artifact
↛ actual acquisition occurrence

MechanicalDefectScanner
→ MechanicalDefectCandidate only

Analyst adjudication
→ InstrumentDefectReceipt
```

runner는 `SCRIPTED_ADVERSARIAL_RESPONSE`만 받아 declared response status와 payload를
replay record로 materialize한다. `RESPONDED / REFUSED / NO_RESPONSE / TECHNICAL_FAILURE`는
scripted record vocabulary이지 실제 participant 상태가 아니다. scripted raw payload는
`OUT_OF_MODEL`이 아니며, 그 판정은 future frozen mapping과 analyst adjudication을
요구한다. author walkthrough와 language/comprehension inspection은 evaluator-side defect
source이고 response occurrence가 아니다. scenario judgment를 first-person attestation이나
내부 mechanism trace로 직접 cast하지 않는다.

P0는 pilot을 실행하지 않는다. P1은 exact v0의 immutable scripted replay,
evaluator-side inspection, defect receipt와
`InstrumentRevisionProposal(PROPOSED_NOT_ADOPTED / UNEXECUTED)`만 발행할 수 있다. P1은
actual acquisition을 실행하거나 proposal을 채택하거나 수정 instrument를 실행할 수 없다.
새 version 채택은 별도 P0 decision/freeze이고, 수정 효과 확인은 그 뒤의 별도 P1 replay다.
실제 human/LLM/other-source acquisition은 source identity, delivery, consent/privacy,
mapping과 missingness를 별도 pre-run freeze한 뒤에만 연다.

P0의 schema·validator 통과는 human/LLM/D2a trace, placement winner, D2a k→k+1 recursion,
durable TargetForm, Episode/Narrative writer 또는 claim support가 아니다.

### 3C-P1. `INTERP-DIALOGUE-001P1-v0` — Scripted development pilot

**상태: `EXECUTED / EVALUATED — SCRIPTED DEVELOPMENT PILOT ONLY`**

[`P1 preregistration`](scenarios/interp-dialogue-001/elicitation/p1-development-pilot-preregistration.md)에
고정된 exact P0-v0와 30-session coverage를
[`execution report`](scenarios/interp-dialogue-001/elicitation/p1-development-pilot-v0-report.md)에
따라 실행했다. 30개 session은 24개 run artifact로 materialize됐고, session input·run·mechanical
candidate set·mapping candidate set 총 96개 생성 artifact와 content manifest가 deterministic
rebuild로 검증됐다.

mechanical scanner는 candidate 0개를 냈지만 이는 PASS가 아니다. evaluator-side walkthrough와
language inspection candidate를 analyst가 판정해 9개를 `CONFIRMED`, 4개를 `DEFERRED`, 1개를
`REJECTED`로 남겼다. 8개 revision proposal은 모두
`PROPOSED_NOT_ADOPTED / UNEXECUTED`이며 P1은 instrument byte, claim registry 또는 runtime을
수정하지 않았다.

```text
scripted replay determinism
!= actual delivery/response occurrence
!= frozen response-to-observation mapping
!= human, persona, latent or mechanism evidence
!= registry claim support
```

다음 권한 단계는 각 proposal을 `ACCEPTED / REJECTED / DEFERRED`로 판정하는 별도 P0-v1
decision/freeze다. 채택된 revision도 새 version으로 동결하고 P1-v1에서 다시 실행하기 전에는
defect가 수정됐다고 선언할 수 없다.

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

## 6A. Volume I.5 — Constitutional Consolidation, 2026-01-27–02-04

**상태: `PLANNED — PARALLEL SOURCE-CRITICAL DOCUMENTATION`; runtime·empirical blocker 아님**

후속 제공된 `pluss/만족수면퀄리아통합.txt`는 `0121 만족`의 첫 206행과 `0121 수면`
407행 전체를 byte-level로 재사용하고, `0122 newqual`을 `ΞM` 문법으로 재작성·확장한
뒤 CVJU block을 덧붙인다. `0127 maybe통합1:L1`은 같은 이름의 역사적 문서를 세 입력 중
하나로 직접 열거한다. 두 artifact의 동일성은 미식별이지만 내용 합치는 강한 계보를
지지한다. 따라서 기존 Chapter 10–11의 “독립 파일 부재”는 내용 계보 복구로 수정하되,
2026-07-13 ZIP entry 시각만으로 1월의 독립 원본성이나 작성시각을 인증하지 않는다.

이 병렬 권은 최소한 다음 후기 문서군을 source-critical하게 대조한다.

- `Overqorld/0127 maybe통합1`
- `Overqorld/coreannex.txt`
- `UNIVERSSE/0130 추상x현실 1`
- `UNIVERSSE/0203 시간공간부채`
- `UNIVERSSE/0204 귀결for코어`
- 복구된 `pluss/만족수면퀄리아통합.txt`와 내용상 연결된 형식화 가지

복원 시 다음 네 층을 분리한다.

```text
동시대 직접 구조
≠ 후기 합성·재작성
≠ 현재 연구의 독립 재발견
≠ 물리·우주적 과잉 일반화
```

Volume I.5의 source link는 claim registry의 `historical_cases` 후보를 보강할 수 있지만,
active adoption, implementation, structural support 또는 human-empirical support를 자동으로
올리지 않는다. 첫 provenance 판정은
[`Source-Recovery Record`](adoption-records/2026-07-13-recovered-satisfaction-sleep-qualia-provenance.md)에
고정한다.

## 명시적 HOLD

- 완성된 `WarrantState`
- 주관적/생물학적 독립 시계 상태
- 물리 은유의 측정량 승격
- 생리학 계수와 인간 일반 정확도 주장
- 몸·기억·세계·관계의 동시 확장
