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
- RFC 0001, RFC 0002, RFC 0003

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

**상태: `MORPH-001A` instrumentation `IMPLEMENTED`; envelope/load comparison `PROPOSED` — RFC 0003**

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

### 3B-B. Accommodation envelope와 excess

**상태: `PLANNED / UNIMPLEMENTED`**

별도 typed `AccommodationEnvelope` policy를 정의하고 demand가 그 범위를 벗어난
부분을 competing excess operator로 비교한다. `[0, 1]` state bound나 단순
`requested - committed`를 envelope·excess·residual strain으로 재명명하지 않는다.

### 3B-C. Load와 outcome comparison

**상태: `PROPOSED / UNIMPLEMENTED`**

envelope measurement가 식별된 뒤에만 `MorphicLoadProfile`과 residual/recovery/retention
outcome을 정의한다. 이 단계까지 완료되기 전에는 퀄리아·주관적 시간·정신 시간량을
출력하지 않는다.

## 4. Dynamics v0.3 — 첫 descriptive transgression

**상태: `PLANNED`**

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
