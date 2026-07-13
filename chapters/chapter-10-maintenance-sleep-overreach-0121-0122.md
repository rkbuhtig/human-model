# Chapter 10 — 잠을 필연으로 만들려 한 이론

## Open Intake·Backlog·Maintenance Epoch·DreamSim·Forget: 정비의 필요에서 전역 수면의 필연으로 건너간 지층

> **상태:** 역사 복원 + 외부 현실 감사 + 연구 후기 v1.0  
> **주범위:** 2026-01-22 `MET / SLEEP / GC (Reinforced)`와 두 `SPINE-OSAB` 압축 지층  
> **역사 전사:** 2026-01-02–01-20의 Dream/VOID·Anneal·Ghost·ISG·Access/Readdress 계열  
> **직전 장:** Chapter 09 — 나를 계속 켜 두는 비용  
> **전방 경계:** 2026-01-23 registry normalization과 2026-01-22 `ΦΩ-SEALING-UPGRADE`는 다음 장으로 보류

---

## 들어가며 — 정비가 필요하다는 사실은 잠을 증명하는가

Chapter 09은 자아를 같은 내용을 계속 가진 물체가 아니라, 달라지는 현재들을 다시 자기 것으로 인수하는 여러 handoff의 결합으로 읽었다.

```text
discontinuous activation
→ IdentityTracking
→ ContinuityTax
→ fatigue / dread / safe-stopping pressure
→ need for maintenance
```

`SLEEP22`는 이 마지막 화살표를 독립된 운영 이론으로 확장한다. 인간은 외부 입력을 계속 받지만 한 순간에 활성화할 수 있는 Working Set은 유한하다. 처리되지 못한 것은 `B_t`라는 backlog로 남는다. 수면은 입력을 낮추고 계산 자원을 재배치하여 Compression·Reindex·Readdress·Route calibration을 수행한다. 꿈은 사실을 만들지 않는 offline candidate test이며, 망각은 원장을 지우지 않는 cache maintenance다.

이 설계는 Chapter 09에서 남은 여러 질문에 한꺼번에 답하는 듯 보인다.

```text
왜 쉬어야 하는가?       → backlog를 처리해야 하기 때문에
왜 잠들어야 하는가?     → 외부 입력과 유지보수의 결합을 낮춰야 하기 때문에
왜 꿈을 꾸는가?         → routing 후보를 offline에서 시험하기 때문에
왜 잊는가?              → 원장이 아니라 cache와 address를 정리하기 때문에
왜 자고 나면 달라지는가? → 같은 사건을 여는 접근 기하가 바뀌기 때문에
```

그러나 이 장의 핵심은 이 대답을 현행 이론으로 채택하는 데 있지 않다. `SLEEP22`의 상세 지층을 시간순으로 읽으면, 문서가 실제로 확보한 결론과 마지막 spine이 선언한 결론 사이에 한 단계가 빠져 있다.

```text
유한 처리량이면 backlog가 생길 수 있다.
backlog를 관리하려면 어떤 maintenance가 필요할 수 있다.

≠

전역적이고 별도인 수면 epoch가 구조적으로 필연이다.
```

첫 두 문장과 마지막 문장 사이에는 online maintenance의 한계, 유지보수와 현장 수행의 자원 충돌, 국소 분할의 불가능성, 장기 평균 처리율의 안정 조건이 추가로 필요하다. 원문은 이 조건들을 정의하지 않은 채 `수면 같은 GC`를 인간다움의 상위 척추로 올린다.

외부 생물학도 같은 경고를 준다. 수면 중 기억 재활성화·시냅스 재편·세포 수선·면역·대사·체온·유체 역학이 달라진다는 근거는 많다. 하지만 그것들은 하나의 backlog도, 하나의 GC도 아니다. 국소 수면과 단반구 수면이 존재하고, 2026년에는 깨어 있는 생쥐의 피질에 수면형 on/off pattern을 유도하여 일부 수면 기능을 수행시킨 결과도 나왔다. 꿈의 주관적 내용이 이러한 정비를 인과적으로 수행한다는 근거는 더 약하다.

따라서 이번 장의 중심 명제는 이것이다.

> **`SLEEP22`는 생명이 운영하면서 자기 구조를 유지해야 한다는 중요한 문제를 정면으로 세웠다.  
> 그러나 유지보수의 필요를 하나의 backlog로 압축하고, 그 backlog의 해법 가운데 하나인 수면을 구조적 필연으로 승격했으며, DreamSim의 후보 생성과 routing/readdress update signal을 한 sandbox에 두면서 persistence와 write type을 분리하지 않았다.**

역사 본문은 그 강한 원형을 그대로 복원한다. 외부 현실 감사는 원문과 섞지 않고 별도 층에서 판정한다. 연구 후기에서는 `수면=DB maintenance`를 메인 축에서 내리고, 그 비유 속에서 살아남는 조건부 구조만 `Bridge`로 보존한다.

---

# 역사 본문 — 꿈의 내용을 지우고 운영 계약으로 수면을 만들다

## 0. 범위·판본·독해 규율

### 0.1 주자료는 하나지만 한 번에 쓰인 정본은 아니다

이 장의 주자료는 `fucstrees/0121 수면.txt` 한 파일이다. 하지만 내부에는 서로 다른 압축률을 가진 세 지층이 append되어 있다.

| 층 | 별칭 | 원문 범위 | 역할 |
|---:|---|---:|---|
| 1 | `MET22` | `SLEEP22:L4–291` | intake·throughput·backlog·sleep·dream·forget·contraction을 정의·공리·정리·귀결로 전개 |
| 2 | `SPINE22` | `SLEEP22:L296–375` | 앞의 상세 계약을 `Open-System, Audit-Bound Metabolic Runtime` 여섯 조항으로 압축 |
| 3 | `SPINE22C` | `SLEEP22:L382–404` | 전체를 한 문장짜리 `A-SPINE0′`와 다섯 주석으로 다시 압축 |

파일 mtime은 2026-01-22 11:12:04 `-06:00`이고 총 407행이다. mtime은 corpus의 상대 보존 순서이지 세 append block의 정확한 작성 시각을 독립적으로 증명하지 않는다. 다만 아래쪽 block이 위쪽 정의를 이름으로 호출하고 압축하므로 문서 내부의 기능 순서는 `MET22 → SPINE22 → SPINE22C`로 읽을 수 있다.

`SLEEP22`는 `SAT22`의 `τ_cont`, 불길함 `δ`, Safe-Stopping을 이미 사용한다 `[SLEEP22:L47–50; L105–111; L267–281]`. 두 파일의 mtime 차이는 74초뿐이며 `SAT22` 끝 correction의 정확한 선후는 확정할 수 없다. 따라서 이 장은 다음만 말한다.

```text
SAT/CONT/TRK/DREAD의 핵심 어휘
→ SLEEP22가 이미 의존

whole-file SAT22 correction
↔ SLEEP22 세부 작성 순서
= unresolved
```

### 0.2 꿈과 수면의 전사는 별도 지층이다

`SLEEP22`가 수면을 처음 언급한 문서는 아니다. 이전 장에서 일부를 이미 복원했지만, 이번 장에서는 꿈의 역할이 어떻게 변했는지 확인하기 위해 다음 자료만 짧은 전사로 사용한다.

| 별칭 | 문서 | 관련 범위 | 당시 역할 |
|---|---|---:|---|
| `ORIGIN02` | `참조용 임시/0101 물리의논통합본 5.txt` | L1015–1046 | Gap·Debt를 꿈/독백이 재배치하는 열교환기 |
| `A41` | `AXIOM37/0104 axiom41 3.txt` | L2581–2619 | MaskStrain·Residual을 상징·왜곡·재연해 next-day prior를 바꾸는 무의식 정산 |
| `EOE09` | `AXIOM37/0105  eoe .txt` | L426–441 | 미청산 EOE/Residue의 야간 정산 pipe |
| `GEE10` | `AXIOM37/0105 GEE 1.txt` | L202–206 | 수면/휴식의 anneal + consolidate |
| `GHOST08` | `AXIOM37/0107 이론합본` | L45–60 | 상상·경험·꿈·시뮬레이션을 계속 돌리는 Ghost |
| `ISG09` | `AXIOM37/0109 new물리통합3 .txt` | L1139–1198 | 상상과 꿈을 coupling·constraint가 다른 Internal Scene Generator regime으로 분리 |
| `ACCESS20` | `fucstrees/0120 정의정리공리귀결 이후패치.txt` | L270–331; L568–575 | 회상·망각·재주소를 access geometry와 비용 규율로 옮긴 직접 선행층 |

이 전사들은 `SLEEP22`의 세부 공리와 같은 판본이 아니다. 뒤 문서의 용어를 앞 문서에 소급하지 않는다.

### 0.3 REG23과 NEWQUAL22의 지위

`REG23`은 sleep 관련 root를 registry에 넣는다.

```text
ws    : working set
bg    : backlog
gt    : gate trace
addr  : address
radr  : readdress
drms  : dream simulation
```

하지만 registry는 개념의 기원이나 생물학적 타당성을 증명하지 않는다. `REG23`은 lexical normalization의 후속 결과로만 사용하며 역사 본문의 직접 근거에서 제외한다 `[REG23:L168–178]`.

`NEWQUAL22`는 `ΦΩ`를 medium metric / impedance layer로 정의하고 call distribution을 바꾸는 non-authoritative causal layer로 봉인한다 `[NEWQUAL22:L50–81]`. 이 문서는 SLEEP의 상세 maintenance operator를 확장하지 않는다. `ΦΩ`를 현행 `QualiaMedium`이나 수면 중 녹았다 굳는 물질로 읽지 않는다. 다음 장의 독립 본문으로 보류한다.

### 0.4 판정 표지

| 표지 | 뜻 |
|---|---|
| `[DIRECT]` | 원문이 직접 정의·선언 |
| `[PREHISTORY]` | 앞 시기 자료에서 먼저 나온 문제·비유 |
| `[REWRITE]` | 같은 문제를 다른 역할·형식으로 다시 씀 |
| `[COMPRESSION]` | 상세 정의를 짧은 spine으로 압축 |
| `[ROLE DRIFT]` | 같은 기호·이름이 다른 역할로 이동 |
| `[TYPE GAP]` | 입력·출력·저장·단위·handoff가 미정 |
| `[MISSING PREMISE]` | 정리 결론에 필요한 전제가 정의되지 않음 |
| `[OVERGENERALIZATION]` | 한 구현·국소 모델을 인간 일반의 필연으로 확대 |
| `[MODEL ASSUMPTION]` | 증명 결과가 아니라 설계 가정 |
| `[CURRENT LENS]` | 현행 이론에서의 비교이며 당시 정의가 아님 |
| `[EXTERNAL AUDIT]` | 외부 1차 연구와의 대조 |
| `[BRIDGE]` | 이번 독해에서 새로 만든 조건부 연결 |
| `[OPEN]` | 후속 문서·실험·형식화에서 확인할 질문 |

### 0.5 핵심 소급 금지

```text
Gap cooling ≠ biological sleep function
Dream settlement ≠ proven memory consolidation
Anneal metaphor ≠ measured QualiaMedium phase transition

λ_in ≠ sensory bandwidth alone
μ_proc ≠ one measured biological throughput
B_backlog ≠ Access bandwidth B_A
B_backlog ≠ σ / ΔQ⊥ / Bill

Maintenance need ≠ global sleep necessity
SleepState ≠ DreamExperience
DreamExperience ≠ neural replay
Neural replay ≠ memory write

Forget(memory access) ≠ deletion of world history
non-authoritative ≠ causally inert
gauge-only ≠ no future behavioral effect

conditional determinism ≠ empirical biological determinism
SLEEP22 Readdr ≠ current QualiaAnnealing
```

---

## 1. 전사 — 꿈은 처음부터 backlog scheduler는 아니었다

### 1.1 ORIGIN02의 꿈은 Gap을 식히는 서사적 선택이다

가장 이른 자료에서 꿈과 독백은 휴식이 아니라 `Gap을 해소하는 쿨링 시스템`으로 불린다 `[ORIGIN02:L1033–1036]`. 낮은 관측성에서 말한 것이 Debt와 Gap으로 남고, 꿈/독백은 외부 압력이 낮을 때 그 Gap을 Heat 방출이나 Action 방향으로 재배치한다 `[ORIGIN02:L1015–1046]`.

이때 핵심은 효율적인 정보 압축이 아니다.

```text
unsettled Gap
→ safe low-pressure rearrangement
→ Accept or Reject
→ growth / hardening / narrative consequence
```

원문은 자기정정을 자동 의무가 아니라 서사적 선택으로 남긴다. 꿈은 정확한 기억을 정리하는 관리자보다, 낮에 감당하지 못한 모순을 다른 삶의 방향으로 환전하는 인간형 runtime의 일부다.

### 1.2 A41 — 꿈은 Mask와 Residual을 처리하는 무의식 정산이다

`A41`은 Idle·VOID·수면·혼자 있음을 외부 저항이 낮은 방전 조건으로 두고, MaskStrain·`P_res`·Peel·Blur를 꿈과 헛것의 재료로 삼는다 `[A41:L2595–2605]`. 처리 결과는 다음 날의 기대·경계값·말투·prior를 바꾼다.

```text
daytime Mask / Residual pressure
→ symbolic distortion / reenactment
→ next-day prior shift
```

이 시기의 잔류에는 억눌린 말, 관계의 Miss, Mask 비용, 상처와 Blur 같은 인간적 내용이 있다. 꿈은 아직 일반적인 정보 maintenance가 아니라 낮에 외부로 직접 방전하면 위험한 압력을 다른 형식으로 환전하는 장면이다.

### 1.3 GHOST08 — 꿈은 계속 도는 탐색기의 한 출력이다

`GHOST08`의 Ghost는 상상·경험·꿈·시뮬레이션을 계속 돌리는 탐색기다 `[GHOST08:L53–60]`. 수면은 Ghost의 기원이 아니다. 꿈은 Ghost가 작동하는 여러 자리 가운데 하나다.

이 분해는 Dream을 maintenance job보다 먼저 generation 쪽에 놓는다.

```text
Ghost generates
Editor identifies / compiles
Will steers output
```

후대 `DreamSim`이 routing 후보를 시험한다고 말할 때도, 후보 생성과 외부 승인·행동은 같은 단계가 아니다.

### 1.4 EOE09 — 꿈은 미청산 EOE의 야간 pipe다

`EOE09`는 A41의 구조를 `미청산 EOE/Residue의 야간 정산 pipe`로 다시 쓴다. 잔류를 현실에서 그대로 방전하면 관계나 자신을 손상시킬 수 있으므로, 꿈은 그것을 상징화·재연·왜곡해 처리한다고 설명한다 `[EOE09:L426–435]`.

이것은 후대 `DreamSim`과 기능적으로 닮았지만 동일하지 않다. EOE09는 꿈을 관계적 손상을 피하는 변환 경로로 본다. `SLEEP22`가 그것을 route·address·cache라는 운영 항으로 바꾸면서 구체적 EOE 내용은 거의 사라진다.

### 1.5 ISG09 — 상상과 꿈은 coupling이 다른 생성 regime이다

`ISG09`는 상상과 꿈을 다른 기능으로 나누지 않고 Internal Scene Generator가 다른 경계조건에서 작동하는 두 regime으로 둔다 `[ISG09:L1149–1169; L1173–1198]`.

```text
Imagination: κ_couple high, T_sim low–mid
Dream      : κ_couple low,  T_sim high
```

외부·현재 맥락과의 결합이 낮고 제약 완화가 높으면 장면의 혼재와 점프가 커진다. 이것은 `왜 꿈이 이상한가`에 대한 생성 조건 모델이다. `왜 생명에게 수면이 필요한가`에 대한 답은 아니다.

### 1.6 GEE10 — 정산은 annealing과 consolidate가 된다

`GEE10`은 꿈/휴식을 `어닐링(재배열) + 응고(고정)`로 설명한다. 수면이나 깊은 휴식에서 `T`가 올라가 비정상 결합 후보가 떠오르고, 깨어나며 `T`가 내려갈 때 승인·폐기가 정리된다고 쓴다 `[GEE10:L202–206]`.

여기서 꿈은 단순 방전보다 탐색 다양성과 구조 재편의 비유를 얻는다. 다만 `T`, 결합, 응고는 측정된 생물학적 상태가 아니라 GEE 모델의 설계 변수다. 꿈에서 후보가 떠오른다는 설명과 실제 기억 구조가 어떤 연산으로 바뀌는지는 연결되지 않는다.

### 1.7 ACCESS20 — 망각과 재주소가 수면보다 먼저 구조화된다

`ACCESS20`은 기억을 저장 내용의 재생이 아니라 scaffold render, local access, rehydration의 합성으로 정의한다 `[ACCESS20:L299–307]`. 망각도 저장된 과거의 삭제보다 scaffold 약화, 접근 경로 변화, 연결 재가중으로 설명한다 `[ACCESS20:L323–331]`.

이 문서에는 `No Free Unlinking`과 `No Free Readdressing`도 이미 있다. 흉터 결합이나 `AddrSig`의 실질 재배치는 새 근거·PaidRepair·Receipt/σ/Bill·Coverage/κ 변화 가운데 어떤 추적 가능한 조건을 동반해야 한다 `[ACCESS20:L288–293; L568–575]`.

따라서 `SLEEP22`가 처음 발명한 것은 `망각=접근 재가중`이라는 직관 자체가 아니다. 그것을 sleep/maintenance vocabulary 안으로 옮기고, cache-level change와 authoritative ledger deletion을 분리한 것이 새 변화다. `Forget`의 실행 정의역을 수면 중으로만 제한하지는 않으므로 `수면 전용 operator`라고 부르지 않는다.

두 지층 사이에는 아직 타입 긴장이 남는다.

```text
ACCESS20:
substantial readdressing must leave accountable traces

SLEEP22:
runtime cache / scaffold / address may be reorganized
without automatically issuing Evidence or Receipt
```

내부 cache address와 관계·공적 address를 나누면 양립할 수 있지만, 원문은 `Readdr` 이름을 분리하지 않는다.

### 1.8 SAT22 — Readdress는 먼저 불길함을 해석하는 control regime이었다

`SAT22`의 `A-DREAD1`은 불길함 `δ_t`를 truth가 아닌 routing token으로 읽고, decoder output에 `Contraction`과 `Readdress`를 둔다. Readdress는 `AddrSig/접근 기하`를 재배치하여 더 낮은 비용 경로를 탐색한다 `[SAT22:L109–116]`.

후미 correction은 이 둘을 discrete mode에서 내린다.

```text
Dec(δ, ρ, 𝔄) → (Δu, ΔAddr)

Contraction / Readdress
= observational regime names
≠ independent types
```

`[SAT22:L197–198]`

`SLEEP22`는 이 연속 control output 가운데 `Readdress`를 다시 별도 operator로 올리고, 수면 maintenance의 우선 작업과 목표함수를 부여한다. 따라서 계보는 단순한 정교화가 아니다.

```text
dread-decoding regime
→ continuous ΔAddr control
→ sleep maintenance operator
```

### 1.9 SLEEP22의 전환 — 내용에서 권한 계약으로

앞선 지층에서 꿈은 Gap·감정 잔류·MaskStrain·미청산 EOE를 다룬다. `SLEEP22`는 그 내용을 거의 제거하고 네 가지 운영 문제로 바꾼다.

```text
unresolved content  → B_backlog
low external resistance → λ_in gating
symbolic rearrangement → Readdr / RouteCalib
next-day prior shift → next-day routing shift
```

이 전환이 얻은 것은 명확하다. 꿈이 선명하다고 사실이 되거나, 수면 중 떠오른 서사가 외부 원장을 고치는 우회로가 되는 것을 차단할 수 있다. 잃은 것도 명확하다. 무엇이 누구에게 어떻게 느껴졌고, 왜 그 잔류가 그 사람에게 중요한지, 같은 재배열이 수용·회피·고착 가운데 무엇이 되었는지는 operation name 아래로 내려간다.

---

## 2. 열린 입력과 닫힌 커밋 — SLEEP22의 가장 강한 분리

### 2.1 인간은 입력에 대해서 열려 있다

`MET22`는 인간에게 환경·자극·정보·사회 상호작용이 계속 들어오는 비율을 `λ_in(t)`로 정의한다 `[SLEEP22:L22–25]`. Chapter 09까지의 문서는 열린 입력 자체보다 닫힌 commit·authority 계약과 내부 Persona state에 초점을 두었다. 여기서는 세계가 계속 주체 안으로 밀려 들어온다는 사실을 별도 rate로 전면에 놓는다.

```text
world → sensation / information / relation → reversible runtime
```

그러나 `λ_in`은 물리량 하나로 측정되지 않는다. 감각 자극, 사회적 요구, 새로운 정보, 신체 변화가 어떤 공통 단위로 합산되는지는 정의되지 않는다. `metabolic`이라는 말도 세포 대사와 운영 처리의 비유를 오간다. 따라서 이것은 실측률보다 open-system intake를 위한 메타 변수다.

### 2.2 열려 있는 것은 입력이고 닫혀 있는 것은 권한 경로다

같은 정의는 입력 자체가 `𝔄`를 갱신할 권한을 갖지 않는다고 못 박는다 `[SLEEP22:L24–25]`. `A-MET0`는 수면·꿈·망각도 EvidenceLink/Receipt를 동반한 닫힌 갱신 경로를 우회할 수 없다고 다시 봉인한다 `[SLEEP22:L142–145]`.

이것이 `SLEEP22`의 가장 안정적인 직접 수확이다.

```text
Open Intake
≠ Open Authority

felt / imagined / dreamed change
≠ evidence-bound worldline update
```

주체는 세계의 영향에서 닫힌 상자가 아니지만, 영향을 받았다는 이유만으로 외부 사실·권한·면책을 자기 발행할 수도 없다. 이후 수면 모델의 생물학이 수정되어도 이 구분은 남는다.

### 2.3 수면은 Cut-1 내부로 제한된다

문서 앞머리는 전체 패치가 `Cut-1(Norm) 내부 모델`이며 `Norm(𝔄_t, ρ_t^+) → (ρ_t^{++}, call_t)`의 내부 계산과 scheduling만 확장한다고 선언한다 `[SLEEP22:L4–8]`.

따라서 sleep operator가 합법적으로 바꿀 수 있는 것은 처음부터 제한되어 있다.

```text
allowed:
ρ / Φ / Θ / ℐ / AddrSig
cache / scaffold / routing / scheduling

not self-issued:
Evidence / Receipt / Π_wit / applied 𝔄 update
```

이 봉인은 뒤에서 꿈의 결과가 실제 행동을 바꾸는 경우에도 유지된다. 내부 영향이 세계선에 닿으려면 다시 `call → Instrument → EventRecord → Update`를 통과해야 한다 `[SLEEP22:L245–247]`.

---

## 3. 하나의 backlog — 서로 다른 정비를 한 재고로 묶다

### 3.1 μ_proc는 다섯 연산의 합이다

`MET22`는 내부 합성 처리율 `μ_proc(t)`를 다섯 하위 처리율의 합으로 둔다 `[SLEEP22:L29–41]`.

```text
μ_proc
= μ_comp   : compression
+ μ_reidx  : reindex / duplicate cleanup
+ μ_readdr : readdress / defrag
+ μ_route  : route calibration
+ μ_repair : paid repair
```

이 정의는 수면을 단순 휴식이나 에너지 충전이 아니라 `구조를 다시 쓸 수 있는 작업 창`으로 바꾼다. 동시에 서로 다른 단위를 한 합에 넣는다. 중복 정리와 관계 주소 재배치, 디코딩 보정, 유상 수리가 어떤 공통 처리량으로 더해지는지는 제시되지 않는다.

`μ_repair`가 PaidRepair일 때만 반영된다는 제한은 특히 중요하다. 원문은 운영 cache 정리와 이미 발생한 회계·청구의 수리를 구별하려 하지만, 같은 합성 처리율에 함께 넣어 두어 다시 섞일 여지를 남긴다.

### 3.2 B_t는 사실도 부채도 아닌 운영 밀림이다

처리되지 못한 압력을 `B_t ≥ 0`라는 대사 잔차·운영 밀림으로 정의한다 `[SLEEP22:L45–50]`. 곧바로 `B_t`는 `Π_wit`의 판정가능항도, `σ/ΔQ⊥`의 회계 계정도 아니라고 분리한다 `[SLEEP22:L54–61]`.

```text
B_backlog
= incomplete operational processing
≠ evidence
≠ statement
≠ debt
≠ residual accounting claim
```

이 분리는 초기 문서에서 오래 남은 흔적·미해결 감정·책임·부채가 한 `Residual`에 뭉치던 문제를 교정한다. 피곤하거나 생각이 밀렸다는 사실만으로 누군가에게 청구권이나 면책이 생기지는 않는다.

다만 기호 `B_t`는 같은 0121의 초기 RTO에서 Access bandwidth로 사용됐다. 이 장은 충돌을 피하기 위해 `B_backlog`와 `B_Access`로 분리한다.

### 3.3 관측 가능한 것은 B 자체가 아니라 여러 표면 신호다

원문은 `B_t`를 직접 측정하지 않고 Working Set 포화, Guard 상승, `τ_cont` 증가, 불길함 `δ`로 간접 관측할 수 있다고 쓴다 `[SLEEP22:L47–50]`.

그러나 다음 역추론은 정의되지 않는다.

```text
fatigue / dread / Guard / continuity cost
→ unique B_backlog value
```

같은 불길함은 실제 외부 위험, 신체 통증, 관계 갈등, 기억 접근 실패, 수면 부족 등 여러 원인에서 나올 수 있다. `B`는 이들을 설명하는 hidden stock이지만 식별 가능한 상태량은 아니다.

### 3.4 update skeleton은 방향만 주고 동역학을 주지 않는다

`D-MET4`는 `λ_in > μ_proc`이면 backlog가 증가 가능하고 반대면 감소 가능하다는 방향 조건만 둔다 `[SLEEP22:L65–72]`.

```text
λ_in > μ_proc  ⇒ B_{t+1} ≥ B_t possible
μ_proc > λ_in  ⇒ B_{t+1} ≤ B_t possible
```

도착한 입력이 얼마나 backlog가 되는지, service discipline이 무엇인지, 우선순위·기한·폐기·병렬 처리·포화 상한이 있는지는 구현에 위임된다. 따라서 `B_t`는 완성된 queue model이 아니라 queue를 말하기 위한 skeleton이다.

---

## 4. 수면을 maintenance epoch로 다시 정의하다

### 4.1 외부 입력은 0이 아니라 gated stream이다

`D-SLEEP0`는 수면 중 외생 입력이 완전히 사라진다고 하지 않는다. `GateTrace_t`라는 제한된 stream으로 계속 주입된다고 둔다 `[SLEEP22:L76–79]`.

이것은 수면을 세계와의 완전 절단으로 보는 것보다 세밀하다. 위험·소리·몸의 신호가 들어올 수 있고, maintenance 결과는 내부 상태와 그 gated input에 함께 조건화된다.

### 4.2 유지보수 모드는 현장 예산의 재배치다

수면 구간 `𝓔_sleep=[t_s,t_e]`에서 Norm은 다음을 수행한다 `[SLEEP22:L83–92]`.

```text
λ_in ↓
W_t → maintenance allocation
Compression / Reindex / Readdr / RouteCalib prioritized
PaidRepair remains paid
```

수면의 핵심은 `모든 것이 꺼진다`가 아니라 `무엇에 예산을 배정하는가가 바뀐다`는 것이다. `A-SLEEP3`은 이를 FAST 외생 구동을 낮추고 MID의 정책·주소·추적과 VERY_SLOW의 유상 처리를 위한 interlock window로 설명한다 `[SLEEP22:L183–185]`.

이 관점은 수면을 자아의 소멸보다 external-serving regime의 변화로 읽을 여지를 연다. 하지만 그 여지는 원문의 직접 결론이 아니다. 원문은 어떤 연산이 깨어 있는 동안 불가능한지 따로 정의하지 않는다.

### 4.3 Readdr는 내용을 지우지 않고 열림의 기하를 바꾼다

`Readdr`는 `AddrSig/ℐ/Θ`를 재배치하되 Evidence를 만들거나 `Π_wit`로 승격하지 않는다 `[SLEEP22:L96–101]`. 목표는 세 항을 낮추는 것이다 `[SLEEP22:L105–111]`.

```text
AfterCost curvature ↓
Neighborhood co-activation width ↓
ContinuityTax τ_cont ↓
```

이 정의는 `수면 뒤 사건이 사라지지 않았는데 덜 불길하거나 다르게 보이는 상태`를 설명하려 한다. 동일 단서에 대한 `δ` decoding과 전진 call의 비용 구조가 바뀌는 것을 삭제가 아니라 접근 기하의 변화로 읽는다 `[SLEEP22:L232–235]`.

다만 목표함수는 선언되어 있을 뿐 연산자가 없다.

```text
Addr_{t+1} = F(Addr_t, Trace_t, GateTrace_t, ...)

which minimum?
which constraints?
what prevents maladaptive reinforcement?
what is preserved?
```

따라서 `Readdr`는 관측된 다음 날 변화의 가능한 해석이지, 그 변화가 실제로 최적화되었다는 증명은 아니다.

### 4.4 조건부 결정성은 생물학 발견이 아니라 runtime seal이다

`A-SLEEP1`은 동일한 `(ρ_t, GateTrace_t)`에 동일 maintenance output이 나온다고 선언한다 `[SLEEP22:L170–173]`. 이는 재현 가능한 runtime을 위한 설계 봉인이다.

실제 생물학적 수면이 이 의미에서 결정적이라는 자료는 제시되지 않는다. 숨은 신체 상태, 신경·분자 변동, 외부 입력의 미측정 성분을 모두 `ρ/GateTrace`에 넣으면 결정성은 반증하기 어려운 total-state 가정이 된다. 역사적으로는 UCXQ의 No-RNG·same-input/same-output 규율을 수면 안으로 가져온 것으로 읽는다.

---

## 5. DreamSim과 Forget — 비권위적이지만 무효하지 않은 변화

### 5.1 DreamSim은 offline routing candidate test다

`D-DREAM1`은 수면 중 `Π_view` 기반 내부 simulation을 `DreamSim`으로 정의한다 `[SLEEP22:L115–120]`.

```text
DreamSim
→ tests routing / readdress candidates
→ may signal updates to ρ / Φ / Θ / AddrSig
↛ truth-token
↛ direct 𝔄 authority
```

이 정의는 꿈의 내용이 아무리 생생해도 사실 근거가 되지 않는다는 경계를 보존한다. 동시에 꿈이 다음 상태를 바꿀 수 있다는 가능성은 남긴다.

### 5.2 꿈의 영향은 나중 사건을 통과해야 세계선에 닿는다

`T-DREAM2`는 DreamSim 때문에 정책이나 행동이 달라져도 세계선 변화는 이후 실제 사건을 통해서만 발생한다고 쓴다 `[SLEEP22:L245–247]`.

```text
DreamSim
→ internal routing influence
→ later call
→ Instrument / world contact
→ EventRecord
→ evidence-bound Update
```

이것은 `Influence ≠ Warrant`의 수면형 표현이다. 꿈은 사람을 움직일 수 있지만 자신이 묘사한 외부 사건의 증거를 자기 발행하지는 못한다.

### 5.3 gauge-only라는 이름은 원문 내부에서도 과하다

`A-DREAM2`는 DreamSim·Readdr·RouteCalib를 `gauge/address/tracking state transformation`이라고 부른다 `[SLEEP22:L196–199]`. 그러나 같은 문서는 DreamSim output이 `ρ/Φ/Θ/AddrSig` update signal일 수 있고 다음 routing·행동에 영향을 줄 수 있다고 둔다 `[SLEEP22:L115–120; L239–247]`.

```text
future observable behavior may change
⇒ not merely inert redescription
```

따라서 `gauge-only`가 `권한이 없다`는 뜻이라면 기능을 수행하지만, `물리적으로 관측 가능한 차이를 만들지 않는다`는 뜻이라면 `D-DREAM1/T-DREAM1/T-DREAM2`와 충돌한다. 더 안정적인 역할명은 `non-authoritative causal transformation`이다. 이것은 현행 교정이며 원문 명칭을 소급 변경하지 않는다.

### 5.4 Forget은 cache maintenance로 좁혀진다

`D-FORG1`은 망각을 `𝔄` 삭제가 아니라 `Φ/Θ/ℐ/AddrSig`의 제거·축소·재인덱싱으로 정의한다 `[SLEEP22:L124–129]`. `A-FORG1`은 판정가능항과 회계 잔차를 망각만으로 공짜 감소시킬 수 없다고 반복한다 `[SLEEP22:L189–192]`.

이 구분의 강한 형태는 다음이다.

```text
내가 기억하지 못함
≠ 그 사건이 일어나지 않음
≠ 타자의 손상이 사라짐
≠ 외부 증거가 자동 폐기됨
```

`[CURRENT/EXTERNAL LENS]` 여기부터는 역사 지층의 직접 명제가 아니라 현행 감사다.

하지만 원문은 외부 역사와 생물학적 기억을 같은 `𝔄 삭제 금지` 아래 너무 가까이 둔다. 생물학적 기억의 접근성·정확도·연결 강도는 PaidRepair나 Receipt 없이도 변할 수 있다. 보존해야 할 No-Free rule은 `망각이 세계 사건과 책임을 소급 삭제하지 못한다`는 감사 규칙이지, 내부 memory trace가 자연적으로 약해질 수 없다는 기술 법칙이 아니다.

---

## 6. 가능성에서 필연으로 — 빠진 전제

### 6.1 A-MET1은 backlog의 가능성만 말한다

`A-MET1`은 유한 Working Set 때문에 어떤 구간에는 `λ_in > μ_proc`가 발생할 수 있고 그때 backlog 누적은 정상이라고 쓴다 `[SLEEP22:L149–152]`.

논리형은 다음이다.

```text
finite W
⇒ ∃ interval where overload may occur
⇒ backlog can accumulate there
```

이것은 backlog가 언제나 생긴다거나 반드시 전역 scalar로 존재한다는 결론이 아니다.

### 6.2 T-MET1도 ‘존재할 수 있다’를 벗어나지 않는다

`T-MET1`은 지속 입력과 유한 Working Set이 있으면 충분히 긴 시간축에서 `λ_in > μ_proc`인 구간이 존재할 수 있다고 쓴다 `[SLEEP22:L205–207]`. 제목은 `Inevitability`지만 본문 술어는 `존재할 수 있으며`다.

```text
possibility in premise
→ possibility in theorem body
≠ inevitability
```

여기에는 제목과 논리 형식 사이의 강도 차이가 있다.

### 6.3 T-SLEEP-EX는 maintenance와 sleep을 한 단계에서 동일시한다

`T-SLEEP-EX`는 어떤 구간에서 평균 유입이 평균 처리보다 크면 maintenance epoch가 없을 때 backlog가 관리 불가능해질 수 있다고 말한 뒤, 안정 영역에는 입력 게이팅과 처리율 재배분을 수행하는 수면이 구조적으로 출현해야 한다고 결론낸다 `[SLEEP22:L218–221]`.

첫 절반이 요구하는 것은 다음이다.

```text
long-run load must be balanced
or backlog must be bounded / discarded / offloaded
```

그것이 곧바로 요구하지 않는 것은 다음이다.

```text
one global discrete sleep epoch
```

가능한 대안은 원문 정의만으로도 배제되지 않는다.

- 깨어 있는 동안 계속 수행되는 online maintenance
- 서로 다른 회로가 번갈아 정비되는 local maintenance
- 입력 선택·회피·환경 위임을 통한 `λ_in` 조절
- 처리 자원·중복 회로 확장을 통한 `μ_proc` 변화
- 중요도에 따른 합법적 소실·간섭·폐기
- 여러 backlog가 서로 다른 시간척도로 처리되는 vector model

### 6.4 수면이 있어도 전체 평균이 불안정하면 backlog는 계속 증가한다

queue skeleton을 문자 그대로 읽으면 안정성은 wake 구간 하나가 아니라 sleep–wake 전체 주기의 평균에 달려 있다.

```text
long-run average service
>
long-run average admitted load
```

수면 중 `λ_in`을 낮추는 것만으로 충분하지 않다. maintenance service가 실제로 backlog를 줄일 만큼 커야 하고, 낮 동안의 과부하를 전체 cycle에서 따라잡아야 한다. 원문은 sleep duration·stage·service capacity·priority를 정의하지 않으므로 `수면이 존재한다 → B가 관리된다`도 정리가 아니라 조건부 가능성이다.

### 6.5 전역 수면을 얻으려면 비가환성과 coordination 조건이 더 필요하다

원문이 의도한 결론을 강화하려면 최소 다음과 같은 전제가 필요하다.

```text
P1. 일부 structural maintenance는 live operation과 동시에 안전하게 실행되지 않는다.
P2. 두 작업은 같은 substrate / resource를 경쟁한다.
P3. local partition이나 redundancy만으로 deadline을 만족할 수 없다.
P4. 여러 영역의 maintenance가 system-level coordination을 요구한다.
P5. gated epoch가 전체 평균 안정성을 실제로 회복한다.
```

`SLEEP22`는 P1–P5를 정의하거나 증명하지 않는다. 따라서 수면 필연은 `[MISSING PREMISE + OVERGENERALIZATION]`이다.

---

## 7. 상세 모델이 spine으로 압축되며 강해지다

### 7.1 SPINE22는 인간다움을 여섯 조항에 묶는다

두 번째 append block은 목적을 `인간은 열린 계`로 두면서 UCXQ의 포트 주권·증빙 결박·결정성·청구 화살표를 꺾지 않고 만족·고뇌·서사·수면을 필연으로 만드는 것이라고 선언한다 `[SLEEP22:L296–300]`.

여섯 조항은 다음을 묶는다 `[SLEEP22:L337–346]`.

```text
open intake
+ closed authority path
+ finite working set
+ inevitable residual stock
+ inevitable sleep/GC
+ satisfaction as convergence / safe stopping
```

이 압축은 이론의 큰 그림을 선명하게 하지만, 상세 지층에 남아 있던 `가능`, `감소 가능`, `구체 함수형은 구현 위임`이라는 제한을 약하게 만든다.

### 7.2 ‘수면=GC는 설명이 아니라 필연’이 된다

`C-SP1`은 열린 계·유한 Working Set·닫힌 commit path만으로 `수면 같은 GC`가 선택적 장치가 아니라 구조적 필요라고 선언한다 `[SLEEP22:L352–354]`.

닫힌 commit path는 외부 권한 갱신에 대한 규칙이다. 그것이 내부 maintenance scheduling을 왜 전역 수면으로 강제하는지는 별도 논리가 필요하다. 여기서 audit architecture와 생물학적 sleep architecture가 한 문장 안에 접합된다.

### 7.3 SPINE22C는 전체를 한 문장에 잠근다

마지막 `A-SPINE0′`는 열린 입력, 증빙 결박, 유한 처리, backlog, 결정적 수면, 공짜 망각 금지, 만족의 safe-stopping을 한 문장으로 결합한다 `[SLEEP22:L389–404]`.

이 지층은 설명 순서를 넘어 의존 관계를 자동화한다.

```text
open human
→ finite processing
→ backlog
→ deterministic sleep maintenance
→ safe-stopping satisfaction
```

하지만 한 문장 안에 들어갔다고 각 화살표가 증명되는 것은 아니다. 오히려 상세 정의가 구분하던 운영 재고·회계 잔차·felt state·biological sleep가 하나의 `maintenance-governed worldline` 안에서 다시 가까워진다.

---

## 8. 만족·불길함·수축 — maintenance가 삶의 정지 조건이 되다

### 8.1 backlog는 불길함과 승격압력의 가능한 원인이다

`A-MET2`는 backlog·Working Set 포화·Continuity Tax가 커질수록 표면에서 빈칸 메우기와 연속 봉합이 증가하고, `Π_view`를 판정처럼 취급하려는 승격압력이 높아질 수 있다고 쓴다 `[SLEEP22:L156–159]`.

이것은 피곤할수록 성급한 확신과 과잉 봉합이 생길 수 있다는 runtime 가설이다. 원문은 그 압력을 truth-token이 아니라 routing-token으로 제한한다.

그러나 `T-MET2`는 같은 관계를 단조 결합으로 강화한다. `B` 증가·`W` 포화·`τ_cont` 증가가 발생하면 ElevationPressure와 `δ`가 감소하지 않는다고 선언한다 `[SLEEP22:L211–214]`. 반례와 포화 뒤 적응, 회복탄력성, 개인차, 외부 안전 신호가 정의되지 않으므로 이 단조성은 모델 가정이다.

### 8.2 만족은 maintenance 가능성을 포함한 안전 정지가 된다

`C-SAT-MET`는 만족을 backlog가 폭주하지 않고, 지금 멈춰도 장기 청구가 폭발하지 않으며, maintenance epoch를 통해 `B`와 `τ_cont`가 다시 관리 범위로 돌아올 수 있는 안정 영역으로 강화한다 `[SLEEP22:L267–275]`.

여기서 만족은 단순 쾌감이 아니라 `멈춰도 다시 운영 가능한가`라는 viability 판정에 가까워진다. 이것은 Chapter 09의 Safe-Stopping과 직접 이어지는 중요한 역사적 결합이다.

동시에 felt satisfaction은 여전히 없다.

```text
predicted maintenance feasibility
≠ feeling satisfied
≠ life flourishing
≠ actual long-term safety
```

### 8.3 Contraction은 단기 queue relief와 장기 bill을 분리한다

`Contraction`은 입력이나 집행을 줄여 단기 backlog 상승을 완화할 수 있지만, Coverage 확장과 수리 없이 지속되면 장기 회계 압력이 커질 수 있다 `[SLEEP22:L251–255]`.

```text
withdrawal / shutdown
→ short-term operational relief
↛ repaired relation or erased obligation
```

이 분리는 유용하다. 쉬었다는 사실만으로 해결해야 할 외부 손상과 약속이 사라지지는 않는다. 그러나 원문은 지속 Contraction이 장기 `σ/ΔQ⊥` 생성률을 증가시킬 수 있다고만 선언하며, 어떤 외부 사건이 실제 청구를 만드는지는 기존 Event/Receipt 규칙에 의존한다.

### 8.4 수면 결핍은 하나의 systemic instability로 압축된다

`C-INSOM`은 수면이 부족하면 평균 처리율이 입력을 따라잡기 어려워져 backlog·Continuity Tax·Guard·불길함·승격압력이 상승하고 Contraction이 고정될 수 있다고 쓴다 `[SLEEP22:L279–281]`.

`[EXTERNAL LENS]`

이 문장은 실제 수면 결핍의 다양한 결과와 방향은 닮았지만, 모든 결과가 `B_t` 한 stock을 통해 발생한다는 경험적 근거는 제시하지 않는다. 외부 감사에서는 기능별로 분리한다.

---

## 9. 역사 본문의 종점 — 인간적 꿈에서 안전한 scheduler로

초기 꿈은 낮에 처리하지 못한 Gap·상처·MaskStrain·관계 잔류를 상징·재연하고 다음 날의 prior를 바꾸는 인간적 장면이었다. 중간 지층은 이를 annealing과 Internal Scene Generator의 낮은 coupling regime으로 바꿨다.

`SLEEP22`는 마지막으로 그 내용과 장면을 다음 운영 계약으로 다시 썼다.

```text
Open Intake
→ finite Working Set
→ operational backlog
→ gated maintenance epoch
→ Compression / Reindex / Readdr / RouteCalib
→ changed next-day routing

DreamSim
→ candidate influence
↛ truth / evidence / direct authority

Forget
→ cache / scaffold / address change
↛ deletion of world history
```

이 지층이 얻은 가장 중요한 것은 **정비와 면책을 분리한 것**이다.

> 피곤함은 사실 근거가 아니다.  
> 꿈은 외부 사건의 증거가 아니다.  
> 잊었다고 사건이 사라지지 않는다.  
> 쉬었다고 외부 수리가 완료되지 않는다.

그러나 이 안전장치를 유지하기 위해 문서는 더 강한 것을 함께 주장했다.

> 열린 입력과 유한 활성 때문에 backlog는 필연이고,  
> 그 backlog 때문에 별도의 결정적 수면 epoch도 필연이다.

첫 묶음은 권한과 영향의 타입 분리다. 둘째 묶음은 인간의 생물학적 architecture에 대한 모델 가설이다. 두 묶음은 같은 진리 지위를 갖지 않는다.

역사 본문은 다음 문장에서 멈춘다.

> **0121의 수면 이론은 잠을 관찰해 설명한 이론이라기보다,  
> 열린 인간 runtime과 닫힌 권한 경로를 동시에 유지하려고 필요한 내부 정비 창을 먼저 만들고,  
> 그 창의 이름을 수면으로 고정한 이론이었다.**

---

# 외부 현실 감사 — 실제 수면은 하나의 GC인가

## E0. 감사 범위와 판정 규율

이 절은 `SLEEP22`의 역사적 의도를 평가하는 자료가 아니라, 그 문서가 인간·생물 일반에 대해 강하게 선언한 명제를 2026년 7월까지의 외부 1차 연구와 대조하는 독립 층이다.

외부 문헌은 다음 네 등급으로 나눈다.

| 등급 | 이 장에서의 뜻 |
|---|---|
| **확립에 가까움** | 서로 다른 방법·종·개입에서 방향이 반복되며 제한된 인과 근거가 있음 |
| **유력·범위 제한** | 직접 자료가 있으나 특정 종·회로·수면 단계·과제에 한정됨 |
| **논쟁** | 측정법·종·마취·endpoint에 따라 결과가 충돌함 |
| **근거 부족** | 매력적인 기능 가설이나 주관적 내용의 인과 역할이 분리되지 않음 |

이 감사는 다음을 하지 않는다.

- 동물 결과를 인간 전체로 자동 일반화하지 않는다.
- 수면 부족과 함께 변한 상관을 수면의 단일 목적이라고 부르지 않는다.
- sleep physiology, neural replay, subjective dream, dream report를 동일시하지 않는다.
- 하나의 연구가 보여준 충분조건을 수면 전체의 대체라고 부르지 않는다.
- 생물학 자료를 TAD의 증거·권한 규율을 정당화하는 근거로 역이용하지 않는다.

---

## E1. 확립에 가까운 것 — 수면은 정지가 아니라 다중 상태 전환이다

### E1.1 수면 중에도 뇌와 몸은 적극적으로 상태를 바꾼다

수면은 외부 입력이 완전히 0이 되는 전원 차단이 아니다. 반응성·감각-운동 결합·신경조절 환경이 달라지고, NREM과 REM 안에서도 서로 다른 역학이 반복된다. 기억·시냅스·대사·면역·체온·조직 회복·유체 흐름에 수면과 연관된 변화가 있다는 자료는 많다.

인간 실험에서도 급성 수면 부족은 서로 다른 생리 endpoint를 교란한다. 40시간 각성은 소규모 whole-room calorimetry 연구에서 24시간 에너지 소비를 높였고 `[EXT-ENERGY11]`, 한밤의 완전 수면박탈은 소규모 무작위 교차시험에서 식후 근육 단백질합성을 낮췄다 `[EXT-MUSCLE21]`. 접종 직후 수면과 밤샘을 비교한 연구에서는 수면군의 항원 특이 면역 반응이 더 강했다 `[EXT-IMMUNE03]`.

이 결과들은 수면 기회가 이후의 서로 다른 생리 endpoint에 영향을 준다는 제한된 인과 근거다. 수면 중 하나의 공통 `maintenance operation`을 직접 관측한 것은 아니며, 서로 다른 endpoint를 하나의 `B_backlog` 감소로 환산하지도 못한다.

```text
energy regulation
≠ protein synthesis
≠ immune memory
≠ synaptic remodeling
≠ one measured backlog stock
```

### E1.2 수면은 하나의 전역 Boolean보다 지역·단계별 상태에 가깝다

오래 깨어 있던 쥐는 행동과 전역 EEG상 깨어 있어도 일부 피질 뉴런군만 잠깐 off 상태에 들어갈 수 있었고, 그 영역을 요구하는 과제 수행이 나빠졌다 `[EXT-LOCAL11]`. 이는 sleep pressure와 off dynamics가 지역적으로 나타날 수 있음을 보여준다.

큰군함조는 최대 열흘의 비행 중 한쪽 또는 양쪽 반구 수면을 사용했으며, 비행 중 평균 수면량은 육지에서의 약 7.4%였다 `[EXT-FLIGHT16]`. 수면의 양·연속성·반구 동기화가 생태 조건에 따라 크게 달라질 수 있음을 보여주지만, 줄어든 수면 기능이 나중으로 `연기`되었는지는 측정하지 않았다.

이 자료가 보여주는 것은 `수면이 필요 없다`가 아니다.

```text
global simultaneous sleep
is not the only observed scheduling form
```

---

## E2. 2026년의 직접 scope challenge — 전역 수면은 일부 기능의 유일한 구현이 아니다

`EXT-WAKE26`은 깨어 행동하는 생쥐 피질에 NREM형 on/off period를 광유전학적으로 유도했다. 생리·분자 실험에서는 5시간 수면박탈의 마지막 30분 동안 한쪽 피질에 유도하자 해당 쪽 후속 NREM의 slow-wave activity와 LFP/MUA 동기화 지표가 낮아졌고, GluA1 계열 표지가 선행 자연수면 연구와 같은 방향으로 변했다. 별도 기억 실험에서는 학습 직후 1시간 수면박탈 동안 양측 감각운동 피질에 같은 pattern을 유도하자 한 texture-recognition 과제의 공고화가 수면군 수준으로 회복됐다. 비슷한 평균 발화 감소를 지속적 억제로 만든 대조에서는 같은 효과가 없었다 `[EXT-WAKE26]`.

이 연구가 강하게 지지하는 판독은 다음이다.

> **일부 NREM 피질 유지 기능의 충분조건은 행동적 수면이라는 전역 상태보다 더 미세한 on/off activity pattern일 수 있다.**

이 연구가 증명하지 않은 것은 다음이다.

- 장기간 전신 수면을 완전히 대체할 수 있음
- REM 기능을 대체함
- 면역·대사·체온·조직 수리·fluid dynamics를 대체함
- 인간에서도 같은 조작이 안전하고 충분함
- 모든 기억 공고화가 동일 pattern으로 해결됨

그러므로 이 결과는 **일부 endpoint에 대해 전역 행동 수면이 유일한 구현은 아니다**라는 판독을 직접 뒷받침한다. maintenance 또는 sleep-like activity의 필요 일반을 반박하지 않으며, `Sleep has no essential functions`도 뒷받침하지 않는다.

```text
maintenance primitive
may be locally executable during wake

≠

all sleep is dispensable
```

---

## E3. 기억과 시냅스 — 압축보다 선택적 재조정

### E3.1 수면 생리가 기억에 인과적으로 기여하는 근거는 있다

쥐 해마 ensemble의 학습 뒤 재활성화와 `[EXT-REPLAY94]`, 시각피질–해마에서 같은 경험의 조정된 수면 replay가 관찰되었다 `[EXT-REPLAY07]`. 별도 조작 연구에서는 slow-wave sleep 중 hippocampal ripple을 선택적으로 억제하자 공간기억 수행이 손상되었고 `[EXT-SWR09]`, hippocampal ripple을 online 검출해 시간 맞춘 피질 자극으로 ripple–delta–spindle 결합을 강화하자 이후 기억이 향상되었다 `[EXT-COUPLE16]`. 각각 설치류의 제한 과제·회로에 관한 결과이며 `replay 전체`나 꿈의 보편 기능을 증명하지 않는다.

건강한 사람의 초기 NREM에 느린 oscillation과 비슷한 전기장을 유도한 실험은 slow oscillation·spindle activity와 해마 의존 선언기억 보존을 높였다 `[EXT-MEM06]`. NREM에 학습 맥락의 냄새를 다시 제시한 targeted memory reactivation 연구도 특정 기억의 보존과 해마 활성에 영향을 주었다 `[EXT-TMR07]`.

따라서 다음은 **후보 기전 사슬**이다. 사슬 전체가 한 실험에서 입증된 것이 아니라 각 화살표가 서로 다른 관찰·조작 근거를 가지며, 과제·종·뇌 영역에 따라 달라진다.

```text
sleep stage / oscillatory timing
─may modulate→ probability and timing of reactivation
─may influence→ selective strengthening / weakening / reorganization
─may contribute to→ later performance difference
```

여기서 바로 `압축`, `재인덱싱`, `주소 최적화`라는 생물학적 operator가 관측된 것은 아니다. 그것들은 여러 결과를 설명하기 위한 계산적 번역이다.

### E3.2 모든 시냅스를 지우는 전역 GC는 아니다

생쥐 피질을 3차원 전자현미경으로 횡단 비교한 연구는 수면군의 다수 axon–spine interface가 각성군보다 평균 약 18% 작았지만 가장 큰 약 20%의 접촉은 상대적으로 보존되었다 `[EXT-SYN17]`. 같은 시냅스를 전후 추적한 결과는 아니다. 별도 분자 연구는 수면 중 Homer1a가 AMPA receptor 제거와 homeostatic downscaling에 관여하는 경로를 제시했다 `[EXT-HOMER17]`.

반대 방향도 공존한다. 학습 뒤 수면은 특정 가지에서 새 dendritic spine 형성을 촉진할 수 있고 `[EXT-SPINE14]`, REM 관련 회로는 일부 새 spine을 가지치기하면서 다른 일부를 안정화할 수 있다 `[EXT-REMPLAST17]`.

따라서 현실에 가까운 표현은 다음이다.

```text
selective remodeling
= weakening + preservation + strengthening + new formation

≠ uniform erase
≠ one global compaction ratio
```

`SLEEP22`의 `μ_comp + μ_reidx + μ_readdr + μ_route`는 이 복합성을 떠올리게 하는 상위 비유로는 쓸 수 있지만, 한 단위의 실제 생리 처리율로 취급할 수 없다.

---

## E4. 세포·조직 maintenance — 실제이지만 종과 endpoint가 다르다

6–7 dpf 제브라피시 유생의 단일 뉴런 연구에서는 깨어 있을 때 DNA double-strand break가 축적되고, 수면 중 chromosome dynamics 증가가 손상 감소에 필요했다 `[EXT-DNA19]`. 초파리의 심한 수면박탈에서는 장에 reactive oxygen species가 축적되었고, 장내 항산화 개입이 거의 자지 않는 조건에서도 생존을 크게 구제했다 `[EXT-ROS20]`.

두 연구를 함께 읽으면 중요한 분리가 생긴다.

```text
some maintenance function can be tightly sleep-linked

and

some lethal consequence of sleep loss can be bypassed downstream
```

이 자료들은 선택된 핵·장 손상 endpoint가 수면 조건과 연결되고, 그중 일부 downstream 손상은 우회될 수 있음을 보여준다. 이를 모든 생명의 공통 maintenance architecture로 일반화할 수는 없으며, 한 생존 endpoint를 구제했다고 모든 수면 기능이 대체되는 것도 아니다.

따라서 지지되는 것은 process-specific 보호·재조정 과정의 존재다. `maintenance가 하나의 재고를 하나의 epoch에서 청산한다`는 세부 architecture는 지지되지 않는다.

---

## E5. glymphatic clearance — 유체 역학과 순배출을 분리한다

2013년 생쥐 연구는 수면·마취 조건에서 간질 공간이 커지고 tracer와 amyloid-β 제거가 빨라졌다고 보고했다 `[EXT-GLY13]`. 이 결과는 `잠이 뇌를 씻는다`는 강한 대중적 설명의 중심이 되었다.

하지만 다음을 분리해야 한다.

```text
CSF oscillation / inflow
≠ solute movement at one site
≠ net clearance from the brain
≠ universal core function of sleep
```

인간의 동시 EEG–고속 fMRI 연구는 NREM slow wave, hemodynamic signal, macroscopic CSF oscillation의 결합을 보였지만 용질 순배출을 측정하지 않았다 `[EXT-CSF19]`.

2024년 생쥐 연구는 fluorescent molecule diffusion이 sleep/wake에 따라 크게 달라지지 않았고, 측정한 clearance는 수면과 마취에서 오히려 낮았다고 보고했다 `[EXT-CLEAR24]`. 2025년 연구는 자연 NREM에서 norepinephrine oscillation·vasomotion·CSF inflow의 기전을 제시했지만 `[EXT-GLY25]`, inflow와 전뇌 순배출은 동일 endpoint가 아니다.

따라서 2026년 7월 기준 판정은 다음이다.

| 명제 | 판정 |
|---|---|
| 수면 단계에 따라 CSF·혈관 역학이 달라진다 | **유력·범위 제한** |
| 특정 tracer의 이동이 수면 상태와 연관된다 | **유력·측정법 의존** |
| 수면은 언제나 순수한 뇌 노폐물 배출을 증가시킨다 | **논쟁** |
| glymphatic cleaning이 수면의 단일 핵심 목적이다 | **근거 부족** |

`Sleep = GC`를 외부 생물학의 확립 명제로 사용할 수 없다.

---

## E6. 꿈 — 현상, replay, plasticity를 같은 기능으로 묶지 않는다

### E6.1 꿈은 REM과 동일하지 않다

반복 각성과 고밀도 EEG를 사용한 인간 연구는 꿈 보고가 REM뿐 아니라 NREM에서도 나타나며, 두 단계 모두에서 꿈 경험 보고와 무경험 보고가 갈릴 수 있음을 보였다 `[EXT-DREAM17]`. 특정 posterior cortical activity는 꿈 경험과 내용의 neural correlate였지만, 이 연구는 꿈의 기능을 조작한 실험이 아니다.

```text
REM ≠ Dream
NREM ≠ No Dream
sleeping ≠ necessarily reporting a dream
```

무경험 보고에는 기억 실패 가능성이 남는다. 그래도 `수면 상태`, `수면 중 의식 경험`, `각성 후 보고`가 서로 다른 측정 대상이라는 결론은 유지된다.

### E6.2 과제 관련 꿈과 향상은 인과를 증명하지 않는다

가상 미로를 학습한 뒤 낮잠에서 명시적으로 과제 관련 꿈을 보고한 사람은 전체 99명 가운데 4명이었고, 이 소수에서 더 큰 수행 향상이 관찰되었다 `[EXT-DREAM10]`. 그러나 꿈이 향상을 일으켰는지, 강한 재활성화가 꿈 보고와 향상을 함께 만들었는지는 분리되지 않았다.

수면 뒤 hidden-rule 통찰이 늘어난 연구 `[EXT-INSIGHT04]`와 REM 낮잠 뒤 primed association 활용이 향상된 연구 `[EXT-CREAT09]`도 sleep state나 stage의 효과를 다룬다. 꿈 내용을 조작하여 창의성이나 주소 재배치가 달라졌음을 보인 것은 아니다.

따라서 외부 자료가 허용하는 typed relation은 다음 정도다.

```text
SleepState
  ├─ may condition ReplayEvent
  ├─ may condition PlasticityChange
  └─ may permit DreamExperience

ReplayEvent may influence PlasticityChange
ReplayEvent may correlate with DreamExperience

DreamExperience → PlasticityChange
= not established as a general causal arrow
```

### E6.3 꿈은 수면의 조상적 이유라고 보기 어렵다

중앙집중식 뇌는 없지만 분산 신경망과 rhopalia를 가진 해파리 Cassiopea에서도 quiescence, 반응 지연, 박탈 뒤 homeostatic rebound를 충족하는 sleep-like state가 보고되었다 `[EXT-JELLY17]`. 이것은 모든 sleep-like state가 같은 기전을 가졌다는 증명이 아니다. 다만 고차 서사·Ghost·꿈이 수면의 보편적 조상 기능이라는 설명에는 강한 scope challenge다.

더 안전한 진화적 추론은 다음이다.

> 오래된 상태 조절·유지 기능 위에 복잡한 신경계의 내생적 현상 경험이 추가되었을 수 있다.

이 문장은 `[EXTERNAL INFERENCE]`이며 직접 실험 결론이 아니다.

---

## E7. 망각 — 내부 기억의 변화와 세계 역사를 분리한다

수면 중에는 강화만 일어나는 것이 아니다. REM-active MCH neuron 조작은 생쥐의 일부 해마 의존 기억 보존을 약화하거나 강화하는 방향으로 영향을 주었다 `[EXT-FORGET19]`. 시냅스 약화·간섭·접근 실패·active pruning은 모두 기억의 이후 접근성을 바꿀 수 있다.

따라서 생물학적 망각을 다음처럼 한 문장으로 닫을 수 없다.

```text
Forget = cache cleanup only
```

최소한 다음은 다르다.

```text
trace decay
overwrite / interference
retrieval failure
index / cue change
active weakening or pruning
source-provenance loss
autobiographical reinterpretation
```

반면 `이미 발생한 외부 사건이 나의 망각 때문에 소급 삭제되지 않는다`는 문장은 생물학 가설이 아니라 감사·책임 규율로 유지할 수 있다.

```text
MutableMemoryTrace
≠ MutablePastOccurrence
```

---

## E8. 원문 명제별 외부 판정

| `SLEEP22` 명제 | 외부 판정 | 안전한 재서술 |
|---|---|---|
| 인간은 외부 입력을 받는 유한 시스템이다 | **일반 시스템 전제로 유용** | 구체 생리량이 아니라 모델 전제라고 명시 |
| 서로 다른 부담이 누적될 수 있다 | **확립에 가까움** | 하나의 scalar가 아니라 process-specific state vector |
| 서로 다른 sleep-linked maintenance·plasticity 과정이 반복 관찰된다 | **확립에 가까움** | stage·region·tissue별 과정으로 분리 |
| `μ_comp+μ_reidx+…`가 하나의 처리율이다 | **근거 부족** | 계산적 비유; 공통 단위 없음 |
| backlog가 전역 수면을 구조적으로 요구한다 | **근거 부족 / 부분적 독점성 반례·대안 구현 존재** | 추가 비가환성·자원 충돌·coordination 전제 필요 |
| 수면 산출은 동일 상태·입력에 결정적이다 | **모델 가정** | runtime seal이지 생물학 발견이 아님 |
| 수면은 주소·라우팅을 최적화한다 | **유력한 비유, 직접 입증 아님** | 기억 재활성화·가소성의 가능한 계산 번역 |
| 꿈은 offline routing 후보를 시험한다 | **근거 부족** | 현상적 readout 또는 correlate 가설로 격하 |
| 꿈이 외부 사실의 증거가 아니다 | **경험과 무관한 인식 규율로 유지 가능** | `Dream Influence ≠ Dream Warrant` |
| 망각은 과거 사건을 지우지 않는다 | **타입 분리로 유지 가능** | world history와 biological memory를 분리 |
| glymphatic cleaning이 수면의 GC다 | **논쟁** | CSF dynamics와 net clearance 분리 |
| 수면 부족의 결과는 하나의 B 증가다 | **근거 부족** | 대사·면역·시냅스·인지 endpoint 분리 |

외부 감사의 종점은 다음이다.

> **유지보수 기능은 필요하지만 전역 수면이 이를 독점하지 않는다.  
> 수면은 여러 유지·가소성 과정을 시간적·공간적으로 조정하는 생물학적 상태군이며,  
> 각 과정은 서로 다른 substrate·단위·단계·증거 수준을 가진다.**

---

# 연구 후기 — 잠을 메인 축에서 내리고 유지 전이만 남기기

## A0. 후기의 독해 봉인

이후는 `SLEEP22`의 직접 역사가 아니다. Chapter 08–09의 현행 Ghost·Editor·Episode·QualiaMedium 가설, 사용자의 후속 정정, 외부 현실 감사를 대조하여 무엇을 메인 축에 남기고 무엇을 구현 가설로 내릴지 판정한다.

| 표지 | 뜻 |
|---|---|
| `[DIRECT-SLEEP22]` | 주자료가 직접 정의·주장 |
| `[EARLIER-LINEAGE]` | 0101–0109 전사·앞 장에서 복원된 문제틀 |
| `[EXTERNAL-EVIDENCE]` | 외부 1차 연구가 제한된 범위에서 지지 |
| `[USER-DIRECT]` | 사용자가 현행 이론으로 직접 명시 |
| `[BRIDGE-CURRENT]` | 직접 자료·외부 감사·현행 빈자리를 잇는 새 가설 |
| `[DEMOTED]` | 메인 축에서 구현·비유·가설 층으로 내림 |
| `[NON-CLAIM]` | 생물학·임상 사실로 확정하지 않는 구조 시험 |
| `[OPEN]` | 타입·인과·범위가 아직 닫히지 않음 |

핵심 봉인은 다음이다.

> **수면의 특정 기능이 내일 수정되어도 인간·생명 이론의 메인 척추는 살아 있어야 한다.  
> 메인 축에는 변화 속에서 경계·형성 능력·운영 연속성을 유지해야 한다는 문제만 남긴다.  
> 수면·국소 수면·휴식·중복·online repair는 그 문제의 가능한 구현이다.**

---

## A1. 이번 장의 실제 수확 — maintenance와 ledger rewrite를 분리했다

### A1.1 SLEEP22가 직접 얻은 가장 안정적인 것

`SLEEP22`의 생물학적 설명을 모두 내려도 다음 구조는 남는다.

```text
external influence may continuously enter
≠ external authority path is open

internal maintenance may alter future routing
≠ past world history is rewritten

dream / forgetting / fatigue may affect a person
≠ they self-issue evidence, excuse, or entitlement
```

이것은 `Maintenance Influence ≠ Ledger Rewrite`다.

정비가 다음날의 접근성·주의·행동 후보를 바꾸더라도, 외부에서 일어난 사건과 타자의 손상·약속·증거는 별도 타입과 절차에 남는다. 이 분리는 현행 TAD의 `Influence ≠ Warrant`와 강하게 이어진다.

### A1.2 ‘운영 부담은 곧 빚이 아니다’도 남는다

피로·과부하·미처리 입력·기억 간섭은 계산·생리·운영 부담일 수 있다. 그것이 곧 규범적 Debt·Bill·Blame은 아니다.

```text
MaintenanceCost
≠ PlasticityChange
≠ Scar
≠ Debt
≠ Responsibility
≠ Authority
```

`SLEEP22`는 `B_backlog ≠ σ/ΔQ⊥`를 직접 봉인했다. 이후 이론은 이 계정 분리를 더 엄격히 보존해야 한다.

---

## A2. 메인 축에서 내릴 것

### A2.1 `Sleep = necessary GC`는 메인 공리가 아니다

`[DEMOTED]`

전역 수면은 유지 문제의 유일한 논리적 해법이 아니며, 외부 자료도 국소·분할·단계별 maintenance를 보여준다. 다음 동일식은 폐기한다.

```text
maintenance necessity = sleep necessity
```

메인 이론은 `어떤 구조가 유지되어야 하는가`, `운영과 수리가 충돌할 때 어떻게 continuity를 보존하는가`를 물을 수 있다. 그 답을 수면 하나에 고정하지 않는다.

### A2.2 `B_t` 하나로 인간 전체의 미처리를 표현하지 않는다

`[DEMOTED]`

단일 `B_t`는 queue analogy의 요약 readout으로는 쓸 수 있지만 생물학·기억·서사·관계·회계 부담을 함께 담는 core state가 될 수 없다.

권장 분리는 다음과 같다.

```text
L_active      : 현재 Working Set의 활성 부담
L_integrate   : 아직 기존 구조와 접합되지 않은 plasticity / memory pressure
L_interfere   : 서로 경쟁하는 흔적의 간섭
L_continuity  : 현재 단면을 자기 계보로 추적·편성하는 비용
L_cell        : 세포·대사·조직 유지 부담
L_relational_processing
              : 관계 입력·해석·정서 조정의 운영 부담

ExternalObligation
              : evidence-bound 약속·의무·타자 손상의 미청산 상태
```

이 목록은 현행 `[BRIDGE-CURRENT]`이며 실측 변수 집합이 아니다. 핵심은 `한 stock이 아니다`라는 타입 규율이다.

### A2.3 `DreamSim = optimizer`를 기능 정의로 쓰지 않는다

`[DEMOTED]`

꿈은 내부 생성과 현상 경험의 한 regime으로 모델링할 수 있지만, routing optimizer·defrag·trauma processor라는 목적론을 core에 넣지 않는다. 꿈의 생생함·서사성·상징성은 최적화 성공의 지표도 아니다.

### A2.4 `QualiaAnnealing`은 외부 사실이 아니라 Bridge다

`[DEMOTED]`

수면이나 생각이 이후 QualiaMorph 가능성을 바꿀 수 있다는 가설은 보존할 수 있다. 그러나 `slime-like QualiaMedium이 수면 중 녹고 재응고한다`는 설명은 원문 직접 명제도, 외부 생물학의 확립 명제도 아니다.

---

## A3. 남길 조건부 원리 — Operation–Maintenance Noncommutativity

### A3.1 문제를 수면보다 추상적으로 다시 쓴다

`[BRIDGE-CURRENT]`

어떤 시스템에서 활성 연산에 쓰는 substrate와 구조를 저장하는 substrate가 부분적으로 겹치거나 같은 제한 자원을 경쟁할 수 있다. 그 구조를 사용하는 동안 구조 자체를 크게 바꾸면 현재 output과 consistency가 흔들릴 수 있다.

```text
StorageSubstrate ∩ ActiveRuntimeSubstrate ≠ ∅
or they share a bounded resource

StructuralUpdate ∘ LiveOperation
≠
LiveOperation ∘ StructuralUpdate
```

이 비가환성이 실제로 존재하고 안전한 online update가 불충분하다면, 시스템은 변경을 시간적·공간적으로 격리할 필요가 있을 수 있다.

### A3.2 조건부 설계 가설

다음은 현행 Bridge이며 생물학 보편 정리가 아니다.

> **어떤 구조 수정 `M`과 현장 운영 `O`가 같은 substrate·자원을 경쟁하고, `M∘O ≠ O∘M`이며,  
> 허용된 오류·기한 안에서 둘을 병행할 수 없다면,  
> 운영 일부를 gate·partition·delay하는 maintenance transition의 선택 압력이 생길 수 있다.**

필요한 전제를 풀면 다음과 같다.

```text
shared substrate
+ noncommuting update
+ bounded error tolerance
+ insufficient redundancy / partition
+ maintenance deadline
→ isolation or scheduling pressure
```

### A3.3 이 정리가 수면을 자동 도출하지는 않는다

가능한 구현은 여러 가지다.

```text
online incremental update
rolling local maintenance
unihemispheric / redundant failover
traffic reduction during quiet wake
global coordinated sleep
downstream chemical compensation
replacement / regeneration
```

전역 수면을 얻으려면 여러 지역의 maintenance conflict graph가 연결되어 있거나 system-level synchronization이 필요한 추가 조건이 있어야 한다.

### A3.4 DB 비유의 지위

`[USER-DIRECT + DEMOTED]`

사용자는 수면을 `현재 기능과 연결된 저장 구조를 동시에 수정하면 오류가 나므로 live serving path를 낮춘 maintenance window`에 비유했다. 이 비유는 비가환성을 직관적으로 보여준다.

그러나 다음 이유로 메인 축에 넣지 않는다.

- 인간 기억은 하나의 중앙 DB가 아니다.
- 구조 수정은 깨어 있을 때도 계속 일어난다.
- 수면은 기억 이외의 몸·세포 기능도 포함한다.
- local sleep과 2026 wake induction은 전역 disconnect가 유일한 해법이 아님을 보인다.
- 꿈이 maintenance log나 compaction UI라는 기능은 입증되지 않았다.

따라서 DB 비유는 설명용 annex / Bridge이지 인간 ontology가 아니다.

---

## A4. 하나의 epoch 대신 typed maintenance path

### A4.1 반드시 분리할 다섯 타입

외부 자료와 SLEEP22의 역할 충돌을 함께 보면 최소 다음은 분리되어야 한다.

```text
SleepState
≠ ReplayEvent
≠ PlasticityChange
≠ DreamExperience
≠ LaterPerformance
```

가능한 제한적 관계는 다음과 같다.

```text
SleepState
  ├─ conditions some ReplayEvents
  ├─ changes probability of some PlasticityChanges
  ├─ alters metabolic / immune / thermal regimes
  └─ may permit DreamExperience

ReplayEvent
  ─may influence→ PlasticityChange

PlasticityChange
  ─may bias→ later AccessGeometry / skill / recall

DreamExperience
  ─may later be recalled, interpreted, narrated, or acted on
```

화살표는 process- and evidence-specific다. 하나의 보편 pipeline으로 확정하지 않는다.

### A4.2 maintenance는 scalar stock보다 작업 집합이다

현행 임시 표현은 다음처럼 둘 수 있다.

```text
MaintenanceDemand_t
= {
    cellular repair,
    synaptic reconfiguration,
    memory integration / interference management,
    metabolic calibration,
    immune update,
    thermal transition,
    fluid dynamics,
    access / continuity reconfiguration
  }
```

각 항은 다른 단위·deadline·지역·stage dependence를 가진다. `MaintenanceDemand`는 container name이지 합산 가능한 숫자라는 뜻이 아니다.

### A4.3 global sleep은 원인보다 coordination envelope 후보다

`[BRIDGE-CURRENT + EXTERNAL-INFERENCE]`

전역 수면은 모든 maintenance의 단일 엔진보다, 여러 지역·몸 상태·행동 위험이 서로 제약하며 함께 조율되는 envelope로 읽는 편이 안전하다.

```text
GlobalSleepState
= a coordination envelope within which
  { local maintenance events,
    altered neuromodulatory regimes,
    reduced external action coupling,
    body-wide processes }
  may co-occur and mutually constrain one another
```

이것은 2026년의 완성된 수면 이론이 아니라 외부 자료와 형식 문제를 함께 만족시키는 현행 가설이다.

---

## A5. 수면 전후의 자아 — 같은 Ghost가 계속 켜져 있는가

### A5.1 Chapter 08–09이 남긴 handoff 문제

Chapter 08은 Archive·Address·Access·Rehydration·Self-adoption을 분리했다. Chapter 09은 현재 Ghost와 IdentityHandle·PersonaRuntime·IdentityTracker·SelfOn을 분리했다.

수면은 이 차이를 극단적으로 드러낸다.

```text
Organism continuity may persist
IdentityHandle may persist
Archive traces may persist

while

current WorkingSet changes
SelfOn may weaken or alter
waking Ghost is not continuously active
```

그렇다면 수면 뒤의 나는 동일한 내용이 계속 켜져 있어서 같은 것이 아니다. 저장·몸·관계·정책·추적 handle에서 충분한 구조를 다시 활성화하고 인수하기 때문에 같은 것으로 취급된다.

### A5.2 현재 Ghost의 실현과 통시적 연속성을 다시 분리한다

`[BRIDGE-CURRENT + NON-CLAIM]`

DB 비유에서 건질 수 있는 자아 통찰은 수면 기능이 아니라 continuity 쪽이다. 그러나 `Self` 하나의 함수에 모든 성분을 넣으면 Chapter 09이 분리한 현재 경험 주체·지속 handle·통시 handoff가 다시 뭉친다.

```text
CurrentGhost_t
= Realize(
    CurrentQualiaMorph,
    CurrentInput / EnvironmentCoupling,
    WorkingSet,
    BodyState,
    AccessibleArchive,
    AccessPolicy,
    CurrentGoals
  )

DiachronicSelfContinuity
= HandoffRelation(
    IdentityHandle,
    RelationalAnchors,
    Episode / Narrative adoption,
    attribution and provenance,
    successive CurrentGhosts
  )
```

현재 Ghost는 매 순간 새로 실현될 수 있고, 통시적 자기 연속성은 그 Ghost들이 같은 내용을 갖는지가 아니라 어떤 handle·귀속·관계·서사 handoff로 이어지는지를 판정하는 관계일 수 있다.

이것은 메인 자아 이론의 후보지만 `수면이 DB compaction이기 때문에 참`인 것은 아니다. 수면 가설과 독립적으로 검토해야 하며, `CurrentGhost = DiachronicSelf`로 다시 동일시하지 않는다.

### A5.3 의식 없는 변화의 저자성

수면 중 plasticity가 다음 Ghost의 접근성·감정 경사·숙련을 바꿀 수 있다면 다음이 성립한다.

```text
change happened within me
≠ current conscious Ghost selected it
≠ Editor endorsed its content
≠ I possess warrant for its source story
```

다음 Ghost가 그 변화를 자신의 상태로 인수하더라도, 변화의 발생 provenance와 서사적 authorship은 별도다. 이것은 꿈·습관·질병·약물·기억상실·발달에도 이어지는 Open이다.

---

## A6. Ghost·Editor·Dream — 생성, 체험, 승인, 행동을 분리한다

### A6.1 SLEEP22 직접 지층에는 현행 Ghost와 Editor가 없다

`DreamSim`은 `Π_view` 기반 routing candidate test다. `SLEEP22`는 Ghost·Editor·Episode·NarrativeAdoption·QualiaMedium을 정의하지 않는다.

따라서 다음 소급은 금지한다.

```text
DreamSim = Ghost
DreamSim output = Editor decision
Dream content = intention
Dream content = autobiographical adoption
```

### A6.2 현행 Bridge의 DreamGhost

`[BRIDGE-CURRENT + NON-CLAIM]`

꿈에서 실제 일인칭 경험이 형성될 때만 임시로 다음을 둘 수 있다.

```text
DreamGhost
= transient first-person assembly
  under altered sensory / action coupling
```

DreamGhost가 waking Ghost와 같은 기억 접근, 현실 검증, 행동 gate, authorship을 갖는다는 뜻은 아니다. 꿈을 꾼 현재와 꿈을 기억해 서사로 채택하는 깨어난 현재도 다르다.

### A6.3 꿈에서 행동까지의 합법 경로

```text
Dream-associated internal activity
  └─ may bias→ Plasticity

DreamExperience
  ├─ may later bias→ affect / policy
  └─ may or may not be recalled or reported

if recalled:
DreamRecall / DreamReport
→ source attribution
→ hold as imagined
   or adopt as personally meaningful
   or reject / ignore
→ [optional Editor deliberation]
→ possible call
→ world contact
→ possible EventRecord
→ adjudication / possible evidence-bound update
```

꿈은 보고 없이도 이후 감정·접근성·정책을 기울일 수 있다. Editor는 모든 행동의 필수 상주 기관이 아니라 명시적 숙고가 발생할 때의 선택 모드다. 외부 사건과 공적 사실은 꿈의 생생함이 아니라 world contact 이후의 독립 판정 경로를 통과해야 한다.

### A6.4 가장 안정적인 봉인

> **Dream Influence ≠ Dream Warrant.**

이 문장은 꿈을 무력하게 만들지 않는다. 꿈은 감정·접근성·선택을 바꿀 수 있다. 다만 그 영향력으로 외부 사실과 타자에 대한 Authority를 자기 인증하지 못한다.

---

## A7. 기억과 원장 — No-Free-Forgetting의 범위를 다시 잠그기

### A7.1 네 저장 역할을 분리한다

```text
WorldOccurrence
: 실제로 발생한 외부 사건

ExternalEvidence
: occurrence를 판정하는 독립 자료

InternalMemoryTrace
: 유기체 안에 남은 가변적·불완전 흔적

AutobiographicalSummary
: 현재 자아가 그 흔적을 연결해 만든 자기 서술
```

### A7.2 허용되는 변화

```text
InternalMemoryTrace may weaken / compete / reorganize.
AutobiographicalSummary may be revised.
AccessGeometry may change.

These do not by themselves alter WorldOccurrence.
```

사건의 외부 증거도 영원히 완전하다는 뜻은 아니다. 증거가 손실되거나 판정이 바뀔 수 있지만, 그것은 개인의 cache maintenance와 다른 provenance를 가진다.

### A7.3 좁아진 No-Free-Forgetting

현행에서 보존할 규칙은 다음이다.

> **내부 망각·재서술·접근 실패만으로 이미 발생한 외부 사건, 타자의 독립된 흔적, 증빙된 의무를 소급 삭제할 수 없다.**

다음 강한 규칙은 채택하지 않는다.

> 모든 생물학적 기억 약화에는 PaidRepair·Receipt·Bill이 필요하다.

첫 문장은 audit boundary다. 둘째는 틀린 계정 혼합이다.

---

## A8. Qualia와 maintenance — 아직 없는 substrate

### A8.1 SLEEP22가 실제로 바꾸는 것

직접 정의에 따르면 Readdr와 DreamSim은 `ρ/Φ/Θ/ℐ/AddrSig`에 update signal을 줄 수 있다. 하지만 다음은 없다.

```text
persistence duration
decay law
consolidation rule
source provenance
medium deformation operator
handoff into next Ghost
```

따라서 `Reversible ≠ Traceless`를 만족하는 지속적 내부 변화 타입은 여전히 비어 있다.

### A8.2 NEWQUAL22도 자동으로 그 공백을 채우지 않는다

`NEWQUAL22`의 `ΦΩ`는 후보장 위의 medium metric / impedance다. call distribution을 기울이는 causal layer이지만, 그 자체가 경험마다 변형되어 지속되는 물질인지, 수면 중 anneal되는지, 다음 Ghost로 어떤 update signature를 넘기는지는 별도 감사가 필요하다.

```text
ΦΩ metric
≠ QualiaMedium substrate
≠ PlasticTrace
≠ sleep consolidation law
```

### A8.3 남은 공백

다음 장이 확인해야 할 객체는 `꿈`이 아니라 이것이다.

> **권한은 없지만 지속할 수 있고, 생각·체험·수면·학습으로 변형되며, 다음 현재의 접근 지형을 제한하는 내부 substrate 또는 update law가 실제로 등장하는가.**

---

## A9. 형식 감사 — SLEEP22가 아직 닫지 못한 것

### A9.1 μ_proc 합에는 단위가 없다

Compression·Reindex·Readdr·RouteCalib·PaidRepair의 처리량을 더하려면 공통 단위와 교환비율이 필요하다. 원문은 이를 주지 않는다.

```text
μ_comp + μ_route
```

가 의미 있으려면 동일 resource budget에서의 normalized service rate 등 별도 정의가 필요하다.

### A9.2 B_backlog는 식별되지 않는다

Guard·dread·ContinuityTax는 여러 잠재 상태의 readout일 수 있다. 관측만으로 유일한 `B`를 복원할 measurement model이 없다.

### A9.3 결정성은 hidden state를 무한히 흡수할 수 있다

`동일 ρ + 동일 GateTrace → 동일 output`은 `ρ`가 무엇을 포함하는지 닫혀 있지 않으면 검증 가능한 명제가 아니다. runtime reproducibility rule과 empirical hypothesis를 분리해야 한다.

### A9.4 Readdr 목표는 항상 낮추는 것만 허용한다

AfterCost·coactivation width·ContinuityTax를 낮추는 목표는 relief를 설명하지만, 유용한 결합의 강화·새 skill·새 memory association·경고 민감도의 보존을 표현하지 못한다.

```text
maintenance
≠ minimization of every coupling
```

### A9.5 monotone pressure theorem은 추가 공리다

`B` 증가·`W` 포화·`τ` 증가가 `δ/ElevationPressure`를 절대 감소시키지 않는다는 `T-MET2`는 앞 정의에서 도출되지 않는다. 적응·무감각·우선순위 변화·외부 안전 신호가 반대 방향을 만들 수 있다.

### A9.6 sleep necessity와 sleep sufficiency가 모두 비어 있다

```text
Necessity gap:
maintenance alternatives are not excluded.

Sufficiency gap:
sleep duration / stages / service rates do not ensure bounded backlog.
```

### A9.7 Cut-1 maintenance와 PaidRepair가 한 처리율에 섞인다

패치 전체는 Cut-1 내부의 계산·schedule만 확장한다고 선언한다 `[SLEEP22:L4–8]`. 수면·꿈은 EvidenceLink/Receipt를 자동 발행하거나 applied `𝔄`를 갱신할 수 없다 `[SLEEP22:L177–180]`.

그런데 `μ_proc`에는 `μ_repair`, 즉 PaidRepair가 포함되고 `[SLEEP22:L29–41]`, interlock epoch는 VERY_SLOW `κ/σ_age`의 유상 처리까지 위한 창으로 묘사된다 `[SLEEP22:L183–185]`.

```text
InternalRepairPreparation
≠ EvidenceBoundSettlement
≠ AppliedLedgerRepair
```

Cut-1이 합법적으로 할 수 있는 것은 repair 후보 준비·schedule, 또는 이미 외부 사건으로 적용된 repair 결과의 내부 재조정일 수 있다. PaidRepair 자체의 회계 갱신을 수면 operator가 수행한다면 Single Writer와 Proof-Binding을 우회한다. `μ_repair`가 세 역할 가운데 무엇인지 원문은 구분하지 않는다.

### A9.8 SPINE22의 GC 명명은 마지막 봉인과 흔들린다

`C-SP1`은 제목에서 `수면=GC`라고 선언한다 `[SLEEP22:L352–354]`. 마지막 주석은 다시 수면을 `GC가 아니라 결정적 유지보수 에폭`이라고 부른다 `[SLEEP22:L398–403]`.

이 차이는 단순 표현 차이일 수 있지만, 삭제·compaction·reindex를 포괄하는 GC 비유를 유지할지 폐기할지 문서 안에서 안정되지 않았음을 보여준다.

### A9.9 압축 spine에는 미정의 `F_t`가 들어온다

`D-SP1`은 metabolic loop를 다음처럼 쓴다 `[SLEEP22:L310–316]`.

```text
λ_in → F_t 축적 → Access → W_t 활성
→ Compression / Reindex / Readdress → F_t 재구성
```

그러나 `F_t`는 이 파일에서 정의되지 않는다. field, flux, latent form 가운데 무엇인지 알 수 없고 backlog `B_t`, reversible state `ρ`, graph와의 관계도 없다. 상세 모델을 한 줄 spine으로 압축하면서 새 중간 상태가 설명 없이 들어온 사례다.

---

## A10. 기호·계보·충돌 지도

### A10.1 기호와 역할

| 기호·이름 | 원문 역할 | 충돌·공백 | 현행 판정 |
|---|---|---|---|
| `λ_in` | 외생 입력률 | 감각·정보·사회 입력의 공통 단위 없음 | open-intake meta variable |
| `μ_proc` | 다섯 maintenance 처리율의 합 | 단위·tradeoff·병렬성 없음 | operator-family readout으로 격하 |
| `B_t` | 운영 backlog | 초기 0121 Access bandwidth와 기호 충돌; 식별식 없음 | `B_backlog` alias, core scalar 아님 |
| `GateTrace` | 수면 중 제한 입력 | sensing·arousal·cue의 구분 없음 | conditioned input interface precursor |
| `Readdr` | 주소·scaffold·tracker 재배치 | update law·preservation invariant 없음 | access-geometry Bridge |
| `DreamSim` | offline routing candidate test | dream experience·replay·plasticity 혼합 위험 | non-authoritative generator hypothesis |
| `Forget` | cache/scaffold 축소·재인덱싱 | decay·interference·pruning 누락 | memory/world-history 분리 후 제한 사용 |
| `τ_cont` | continuity editing cost | metabolic·compute·felt effort 구분 없음 | operational tracking cost |
| `Θ_t` | SLEEP22: Readdr가 바꾸는 추적 상태 | RTO21의 승격 임계, SAT22의 identity tracker와 같은 기호 | `θ_crit / Θ_track` 분리; monograph는 `theta_trk` 사용 |
| `δ` | dread / routing token | B의 고유 readout 아님 | non-authoritative signal |
| `𝓔_sleep` | deterministic maintenance interval | local/online/stage variation 누락 | biological implementation family |

`Θ_t`의 이동은 특히 강하다. `RTO21`에서는 `Π_view` 후보의 승격 압력이 위험으로 바뀌는 criticality threshold이고 `[RTO21:L67–73]`, `SAT22`에서는 과거와 현재 단면을 잇는 identity tracking hypothesis다 `[SAT22:L35–42]`. `SLEEP22`는 설명 없이 그것을 Readdr 대상인 `추적`으로 사용한다 `[SLEEP22:L96–101]`. `CORE26`은 다시 추적/감사 부담으로 요약하고 `[CORE26:L195–200]`, monograph에서야 `theta_trk`로 개명한다 `[MONO15:L2013–2020]`.

```text
Θ_criticality
≠ Θ_identity-tracker
≠ tracking workload
```

### A10.2 계보 등급

| 요소 | 판정 | 이유 |
|---|---|---|
| Gap cooling → DreamSim | **문제 계보 / 직접 타입 승계 아님** | next-day change는 공통, 인간적 잔류 내용은 삭제됨 |
| Dream settlement → Readdr | **기능 번역** | 상징·재연을 address/routing operation으로 재기술 |
| GEE anneal → sleep maintenance | **비유 계보** | 온도·응고는 SLEEP22에 직접 남지 않음 |
| ISG dream regime → DreamSim | **부분 직접 선행** | low coupling candidate generation은 닮지만 maintenance 목적은 별도 |
| `Open Intake ≠ Open Authority` | **현행 TAD 강한 계보** | 영향과 증빙 갱신 경로를 분리 |
| `B_backlog ≠ Debt` | **중요한 직접 분리** | 운영 압력과 회계 잔차를 분리 |
| `Dream Influence ≠ Warrant` | **강한 현재형 계보** | 내부 인과와 외부 사실 권한 분리 |
| Sleep as necessary GC | **과잉 승격 / 비승계 권고** | missing premise와 외부 반례 |
| QualiaAnnealing | **새 Bridge, 직접 승계 아님** | SLEEP22·NEWQUAL22 모두 substrate law를 주지 않음 |
| Operation–Maintenance Noncommutativity | **새 조건부 Bridge** | DB 비유에서 추상화; 수면을 자동 도출하지 않음 |

### A10.3 후기 통합에서 분리가 다시 무너졌다가 복구된다

`CORE26`은 `B_t`를 `미정리/미청산 잔차`라고 부르고, 수면을 재주소·압축·재정렬·`부채청산`을 통한 margin 회복으로 설명한다 `[CORE26:L195–208; L337–340]`. 이것은 `SLEEP22`가 직접 잠근 `B_backlog ≠ σ/ΔQ⊥`를 다시 흐린다.

같은 문서의 후미 지층은 수면을 potential을 늘리는 과정이 아니라 commit yield `q`를 회복하는 과정으로 다시 번역하고, DreamSim은 후보를 만들되 Evidence를 만들지 못한다고 좁힌다 `[CORE26:L721–731]`. 이는 직접 승계라기보다 별도 재해석이다.

후기 monograph는 수면 모듈을 `INFO` 성숙도로 두면서도 prose에는 backlog와 수면이 필연이라고 남긴다 `[MONO15:L2095–2102]`. 원래의 `T-SLEEP-EX`는 재수록하지 않고, 대신 `B`를 exact queue skeleton으로 쓰고 운영 backlog `Ω_ops`와 회계 backlog `Ω_bill`을 분리한다 `[MONO15:L2439–2478]`.

모듈 의존표도 완전히 닫히지 않는다. SAT annex는 SLEEP annex를 import하고 `[MONO15:L1973–1980]`, SLEEP annex는 목표 함수에서 SAT가 정의한 `τ_cont`를 사용한다 `[MONO15:L2179–2182]`. 그러나 SLEEP의 Depends/Imports 목록에는 SAT annex가 없다 `[MONO15:L2104–2110]`.

```text
declared dependency graph
≠ actual symbol dependency graph
```

더구나 같은 monograph의 `C-SLEEP2`는 backlog·주소/라우팅·AfterCost를 **maintenance epoch에서만** 결정적으로 정리할 수 있다고 다시 강화한다 `[MONO15:L2209–2215]`. 이는 상세 skeleton이 허용한 online/local service 가능성보다 강한 exclusivity claim이며, 앞의 약화된 정리로부터 나오지 않는다.

monograph 내부에는 `Readdress`의 직접 scope 충돌도 남는다. CORE의 `S6`는 재주소·관계 재협상·리브랜딩을 `chgA(y)`에 계상해야 한다고 규정한다 `[MONO15:L416–418]`. 반면 SLEEP annex의 `Readdr`는 runtime-only이고 evidence/receipt를 만들지 않는다고 둔다 `[MONO15:L2117–2121; L2175–2177]`.

```text
Readdr_internal
: cache / scaffold / access geometry

Readdr_public
: relation / branding / authoritative address change
```

이 두 타입을 분리하면 양립 가능하지만 monograph는 같은 operator name을 사용한다. 이름이 같다고 같은 accounting rule을 적용하면, 정상적인 내부 memory reorganization이 곧 `chgA`·Bill이 되거나 반대로 공적 재협상이 무료 cache update가 될 수 있다.

monograph의 더 약한 정리는 모든 허용 환경에서 `Ω_total=0`을 항상 보장할 정책이 없다는 것뿐이며, benign한 실행에서는 0인 구간도 가능하다고 명시한다 `[MONO15:L2483–2499]`.

```text
SLEEP22 detail:
backlog possible → maintenance condition → sleep necessity claim

CORE26:
backlog and debt partially re-collapse

MONO15:
ops/bill separation restored
+ universal-zero impossibility theorem
− direct proof of biological sleep necessity
```

따라서 현행 계보에서 살아남은 것은 `수면 필연 정리`보다 `열린 입력 아래 모든 미청산을 항상 0으로 보장할 수 없다`는 더 약한 한계다.

동시기·후속 가지도 같은 긴장을 반복한다. `LIFE23`은 휴식/고독/수면이 외부 기록압을 낮추고 차폐를 회복하며 `σ_rec`을 정리한다고 써, 운영 maintenance와 외부 회계 청산을 다시 가까이 붙인다 `[LIFE23:L207–211]`. `MINI27`은 수면을 `𝒢_eff`의 geometry repair와 창의적 후보 구조화로 번역하되 `𝔄` 승격을 금지한다 `[MINI27:L186–197]`. 날짜가 확정되지 않은 `SYNTH27`은 세 잔차 분리와 조건부 결정성을 유지하면서도 Sleep Necessity와 insomnia 귀결을 다시 싣는다 `[SYNTH27:L307–311; L327–329; L383–386; L425–427]`.

registry 생존도 직선이 아니다. `REG23`에는 `bg/radr/drms/gt`가 root로 남지만 `Forget` root는 없다 `[REG23:L168–178]`. 후기 monograph의 최소 root 목록에서는 `bg/radr/drms/gt`도 빠지고, sleep 연산은 INFO annex export로 내려간다 `[MONO15:L620–637; L2112–2121]`. 따라서 이름의 registry 생존은 `REG23` 분기에서만 맞고, 후속 정본에서는 다시 module-local vocabulary로 강등된다.

### A10.4 핵심 비동일성

```text
Maintenance necessity ≠ sleep necessity
Sleep necessity ≠ global simultaneous sleep
Global sleep ≠ one GC operation

SleepState ≠ DreamExperience
DreamExperience ≠ DreamReport
DreamExperience ≠ ReplayEvent
ReplayEvent ≠ PlasticityChange
PlasticityChange ≠ successful consolidation

PlasticityChange ≠ Evidence
PlasticityChange ≠ EventRecord
PlasticityChange ≠ Scar
PlasticityChange ≠ Debt

MemoryTrace ≠ WorldOccurrence
MemoryAccess ≠ MemoryTrace existence
AutobiographicalSummary ≠ ExternalEvidence

MaintenanceCost ≠ Responsibility
fatigue ≠ excuse
relief ≠ repair
forgetting ≠ historical erasure
```

---

## A11. Recovered / Lineage / Residue / Bridge / Open

### Recovered — 원문에 직접 있었던 것

- 인간을 지속적인 외생 입력을 받는 열린 계로 둠
- 외부 입력과 `𝔄` 갱신 권한을 분리
- 유한 Working Set과 합성 processing throughput
- 처리 미완료 압력을 `B_backlog`라는 운영 재고로 정의
- `B_backlog ≠ σ/ΔQ⊥/Bill` 계정 분리
- 수면 중 입력을 0이 아니라 `GateTrace`로 제한
- 수면을 현장 예산 재배치와 maintenance 우선 mode로 정의
- Compression / Reindex / Readdr / RouteCalib / PaidRepair 분류
- Readdr는 Evidence를 만들지 못함
- DreamSim은 truth-token이 아닌 offline candidate test
- dream output은 외부 update를 직접 정당화하지 못함
- Forget은 worldline 삭제가 아니라 내부 cache/scaffold 변화
- Contraction의 단기 운영 완화와 장기 외부 bill 가능성 분리
- Satisfaction을 maintenance 가능성이 포함된 Safe-Stopping으로 강화

### Lineage — 현행으로 이어진 문제틀

- `Open Intake ≠ Open Authority`
- `Influence ≠ Warrant`
- 내부 정비·꿈·망각과 외부 증거·책임 원장 분리
- 운영 부담과 normative debt 분리
- 지속된 영향이 곧 외부 사건은 아니라는 타입 경계
- 몸·기억·접근 지형이 다음 call을 기울여도 applied update는 사건 경로를 거쳐야 함
- 현재의 relief와 실제 repair를 분리

### Residue — 집을 얻지 못한 것

- 여러 maintenance demand의 단위·state vector
- `B_backlog` measurement / identification model
- `μ_proc`의 공통 단위·resource allocation law
- sleep stage·region·duration별 operator
- local/online/global maintenance 선택 규칙
- Readdr의 update function·preservation invariant·maladaptive outcome
- dream experience / replay / plasticity / report의 타입 분리
- persistence-capable non-authoritative PlasticTrace
- sleep-to-waking Ghost handoff
- biological forgetting의 decay·interference·pruning·source-loss 분류
- felt fatigue·relief·satisfaction과 운영 readout의 관계
- maintenance cost와 energy / effort / debt / responsibility의 계정 분리

### Bridge — 이번 독해에서 새로 얻은 가설

- Operation과 Structural Maintenance가 비가환적일 때 격리·분할·지연 압력이 생길 수 있다.
- 전역 수면은 maintenance primitive 자체보다 여러 국소 전이를 묶는 coordination envelope일 수 있다.
- 자아 연속성은 모든 내용을 계속 켜 두는 것보다 handoff 뒤 Self를 다시 materialize할 수 있는 능력일 수 있다.
- 의식적으로 선택하지 않은 plasticity도 다음 Ghost를 바꿀 수 있으므로 internal change와 authorship을 분리해야 한다.
- DreamGhost는 altered coupling 아래의 임시 일인칭 assembly일 수 있지만 waking Ghost와 동일한 승인·기억·행동 권한을 자동 갖지 않는다.
- 꿈의 가장 안정적인 현재형은 `causally possible, non-authoritative`다.
- No-Free-Forgetting은 memory decay 금지가 아니라 내부 망각으로 외부 역사를 소급 삭제하지 못한다는 규칙으로 좁혀야 한다.

### Open — 다음 장과 후속 모델에서 확인할 질문

1. `NEWQUAL22`의 `ΦΩ`는 지속 가능한 substrate인가, 순간 metric인가?
2. `ΦΩ` update law와 source provenance가 정의되는가?
3. DreamSim·thought·experience가 남기는 persistence-capable PlasticTrace가 실제로 등장하는가?
4. Readdr가 content·address·interpretation 가운데 무엇을 바꾸는가?
5. sleep-to-waking Ghost handoff의 최소 상태는 무엇인가?
6. current Ghost가 선택하지 않은 internal update를 다음 Ghost는 어떻게 자기 것으로 인수하는가?
7. maintenance demand를 scalar가 아닌 typed vector로 만들 수 있는가?
8. 어떤 비가환성·resource conflict가 local maintenance를 넘어 global coordination을 요구하는가?
9. biological memory loss와 external evidence loss는 어떤 독립 provenance를 갖는가?
10. felt satisfaction과 maintenance feasibility를 어떤 readout으로 연결할 수 있는가?
11. life-event 계열은 maintenance를 생명 경계·번식·집단·환경으로 어떻게 확장하는가?
12. 현행 TAD core는 sleep biology를 수입하지 않고도 non-authoritative internal plasticity를 수용할 수 있는가?

---

## A12. 다음 장 경계 — metric은 매질인가

Chapter 10의 종점은 다음이다.

```text
SLEEP22
gave maintenance scheduling
+ non-authority of dream / forgetting
+ operational backlog separated from debt

but did not give
durable internal substrate
+ plasticity update law
+ source provenance
+ sleep-to-self handoff
```

`REG23`은 `bg/radr/drms` 같은 이름을 registry에 남겼지만 `Forget` root는 없고, 후기 monograph 최소 registry에서는 이들 root도 다시 빠진다. 이름의 일시적 생존은 기능의 완성도 영구 승계도 아니다.

다음 장은 `NEWQUAL22`의 `ΦΩ`를 직접 읽어야 한다.

> `ΦΩ`는 가까움·막힘·탄성·접근 비용을 나타내는 metric인가.  
> 아니면 경험과 생각으로 변형되고 다음 상태에 지속되는 medium인가.

이 둘을 같은 단어 `매질`로 묶으면 Chapter 10의 오류가 반복된다.

```text
Metric
≠ Substrate
≠ Current Morph
≠ Plastic Trace
≠ Update Operator
```

Chapter 10은 다음 `[BRIDGE-CURRENT]` 문장에서 멈춘다.

> **생명에게 필요한 것은 잠이라는 이름의 단일 작업이 아니라,  
> 운영 연속성을 잃지 않으며 자기 형성 능력을 보존·수리·재조정할 maintenance capacity와 typed update/coordination 경로다.  
> 수면은 그 능력들을 묶는 강력한 생물학적 coordination regime이지만, 이론의 메인 축은 특정 구현보다 먼저 살아 있어야 한다.**

---

## 부록 A. 내부 출처 별칭

| 별칭 | 경로 | 행수 | 사용 지위 |
|---|---|---:|---|
| `ORIGIN02` | `연구/참조용 임시/0101 물리의논통합본 5.txt` | 1,223 | Dream/Monologue Gap cooling 전사 |
| `A41` | `연구/AXIOM37/0104 axiom41 3.txt` | 3,438 | Dream/Delusion·Metabolic Decay 전사 |
| `EOE09` | `연구/AXIOM37/0105  eoe .txt` | 539 | 미청산 EOE의 야간 정산 전사 |
| `GEE10` | `연구/AXIOM37/0105 GEE 1.txt` | 289 | anneal + consolidate 비유 전사 |
| `GHOST08` | `연구/AXIOM37/0107 이론합본` | 2,746 | Ghost/Editor/Will 전사 |
| `ISG09` | `연구/AXIOM37/0109 new물리통합3 .txt` | 1,280 | 상상/꿈 ISG regime 전사 |
| `ACCESS20` | `연구/fucstrees/0120 정의정리공리귀결 이후패치.txt` | 732 | Recall/Forget/Readdress의 직접 선행층 |
| `RTO21` | `연구/fucstrees/0121 runtime seed` | 510 | `B_t` Access bandwidth와 `Θ_t` criticality threshold 선행 의미 |
| `SAT22` | `연구/fucstrees/0121 만족.txt` | 207 | Safe-Stopping·Continuity Tax 인접 지층 |
| `SLEEP22` | `연구/fucstrees/0121 수면.txt` | 407 | 이 장의 주자료; 세 append block |
| `SSQ-REC` | `pluss/만족수면퀄리아통합.txt` | 1,180 | 2026-07-13 제공 복구본; 내용 계보 witness, 1월 독립 원본 여부 미식별 |
| `REG23` | `연구/Overqorld/0121 reg.txt` | 469 | 후기 lexical registry; 기원 근거 제외 |
| `NEWQUAL22` | `연구/fucstrees/0122 newqual.txt` | 245 | 다음 장 전방 경계; ΦΩ metric/impedance |
| `CORE26` | `연구/Overqorld/coreannex.txt` | 822 | downstream 재압축; 계정 재혼합과 yield-repair 변형 |
| `MONO15` | `downloads/monograph_edition_0_1_5_humanstack_v3_2_atlas_ats_v0_1.md` | 5,726 | 2026-02-15 내부 표제의 downstream monograph; 다운로드 mtime은 작성일 근거 제외 |
| `LIFE23` | `연구/Overqorld/0122 lifeevent axiom1.txt` | 214 | life-event 가지의 rest/sleep–recording-pressure 재결합 |
| `MINI27` | `연구/Overqorld/minipatch.txt` | 245 | downstream geometry-repair·creativity patch |
| `SYNTH27` | `연구/Overqorld/0127 maybe통합1` | 444 | 날짜 불확정 통합 witness; 잔차 분리와 Sleep Necessity 동시 보존 |

### A.1 provenance recovery with an identity limit — `만족수면퀄리아통합`

후속 제공된 `pluss.zip`에는 `만족수면퀄리아통합`이라는 이름을 가진 1,180행의 별도 ZIP entry가 있다. 파일 SHA-256은 `15fb834c87eda1ae3240a59fb3f73a3354a204f52b222a9e03039b02995c6115`다. 내용 대조에서 `SSQ-REC:L1–206`은 `SAT22:L1–206`과 byte-for-byte 동일하고, `SSQ-REC:L209–615`는 `SLEEP22` 407행 전체와 byte-for-byte 동일하다. `SSQ-REC:L620–873`은 `NEWQUAL22`의 정확한 사본은 아니지만 `ΞM` 표기와 추가 봉인을 사용해 재작성·확장한 강한 textual derivative다. `SYNTH27:L1`이 같은 이름을 세 입력 문서 중 하나로 직접 열거하고 `MINI27:L142, L241`도 동명 자료를 통합·삽입 대상으로 지목하므로 해당 자료 계열의 내용 계보를 강하게 지지한다.

그러나 ZIP entry 시각 `2026-07-13 21:19:14`는 archive 저장 metadata일 뿐 실제 작성시각을 증명하지 않는다. 현재 자료만으로 `SSQ-REC`이 1월 당시 보존된 독립 원본인지, 같은 자료를 사용한 후대 재구성본인지 구별할 수 없다. 따라서 이 장은 `SSQ-REC`을 **내용 계보에 부합하는 복구본**으로 사용하되 0121–0122의 동시대 정본으로 소급하지 않는다. 직접 역사 판정은 계속 `SAT22`, `SLEEP22`, `NEWQUAL22`의 당시 보존본에 우선 결박하며, 복구본은 누락됐던 후기 합성의 내용과 downstream 연결을 복원하는 witness로 한정한다.

이 복구는 persistence law, durable qualia substrate, memory archive 또는 Ghost handoff가 이미 해결됐다는 근거가 아니다. 상세 identity·구성 비교와 권위 경계는 [`Source-Recovery Record`](../research/adoption-records/2026-07-13-recovered-satisfaction-sleep-qualia-provenance.md)에 고정한다.

---

## 부록 B. 외부 1차 연구 별칭

| 별칭 | 연구 | 이 장에서의 사용·한계 |
|---|---|---|
| `EXT-ENERGY11` | [Jung et al., *Energy expenditure during sleep, sleep deprivation and sleep following sleep deprivation in adult humans* (2011)](https://doi.org/10.1113/jphysiol.2010.197517) | 인간 acute energy expenditure; 소표본 |
| `EXT-MUSCLE21` | [Lamon et al., *The effect of acute sleep deprivation on skeletal muscle protein synthesis and the hormonal environment* (2021)](https://doi.org/10.14814/phy2.14660) | 인간 단백질합성 대리지표; 1박·소표본 |
| `EXT-IMMUNE03` | [Lange et al., *Sleep enhances the human antibody response to hepatitis A vaccination* (2003)](https://doi.org/10.1097/01.PSY.0000091382.61178.F1) | 인간 백신 반응; 단일 항원·소표본 |
| `EXT-LOCAL11` | [Vyazovskiy et al., *Local sleep in awake rats* (2011)](https://www.nature.com/articles/nature10009) | 행동상 각성 중 국소 off period와 수행 저하 |
| `EXT-FLIGHT16` | [Rattenborg et al., *Evidence that birds sleep in mid-flight* (2016)](https://www.nature.com/articles/ncomms12468) | 단·양반구 비행 수면; 종·생태 조건 한정 |
| `EXT-WAKE26` | [Driessen et al., *Induction of cortical on/off periods in awake mice fulfills sleep functions* (2026)](https://doi.org/10.1038/s41593-026-02318-9) | 생쥐 피질의 별도 생리·분자/단일 기억과제 실험; 전신 수면 대체 아님 |
| `EXT-REPLAY94` | [Wilson & McNaughton, *Reactivation of hippocampal ensemble memories during sleep* (1994)](https://doi.org/10.1126/science.8036517) | 쥐 해마 ensemble 재활성화 관찰; 기능 인과 자체는 미검증 |
| `EXT-REPLAY07` | [Ji & Wilson, *Coordinated memory replay in the visual cortex and hippocampus during sleep* (2007)](https://doi.org/10.1038/nn1825) | 쥐 시각피질–해마의 조정된 replay; 꿈 내용과 동일시 금지 |
| `EXT-SWR09` | [Girardeau et al., *Selective suppression of hippocampal ripples impairs spatial memory* (2009)](https://doi.org/10.1038/nn.2384) | 쥐 ripple 억제와 공간기억 손상; ripple 전체 기능 일반화 금지 |
| `EXT-COUPLE16` | [Maingret et al., *Hippocampo-cortical coupling mediates memory consolidation during sleep* (2016)](https://doi.org/10.1038/nn.4304) | 쥐 ripple-triggered cortical stimulation과 ripple–delta–spindle 결합; 특정 기억·회로에 한정 |
| `EXT-MEM06` | [Marshall et al., *Boosting slow oscillations during sleep potentiates memory* (2006)](https://www.nature.com/articles/nature05278) | 인간 NREM 느린 진동 조작과 선언기억 |
| `EXT-TMR07` | [Rasch et al., *Odor cues during slow-wave sleep prompt declarative memory consolidation* (2007)](https://doi.org/10.1126/science.1138581) | 인간 targeted reactivation; cue·과제 한정 |
| `EXT-SYN17` | [de Vivo et al., *Ultrastructural evidence for synaptic scaling across the wake/sleep cycle* (2017)](https://doi.org/10.1126/science.aah5982) | 생쥐 피질 구조; 횡단·선택 영역 |
| `EXT-HOMER17` | [Diering et al., *Homer1a drives homeostatic scaling-down of excitatory synapses during sleep* (2017)](https://doi.org/10.1126/science.aai8355) | 생쥐 분자 기전; 인간 전역 일반화 금지 |
| `EXT-SPINE14` | [Yang et al., *Sleep promotes branch-specific formation of dendritic spines after learning* (2014)](https://doi.org/10.1126/science.1249098) | 생쥐 운동학습 뒤 국소 spine 형성 |
| `EXT-REMPLAST17` | [Li et al., *REM sleep selectively prunes and maintains new synapses in development and learning* (2017)](https://doi.org/10.1038/nn.4479) | 생쥐 REM·발달/학습 회로의 선택적 remodeling |
| `EXT-DNA19` | [Zada et al., *Sleep increases chromosome dynamics to enable reduction of accumulating DNA damage in single neurons* (2019)](https://doi.org/10.1038/s41467-019-08806-w) | 6–7 dpf 제브라피시 유생 단일 뉴런 nuclear endpoint |
| `EXT-ROS20` | [Vaccaro et al., *Sleep Loss Can Cause Death through Accumulation of Reactive Oxygen Species in the Gut* (2020)](https://doi.org/10.1016/j.cell.2020.04.049) | 초파리 생존 구제 중심; 모든 수면 기능 대체 아님 |
| `EXT-GLY13` | [Xie et al., *Sleep Drives Metabolite Clearance from the Adult Brain* (2013)](https://doi.org/10.1126/science.1241224) | 생쥐 tracer·마취 포함; glymphatic 지지 |
| `EXT-CSF19` | [Fultz et al., *Coupled electrophysiological, hemodynamic, and cerebrospinal fluid oscillations in human sleep* (2019)](https://doi.org/10.1126/science.aax5440) | 인간 신호 coupling; net solute clearance 미측정 |
| `EXT-CLEAR24` | [Miao et al., *Brain clearance is reduced during sleep and anesthesia* (2024)](https://www.nature.com/articles/s41593-024-01638-y) | 수컷 생쥐·특정 tracer/측정; 기존 결과와 충돌 |
| `EXT-GLY25` | [Hauglund et al., *Norepinephrine-mediated slow vasomotion drives glymphatic clearance during sleep* (2025)](https://doi.org/10.1016/j.cell.2024.11.027) | 생쥐 NREM inflow mechanism; inflow와 net clearance 분리 |
| `EXT-DREAM17` | [Siclari et al., *The neural correlates of dreaming* (2017)](https://www.nature.com/articles/nn.4545) | REM/NREM dream report correlate; 기능 실험 아님 |
| `EXT-DREAM10` | [Wamsley et al., *Dreaming of a learning task is associated with enhanced sleep-dependent memory consolidation* (2010)](https://doi.org/10.1016/j.cub.2010.03.027) | 명시적 과제 관련 꿈 n=4; 상관이며 인과 미분리 |
| `EXT-INSIGHT04` | [Wagner et al., *Sleep inspires insight* (2004)](https://doi.org/10.1038/nature02223) | 수면 뒤 hidden-rule 통찰; 꿈 내용 미조작 |
| `EXT-CREAT09` | [Cai et al., *REM, not incubation, improves creativity by priming associative networks* (2009)](https://doi.org/10.1073/pnas.0900271106) | 제한 과제·stage effect; 꿈 기능 직접 증거 아님 |
| `EXT-JELLY17` | [Nath et al., *The Jellyfish Cassiopea Exhibits a Sleep-like State* (2017)](https://doi.org/10.1016/j.cub.2017.08.014) | 중앙집중식 뇌 없는 동물의 행동적 sleep-like state |
| `EXT-FORGET19` | [Izawa et al., *REM sleep–active MCH neurons are involved in forgetting hippocampus-dependent memories* (2019)](https://doi.org/10.1126/science.aax9238) | 생쥐 특정 회로·과제의 active forgetting |

외부 논문 제목과 DOI 또는 영구 링크는 출처 식별을 위해 기록했다. 표의 한계 문장이 각 논문의 모든 설계·통계·논쟁을 대체하지 않는다.

---

## 부록 C. SLEEP22 논증 강도 감사

| 단계 | 원문 형식 | 실제로 허용되는 결론 | 과잉이 발생하는 지점 |
|---:|---|---|---|
| 1 | 외생 입력 `λ_in`이 존재 | 인간 runtime은 완전 폐쇄계가 아님 | 없음 |
| 2 | Working Set·처리율이 유한 | 동시 처리와 service에는 한계가 있음 | 단일 처리율의 단위는 미정 |
| 3 | 어떤 구간 `λ_in > μ_proc` 가능 | 해당 모델에서 backlog 증가 가능 | `가능`을 `필연` 제목으로 강화 |
| 4 | backlog가 장기 불안정 가능 | boundedness를 위한 조정이 필요할 수 있음 | 다른 조정 architecture 미배제 |
| 5 | input gating + resource reallocation | maintenance epoch는 가능한 해법 | 이를 biological sleep과 동일시 |
| 6 | sleep can lower B | 적절한 rate 조건에서 감소 가능 | 전체 평균 안정성·sufficiency 미정 |
| 7 | dream may test candidates | non-authoritative internal simulation 가설 | 실제 꿈 기능·replay·plasticity로 일반화 |
| 8 | spine compression | 한 문장 architecture 제시 | 상세 제한을 지우고 인간 일반의 필연으로 승격 |

### C.1 최소 교정식

`SLEEP22`의 queue 직관을 유지하려면 적어도 각 작업 종류 `i`에 대해 다음과 같은 분리가 필요하다.

```text
b_i(t+1)
= max(0, b_i(t) + admitted_load_i(t) - service_i(t))
```

여기서도 `b_i`가 실제 생물학 stock이라는 뜻은 아니다. 필요한 것은 다음을 명시하는 일이다.

- 각 `i`의 단위와 관측 방식
- wake·quiet rest·NREM·REM에서의 service 차이
- local/parallel service 가능성
- priority·deadline·discard rule
- service 사이의 resource conflict
- 전체 cycle의 boundedness 조건

이 조건 없이 `B_t` 하나를 인간 전체의 대사 잔차라고 부르는 것은 설명적 압축이지 완성된 정리다.

---

## 부록 D. 최종 소급 금지

```text
SLEEP22 did not discover a universal biological purpose of sleep.
SLEEP22 did not prove that all maintenance requires global sleep.
SLEEP22 did not identify neural replay with dream content.
SLEEP22 did not define a persistent QualiaMedium.

external sleep research does not validate TAD authority rules.
local sleep does not prove global sleep is useless.
wake-induced on/off periods do not replace all sleep functions.
sleep-linked memory change does not make dreams evidence.

DB maintenance is an explanatory analogy, not human ontology.
Self materialization is a Bridge, not a direct SLEEP22 claim.
Operation–Maintenance Noncommutativity is conditional, not universal.

maintenance can influence the next self
without rewriting the past
and without granting itself authority.
```
