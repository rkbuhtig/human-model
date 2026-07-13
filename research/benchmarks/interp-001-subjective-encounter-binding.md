# INTERP-001 — Subjective Encounter, Delayed Assembly, and Adjudication

| 항목 | 값 |
|---|---|
| Status | `DRAFT PREREGISTRATION / UNIMPLEMENTED — OPERATOR AND FIXTURE MANIFEST OPEN` |
| Current slice | `INTERP-001A` terminology, lineage and falsification contract |
| Future execution | detached lab before Dynamics integration |
| Evaluation kind | structural capability/discriminability matrix; not predictive validation |
| Human empirical status | `OPEN` |

## 질문

matched counterfactual run에서 같은 외부 evidence fixture와 같은 material 수·크기에도
현재 수용 상태, material access, assembly topology와 Ghost exploration이 서로 다른
interpretive integration의 방향과 시점을 구조적으로 구분할 수 있는가?

fixture가 directional profile, bridge와 exploration path를 선언하므로 이 matrix만으로
predictive superiority를 주장하지 않는다. 예측력은 후속 hidden-oracle/held-out
protocol의 별도 문제다.

## 분석 단위와 시간

```text
source occurrence fixture
protocol current reexposure | source-uncertain current access
SubjectiveEncounterFormProxy
optional private-trace role / EpisodeMaterialReference
EpisodeAssemblyCandidate
InterpretiveBindingCandidate
BindingAdjudicationReceipt
EpisodeIntegrationReceipt | None
TargetFormReadoutChangeReceipt | None
```

각 artifact는 다음 시간을 섞지 않는다.

```text
world_occurrence_at             # known / claimed / unknown
encounter_formed_at             # 각 accepted encounter receipt의 시각
earliest_encounter_known_as_of(snapshot_id)  # optional readout
current_access occurred / available / processed times
assembly_proposed_at
adjudication_at
effective_from_access_ordinal
narrative_write_at              # detached lab에서는 없음
```

`CurrentAccessOccurrence`는 RFC 0002 current reexposure와 동일 타입이 아니다.
reexposure가 trigger가 될 수도 있고 spontaneous/invoked access처럼 source가
불확실할 수도 있다.

## 고정 경계

```text
SubjectiveEncounterFormProxy ≠ actual qualia / first-person report
ReceptionStateSnapshot ≠ measured human mood
felt coherence ≠ external truth
EpisodeMaterialReference ≠ integrated Episode
Ghost candidate ≠ adjudication ≠ Episode integration
BindingIgnition ≠ Narrative promotion
TargetFormReadout ≠ ExternalTarget identity or property
```

어떤 experimental policy도 EvidenceLink, EvidenceAssessment, ActionOccurrence 또는
WorldOutcome을 생성·강화하지 않는다.

## declared component profiles

첫 lab은 positive/negative를 상쇄하는 scalar를 만들지 않는다.

```text
ReceptionStateSnapshot:
  positive_direction_receptivity
  negative_direction_receptivity
  ambiguity_tolerance
  exploration_bandwidth

SubjectiveEncounterFormProxy:
  positive_direction_fit
  negative_direction_fit
  ambiguity
  activation
```

- unit: `declared_ordinal_simulation_component`
- missing: explicit reason; never zero-imputed
- source/writer: detached experiment policy
- identity: model ID/version, policy digest, pre-access snapshot digest
- aggregation: no cross-component addition or cancellation

이 component는 expected-output label이 아니다. formation/adjudication operator가 fixture의
정답 label을 직접 읽으면 실패다.

## 경쟁 모델

### Reception mechanism

```text
R0  state-independent
R1  reception changes accessible material subset/order only
R2  reception changes candidate coherence only
R3  access + coherence with separately declared operators
```

### Interpretation model

```text
I0  signed material count / magnitude profile

I1  I0 + one fixed direction threshold

I2  R1 access result + fixed assembly/adjudication rule

I3  R3 + EpisodeAssemblyCandidate topology
       + non-membership / unsettled relations

I4  I3 + object-scoped pre-access TargetFormReadout
       + manifest-frozen Ghost exploration path
       + ordinal-delayed readout feedback
```

I3의 효과가 방향별 threshold 변경과 동치면 I1 variant로 축소한다. I4가 I3와 다른
manifest-frozen 구조 구분을 만들지 못하면 TargetForm/Ghost path 자유도를 축소한다.

효과 식별을 위해 다음 crossed cells를 각각 실행한다.

```text
Reception × topology:
R0 + fixed topology
R1 + fixed topology
R2 + fixed topology
R3 + fixed topology
R0 + variable topology
R1 + variable topology
R2 + variable topology
R3 + variable topology

TargetForm × Ghost:
I3 + TargetForm only, Ghost path fixed
I3 + Ghost path only, TargetForm fixed
I3 + TargetForm + Ghost path
```

TargetForm 효과는 Ghost를 고정한 paired run에서, Ghost 효과는 TargetForm을 고정한
paired run에서 각각 유지·폐기한다.

### Target-form source model

```text
TF0  experimenter-declared synthetic NarrativeTerrainFixture
     projected from the reserved historical concept
TF1  TF0 + object-scoped adopted EpisodeIntegrationReceipt
         + contested BindingAdjudicationReceipt
TF2  TF1 + object-scoped implicit/plastic trace
         + pre-access accessibility snapshot
```

readout source는 fixture 결과를 본 뒤 선택하지 않는다. 각 run은 model ID/version,
source refs와 target-resolution status를 기록한다.
`NarrativeTerrainFixture`는 `HumanState.narrative`나 구현된 Narrative Field가
아니며 역사적 Narrative를 인증하지 않는다.

### Experience-material representation

```text
EF0  subjective-encounter-backed optional private-trace role
     + assembly-independent EpisodeMaterialReference
     + AssemblyMaterialMembershipCandidate

EF1  episode-material candidate
     + SubjectiveEncounterFormProxy sidecar
```

identity, provenance와 구조 구분 결과가 같으면 별도 `ExperienceFragment` residence를
만들지 않는다.

## Implementation-blocking manifest

이 문서는 type, lineage, comparison surface와 failure boundary를 먼저 고정한
`DRAFT PREREGISTRATION`이다. 코드를 시작하기 전 별도 manifest에서 다음을 exact
value/operator로 동결하고 digest를 발급해야 한다.

```text
complete fixture IDs and component values
model별 allowed input fields
access operator
candidate-coherence operator
bridge/topology construction rule
Ghost exploration operation semantics
BindingAdjudicatorPolicy
fixture별 exact semantic predicates
expected pass/fail model × fixture cells
freeze timestamp / policy digest / no-retuning rule
```

manifest freeze 뒤 outcome을 보고 operator, fixture value 또는 expected predicate를
바꾸면 새 version과 preregistration이 필요하다.

## Semantic comparison view

raw artifact 전체나 content digest에는 model/policy identity가 포함되므로 model
동치·차이를 판정하는 데 사용하지 않는다. 다음 metadata-free projection을
`semantic_comparison_view@1` 후보로 고정하고, exact schema는 위 manifest에서
동결한다.

```text
EncounterFormationReceipt presence / count
subjective-form component profile
current-encounter → source-encounter lineage relation
canonical fixture material keys or source-relative semantic aliases / order
assembly membership roles / topology
candidate direction component profile
adjudication outcome
unsettled relation
EpisodeIntegration presence
effective access ordinal
```

`sufficient`, `capability difference`, `observationally equivalent`는 오직 fixture별
expected predicate를 이 projection에 적용한 결과를 뜻한다. predictive accuracy를
뜻하지 않는다. manifest는 run-local artifact ID를 comparison key/alias로 바꾸는
normalization을 고정하며 candidate, receipt와 policy ID는 이 view에 들어오지 않는다.

## Structural fixture matrix

각 primary fixture는 direction을 뒤집은 mirror fixture를 포함한다.

### P1 — matched source fixture, 다른 수용 상태

```text
isolated matched counterfactual ledgers
+ same canonical source fixture and source occurrence identity reused across ledgers
+ same declared claim/evidence-content projection
+ different declared ReceptionState profiles
→ subjective-form / access / candidate 차이 가능
→ declared evidence-content projection digest identical
```

같은 source occurrence identity를 서로 격리된 ledger에서 재사용하는 것은 허용하지만,
한 ledger 안에서 두 조건에 중복 처리하지 않는다. run-local metadata나 artifact identity를
포함한 full digest는 같다고 요구하지 않고, 명시된 content projection만 비교한다.

### P2 — 부유 material과 지연 결합

```text
access ordinal k:
  directionally incongruent reception
  + encounter-backed material ref
  → access receipt without assembly membership 가능

later access ordinal m > k:
  compatible reception
  + new CurrentAccessOccurrence
  → distinct current EncounterFormationReceipt
  → same source lineage, possibly different subjective-form profile
  → new assembly candidate / interpretive-binding candidate 가능
```

과거 encounter, trace와 material ref는 불변이고 external Evidence content projection도
같다. accessibility, membership와 unsettled outcome은 각각 새 relation/receipt로
표현한다.

### P3 — 상태 변화만 있고 current access는 없음

```text
ReceptionState changes
+ no CurrentAccessOccurrence
→ no historical material rewrite
→ no new encounter / assembly / adjudication receipt
```

### P4 — 같은 exact access set, 다른 assembly/coherence

accessed material identity와 order를 동일하게 고정하고 reception profile만 바꾼다.
I2는 같은 결과를, I3는 다른 assembly/adjudication candidate를 낼 수 있어야 한다.
이 fixture가 없으면 I3와 I2는 구분되지 않는다.

Reception이 material 없이 결과를 직접 생성하지 못하도록 다음 control을 함께 둔다.

```text
current access 있음 + relevant material 없음
→ no binding candidate generated from reception alone

strong manifest-frozen opposite-direction topology
+ incongruent reception
→ opposite-direction adopted transition remains possible

balanced reception profile
→ direction not forced

same reception + different material topology
→ different structural outcome remains possible
```

### P5 — 같은 count/magnitude, 다른 topology

```text
matched run A: isolated clusters declared before execution
matched run B: manifest-frozen bridge relation
```

bridge는 결과를 본 뒤 붙이지 않는다. I0/I1은 같은 profile을, I3/I4는 다른
AssemblyIgnition capability를 보일 수 있다.

### P6 — 같은 material/target source, 다른 Ghost path

```text
broaden / contrast / counterfactual path
→ moderation / integration candidate 가능

confirmation-only / rehearsal path
→ reinforcement / polarization candidate 가능
```

Ghost가 expected outcome label을 읽거나 adjudication/integration을 직접 수행하면 실패다.

### P7 — protocol redelivery, reexposure와 source-uncertain access

```text
same occurrence + canonical payload + new delivery
→ no new access/encounter/assembly/adjudication

RFC 0002 current reexposure
→ new access trigger 가능
→ source EvidenceLink strength unchanged

spontaneous/invoked access
→ zero-or-more claimed/unknown source refs
→ no fabricated source occurrence
```

### P8 — ordinal feedback negative control

access ordinal k에서 생성한 TargetForm readout change를 encounter k에 다시 사용하면
실패다.

```text
output from access k
→ effective_from_access_ordinal > k
```

같은 timestamp라도 더 큰 processing/access ordinal의 새 occurrence는 허용할 수 있다.

### P9 — Narrative promotion negative control

AssemblyIgnition, BindingAdjudication 또는 EpisodeIntegration만으로 Narrative Field가
바뀌면 실패다. detached lab은 authored ΔC / α / β gate나 implicit-formation writer를
구현하지 않으며 Narrative write를 출력하지 않는다.

### P10 — interpreted target scope

```text
same actor state
+ interpreted target A history
→ TargetFormReadout[A, relation/context scope]

same actor state
+ interpreted target B history
→ TargetFormReadout[B, relation/context scope]
```

interpreted target ref를 external entity identity로 인증하거나 A의 integration이 명시된
cross-target relation 없이 B의 readout을 바꾸면 실패다.

### P11 — prefix and policy controls

- future access/event를 추가해도 과거 receipt prefix와 digest는 바뀌지 않는다.
- policy를 바꾸면 derived artifact와 policy digest가 함께 바뀐다.
- policy variation은 source occurrence, external evidence와 prior trace를 바꾸지 않는다.

## 기준 출력

첫 구현은 총점이나 예측 확률 하나를 만들지 않는다.

```text
CurrentAccessOccurrence
EncounterFormationReceipt
AccessReadoutReceipt
EpisodeMaterialReferenceSet
EpisodeAssemblyCandidateSet
AssemblyMaterialMembershipCandidateSet
InterpretiveBindingCandidateSet
BindingAdjudicationReceiptSet
EpisodeIntegrationReceipt | None
AssemblyIgnitionReceipt | None
BindingIgnitionReceipt | None
TargetFormReadoutChangeReceipt | None
```

각 artifact는 actor, interpreted-target/external-entity resolution, source refs,
model/policy version, pre-access snapshots, processing/access ordinal, missingness와
content digest를 보존한다. candidate는 immutable하고 outcome은 append-only receipt다.

## 성공 조건

1. manifest freeze 뒤 retuning 없이 같은 evidence/material 총량에서 R0–R3와 I2–I4의 declared capability difference가 재현된다.
2. exact access-set control에서 I3와 I2를 구분하는 fixture가 있다.
3. 과거 artifact, external Evidence와 source identity가 모든 condition에서 보존된다.
4. reception/access/coherence/TargetForm/Ghost path 효과를 ablation으로 각각 제거할 수 있다.
5. future events를 추가해도 동일 prefix receipt가 바뀌지 않는다.
6. 이 성공을 predictive 또는 human-empirical support로 보고하지 않는다.

## 즉시 실패 조건

- reception/subjective proxy가 Evidence strength, source truth 또는 target identity를 바꿈
- formation/adjudication operator가 허용 입력 대신 expected-output label을 직접 읽음
- 상태 변화만으로 모든 과거 material을 자동 재처리함
- 결과를 본 뒤 bridge edge나 accessed subset을 선택함
- material에 mutable assembled/accessibility/unsettled enum을 저장함
- Ghost candidate가 scoped adjudication 없이 integration receipt를 씀
- Episode integration이 authored Narrative gate를 우회함
- 같은 access ordinal에서 TargetForm feedback fixed point를 계산함
- 한 interpreted target의 form을 전역 lens로 모든 target에 적용함
- RFC 0002 reexposure와 detached current access를 동일 타입으로 alias함
- unknown source time/identity를 protocol이 발명함

## 폐기·축소 규칙

```text
I0/I1 equivalent to graph/reception models across all frozen predicates
→ Episode topology / reception mechanism 축소

R1 equivalent to R3 across all frozen predicates
→ candidate-coherence operator 제거

R2 equivalent to R3 across all frozen predicates
→ access operator 제거

I3 + TargetForm equivalent to I3 across all frozen predicates
→ TargetForm 자유도 제거

I3 + Ghost path equivalent to I3 across all frozen predicates
→ Ghost-path 자유도 제거

TF0 equivalent to TF1 equivalent to TF2
→ TF0만 유지

TF0 equivalent to TF1 across all frozen predicates
→ integration/binding source contribution 제거

TF1 equivalent to TF2 across all frozen predicates
→ implicit/plastic/pre-accessibility source contribution 제거

EF0 and EF1 observationally equivalent
→ 별도 ExperienceFragment residence를 만들지 않음
```

source interaction을 허용한다면 TF source의 factorial matrix와 interaction retirement
predicate를 manifest에서 execution 전에 동결한다.

synthetic 구조 구분 성공은 인간 경험적 support도 predictive support도 아니다.
predictive claim으로 승격하려면 independent measurement mapping, hidden oracle,
preregistered train/held-out split과 complexity penalty가 필요하다.

## 비출력

```text
actual qualia
human mood score
universal ignition threshold
Narrative truth
MorphicLoadProfile
recovery or mental-time quantity
relationship health or love score
```
