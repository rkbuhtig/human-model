# Chapter 09 — Touched Concepts

이 문서는 Chapter 09 배치가 기존 C-ID와 대조한 위치, 기존 C-ID가 소유하지 않는 identity·continuity·subject 후보의 목적지를 기록한다.

정의는 `termbase/concepts/`, 역사 후보 설명은 `extraction-map.md`, 형제 비교와 concept 판정은 후속 `termbase/clusters/`가 소유한다.

이번 intake는 기존 concept 정의·특성·판정을 변경하지 않는다.

## 1. 기존 concept 대조

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH09-055~056` Judgment/Norm과 typed call
  - `X-CH09-062` 전략적 선택 문턱
  - `X-CH09-066~069` Persona Policy Attractor
  - `X-CH09-070~077` plural proposals·Aggregate
  - `X-CH09-087` continuous call intensity/address adjustment
- 유지한 경계:

```text
proposal이 생성됨
≠ proposal weight가 커짐
≠ proposals가 집계됨
≠ call이 선택됨
≠ body execution이 승인됨
≠ external action이 수행됨

반복되는 선택 성향
≠ 이번 행동 경로 선택
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `Judgment/call selection RELATED-OR-NARROWER-CANDIDATE-OF C0001`, 상태 `HOLD`.
  - `Aggregate`는 선택 과정 후보지만 C0001 자체인지 partitive component인지 미정이다.
  - `PersonaPolicyAttractor`는 선택 성향을 조건 짓는 state/model 후보이며 선택 occurrence가 아니다.
- 주의:
  - policy fixed point를 action path selection과 synonym MERGE하지 않는다.
  - proposal plurality를 복수 선택자·복수 자아로 바꾸지 않는다.

### C0002 — 외부 occurrence

- 사용한 후보:
  - `X-CH09-056~058` call→Instrument→EventRecord
  - `X-CH09-096` public handle과 lived/authored 분리
  - `X-CH09-098` Thought-as-experience Bridge
  - `X-CH09-103` Episode/Narrative handoff
- 유지한 경계:

```text
내부 Thought가 경험됨
≠ external occurrence가 성립함

call이 선택됨
≠ Instrument interaction이 일어남
≠ EventRecord가 생김
≠ 현재 자아가 사건을 자기 역사로 인수함
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `Instrument interaction`과 external occurrence의 generic/partitive 관계는 후속 action cluster에서 비교한다.
  - `EventRecord`, `Episode`, `NarrativeAdoption`은 occurrence 자체가 아니다.
- 주의:
  - 생각이 내부 흔적을 남길 수 있다는 이유로 performed action으로 승격하지 않는다.
  - 현재 identity stance가 과거 occurrence를 소급 mint·삭제하지 않는다.

### C0003 — 결과 상태 후보군

- 사용한 후보:
  - `X-CH09-058` Update 적용 상태
  - `X-CH09-088~091` predicted/actual safe stopping
  - `X-CH09-083~085` discontinuous activation과 continuity inference
- 유지한 경계:

```text
EventRecord가 생성됨
≠ Update가 APPLIED됨
≠ external world outcome이 실현됨
≠ 결과가 관측됨
≠ 결과가 정산됨

safe-stopping이 예측됨
≠ 실제 장기 viability가 확보됨
≠ felt satisfaction이 생김
```

- 판정: `HOLD` 유지.
- 보류 이유:
  - APPLIED/REJECTED/NOOP는 update application status이며 world·relation outcome과 같은 genus인지 미정이다.
  - PredictedSafeStopping은 forecast state, ViabilitySafeStopping은 실제 생존 결과, FeltSatisfaction은 current surface 후보다.
- 주의:
  - Chapter 09은 C0003의 단일 genus를 닫지 않는다.

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH09-057~060` EventRecord·Update·𝔄
  - `X-CH09-094~096` attribution subject와 public handle
  - `X-CH09-103` EpisodeProvenance/NarrativeAdoption handoff
- 유지한 경계:

```text
occurrence record
≠ applied state update
≠ evidence artifact
≠ attribution/accountability subject
≠ Episode
≠ adopted self-history
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `EventRecord y`는 C0004의 역사적 좁은 후보 또는 관련 엔진 기록일 수 있으나 synonymy는 cluster에서 판정한다.
  - `EpisodeProvenance`는 여러 occurrence·experience·outcome의 묶음 계보 후보이며 occurrence record와 다르다.
- 주의:
  - public handle이 지속된다는 사실을 lived-by-me·authored-by-me로 번역하지 않는다.
  - `𝔄` 전체를 C0004로 흡수하지 않는다.

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH09-018~033` Q/Z/당김/제약/불일치/Φ/Meta/FlexCost
  - `X-CH09-051~052` SelfOn readout
  - `X-CH09-081~082` Φ continuity actor→label correction
  - `X-CH09-086~090` Dread·FeltSatisfaction
  - `X-CH09-093` ExperientialSubject
- 유지한 경계:

```text
현재 Φ에 방향·막힘이 느껴짐
≠ 외부 truth가 확인됨
≠ persistent medium state가 기록됨

SelfOn이 켜짐
≠ numerical identity가 증명됨
≠ organism이 계속 존재함
≠ public attribution subject가 동일함

불길함을 느낌
≠ 실제 위험을 앎

충족감을 느낌
≠ 실제 장기 safe-stopping이 성립함
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `Q/Z/Φ/Meta`는 C0005의 역사적 surface 구성 후보군이지만 content·render·readout·meta-readout이 서로 다른 genus일 수 있다.
  - `SelfOn`, Dread, FeltSatisfaction은 current surface와 가까우나 identity inference·routing·stability와 분리해야 한다.
  - `ExperientialSubject`는 surface가 아니라 그 surface가 현재 성립하는 subject-role 후보일 수 있다.
- 주의:
  - C0005를 모든 phenomenal component·readout·subject·identity feeling의 바구니로 만들지 않는다.
  - QUAL13 Φ를 QualiaMedium과 MERGE하지 않는다.

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH09-026` Φ next-tick influence
  - `X-CH09-039~041` Seed·body modulation
  - `X-CH09-047~053` AddrSig·bandwidth·trace bias
  - `X-CH09-061~062` Thought generation과 Judgment gate
  - `X-CH09-066~069` Persona Policy Attractor
  - `X-CH09-071~074` allocation·Aggregate·explanation
  - `X-CH09-086~087` Dread routing signal
- 유지한 경계:

```text
Φ
Seed
body rhythm
AddrSig
Persona attractor
proposal object
α allocation
Dread

≠ C0006

위 entity·state·readout이
권위 없이 다음 candidate·Access·policy·call을 바꾸는 relation
= C0006과 대조할 위치
```

- 판정: `KEEP` 유지.
- 확인된 대비:
  - current Φ는 next-tick 후보를 바꿔도 current ledger를 쓰지 못한다.
  - Seed·t_b는 easy/urgent/costly/vivid를 바꿔도 evidence·면책을 발행하지 않는다.
  - α_t는 proposal 발언 가중치지만 external Authority가 아니다.
  - Dread는 routing signal이지 truth-token이 아니다.
- 관계 후보:
  - `source entity --C0006 relation--> candidate/access/policy change`, 상태 `HOLD`.
- 주의:
  - identity 용어를 C0006에 병합하지 않는다.
  - `next-tick`, `through Access`, `through W`를 C0006의 보편 필수 특성으로 고정하지 않는다.

### C0007 — 수행 활동 후보군

- 사용한 후보:
  - `X-CH09-030~033` representation fitting·reconfiguration
  - `X-CH09-055~058` Judgment·call·Instrument·Update process
  - `X-CH09-072` Aggregate
  - `X-CH09-078~082` tracking·stitching work
  - `X-CH09-100` PlasticUpdateSignature Bridge
- 유지한 경계:

```text
불일치를 느낌
≠ 표상을 재배열하는 작업이 수행됨
≠ candidate 비교가 수행됨
≠ call이 선택됨
≠ external interaction이 수행됨

IdentityTracker state/hypothesis
≠ tracking operation
≠ continuity work amount
≠ resource expenditure
```

- 판정: `HOLD` 유지.
- 후속 cluster 질문:

```text
representation fitting은 수행 노동의 종인가?
Judgment/Aggregate는 하나의 decision process의 부분인가?
continuity stitching은 tracking process의 부분인가 별도 repair work인가?
PlasticUpdate는 수행 활동인가 state transition인가?
```

- 주의:
  - 계산·추론이 있다는 이유만으로 모든 후보를 C0007 아래 개설하지 않는다.
  - operation과 그 비용·결과·기록을 분리한다.

### C0008 — 실제 자원 지출

- 사용한 후보:
  - `X-CH09-030~032` FlexCost·Overstretch·Frustration
  - `X-CH09-039~040` Seed/body modulation과 Access budget
  - `X-CH09-048` Access bandwidth
  - `X-CH09-080` Continuity Tax
  - `X-CH09-088~091` safe-stopping·bill estimate
- 유지한 경계:

```text
필요 변형량
≠ 실제 수행량
≠ 실제 자원 지출

capacity limit
≠ current Spend

Continuity Tax
≠ metabolic energy
≠ actual resource expenditure
≠ normative debt

felt Frustration
≠ measured expenditure
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - actual tracking/stitching이 계산·주의·대사 자원을 사용했다는 독립 관측이 있을 때 C0008과 대조한다.
  - `B_A`는 capacity 상태 후보이지 지출 occurrence가 아니다.
- 주의:
  - Tax·Cost·Budget 철자만으로 C0008에 병합하지 않는다.

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보:
  - `X-CH09-037` instance provenance gap
  - `X-CH09-057~060` EventRecord·𝔄·typed update fields
  - `X-CH09-080` Continuity Tax
  - `X-CH09-094~096` attribution subject·ledger handle
  - `X-CH09-100` PlasticTrace Bridge
  - `X-CH09-103~105` provenance·responsibility·authority handoff
- 유지한 경계:

```text
EventRecord
≠ work-performance record
≠ expenditure record
≠ dependency/provenance trace
≠ attribution record
≠ continuity-work estimate
≠ PlasticTrace
≠ responsibility handoff record
≠ authority transfer record
```

- 판정: `HOLD / SUBJECT-FIELD SPLIT` 유지.
- 강화된 이유:
  - Chapter 09은 기록 대상이 occurrence, update, instance lineage, attribution subject, responsibility succession, authority transfer로 다시 갈라짐을 보여준다.
  - `𝔄`가 event/evidence/attribution/billing을 한 register에 넣어도 concept 동일성이 생기지 않는다.
- 주의:
  - C0009를 identity provenance와 모든 handoff 기록의 상위 바구니로 되살리지 않는다.

## 2. 기존 C-ID가 소유하지 않는 주요 후보군

### 2.1 identity identifier / contract family

```text
X-CH09-035  persistent contract
X-CH09-036  Persona / Identity Handle
X-CH09-037  instance provenance gap
X-CH09-038  handle persists while runtime feels unfamiliar
```

- 상태: 전부 `HOLD`.
- C0004·C0009는 handle의 record를 다룰 수 있어도 identifier/contract 자체를 소유하지 않는다.
- 후속 질문:

```text
handle은 identifier인가 contract인가 relation인가?
contract sameness와 instance sameness는 어떤 관계인가?
fork / merge / termination은 occurrence·record·authorized transfer 중 무엇을 요구하는가?
```

### 2.2 runtime state family

```text
X-CH09-045 Persona Runtime Object
X-CH09-047 AddrSig
X-CH09-048 B_A
X-CH09-049 θ_H
X-CH09-050 L_t
```

- 상태: 전부 `HOLD`.
- runtime object는 identity handle·current surface·policy attractor와 다르다.
- 구성요소 목록이 하나의 concept definition인지, 여러 typed state의 aggregate인지 미정이다.

### 2.3 current self readout family

```text
X-CH09-051 SelfOn
X-CH09-052 SelfOn failure mode
X-CH09-085 SelfOn ≠ IdentityTracker
X-CH09-090 FeltSatisfaction gap
```

- 상태: 전부 `HOLD`.
- C0005와 가까우나 readout content·mode·subject·identity feeling을 분리해야 한다.

### 2.4 policy attractor family

```text
X-CH09-066 Persona Policy Attractor
X-CH09-067 moving attractor
X-CH09-068 convergence gap
X-CH09-069 Handle/Attractor identity gap
```

- 상태: 전부 `HOLD`.
- operator·존재·유일성·복수 basin·transition 조건이 없으므로 model hypothesis다.
- C0001은 개별 선택을 소유하며 attractor state 전체를 소유하지 않는다.

### 2.5 continuity inference / work family

```text
X-CH09-078 Identity Tracker
X-CH09-079 tracking hypothesis firewall
X-CH09-080 Continuity Tax
X-CH09-081~082 Φ actor→label correction
X-CH09-083~084 activation jump possibility / missing premise
```

- 상태: 전부 `HOLD`.
- 구분:

```text
tracker state/hypothesis
≠ tracking operation
≠ stitching output
≠ felt continuity
≠ work amount
≠ resource expenditure
≠ proof of identity
```

### 2.6 subject-role family

```text
X-CH09-092 OrganismicContinuity
X-CH09-093 ExperientialSubject
X-CH09-094 AttributionSubject
X-CH09-095 relation gap
X-CH09-096 ledger subject ≠ self adoption
```

- 상태: 전부 `HOLD`.
- `subject`라는 공통 명칭만으로 generic relation을 승인하지 않는다.
- generic / partitive / associative 중 무엇인지 cluster에서 비교한다.

### 2.7 proposal object / committee family

```text
X-CH09-070 object proposal
X-CH09-071 allocation weight
X-CH09-072 Aggregate
X-CH09-073 explanation firewall
X-CH09-074 consensus firewall
X-CH09-075 proposal plurality ≠ identity plurality
X-CH09-076~077 committee/persona/SelfOn gap
```

- 상태: 전부 `HOLD`.
- OBJ object는 current proposal source일 수 있지만 person·alter·self가 아니다.

### 2.8 persistence-capable non-authoritative change

```text
X-CH09-034 QUAL13 persistence gap
X-CH09-097 ρ/𝔄 middle-layer gap
X-CH09-098 Thought-as-experience Bridge
X-CH09-100 PlasticTrace / QualiaMedium Bridge
```

- 상태: direct gap은 `HOLD`; Bridge labels는 `BRIDGE-CURRENT / HOLD`.
- 중요한 경계:

```text
persistent
≠ authoritative

reversible
≠ traceless

PlasticTrace
≠ stored record object
≠ EventRecord
≠ Evidence
≠ Scar
≠ Debt
```

### 2.9 handoff family

```text
X-CH09-101 BodyHandoff
X-CH09-102 Memory / AccessPolicy / Ghost Handoff
X-CH09-103 EpisodeProvenance / NarrativeAdoption Handoff
X-CH09-104 ResponsibilityBookkeepingHandoff
X-CH09-105 AuthorityScopeContinuity / AuthorizedTransferEvent
```

- 상태: 전부 `BRIDGE-CURRENT / HOLD`.
- 공통 `handoff` 철자가 같은 genus를 보증하지 않는다.
- 일부는 state succession, 일부는 provenance relation, 일부는 public legal/authority transition일 수 있다.

## 3. concept 관계 후보

관계 후보는 새 C-ID 개설 없이 기록한다.

```text
PersonaHandle
  RELATED-TO PersonaRuntimeObject
  relation kind: HOLD

PersonaRuntimeObject
  MAY-REALIZE PersonaPolicyAttractor
  relation kind: HOLD

ClockCoordination
  MAY-CONDITION SelfOn
  relation kind: HOLD

IdentityTracker
  PRODUCES-OR-SUPPORTS felt continuity
  relation kind: HOLD

ContinuityTax
  COST-OF tracking/stitching process candidate
  relation kind: HOLD

OrganismicContinuity
ExperientialSubject
AttributionSubject
  generic / partitive / associative: HOLD

proposal object
  PART-OF-OR-RELATED-TO committee process candidate
  relation kind: HOLD
```

`MERGE`는 없다.

## 4. 기호 epoch 결과

```text
Φ@QUAL13-READOUT
≠ Φ@UCXQ21-SURFACE
≠ Φ@SAT22-ACTOR
≠ Φ@SAT22-LABEL

Q@QUAL13-PERC-LUMP
≠ ΔQ⊥@UCXQ21-RESIDUAL

θ_crit@RTO21
≠ Θ_track@SAT22

B_A@RTO21
≠ B_backlog@SLEEP22

κ_bind
≠ L_self
≠ ClockFirewall

α_alloc
≠ Authority

ρ_rev@UCXQ21
≠ R_runtime@RTO21
```

`B_backlog@SLEEP22`는 Chapter 10 전방 예약만 남긴다.

## 4-A. 보정 추가 후보의 concept 대조

`extraction-map.md` J절의 `X-CH09-116~127`에 대한 대조다. 이 절도 기존 C-ID의 정의·특성·판정을 바꾸지 않는다.

### 4-A.1 자기 경계 관계 축 — `X-CH09-116~122`

기존 termbase는 이 축들을 소유하지 않는다. C0001~C0009는 행동 경로 선택, 외부 occurrence, 결과 상태, occurrence record, 현재 체험 표면, 비권위적 인과 영향, 실제 노동, 실제 지출, 회계 기록을 다루며 **관계적 자기 경계 축은 없다.**

- 상태: 전부 `HOLD`.
- 권한: `BRIDGE-CURRENT`. 0121 원문의 직접 정의가 아니므로 계보 근거로 쓰지 않는다.

C0006과의 경계가 핵심 질문이다.

```text
C0006
= 어떤 source가 Grounds·warrant·writer 권한 없이 변화를 일으키는 관계

X-CH09-121 NarrativeGravity
= 역사적 관계 지형이 경계 축을 기울이는 편향
```

둘은 같은 관계일 수 있고, C0006의 적용 사례일 수 있고, 별도 관계일 수 있다.

```text
NarrativeGravity NARROWER-OR-RELATED-CANDIDATE-OF C0006
상태: HOLD
재개 조건: 자기 경계 축 편향이 일반 후보·주의 편향과 갈라지는 대비 확보
```

C0009와의 경계도 확인한다. `AccountableResponsibility`는 귀속 기록의 대상일 수 있으나 기록 자체는 아니다.

```text
AccountableResponsibility RELATED-CANDIDATE-OF C0009
상태: HOLD
재개 조건: C0009 subject-field split 뒤 attribution record 후보와 대조
```

`X-CH09-117`은 여섯 축을 한 묶음으로 제안하므로 **subject field 후보**로 표시한다. README 4.7에 따라 이 상태로는 C-ID 발급 조건을 만족하지 않는다.

### 4-A.2 몸 상태 이동과 유일성 주장 — `X-CH09-123~124`

```text
X-CH09-039  Seed          저속 상수 편향
X-CH09-040  t_b           연속 리듬 변조
X-CH09-123  Embodied Drift 현재 상태 변화의 결합 이동
```

세 후보는 모두 접근·비용 지형을 기울이지만 시간 규모와 원천이 다르다. 같은 `[RTO21]` 파일에 있다는 이유로 병합하지 않는다.

- `X-CH09-123` 상태: `HOLD`. epoch는 `RTO21-D` Draft 권한이다.
- `X-CH09-124` 상태: `HOLD`. 유일성 주장 자체를 과잉 일반화 후보로 보존한다.

`X-CH09-124`는 concept 후보라기보다 **발급 조건 판정 시 걸리는 제약**이다. 개인차가 세 변수에서만 나온다는 주장이 참이면 Persona 계열 후보의 차별 특성이 달라지므로 identity cluster에서 함께 확인한다.

### 4-A.3 현행 변형·기억·언어 Bridge — `X-CH09-125~127`

세 후보는 `X-CH09-097~100`의 persistence-capable non-authoritative 공백과 같은 대상을 향한다.

```text
X-CH09-125  변형 유동성·안정화·재유동화
X-CH09-126  기억을 현재 재형성 제약으로 보는 제안
X-CH09-127  언어를 재접근 anchor로 보는 제안
```

- 상태: 전부 `HOLD`.
- `X-CH09-125`의 `QualiaAnnealing`은 Chapter 10 전방 예약이다. 이번 배치는 발생 지점만 등록한다.
- `X-CH09-126`은 C0004와 대조하지만 record가 아니라 **저장 대상**에 관한 주장이다.

```text
memory as deformation recipe RELATED-CANDIDATE-OF C0004
상태: HOLD
재개 조건: 저장 내용·접근 제약·현재 재구성의 관계 확정
```

- `X-CH09-127`은 `X-CH09-029` Why-token의 확대가 아니다. Chapter 09 계보표도 이를 `제한적 선행`으로만 판정한다.

## 5. 후속 cluster queue

이번 intake 뒤 가능한 cluster는 다음과 같다. 순서는 이번 PR에서 확정하지 않는다.

1. **Identity Roles Cluster**
   - Handle / RuntimeObject / SelfOn / PolicyAttractor / IdentityTracker / ContinuityTax
2. **Cross-Clock Cluster**
   - body·experience·commit clocks / coordination / readout / firewall
3. **Subject Roles Cluster**
   - Organismic / Experiential / Attribution subject
4. **Proposal Committee Cluster**
   - object / proposal / allocation / Aggregate / Judgment
5. **Persistent Non-Authority Cluster**
   - transient ρ / persistent plasticity / PlasticTrace / 𝔄
6. **Handoff Cluster**
   - body / memory / access policy / Ghost / Episode / responsibility / authority
7. **Phenomenal Components Cluster**
   - Q / Z / pull / constraint / mismatch / Φ / Meta / FlexCost
8. **Continuity and Stability Cluster**
   - tracker / continuity work / felt continuity / safe-stopping / felt satisfaction
9. **Self-Boundary Axis Cluster**
   - belonging / stake / responsibility / authorship / identity dependence / authority scope
10. **Embodiment Modulation Cluster**
   - Seed bias / body rhythm / current-state coupled drift / individual-difference claim

기본값은 전부 `HOLD`다. 리뷰 뒤 가장 경계가 잘 드러난 cluster 하나만 다음 PR로 구체화한다.

9번과 10번은 보정 배치에서 추가됐다. `X-CH09-125~127`은 5번 Persistent Non-Authority Cluster의 입력에 포함한다.

## 6. 최종 판정

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

새 C-ID 없음. `MERGE` 없음. 기존 concept 정의·특성·판정 변경 없음.

보정 배치 뒤에도 같다. `X-CH09-116~127`은 전부 `HOLD`이며 기존 판정을 건드리지 않는다. 이 보정은 판정 교정이 아니라 coverage 완성이므로 `harmonization` 기록을 만들지 않는다.

```text
최초 intake  X-CH09-001~115
보정 추가    X-CH09-116~127
합계         127
```
