# INTERP-001D1 — Target-Form Source and Ghost-Path Ablation

| 항목 | 값 |
|---|---|
| Status | `PREREGISTERED — THREE-BLOCK CONTRACT FROZEN / UNEXECUTED` |
| Current slice | `INTERP-001D1` detached source, formation and exploration ablation |
| Machine contracts | execution/evaluation manifest, cell-result schema and future run-carrier schema |
| Matrix | three isolated blocks, 24 fixtures × block-specific models = 88 cells |
| Evaluation kind | synthetic structural conformance and evaluator-only development/sealed discrimination |
| Runtime integration | 없음 |
| Human empirical status | `NOT TESTED` |

## 질문

`INTERP-001B`는 neutral/no-effect TargetForm과 fixed Ghost 아래에서 reception-conditioned
access와 candidate coherence를 실행했다. 다음 질문은 그 결과를 곧바로 durable human
state로 옮기는 것이 아니다. 먼저 다음 세 능력을 서로 다른 실험으로 분리한다.

1. outcome을 보지 않는 source compiler가 서로 다른 declared historical-source
   fixture에서 object-scoped `DeclaredTargetFormReadoutProfile`을 산출할 수 있는가?
2. 외생적으로 공급된 pre-access TargetForm과 ReceptionState가 current encounter
   formation에 서로 다른 간선으로 작용하는가?
3. exact accessible material을 고정했을 때, TargetForm context와 manifest-declared
   Ghost path가 candidate 구조를 서로 다르게 바꾸는가?

이 세 질문은 하나의 성공 조건이 아니다.

```text
Block A source-compiler success
≠ Block B supplied-input sensitivity
≠ Block C Ghost-path structural distinction
```

특히 Block B가 성공해도 “TargetForm이 Episode/Narrative에서 내려온다”는 source claim은
성립하지 않는다. 반대로 Block A가 다른 readout을 만들더라도 그 **산출 readout
자체**의 encounter/Ghost downstream necessity는 D1이 판정하지 않는다. Block B와 C는
A 출력을 인계받지 않고 외생적으로 supplied된 profile/context에 대한 sensitivity만 별도로
판정한다.

## 예약어와 현행 fixture의 경계

`Episode`와 `Narrative Field`는 기존 연구에서 큰 시간·승격 단위로 예약한다.
`Episode`는 작은 fragment나 잠깐의 해석 후보가 아니고, `Narrative Field`는 하나의
current mood, explicit belief 또는 전역 positive/negative lens가 아니다.

동시에 역사 문서의 Ghost·Editor·Episode·Narrative가 모든 epoch에서 하나의 안정된
canonical object model을 가졌다고 소급하지 않는다. D1은 다음과 같은 detached source
fixture만 선언한다.

```text
NarrativeTerrainFixture
prior object-scoped EpisodeIntegrationReceipt fixture
prior contested BindingAdjudicationReceipt fixture
implicit/plastic trace fixture
pre-access accessibility snapshot fixture
```

```text
NarrativeTerrainFixture
≠ HumanState.narrative
≠ implemented Narrative Field
≠ certified recovery of a historical Narrative

EpisodeIntegrationReceipt fixture
≠ human Episode integration
≠ authored Narrative write
```

작은 현상적 경험 조각을 새 persistent `ExperienceFragment` residence로 만들지 않는다.
D1은 기존 경계에 따라 `SubjectiveEncounterFormProxy`-backed optional private-trace role,
assembly-independent `EpisodeMaterialReference`와 access/assembly-specific relation만 쓴다.

```text
EpisodeMaterialReference
≠ EpisodeAssemblyCandidate
≠ integrated Episode
≠ Narrative Field write
```

## 가설적 전체 인과 사슬과 D1의 절단점

아래는 후속 연구가 판별해야 할 가설적 전체 사슬이다. 모든 입력과 출력의
시간 계약은 `processing_sequence / access_ordinal`을 따르며, wall-clock timestamp만으로
인과 순서를 추정하지 않는다.

```text
prior source fixtures with effective ordinal < k
→ DeclaredTargetFormReadoutProfile_before_k

ReceptionStateSnapshot_before_k
+ DeclaredTargetFormReadoutProfile_before_k
+ current access/source fixture_k
→ SubjectiveEncounterFormProxy_k
→ access-specific material view_k
→ Ghost exploration trace_k
→ immutable InterpretiveBindingCandidate_k
→ separate BindingAdjudicationReceipt_k
```

D1은 이 전체 사슬을 한 run으로 구현하지 않는다. 세 block은 각각 fresh detached
ledger에서 다른 supplied fixture를 읽고 독립적으로 끝난다.

```text
Block A source projection
≠ Block B supplied TargetForm input

Block B encounter-form output
≠ Block C supplied accessible-material fixture

Block A output ↛ Block B input
Block B output ↛ Block C input
```

각 cell은 자신의 출력을 다시 입력으로 소비하지 않는다.

```text
candidate/adjudication at k
↛ DeclaredTargetFormReadoutProfile_before_k
↛ encounter formation at k
↛ durable TargetForm write
↛ Narrative Field write
```

`TargetFormReadoutChangeReceipt`, future-effective revision, retention, decay,
revalidation과 later-access feedback은 `INTERP-001D2`의 별도 계약 전까지 비출력이다.

## 공통 측정·권한 경계

모든 declared component는 `declared_ordinal_simulation_component` rank `0/1/2` 또는
명시적 missing reason을 사용한다. positive/negative 방향은 동시에 높거나 낮을 수 있고
서로 상쇄하지 않는다. ordinal component에 덧셈, 평균, 차이, 곱셈, 나눗셈 또는 L1/L2
aggregate를 적용하지 않는다.

```text
DeclaredTargetFormReadoutProfile
≠ external target identity or property
≠ actual target image measured in a person
≠ global actor mood

ReceptionStateSnapshot
≠ human-calibrated mood
≠ source provenance

SubjectiveEncounterFormProxy
≠ actual qualia
≠ first-person report
≠ EvidenceLink

felt coherence / adjudication
≠ external truth
```

모든 block에서 source occurrence, EvidenceLink/EvidenceAssessment, action, authority,
observation, world outcome, prior encounter/material과 Narrative-write projection은
before/after가 동일해야 한다. target-resolution status가 `claimed` 또는 `unknown`이면
compiler나 Ghost가 이를 `resolved`로 올릴 수 없다.

## Block A — `SOURCE_COMPILER`

### 목적

supplied TargetForm label을 입력하는 대신 pre-k immutable source fixture만 읽어
object-scoped `DeclaredTargetFormReadoutProfile`을 산출한다. compiler는 current access, current/future
encounter, candidate, adjudication, integration, evaluator split과 expected outcome을
볼 수 없다.

각 source와 readout은 다음 scope를 보존한다.

```text
actor_id
interpreted_target_ref
external_entity_ref? + target_resolution_status
relation_scope
context_scope
source effective ordinal
source/compiler model ID, version and digest
```

compiler의 closed profile은 다음 field만 가진다.

```text
positive_direction_support       # tagged ordinal 0/1/2
negative_direction_support       # tagged ordinal 0/1/2
source_kinds_used
contested_present
accessibility_relation
effective_before_access_ordinal
```

이 profile은 durable TargetForm object가 아니라 declared source projection이다.

한 target의 source가 명시된 cross-target relation 없이 다른 target의 readout을 바꾸면
실패다. 같은 interpreted target도 relation/context scope가 다르면 별도 readout이다.

### 경쟁 source compiler

| model | exact source allowance |
|---|---|
| `TF0` | scoped synthetic `NarrativeTerrainFixture` support의 componentwise max |
| `TF1` | `TF0` + scoped prior adopted `EpisodeIntegrationReceipt` support의 componentwise max; contested receipt는 unsettled로만 보존 |
| `TF2` | `TF1` + pre-access accessibility를 통과한 scoped implicit/plastic support의 componentwise max |

`contested` source는 adopted integration으로 cast하지 않는다. implicit/plastic trace는
authored Narrative source로 cast하지 않는다. pre-access accessibility는 source content를
mutate하지 않고 compiler ordinal에서 사용할 수 있는 source relation만 제한한다.

source contribution은 `source_kinds_used`와 scope lineage를 보존한다. contested source는
`source_position + source_kind + contested_present`만 unsettled diagnostic으로 남기고,
그 direction profile·status·opaque alias는 D1 출력이 아니며 readout max에 절대
들어가지 않는다.
방향 성분을 하나의 signed scalar로 합치거나 conflicting source를 임의로 승자 하나로
만들지 않는다. exact projection
operator와 missingness는 execution manifest에 고정되며 compiler output은 그 선언 이외의
field를 만들 수 없다.

### Block A matrix

```text
fixtures: srcfx001 ... srcfx008
models per fixture: TF0, TF1, TF2
isolated cells: 8 × 3 = 24
```

fixture family는 최소한 다음을 포함한다.

- terrain-only source에서 TF0/TF1/TF2 agreement
- prior adopted integration source가 TF0/TF1을 가를 수 있는 contrast
- contested source가 adopted source와 같지 않음을 보이는 contrast
- implicit/plastic source와 accessibility가 TF1/TF2를 가를 수 있는 contrast
- 같은 actor의 target A source가 target B로 누출되지 않는 control
- relation/context scope와 target-resolution status 보존
- positive/negative direction mirror와 source-order mirror
- 같은 pre-k source set에 post-k source만 함께 선언한 matched fixture에서
  compiler projection이 바뀌지 않는 effective-order control

### Block A 판정

```text
TF0 == TF1 == TF2
on SOURCE_SUBSTANTIVE across all 8 fixtures
→ 아래 두 factor-retirement 조건이 모두 성립할 때만 TF0로 축소 검토

TF0 == TF1
on SOURCE_SUBSTANTIVE across all 8 fixtures
→ adopted Episode-integration source allowance만 제거
↛ contested diagnostic을 readout support로 cast하거나 그 diagnostic으로 factor를 구제

TF1 == TF2
on SOURCE_SUBSTANTIVE across all 8 fixtures
→ implicit/plastic + pre-access accessibility source allowance 제거
```

다른 readout을 산출했다는 사실만으로 source model이 downstream에 필요하거나 실제 인간의
Episode/Narrative가 TargetForm을 형성한다고 판정하지 않는다.

## Block B — `ENCOUNTER_FORMATION`

### 목적

pre-access TargetForm과 ReceptionState가 current access에서 생성되는
`SubjectiveEncounterFormProxy`에 필요한지 분리한다. Block B의 TargetForm은 declared
intervention input이다. Block A compiler output과 같은 cell에서 혼용하거나 source-derived
TargetForm이라고 보고하지 않는다.

### 2×2 formation intervention

| model | ReceptionState formation edge | TargetForm formation edge |
|---|---|---|
| `E0` | 없음; current source base formation만 사용 | 없음 |
| `ER` | declared reception-eligibility operator만 사용 | 없음 |
| `ET` | 없음 | declared target-directional-compatibility operator만 사용 |
| `ERT` | reception eligibility 사용 | target compatibility 사용; 두 operator를 별도 적용 |

`E0`는 current source-only formation baseline이다. `ER`와 `ET`는 각각 하나의 pre-access
input만 읽고, `ERT`는 두 operator를 별도로 호출해 hidden interaction이나 하나의
`reception × target congruence` scalar를 만들지 않는다. interaction이 필요해 보여도 frozen
v1 결과를 본 뒤 추가하지 않고 새 manifest version에서 사전등록한다.

formation operator는 expected direction이나 adjudication label을 입력받지 않는다.
pre-access R/T가 같은 current source의 주관적 proxy를 기울일 수는 있지만, source
occurrence, source encounter receipt, material provenance 또는 external evidence를 바꾸지
않는다. no current access에서는 어떤 formation model도 새 encounter를 만들지 않는다.

### Block B matrix

```text
fixtures: encfx001 ... encfx008
models per fixture: E0, ER, ET, ERT
isolated cells: 8 × 4 = 32
```

fixture family는 최소한 다음을 포함한다.

- same source + same TargetForm, different ReceptionState
- same source + same ReceptionState, different object-scoped TargetForm
- exact R×T crossed pair에서 ER/ET/ERT factorization
- high-positive/high-negative와 low/low를 scalar net-valence가 합치지 못하는 contrast
- same dominant direction에서 ambiguity/activation만 다른 contrast
- strong current source가 prior TargetForm이나 ReceptionState의 absolute gate가 아님을
  보이는 control
- no current access와 source-free current access에서 content를 발명하지 않는 control
- positive/negative direction mirror와 target-scope mismatch control

formation으로 같은 proxy가 나온 matched pair에서는 formation-only downstream 차이가
남아서는 안 된다. 차이가 남으면 R/T가 encounter proxy를 우회해 답을 직접 쓴 것이다.

### Block B 판정

```text
E0 == ER AND ET == ERT
on FORMATION_SUBSTANTIVE across all 8 fixtures
→ ReceptionState formation edge 제거

E0 == ET AND ER == ERT
on FORMATION_SUBSTANTIVE across all 8 fixtures
→ TargetForm formation edge 제거

ERT requires unregistered interaction
→ frozen v1로 지원하지 않고 새 version 전까지 HOLD
```

Block B가 성공해도 supplied TargetForm에 대한 synthetic input sensitivity만 성립한다.
Block A source compiler의 성공이나 인간의 기분·퀄리아 법칙을 대신하지 않는다.

## Block C — `GHOST_PATH`

### 목적

current access가 공급한 material identity와 order를 네 model에 대해 정확히 고정하고,
pre-access TargetForm context와 externally frozen Ghost path의 기여를 2×2로 분리한다.
ReceptionState, source content, component magnitudes, substrate topology와 adjudicator policy도
matched cell 사이에서 동일하다.

### 2×2 Ghost ablation

| model | TargetForm context available to Ghost | declared path variation |
|---|---|---|
| `G0` | neutral/no-effect control | fixed canonical traversal |
| `GT` | supplied object-scoped pre-access TargetForm이 candidate eligibility에만 관여 | fixed canonical traversal |
| `GP` | neutral/no-effect control | manifest-declared Ghost program |
| `GTP` | supplied TargetForm이 candidate eligibility에 관여 | 같은 manifest-declared Ghost program |

path/program은 result에 맞춰 adaptive하게 선택하지 않는다. execution 전에 operation sequence,
frontier/budget, topology view, fixed phase order와 available information을 고정한다. `broaden`, `contrast`,
`counterfactual`, `confirmation-only`, `rehearsal`은 outcome label이 아니라 등록된
탐색 연산이다.

Ghost가 기록할 수 있는 것은 다음 구조적 trace뿐이다.

```text
exact accessible material positions and order
visited material positions and order
registered exploration operations and phase order
created/proposed candidate relation
candidate set before adjudication
```

Ghost program은 immutable candidate view만 transform하고 source/material을 mutate하거나
Evidence를 만들지 않는다. candidate generation과 adjudication은 별도이며 program은
adjudicate하거나 integrate하지 않는다.

```text
Ghost exploration trace
≠ candidate endorsement
≠ BindingAdjudicationReceipt
≠ EpisodeIntegrationReceipt
≠ TargetForm revision
≠ Narrative write
```

같은 candidate set인데 model에 따라 adjudication label만 달라지면 Ghost-path 효과가
아니다. path 차이가 visited subset으로 전부 설명되면 그 효과는 별도 access/path-selection
mechanism으로 축소한다. 최소 한 matched control은 accessible set뿐 아니라 visited set과
order도 같게 두고 operation/relation 차이만 비교한다.

### Block C matrix

```text
fixtures: ghfx001 ... ghfx008
models per fixture: G0, GT, GP, GTP
isolated cells: 8 × 4 = 32
```

fixture family는 최소한 다음을 포함한다.

- exact access/topology에서 TargetForm-only contrast `G0` vs `GT`
- exact access/topology에서 path-only contrast `G0` vs `GP`
- TargetForm × path full factorial `G0/GT/GP/GTP`
- same accessible and visited set/order, different registered operation relation
- 같은 path가 material graph에 따라 positive/negative/contested candidate를 만들 수 있는
  direction mirror
- confirmation-only나 rehearsal이 항상 극단화하고 broaden이 항상 완화하도록 결과가
  이름에 박혀 있지 않은 mirror
- no material/no access에서 Ghost가 candidate를 발명하지 않는 control
- target A guidance/path가 target B candidate를 바꾸지 않는 scope-mismatch control

### Block C 판정

```text
G0 == GT AND GP == GTP
on GHOST_SUBSTANTIVE across all 8 fixtures
→ TargetForm context 자유도 제거

G0 == GP AND GT == GTP
on GHOST_SUBSTANTIVE across all 8 fixtures
→ variable Ghost path 제거

every G0/GP substantive difference
co-occurs with an access/visit difference
AND at least one substantive difference exists
→ interpretation mechanism이 아니라 access/path-selection mechanism으로 축소
```

Ghost는 완화 최적화기가 아니다. broaden, rehearsal 또는 counterfactual 중 어떤 연산도
보편적으로 더 합리적·긍정적·건강한 결과를 보장하지 않는다.

## Evaluator-only development / sealed split

execution manifest는 fixture input, model과 operator만 포함한다. development/sealed
membership, semantic family, mirror relation, expected signature, retirement predicate와
pass/fail label은 evaluation manifest에만 존재한다.

| block | development fixtures | sealed fixtures |
|---|---|---|
| `SOURCE_COMPILER` | `srcfx001`–`srcfx004` | `srcfx005`–`srcfx008` |
| `ENCOUNTER_FORMATION` | `encfx001`–`encfx004` | `encfx005`–`encfx008` |
| `GHOST_PATH` | `ghfx001`–`ghfx004` | `ghfx005`–`ghfx008` |

future runner/source compiler/operator는 execution manifest만 읽고 serialized run을 만든 뒤
종료해야 한다. 별도 evaluator만 raw run과 evaluation manifest를 읽는다. evaluation manifest,
source compiler, operator declaration과 implementation digest는 sealed result를 보기 전에
고정한다. result를 본 뒤 expected predicate, path, source contribution 또는 fixture를
바꾸면 새 version·digest와 prior run 보존이 필요하다.

development fixture는 schema, lineage, operator invocation과 mechanical invariant를
확인하는 데 쓸 수 있다. sealed fixture는 같은 frozen implementation으로만 평가한다.
exact grouping은 evaluation manifest에 직렬화된 evaluator-only metadata다. 이 구분은
runner/operator API에서만 보이지 않으며, 연구자에게 숨겨진 답이나 독립 예측
partition을 주장하지 않는다. mirror pair는 같은 partition에 있을 수 있고, role-blind
opaque identity를 제거한 뒤에도 development/sealed를 exact structural duplicate로 가정하지
않는다.

`sealed`는 이 repository에서 인간 자료를 숨겼다는 뜻이 아니다. evaluator-only synthetic
role이며, 이 split의 성공도 human prediction 또는 external validity가 아니다.

## 공통 challenger와 축소 규칙

D1 evaluator는 복잡한 model끼리만 비교하지 않는다. 각 block에서 적용 가능한 범위에
다음 simple challenger를 등록한다.

- material count와 componentwise magnitude/max profile
- dominant-direction category
- fixed direction/rank threshold
- reception–target congruence boolean
- simple declared target/reception lookup
- fixed access/topology/adjudication baseline

복잡 model의 sealed semantic signature가 challenger와 같으면 그 challenger와 공유하는
**named comparison target** 안에서만 구별력을 유지할 근거가 줄어든다. 이는 인간
예측력 판정이 아니라 frozen synthetic fixture 안의 target-scoped 축소 규칙이다.

```text
complex D1 model == simpler challenger on one named common target
→ REDUCE discriminability on that target only
↛ retire the whole model, block, factor or full ordinal profile
```

factor 자체의 제거는 별도로 사전등록된 factor-retirement predicate가 해당 block의 모든
필요 projection과 fixture에서 성립할 때만 검토한다.

## 즉시 무효 조건

다음은 observational equivalence가 아니라 run/contract 무효다.

- runner/compiler/operator가 evaluation manifest, split role, semantic alias 또는 expected
  output을 읽음
- current/future candidate·adjudication·integration 또는 sealed outcome이 Block A source에
  들어감
- supplied TargetForm label과 source-derived TargetForm을 같은 source claim에서 혼용함
- ReceptionState와 TargetForm을 하나의 hidden scalar나 중복 operator로 계산함
- Ghost path를 outcome, adjudication 또는 expected direction을 본 뒤 선택함
- Ghost arm의 candidate trace는 같은데 adjudication label만 직접 바꿈
- material에 mutable accessibility/assembled/unsettled enum을 저장함
- TargetForm/Reception/Ghost가 Evidence strength, source truth, external target identity,
  action, authority 또는 WorldOutcome을 만듦
- no-access 상태에서 새 encounter/candidate를 만들거나 과거 source/encounter를 재작성함
- 한 target의 source가 명시된 relation 없이 다른 target으로 누출됨
- access ordinal k의 output을 encounter k 또는 readout-before-k에 다시 사용함
- adjudication/integration에서 durable TargetForm 또는 Narrative Field를 자동 write함
- sealed result를 본 뒤 같은 manifest version의 compiler, fixture, path, predicate를 retune함

## 기준 출력과 비출력

후속 D1 machine run의 기준 출력은 source/readout, encounter-formation과 Ghost/candidate의
detached structural projection이다. exact closed-world field는 execution/result schema에
고정한다. evaluator는 append-only candidate/adjudication lineage를 비교할 수 있지만,
D1 run은 그 결과를 현재나 이후 cell의 source로 소비하지 않는다.

`interp-001d1-v1-run.schema.json`은 후속 runner가 만들어야 할 88-cell envelope,
execution/result-schema digest, runner implementation/bundle digest, evaluation invisibility와 run
integrity를 미리 고정한 **future carrier schema**다. D1은 runner나 executed run artifact를
만들지 않는다.

다음은 D1의 명시적 비출력이다.

```text
durable TargetForm state or writer
TargetFormReadoutChangeReceipt / revision
retention, decay, reconsolidation or revalidation
same-ordinal or later-access feedback
authored Narrative Field write
implicit-formation writer
runtime Ghost agent or adaptive path selector
HumanState, routing, Evidence, action or WorldOutcome change
separate persistent ExperienceFragment store
actual qualia or first-person experience
human mood, memory, Episode or Narrative measurement
recovery, relationship health, MorphicLoad or mental-time quantity
```

## 성공 의미와 claim 상태

Block A 성공은 outcome-blind synthetic source compiler가 TF0–TF2 사이의 declared
readout distinction을 만든다는 뜻이다. Block B 성공은 supplied pre-access intervention에
대한 synthetic formation sensitivity다. Block C 성공은 exact-access fixture 안에서
TargetForm context나 declared path가 candidate 구조를 구분한다는 뜻이다.

```text
A success ≠ B success ≠ C success

all three synthetic successes
≠ actual human TargetForm exists
≠ human Episode/Narrative source law
≠ Ghost is human reason or consciousness
≠ predictive superiority
≠ human empirical support
```

manifest freeze와 schema validation만으로 `HM-DYN-004`, `HM-INV-013`,
`HM-TYPE-008` 또는 `HM-TYPE-009`의 implementation status를 올리지 않는다. 실행 전
상태는 `FROZEN / UNEXECUTED`이며 structural support도 아직 비어 있다. D1 실행이
conform하더라도 human/predictive claim은 별도 measurement, hidden oracle와 held-out
human protocol 전까지 `OPEN`이다.

## 다음 gate

먼저 후속 D1 runner/evaluator가 frozen execution manifest와 carrier schema만으로 88-cell run을
생성·검증하고, retuning 없이 block별 구별과 target-scoped retirement rule을 판정해야
한다. 그 다음에만 `INTERP-001D2`를 연다. D2는 다음을 별도로 사전등록해야
한다.

- access ordinal보다 늦게만 effective한 TargetForm source/readout change
- writer, retention, decay, revalidation과 reconsolidation
- current access가 없는 상태 변화의 no-op
- future extension에 대한 prefix stability
- outcome/retention protocol과 단순 baseline

D2 성공 전에는 TargetForm을 `HumanState`의 durable field로 추가하거나 Episode/Narrative
writer와 접합하지 않는다.
