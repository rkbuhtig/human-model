# Chapter 10 Terminology Intake — Scope

## 0. 목적

이 배치는 Chapter 10 `잠을 필연으로 만들려 한 이론`이 복원한 2026-01-22 `SLEEP22` 지층과 그 전사·후기 감사에서 다음 책임을 분리해 추출한다.

```text
미처리·유지 부담이 존재함
≠ 하나의 backlog scalar가 존재함
≠ maintenance operation이 수행됨
≠ 별도 maintenance regime이 필요함
≠ 전역 수면이 유일한 구현임
≠ 수면이 구조적으로 필연임
```

이번 배치는 수면의 정본 ontology를 만들지 않는다. 수면·꿈·기억·가소성·정비·책임을 한 pipeline으로 승인하지 않고, Chapter가 직접 확보한 구분과 과잉 승격, 외부 감사가 요구한 대비를 입력 후보로 보존한다.

중심 원칙은 다음이다.

```text
정비가 필요하다
≠ 잠이 증명된다

같은 수면 구간에 나타난다
≠ 같은 concept다
```

모든 신규 후보의 기본 상태는 `HOLD`다.

## 1. 작업 산출물

```text
research/terminology/projects/chapter-10/
├─ scope.md
├─ extraction-map.md
├─ basic-term-list.md
└─ touched-concepts.md
```

비권위 연구 메모는 다음에 둔다.

```text
research/diary/2026-08-06/
└─ 정비가-필요하다고-잠이-증명되는-것은-아니다.md
```

## 2. 주 조사 질문

### 2.1 열린 입력과 닫힌 권한

- `λ_in`은 무엇의 유입률인가?
- 외부 영향이 계속 들어온다는 것과 외부 사실·권한 갱신 경로가 열린다는 것은 어떻게 다른가?
- sleep·dream·forgetting이 내부 상태를 바꾸면서도 왜 Evidence·Receipt·Warrant를 자기 발행하지 못하는가?
- `Open Intake ≠ Open Authority`는 SLEEP 생물학과 독립적으로 살아남는가?

### 2.2 부담·재고·처리량

- `B_t`는 operational backlog인가, maintenance demand인가, fatigue readout인가?
- 기억 간섭·연속성 비용·세포 유지·관계 처리 부담을 하나의 scalar에 합산할 공통 단위가 있는가?
- `μ_proc`의 Compression·Reindex·Readdr·RouteCalib·PaidRepair는 하나의 처리율인가, operator family인가?
- capacity·load·work·expenditure·debt·record를 어떻게 분리해야 하는가?

### 2.3 maintenance와 sleep

- maintenance demand와 maintenance operation은 어떤 관계인가?
- maintenance가 필요한 것과 별도 maintenance epoch가 필요한 것은 같은가?
- local·online·partitioned maintenance가 왜 불충분한지 원문이 증명하는가?
- `SleepState`, `MaintenanceRegime`, `GlobalSleepCoordination`, `SleepNecessityClaim`은 같은 genus인가?
- 상세 `MET22`의 가능성 문장이 `SPINE22/SPINE22C`에서 필연으로 강화되는가?

### 2.4 dream·replay·plasticity

- `DreamSim`은 runtime operator인가, dream experience인가, neural replay인가?
- `DreamExperience`, `ReplayEvent`, `PlasticityChange`, `DreamReport`, `LaterPerformance`는 어떤 관계인가?
- 꿈이 다음 routing을 바꿀 수 있다는 것과 꿈 내용이 외부 사실의 근거가 되는 것은 어떻게 다른가?
- `gauge-only`라는 명칭이 future causal effect와 양립하는가?

### 2.5 forgetting·memory·history

- SLEEP22의 `Forget`은 trace decay·retrieval failure·index change·active pruning 가운데 무엇을 소유하는가?
- internal memory trace 변화와 external world occurrence·evidence 변화는 어떤 독립 provenance를 가지는가?
- `No-Free-Forgetting`을 어디까지 감사 규율로 보존할 수 있는가?
- biological memory weakening에 Receipt·PaidRepair를 요구하는 과잉 계정 혼합을 어떻게 막는가?

### 2.6 readdress·repair·relief

- `Readdr`는 internal access geometry 변경인가, public relation/address 변경인가?
- `InternalRepairPreparation`, `EvidenceBoundSettlement`, `AppliedLedgerRepair`를 어떻게 분리해야 하는가?
- fatigue·withdrawal·sleep relief와 실제 repair·settlement는 어떻게 다른가?
- `Contraction`의 단기 queue relief와 장기 external obligation은 어떤 관계인가?

### 2.7 continuity·self handoff

- sleep 동안 organism·handle·archive는 지속하면서 current Working Set·SelfOn·Ghost realization은 어떻게 달라지는가?
- sleep-to-waking 변화는 Chapter 09의 handoff family에 어떤 입력을 주는가?
- sleep 중 발생한 plasticity가 다음 Ghost를 바꿔도 current conscious Ghost의 selection·authorship로 볼 수 있는가?
- `DreamGhost`, `CurrentGhost`, `DiachronicSelfContinuity`는 DIRECT가 아니라 어디까지 Bridge인가?

## 3. 출처 ledger와 주장 권한

### 3.1 직접 주자료

| 별칭 | 범위 | 권한 | 역할 |
|---|---|---|---|
| `MET22` | `SLEEP22:L4–291` | `HISTORICAL-DIRECT` | intake·throughput·backlog·sleep·dream·forget·contraction 상세 모델 |
| `SPINE22` | `SLEEP22:L296–375` | `HISTORICAL-COMPRESSION` | 상세 계약을 여섯 조항의 OSAB spine으로 압축 |
| `SPINE22C` | `SLEEP22:L382–404` | `HISTORICAL-COMPRESSION` | 전체를 `A-SPINE0′` 한 문장과 주석으로 재압축 |

문서 내부 기능 순서는 다음으로 읽는다.

```text
MET22
→ SPINE22
→ SPINE22C
```

그러나 뒤 block을 앞 block 전체의 자동 superseder로 보지 않는다. 상세 block의 가능성·구현 위임·미정 변수가 압축 block에서 사라지거나 강해지는 경우는 `COMPRESSION / STRENGTH DRIFT`로 추출한다.

### 3.2 꿈·수면 전사

| 별칭 | 당시 역할 | 권한 |
|---|---|---|
| `ORIGIN02` | Gap·Debt를 낮은 압력에서 재배치하는 꿈/독백 | `PREHISTORY` |
| `A41` | MaskStrain·Residual의 상징·왜곡·재연과 next-day prior 변화 | `PREHISTORY` |
| `EOE09` | 미청산 EOE/Residue의 야간 정산 pipe | `PREHISTORY` |
| `GEE10` | anneal + consolidate 비유 | `PREHISTORY` |
| `GHOST08` | Ghost가 생성하는 상상·경험·꿈·simulation | `PREHISTORY` |
| `ISG09` | coupling·constraint가 다른 dream generation regime | `PREHISTORY` |
| `ACCESS20` | access·rehydration·forgetting·readdress의 직접 선행 구조 | `PREHISTORY / DIRECT-ANTECEDENT` |
| `SAT22` | Dread·Readdress·ContinuityTax·Safe-Stopping 인접 지층 | `ADJACENT-HISTORICAL` |

전사는 문제 계보와 역할 이동만 지지한다. 후대 `DreamSim`, `Backlog`, `Readdr` 정의를 앞 문서에 소급하지 않는다.

### 3.3 후기 lexical·downstream 자료

| 별칭 | 권한 |
|---|---|
| `REG23` | `LATER-LEXICAL`; registry 생존·정규화 확인만 가능 |
| `CORE26` | `DOWNSTREAM-WITNESS`; 운영 backlog와 debt 재혼합·재분리 확인 |
| `MONO15` | `DOWNSTREAM-WITNESS`; module-local vocabulary와 weakened theorem 확인 |
| `LIFE23` | `DOWNSTREAM-WITNESS`; rest/sleep와 recording pressure 재결합 확인 |
| `MINI27` | `DOWNSTREAM-WITNESS`; geometry repair·creativity 재번역 확인 |
| `SYNTH27` | `DOWNSTREAM-WITNESS`; Sleep Necessity 재수록 확인 |

후기 문서의 더 정돈된 명칭을 0122의 최초 정의로 소급하지 않는다. downstream survival은 concept validity나 인간 일반의 진리를 보증하지 않는다.

### 3.4 외부 현실 감사

Chapter의 외부 수면·기억·꿈 연구 대조는 `EXTERNAL-AUDIT` 권한으로 읽는다.

외부 감사는 다음에 사용할 수 있다.

- 서로 다른 concept를 분리할 독립 관측 대비
- 한 구현을 인간·생물 일반으로 확장한 overgeneralization 확인
- 필요조건·충분조건·유일 구현 주장의 scope challenge
- 역사 후보의 발급 재개 조건 기록

외부 감사는 다음에 사용할 수 없다.

- SLEEP22 당시 명칭의 뜻 결정
- external result를 0122의 숨은 정의로 소급
- 동물·회로·단계 결과를 인간 전체의 `KEEP` 근거로 자동 승격
- 한 연구 endpoint를 수면의 단일 목적·본질로 승인

### 3.5 현행 Bridge

다음은 `BRIDGE-CURRENT / HOLD`다.

```text
Operation–Maintenance Noncommutativity
GlobalSleep as coordination envelope
MaintenanceDemand as typed vector/container
DreamGhost
sleep-to-waking Ghost handoff
CurrentGhost / DiachronicSelfContinuity contrast
QualiaAnnealing
```

Bridge는 구조적 공백과 후속 질문을 표지할 수 있지만 C-ID·KEEP·MERGE의 직접 계보 근거가 아니다.

### 3.6 전방 경계

`NEWQUAL22`의 `ΦΩ`는 다음 장이 소유한다.

이번 배치는 다음만 예약한다.

```text
ΦΩ metric / impedance layer
≠ QualiaMedium substrate
≠ PlasticTrace
≠ sleep consolidation law
```

`NEWQUAL22`의 상세 후보·기호·공리는 추출하지 않는다.

## 4. 권한 표지

`extraction-map.md`에서 다음 표지를 사용한다.

| 표지 | 뜻 |
|---|---|
| `HISTORICAL-DIRECT` | SLEEP22 직접 정의·선언 |
| `PREHISTORY` | 앞 지층의 문제·비유·역할 |
| `ADJACENT-HISTORICAL` | 같은 시기 인접 문서와의 역할 이동 |
| `COMPRESSION` | 상세 계약을 spine이 압축 |
| `STRENGTH-DRIFT` | 가능·조건부가 필연·보편으로 강화 |
| `ROLE-DRIFT` | 같은 이름·기호가 다른 타입·역할로 이동 |
| `TYPE-GAP` | input/output/state/unit/provenance가 미정 |
| `MISSING-PREMISE` | 결론에 필요한 전제가 정의되지 않음 |
| `OVERGENERALIZATION` | 구현·국소 모델을 인간·생물 일반으로 확대 |
| `MODEL-ASSUMPTION` | 증명 결과가 아니라 runtime 설계 가정 |
| `LATER-LEXICAL` | 후기 registry/정규화 |
| `DOWNSTREAM-WITNESS` | 후대 재압축·재혼합·강등을 보여주는 자료 |
| `EXTERNAL-AUDIT` | 외부 독립 관측·실험 대조 |
| `BRIDGE-CURRENT` | 현재 연구가 새로 제안한 조건부 연결 |
| `OPEN` | 후속 cluster·Chapter에서 확인할 문제 |

## 5. 핵심 소급 금지

```text
Gap cooling
≠ biological sleep function

Dream settlement
≠ proven memory consolidation

Anneal metaphor
≠ measured QualiaMedium phase transition

λ_in
≠ sensory bandwidth 하나
≠ social demand 하나
≠ metabolic flux 하나

μ_proc
≠ 공통 단위가 확인된 생물학 처리율

B_backlog
≠ B_Access
≠ σ
≠ ΔQ⊥
≠ Bill
≠ one scalar for all maintenance demand

Maintenance demand
≠ maintenance operation
≠ maintenance regime
≠ global sleep
≠ sleep necessity

SleepState
≠ DreamExperience
≠ ReplayEvent
≠ PlasticityChange
≠ DreamReport
≠ LaterPerformance

Dream influence
≠ dream warrant

Forget(memory access/trace)
≠ deletion of world history

non-authoritative
≠ causally inert

gauge-only historical label
≠ empirically inert transformation

Relief
≠ repair
≠ settlement

conditional runtime determinism
≠ empirical biological determinism

SLEEP22 Readdr
≠ current QualiaAnnealing

F_t@SPINE22
≠ F_t@FIELD20 automatic succession
```

## 6. extraction 구조

`extraction-map.md`는 Chapter 02~10의 헤딩+불릿 형식을 따른다.

```text
### X-CH10-NNN — 중립 서술

- 연결된 역사적 명칭
- epoch / 출처 권한
- Chapter 근거
- 선행 대조
- 함께 구분할 후보
- 다음 확인
- 주의
```

큰 절은 다음으로 둔다.

```text
A. source authority·append epoch·compression
B. dream/sleep prehistory
C. open intake / closed authority
D. throughput / backlog / measurement gaps
E. maintenance regime / GateTrace / scheduling
F. maintenance operator family / repair boundary
G. DreamSim / experience / replay / plasticity / report
H. Forgetting / memory / evidence / world history
I. necessity overreach / missing premises / external scope challenge
J. Dread / Contraction / Safe-Stopping / relief
K. self handoff / persistence gap / current Bridges
L. symbols / role drift / downstream witness / NEWQUAL boundary
```

후보 수를 목표로 정하지 않는다. 같은 문단에 있는 역할이라도 genus·truth condition·failure mode가 다르면 별도 후보로 둔다.

## 7. 기존 배치 중복 처리

### Chapter 08

다음은 선행 대조로 사용한다.

```text
F_t / 𝒢_t / W_t
Address / Access / Rehydration
AccessTrace / cost / debt 분리
Unknown split
Forgetting의 접근 실패형 모델
OpenEase / AfterCost
Persona / archive continuity gaps
```

Chapter 10은 동일 후보를 처음 발견한 것처럼 재추출하지 않는다. SLEEP22가 이 역할을 maintenance vocabulary 아래 재배치·강화·혼합한 사건만 추출한다.

### Chapter 09

다음은 선행 대조로 사용한다.

```text
B_A@RTO21
θ_crit@RTO21
Θ_track@SAT22
ContinuityTax
Dread
Safe-Stopping
Persistent Non-Authority gap
Handoff family
QualiaAnnealing forward reservation
```

Chapter 10이 새로 소유하는 것은:

- `B_backlog@SLEEP22`의 직접 역할
- SAT `Readdress`가 SLEEP maintenance operator로 다시 승격된 이동
- `Θ`가 SLEEP에서 추적 대상으로 사용된 추가 drift
- maintenance와 continuity/satisfaction의 새 결합
- sleep-to-waking handoff 공백

이다.

## 8. 관계 판단 규율

이번 intake는 관계 후보만 기록한다.

### Generic 후보

```text
GlobalSleepState NARROWER-CANDIDATE-OF MaintenanceRegime?
SleepMaintenance NARROWER-CANDIDATE-OF MaintenanceOperation?
DreamSim NARROWER-CANDIDATE-OF InternalSimulation?
```

모두 `HOLD`다. genus·차별 특성·외연·대비 사례가 cluster에서 닫혀야 한다.

### Partitive 후보

```text
Compression / Reindex / Readdr / RouteCalib
PART-OF MaintenanceProcess?

ReplayEvent / PlasticityChange
PART-OF Sleep-linked maintenance?
```

같은 구간에 공존한다는 이유만으로 partitive relation을 확정하지 않는다.

### Associative 후보

```text
SleepState RELATED-TO maintenance events
DreamExperience RELATED-TO replay/plasticity
MaintenanceDemand RELATED-TO scheduling pressure
Dread RELATED-TO backlog hypothesis
```

인과 방향과 증거 수준이 다르면 별도 후보로 둔다.

### MERGE

이번 배치에서 synonym `MERGE`를 판정하지 않는다.

## 9. definition gate

다음 압축형 서술은 자동 정의로 사용하지 않는다.

```text
수면은 압축·재색인·재주소·수리 및 꿈 시뮬레이션을 포함하는 GC다.

backlog는 처리되지 않은 정보·감정·대사·관계 부담이다.

꿈은 기억과 감정을 재처리해 다음날 행동을 최적화한다.
```

`및`, `포함`, 여러 genus, 목적론적 결과, external truth leap가 있으므로 전부 `HOLD`다.

## 10. 기존 C-ID와 대조 범위

이번 배치는 기존 concept 정의·특성·판정을 변경하지 않는다.

```text
C0001  선택·routing·call과 maintenance influence 대조
C0002  dreamed occurrence·later action·world contact 대조
C0003  predicted safe stopping·actual viability·maintenance outcome·felt relief 대조
C0004  world occurrence record·dream report·memory trace·maintenance log 대조
C0005  fatigue·dread·dream experience·relief·felt satisfaction 대조
C0006  dream/readdress/maintenance의 비권위적 인과 관계 대조
C0007  compression·reindex·readdress·repair preparation의 수행 활동 관계
C0008  capacity·load·cost·actual expenditure 관계
C0009  backlog·trace·repair·report·address history 기록군 분해
```

판정은 기존 상태를 유지한다.

```text
C0001 KEEP
C0002 KEEP
C0003 HOLD
C0004 KEEP
C0005 KEEP
C0006 KEEP
C0007 HOLD
C0008 KEEP
C0009 HOLD / SUBJECT-FIELD SPLIT
```

## 11. 후속 cluster queue 후보

이번 PR에서 cluster를 실제 판정하지 않는다.

```text
Maintenance Demand Cluster
Maintenance Operation Cluster
Maintenance Scheduling Cluster
Sleep State / Coordination Cluster
Dream / Replay / Plasticity Cluster
Forgetting / Memory / History Cluster
Internal / Public Readdress Cluster
Repair / Relief / Settlement Cluster
Operational Load / Cost / Spend Cluster
Sleep-to-Self Handoff Cluster
```

리뷰 뒤 경계가 가장 잘 드러난 cluster 하나만 다음 작업으로 구체화한다.

## 12. 범위 밖

이번 배치에서는 다음을 하지 않는다.

- 새 C-ID 발급
- synonym `MERGE`
- 기존 concept 정의·특성·판정 변경
- maintenance·sleep·dream 정본 ontology
- 수면의 생물학적 본질·단일 기능·필연성 주장
- 외부 논문별 세부 메타분석
- `Sleep = GC` 승인
- `DreamSim = optimizer` 승인
- `B_t`를 core scalar로 승인
- biological memory decay에 Receipt·PaidRepair 요구
- `DreamGhost`, `QualiaAnnealing`, `Operation–Maintenance Noncommutativity` 정본화
- `NEWQUAL22` 상세 추출
- Chapter 11 intake
- glossary·current-use rename
- runtime/model/code 변경

## 13. 완료 조건

- `MET22 / SPINE22 / SPINE22C` 권한과 강도 이동이 분리됨
- 꿈·수면 전사를 direct SLEEP definition과 구분함
- external audit가 역사 근거와 분리됨
- `MaintenanceDemand / Operation / Regime / SleepState / NecessityClaim`이 분리됨
- `B_backlog ≠ B_Access ≠ Debt`가 고정됨
- `μ_proc`의 operator family·공통 단위 공백이 기록됨
- `DreamSim / DreamExperience / Replay / Plasticity / Report`가 분리됨
- `Forget`의 내부 기억 변화와 외부 역사 삭제가 분리됨
- `InternalReaddress / PublicReaddress`가 분리됨
- `InternalRepairPreparation / Settlement / AppliedRepair`가 분리됨
- 기존 C-ID 판정 변경이 없음
- 새 C-ID·MERGE·runtime 변경이 없음
