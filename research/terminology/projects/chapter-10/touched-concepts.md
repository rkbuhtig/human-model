# Chapter 10 — Touched Concepts

이 문서는 Chapter 10 배치가 기존 C-ID와 대조한 위치, 기존 C-ID가 소유하지 않는 maintenance·sleep·dream·forgetting 후보의 목적지를 기록한다.

정의는 `termbase/concepts/`, 후보 설명은 `extraction-map.md`, 형제 비교와 concept 판정은 후속 `termbase/clusters/`가 소유한다.

이번 intake는 기존 concept 정의·특성·판정을 변경하지 않는다.

## 1. 기존 concept 대조

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH10-027` maintenance influence가 later event path를 통과함
  - `X-CH10-056` maintenance scheduling pressure와 epoch occurrence 분리
  - `X-CH10-062` RouteCalib
  - `X-CH10-074~080` DreamSim·dream influence·later call
  - `X-CH10-113~115` Dread routing·Readdress·Contraction
- 유지한 경계:

```text
internal candidate가 생성됨
≠ routing weight가 바뀜
≠ address가 재배치됨
≠ maintenance window가 요구됨
≠ sleep epoch가 실제 발생함
≠ 행동 경로가 선택됨
≠ body execution이 승인됨
≠ external action이 수행됨
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `RouteCalib RELATED-TO C0001`, 상태 `HOLD`.
  - `Readdress signal RELATED-OR-PART-OF selection preparation`, 상태 `HOLD`.
  - `Contraction`은 선택 결과·정책 regime·body response 가운데 무엇인지 미정이다.
- 주의:
  - future policy를 기울이는 state change를 이번 tick의 행동 경로 선택과 synonym `MERGE`하지 않는다.
  - sleep necessity pressure를 actual SleepState occurrence로 읽지 않는다.
  - dream 내용과 later action의 authorship을 자동 동일시하지 않는다.

### C0002 — 외부 occurrence

- 사용한 후보:
  - `X-CH10-027` internal maintenance→later event path
  - `X-CH10-070` EvidenceBoundRepairPerformance
  - `X-CH10-080` dream influence 뒤 actual world contact
  - `X-CH10-083` ReplayEvent
  - `X-CH10-085` DreamReport
  - `X-CH10-089` forgetting ≠ past occurrence deletion
- 유지한 경계:

```text
DreamExperience가 생김
≠ dreamed external event가 실제 발생함

ReplayEvent가 신경계에서 발생함
≠ 기억 내용의 외부 사건이 다시 발생함

DreamReport가 발화됨
≠ report 내용의 external occurrence가 성립함

repair 계획이 생김
≠ 실제 repair action이 수행됨
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `ReplayEvent`는 생물 내부 occurrence 후보일 수 있으나 C0002의 외부 occurrence와 scope가 다르다.
  - `DreamReport`는 external speech occurrence일 수 있지만 dreamed event의 occurrence가 아니다.
  - `EvidenceBoundRepairPerformance`와 performed action의 generic/partitive 관계는 action cluster에서 비교한다.
- 주의:
  - 기억·꿈·simulation의 내용과 실제 world occurrence를 합치지 않는다.
  - current forgetting이나 reinterpretation이 past occurrence를 소급 mint·삭제하지 않는다.

### C0003 — 결과 상태 후보군

- 사용한 후보:
  - `X-CH10-063~066` Readdr objectives와 output gap
  - `X-CH10-071` AppliedLedgerRepair
  - `X-CH10-086` LaterPerformance
  - `X-CH10-102~103` bounded backlog·sleep sufficiency
  - `X-CH10-115~120` relief·repair·safe stopping·viability·felt state
- 유지한 경계:

```text
maintenance objective가 선언됨
≠ maintenance operation이 성공함
≠ backlog가 실제 감소함
≠ later performance가 향상됨
≠ external repair outcome이 실현됨
≠ ledger repair가 APPLIED됨

PredictedMaintenanceFeasibility
≠ ActualLongTermViability
≠ OperationalRelief
≠ FeltRelief
≠ FeltSatisfaction
```

- 판정: `HOLD` 유지.
- 보류 이유:
  - Readdr objective는 목표 함수 후보이지 result state가 아니다.
  - LaterPerformance는 과제 결과, AppliedLedgerRepair는 application status, viability는 장기 상태, felt relief는 current surface다.
  - `sleep exists`가 bounded backlog나 maintenance success를 보증하지 않는다.
- 주의:
  - Chapter 10은 C0003의 단일 genus를 닫지 않는다.
  - operational improvement·biological outcome·external relation outcome·accounting settlement를 한 결과 concept로 만들지 않는다.

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH10-024` dream/forget의 evidence firewall
  - `X-CH10-027` later EventRecord path
  - `X-CH10-071` AppliedLedgerRepair
  - `X-CH10-085` DreamReport
  - `X-CH10-089~098` world occurrence·memory trace·external evidence 분리
- 유지한 경계:

```text
occurrence record
≠ internal memory trace
≠ DreamExperience
≠ DreamReport content
≠ replay trace
≠ maintenance log
≠ access/readdress history
≠ applied repair state
≠ external evidence artifact 전체
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `DreamReport` 발화 자체의 record는 C0004와 관련될 수 있으나 report 내용이 묘사한 dreamed event의 record는 아니다.
  - `ExternalEvidence`는 occurrence record를 포함·가리킬 수 있지만 evidence 전체와 C0004는 동일하지 않다.
  - `maintenance trace`가 operation occurrence를 기록할 수 있어도 plasticity state 자체와 record는 다르다.
- 주의:
  - memory trace·replay event·dream report를 occurrence record에 자동 병합하지 않는다.
  - 개인 망각을 external record deletion으로 번역하지 않는다.

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH10-040` Dread가 backlog의 고유 readout이 아님
  - `X-CH10-082` DreamExperience
  - `X-CH10-111~113` fatigue·dread·elevation pressure
  - `X-CH10-115~120` Contraction·relief·felt satisfaction
  - `X-CH10-121~122` sleep 중 current Ghost realization Bridge
- 유지한 경계:

```text
피로를 느낌
≠ operational backlog의 크기를 앎
≠ metabolic damage를 앎

불길함을 느낌
≠ 실제 위험이 확인됨
≠ sleep deprivation이 원인임을 앎

꿈을 경험함
≠ dream content가 외부 사실임
≠ ReplayEvent를 직접 관측함

안도·충족을 느낌
≠ repair가 수행됨
≠ 실제 장기 viability가 확보됨
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `DreamExperience`, fatigue, dread, felt relief, felt satisfaction은 C0005의 사례 또는 좁은 후보일 수 있으나 서로 다른 phenomenal genus일 수 있다.
  - `SleepState`는 현재 체험 표면이 아니라 표면·반응성의 조건이 되는 생물 상태 후보다.
  - `CurrentGhost`는 surface보다 넓은 current assembly Bridge다.
- 주의:
  - C0005를 모든 sleep state·dream process·load signal·subject의 바구니로 만들지 않는다.
  - felt state를 hidden stock·truth·viability의 measurement로 쓰지 않는다.

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH10-023~029` Open Intake·maintenance influence·authority closure
  - `X-CH10-061~067` Readdr·RouteCalib
  - `X-CH10-073~080` maintenance/dream influence
  - `X-CH10-084` PlasticityChange
  - `X-CH10-113~117` Dread·Contraction·relief
  - `X-CH10-124` nonselected internal change Bridge
- 유지한 경계:

```text
DreamSim
Readdr
RouteCalib
PlasticityChange
Dread
Contraction
SleepState
MaintenanceResult

≠ C0006

위 entity·state·operation·signal이
Grounds·Warrant·writer authority 없이
다음 access·candidate·policy·행동을 바꾸는 relation
= C0006과 대조할 위치
```

- 판정: `KEEP` 유지.
- 확인된 대비:
  - DreamSim은 future routing을 바꿀 수 있어도 truth-token을 발행하지 않는다.
  - Readdr는 access geometry를 바꿀 수 있어도 external evidence를 만들지 않는다.
  - forgetting·plasticity는 다음 상태를 바꿀 수 있어도 past occurrence를 다시 쓰지 않는다.
  - dread는 routing signal일 수 있어도 위험 truth가 아니다.
- 관계 후보:
  - `Dream-associated source --C0006 relation--> later policy/access change`, 상태 `HOLD`.
  - `MaintenanceResult --C0006 relation--> future behavior`, 상태 `HOLD`.
  - `PlasticityChange NARROWER-OR-RELATED-CANDIDATE-OF persistent non-authoritative influence`, 상태 `HOLD`.
- 주의:
  - DreamSim·Readdr·Dread entity를 C0006 concept에 병합하지 않는다.
  - `during sleep`, `next morning`, `through AddrSig`를 C0006의 보편 필수 특성으로 올리지 않는다.
  - `gauge-only` 철자를 causal inertness로 읽지 않는다.

### C0007 — 수행 활동 후보군

- 사용한 후보:
  - `X-CH10-031~034` μ_proc operator family
  - `X-CH10-059~067` Compression·Reindex·Readdr·RouteCalib
  - `X-CH10-068~072` repair preparation/performance/application 분리
  - `X-CH10-083~084` replay와 plasticity event/process
  - `X-CH10-104~106` local/wake maintenance implementation
- 유지한 경계:

```text
maintenance demand가 존재함
≠ maintenance operation이 수행됨

Compression이 명명됨
≠ 실제 compression work가 관측됨

Readdr objective가 있음
≠ readdress work가 수행됨
≠ access geometry가 실제로 개선됨

repair candidate가 준비됨
≠ external repair work가 수행됨
≠ repair result가 applied됨

ReplayEvent가 발생함
≠ plasticity work 전체가 수행됨
```

- 판정: `HOLD` 유지.
- 후속 cluster 질문:

```text
Compression·Reindex·Readdr·RouteCalib는 maintenance activity의 종개념인가?
아니면 하나의 maintenance process의 부분 단계인가?
RepairPreparation은 수행 노동인가 planning state인가?
ReplayEvent는 maintenance operation인가 condition·input·occurrence인가?
PlasticityChange는 수행 활동인가 transition result인가?
```

- 주의:
  - 연산명·rate가 있다는 이유로 실제 노동 수행을 승인하지 않는다.
  - operation, process part, resource expenditure, result state, record를 분리한다.
  - C0007의 genus는 Chapter 10에서도 닫히지 않는다.

### C0008 — 실제 자원 지출

- 사용한 후보:
  - `X-CH10-021~045` intake·throughput·backlog·capacity
  - `X-CH10-048~057` allocation·service capacity
  - `X-CH10-063~068` cost objectives와 PaidRepair
  - `X-CH10-102` long-run service condition
  - `X-CH10-111~120` fatigue·ContinuityTax·relief
  - `X-CH10-123` typed MaintenanceDemand Bridge
- 유지한 경계:

```text
input rate
≠ workload admitted
≠ operation performed
≠ actual resource expenditure

capacity
≠ current Spend

backlog stock
≠ expenditure occurrence

ContinuityTax
≠ metabolic energy
≠ attention expenditure
≠ normative debt

felt fatigue
≠ measured resource expenditure

PaidRepair label
≠ actual paid resources observed
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - 실제 maintenance work가 time·attention·energy를 사용했다는 독립 관측이 있을 때 C0008과 대조한다.
  - `μ_proc`는 capacity/service readout 후보이지 expenditure occurrence가 아니다.
  - `MaintenanceDemand`는 요구·부담 후보이지 Spend가 아니다.
- 주의:
  - `metabolic`, `cost`, `tax`, `paid`, `load` 철자만으로 C0008에 병합하지 않는다.
  - operational burden과 normative debt를 다시 합치지 않는다.

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보:
  - `X-CH10-035~045` backlog state와 queue history 가능성
  - `X-CH10-047` GateTrace
  - `X-CH10-067` internal/public Readdr scope
  - `X-CH10-068~073` repair preparation·performance·application
  - `X-CH10-075` dream update signal
  - `X-CH10-085` DreamReport
  - `X-CH10-090~098` memory trace·evidence·forgetting
  - `X-CH10-124~128` plasticity·handoff Bridge
- 유지한 경계:

```text
backlog state
≠ backlog measurement record
≠ maintenance work record
≠ expenditure record
≠ GateTrace input
≠ PlasticityTrace
≠ DreamReport
≠ memory trace
≠ readdress history
≠ repair performance record
≠ applied settlement record
≠ responsibility/authority record
```

- 판정: `HOLD / SUBJECT-FIELD SPLIT` 유지.
- 강화된 이유:
  - Chapter 10은 state·operation·input trace·memory trace·report·evidence·repair record가 다시 갈라짐을 보여준다.
  - `trace`, `log`, `stock`, `record`가 같은 runtime에 있어도 concept 동일성이 생기지 않는다.
  - operational backlog와 accounting backlog를 후대 문서가 분리·재혼합한 이력도 C0009 바구니화를 경고한다.
- 주의:
  - C0009를 모든 maintenance·memory·dream 기록의 상위 concept로 되살리지 않는다.
  - B_backlog 자체를 accounting record로 읽지 않는다.

## 2. 기존 C-ID가 소유하지 않는 주요 후보군

### 2.1 Maintenance Demand family

```text
X-CH10-035~045  operational backlog·measurement gap
X-CH10-099      overload possibility
X-CH10-107      multi-process sleep-linked demand
X-CH10-123      typed MaintenanceDemand Bridge
X-CH10-141      demand/operation/regime/state cardinality boundary
```

- 상태: 전부 `HOLD`; `X-CH10-123`은 `BRIDGE-CURRENT / SUBJECT-FIELD`.
- 기존 C-ID는 actual work·spend·record를 일부 다루지만 maintenance demand 자체를 소유하지 않는다.
- 후속 질문:

```text
MaintenanceDemand는 state인가 relation인가 task set인가?
OperationalBacklog는 demand의 종인가 원인인가 결과인가?
서로 다른 demand는 공통 genus가 있는가, 단지 coordination subject field인가?
```

### 2.2 Maintenance Operation family

```text
X-CH10-059 Compression
X-CH10-060 Reindex
X-CH10-061 Readdr
X-CH10-062 RouteCalib
X-CH10-068~072 RepairPreparation / Performance / Application
```

- 상태: 전부 `HOLD`.
- C0007과의 generic/partitive 관계가 미정이다.
- `Compression / Reindex / Readdr / RouteCalib`가 하나의 process의 부분인지 서로 다른 activity type인지 cluster에서 비교한다.
- `AppliedLedgerRepair`는 operation보다 result/application status일 가능성이 크다.

### 2.3 Maintenance Scheduling / Regime family

```text
X-CH10-046~050 GateTrace·sleep interval·allocation
X-CH10-051~058 resource conflict·online/local alternatives·determinism
X-CH10-101~106 necessity gap·local/wake implementation
X-CH10-125 noncommutativity Bridge
```

- 상태: direct candidates는 `HOLD`; Bridge는 `BRIDGE-CURRENT / HOLD`.
- 구분:

```text
scheduling pressure
≠ selected schedule
≠ maintenance interval occurrence
≠ biological SleepState
≠ global coordination envelope
```

- `SleepState NARROWER-CANDIDATE-OF MaintenanceRegime` 여부는 미정이다.
- 생물 상태가 추상 regime을 realize할 수 있어도 synonymy는 아니다.

### 2.4 Sleep State / Coordination family

```text
X-CH10-048~050 𝓔_sleep / sleep-as-maintenance mode
X-CH10-057~058 service sufficiency / coordination envelope
X-CH10-081 SleepState
X-CH10-105~109 local·unihemispheric·wake pattern·evolution scope
X-CH10-108 Sleep=GC role conflict
```

- 상태: 전부 `HOLD`.
- 외부 감사는 global Boolean 하나보다 stage·region·species별 state family를 지지하는 대비를 제공한다.
- external audit로 `KEEP`을 바로 주지 않는다. historical term과 human/biological concept cluster를 먼저 분리한다.

### 2.5 Dream / Replay / Plasticity family

```text
X-CH10-074 DreamSim
X-CH10-082 DreamExperience
X-CH10-083 ReplayEvent
X-CH10-084 PlasticityChange
X-CH10-085 DreamReport
X-CH10-086 LaterPerformance
X-CH10-087 causal gap
```

- 상태: 전부 `HOLD`.
- 가장 중요한 경계:

```text
SleepState
≠ DreamExperience
≠ ReplayEvent
≠ PlasticityChange
≠ DreamReport
≠ LaterPerformance
```

- 가능한 관계는 condition·correlation·causal·report-of·result-of로 나뉜다.
- temporal co-occurrence만으로 partitive relation을 승인하지 않는다.
- DreamSim은 SLEEP22 runtime operator이며 외부 연구의 DreamExperience와 direct synonym이 아니다.

### 2.6 Forgetting / Memory / History family

```text
X-CH10-088 Forget
X-CH10-090 InternalMemoryTrace
X-CH10-091 MemoryAccess
X-CH10-092 AutobiographicalSummary
X-CH10-093 ExternalEvidence
X-CH10-094~097 biological forgetting mechanisms
X-CH10-098 narrowed No-Free-Forgetting
```

- 상태: 전부 `HOLD`.
- 구분:

```text
MutableMemoryTrace
≠ MutableMemoryAccess
≠ MutableAutobiographicalSummary
≠ MutableExternalEvidence
≠ MutablePastOccurrence
```

- C0002·C0004는 occurrence와 record 경계를 제공하지만 memory ontology를 소유하지 않는다.
- `No-Free-Forgetting`은 audit rule 후보이며 biological trace law와 분리한다.

### 2.7 Internal / Public Readdress family

```text
X-CH10-018 ACCESS20 accountable readdress tension
X-CH10-019 SAT→SLEEP role drift
X-CH10-061~067 sleep Readdr·objectives·scope
X-CH10-114 Dread Readdress role drift
```

- 상태: 전부 `HOLD`.
- 구분:

```text
AddressUpdateSignal
≠ InternalReaddressOperation
≠ InternalAccessGeometryResult
≠ PublicReaddressAction
≠ PublicAddressChangeRecord
```

- internal/public은 단순 scope modifier가 아니라 writer·evidence·accounting 조건을 바꿀 수 있다.
- 같은 `Readdr` 철자로 `MERGE`하지 않는다.

### 2.8 Repair / Relief / Settlement family

```text
X-CH10-068 μ_repair / PaidRepair
X-CH10-069 InternalRepairPreparation
X-CH10-070 EvidenceBoundRepairPerformance
X-CH10-071 AppliedLedgerRepair
X-CH10-072 repair cardinality boundary
X-CH10-115~120 Contraction·relief·safe stopping
```

- 상태: 전부 `HOLD`.
- 구분:

```text
repair demand
≠ repair preparation
≠ repair work performed
≠ resource expenditure
≠ repair outcome
≠ ledger application / settlement
≠ felt relief
```

- C0007·C0008·C0003·C0004·C0009가 각각 일부 축과 대조되지만 전체를 소유하는 C-ID는 없다.

### 2.9 Operational Load / Cost / Spend family

```text
X-CH10-021~045 intake·capacity·backlog
X-CH10-063~065 maintenance objectives
X-CH10-111~120 continuity pressure·fatigue·relief
X-CH10-143 Operational Load ≠ Debt
```

- 상태: 전부 `HOLD`.
- 구분:

```text
load
≠ capacity
≠ demand
≠ work amount
≠ actual resource expenditure
≠ felt burden
≠ normative debt
```

- `Tax`, `Cost`, `Metabolic`, `Paid`는 concept 판정을 대신하지 않는다.

### 2.10 Sleep-to-Self Handoff family

```text
X-CH10-121 organism/handle/archive vs current Ghost
X-CH10-122 CurrentGhost / DiachronicSelfContinuity
X-CH10-124 nonselected internal change authorship gap
X-CH10-128 sleep-to-waking handoff
```

- 상태: 전부 `BRIDGE-CURRENT / HOLD`.
- Chapter 09 Handoff Cluster의 새 입력이다.
- 다음을 분리한다.

```text
organism persists
≠ identity handle persists
≠ archive traces persist
≠ current first-person assembly persists
≠ next Ghost adopts change
≠ next Ghost authored change
```

### 2.11 Persistent Non-Authority family

```text
X-CH10-028 authority/persistence separation
X-CH10-075 dream update signal
X-CH10-084 PlasticityChange
X-CH10-124 unconscious internal change
X-CH10-126 persistence-capable gap
X-CH10-127 QualiaAnnealing Bridge
```

- 상태: direct gap은 `HOLD`; Bridge labels는 `BRIDGE-CURRENT / HOLD`.
- Chapter 09의 `ρ/𝔄` middle-layer gap을 강화한다.
- 중요한 경계:

```text
persistent
≠ authoritative

causally effective
≠ evidence-bearing

PlasticityChange
≠ PlasticTrace record object
≠ Scar
≠ Debt
```

## 3. concept 관계 후보

관계 후보는 새 C-ID 개설 없이 기록한다.

```text
OperationalBacklog
  RELATED-TO MaintenanceDemand
  generic / causal / result relation: HOLD

Compression / Reindex / Readdr / RouteCalib
  PART-OF-OR-NARROWER-CANDIDATE-OF MaintenanceProcess
  relation kind: HOLD

SleepState
  MAY-REALIZE MaintenanceRegime
  relation kind: HOLD

GlobalSleepCoordination
  RELATED-TO local maintenance events
  relation kind: HOLD

DreamSim
  RELATED-TO DreamExperience / ReplayEvent / PlasticityChange
  relation kind and direction: HOLD

InternalMemoryTrace
  RELATED-TO MemoryAccess / AutobiographicalSummary
  relation kind: HOLD

InternalReaddress
  RELATED-TO AccessGeometryChange
  relation kind: HOLD

RepairPreparation
  PART-OF-OR-RELATED-TO RepairPerformance
  relation kind: HOLD

Dream-associated source
  --C0006 relation--> later access/policy change
  state: HOLD
```

`MERGE`는 없다.

## 4. 기호 epoch 결과

```text
B_A@RTO21
≠ B_backlog@SLEEP22

Θ_criticality@RTO21
≠ Θ_track@SAT22
≠ Θ_tracking-target@SLEEP22

F_t@FIELD20
≠ F_t@SPINE22 automatic succession

λ_in
= heterogeneous open-intake meta variable candidate

μ_proc
= operator-family aggregate candidate

𝓔_sleep
= maintenance interval/model state
≠ universal biological sleep essence
```

`ΦΩ@NEWQUAL22`는 Chapter 11 전방 예약만 남긴다.

## 5. source authority 결과

```text
HISTORICAL-DIRECT
MET22

HISTORICAL-COMPRESSION
SPINE22 / SPINE22C

PREHISTORY
ORIGIN02 / A41 / EOE09 / GEE10 / GHOST08 / ISG09 / ACCESS20

ADJACENT-HISTORICAL
SAT22

LATER-LEXICAL
REG23

DOWNSTREAM-WITNESS
CORE26 / MONO15 / LIFE23 / MINI27 / SYNTH27

EXTERNAL-AUDIT
sleep / replay / plasticity / dream / local-state studies

BRIDGE-CURRENT
noncommutativity / coordination envelope / typed demand / Ghost handoff / QualiaAnnealing
```

외부 감사와 Bridge는 역사 term origin을 바꾸지 않는다.

## 6. 후속 cluster queue

이번 intake 뒤 가능한 cluster는 다음과 같다. 순서는 이번 PR에서 확정하지 않는다.

1. **Maintenance Demand Cluster**
   - OperationalBacklog / ActiveLoad / IntegrationPressure / ContinuityLoad / process-specific demand
2. **Maintenance Operation Cluster**
   - Compression / Reindex / Readdr / RouteCalib / RepairPreparation
3. **Maintenance Scheduling Cluster**
   - scheduling pressure / gated interval / online-local-global alternatives / determinism
4. **Sleep State and Coordination Cluster**
   - global/local/stage/unihemispheric SleepState / coordination envelope
5. **Dream–Replay–Plasticity Cluster**
   - DreamSim / DreamExperience / ReplayEvent / PlasticityChange / DreamReport / LaterPerformance
6. **Forgetting–Memory–History Cluster**
   - trace / access / cue-index / pruning / source loss / external occurrence/evidence
7. **Internal–Public Readdress Cluster**
   - ΔAddr / InternalReaddr / AccessGeometryChange / PublicReaddress / address record
8. **Repair–Relief–Settlement Cluster**
   - demand / preparation / work / spend / result / settlement / felt relief
9. **Operational Load–Cost–Spend Cluster**
   - rate / capacity / backlog / workload / expenditure / debt
10. **Sleep-to-Self Handoff Cluster**
   - organism / handle / archive / CurrentGhost / next Ghost / adoption / authorship
11. **Persistent Non-Authority Cluster**
   - reversible state / update signal / PlasticityChange / PlasticTrace / authority register

기본값은 전부 `HOLD`다. 리뷰 뒤 경계가 가장 잘 드러난 cluster 하나만 다음 PR로 구체화한다.

## 7. 최종 판정

```text
C0001 KEEP 유지
C0002 KEEP 유지
C0003 HOLD 유지
C0004 KEEP 유지
C0005 KEEP 유지
C0006 KEEP 유지
C0007 HOLD 유지
C0008 KEEP 유지
C0009 HOLD / SUBJECT-FIELD SPLIT 유지
```

새 C-ID 없음. synonym `MERGE` 없음. 기존 concept 정의·특성·판정 변경 없음.

이번 배치의 종점은 다음 경계를 보존하는 것이다.

```text
MaintenanceDemand
≠ MaintenanceOperation
≠ MaintenanceRegime
≠ SleepState
≠ SleepNecessityClaim

DreamExperience
≠ ReplayEvent
≠ PlasticityChange

OperationalLoad
≠ Debt

DreamInfluence
≠ DreamWarrant

Forgetting
≠ HistoricalErasure

Relief
≠ Repair
```
