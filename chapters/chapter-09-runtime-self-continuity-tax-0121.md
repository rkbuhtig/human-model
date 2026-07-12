# Chapter 09 — 나를 계속 켜 두는 비용

## Persona runtime·Cross-Clock Selfness·내부 위원회·Continuity Tax: 내용이 달라도 같은 ‘나’를 추적하려 한 지층

> **상태:** 역사 복원 + 연구 후기 v1.0  
> **주범위:** 2026-01-21 `RUNTIME / SEED / CROSS-CLOCK LOCK`, `UNIFIED THEORY CANON v0.6-UCXQ`와 2026-01-22 `OBJCOMMIT`, `SAT / CONT / TRK / DREAD` addendum  
> **역사 전사:** 2026-01-13 `Qualia Surface & Meta Handle Canon`  
> **직전 장:** Chapter 08 — 저장된 과거는 아직 ‘나’가 아니다  
> **전방 경계:** `MET / SLEEP / GC`, `SPINE-OSAB`, 후기 registry와 0122 Qualia-medium 계열은 다음 장으로 보류

---

## 들어가며 — 같은 내용이 없어도 같은 나일 수 있는가

Chapter 08은 저장된 과거와 현재 활성된 과거를 갈랐다.

```text
Archive / Graph
≠ Address
≠ Access
≠ Rehydration
≠ Self-adoption
```

그 분리는 곧 더 어려운 질문을 만든다.

현재 Working Set은 유한하고, 열리는 기억과 장면은 매 순간 달라진다. 몸의 리듬과 피로가 바뀌면 같은 단서도 다른 이웃을 열고, 방금 전의 나와 지금의 나는 같은 내용을 동시에 쥐고 있지 않다. 그렇다면 무엇이 이 불연속적인 단면들을 계속 하나의 `나`라고 부르게 하는가.

0121의 첫 대답은 놀랄 만큼 비내용적이다.

```text
Persona
≠ 기억 내용
≠ 성격 서술
≠ 한 장치

Persona
= 지속 계약 / runtime handle
= 갱신되는 runtime object
= Cross-Clock Lock 위의 SelfOn readout
= Access 선택 정책의 fixed point
```

하지만 이 네 줄은 한 정의의 점진적 정교화가 아니다. 같은 날의 서로 다른 지층이 `Persona`, `Selfness`, `Identity`에 각기 다른 역할을 맡긴 결과다. 이어지는 만족 addendum는 다시 `나`를 이전 단면과 현재 단면을 최소 변경으로 잇는 가역적 tracking hypothesis로 바꾼다.

```text
현재 단면은 점프할 수 있다.
연속감은 후처리다.
후처리에는 Continuity Tax가 든다.
```

이로써 이론은 고정된 내용이나 영혼 같은 실체 없이도 자기 연속성을 말할 운영 어휘를 얻었다. 동시에 중요한 것이 빠졌다. 2026-01-13의 Qualia 문서는 생각·상·의미 덩어리, 당김, 제약 압력, 막힘을 하나의 느껴지는 표면으로 만들었지만 그 표면을 끝까지 `view-only readout`으로 봉인했다. 0121 통합본은 그 세부마저 `이미지/퀄리아/서사/가설의 투영`이라는 한 줄로 압축한다.

따라서 이번 장의 중심 명제는 이것이다.

> **0121은 ‘같은 내용을 가진 나’를 포기하고, 불연속적인 현재를 계속 추적·편성하는 운영 구조로서의 나를 얻었다.  
> 그러나 그 현재가 세계를 어떤 살아 있는 형상으로 느끼고, 그 경험이 내부를 어떻게 변형하는지는 표면 아래에 비워두었다.**

이 장은 그 공백을 현행 `QualiaMedium`이 원래부터 채우고 있었다고 소급하지 않는다. 먼저 당시의 직접 구조와 충돌을 복원하고, 연구 후기에서만 현재 Bridge를 붙인다.

---

# 역사 본문 — 내용 대신 계약·잠금·추적으로 자아를 만들다

## 0. 범위·판본·독해 규율

### 0.1 1차 자료와 실제 시간 경계

파일명 `0121`은 달력 날짜와 완전히 일치하는 단일 판본명이 아니다. 이 장의 자료는 내부 날짜, 파일 보존 시각, 문서 의존성을 함께 보아 다음처럼 나눈다.

| 층 | 별칭 | 문서 | 행수 | 보존·내부 시각 | 이 장에서의 지위 |
|---:|---|---|---:|---|---|
| 0 | `QUAL13` | `PARADIM/qualia.txt` | 483 | 내부 작성일 2026-01-13; mtime 01-14 18:24:30 `-06:00` | 0121보다 이른 Qualia 전사 |
| 1 | `RTO21` | `fucstrees/0121 runtime seed` | 510 | mtime 01-21 11:21:48 `-06:00` | Persona·Seed·Cross-Clock Lock 주자료 |
| 2 | `UCXQ21` | `fucstrees/0121 이론 1.txt` | 1,589 | mtime 01-21 22:31:54 `-06:00` | 같은 날 저녁 확대 통합본 |
| 3 | `OBJ22` | `fucstrees/0121 객체와 만족 1` | 85 | mtime 01-22 01:11:28 `-06:00` | 내부 proposal committee 곁가지 |
| 4 | `SAT22` | `fucstrees/0121 만족.txt` | 207 | mtime 01-22 11:13:18 `-06:00` | Continuity Tax·Tracker·Safe-Stopping 후속 |
| → | `SLEEP22` | `fucstrees/0121 수면.txt` | 407 | mtime 01-22 11:12:04 `-06:00` | 다음 장 전방 경계 |
| → | `REG23` | `Overqorld/0121 reg.txt` | 469 | mtime 01-23 21:59:18 `-06:00` | 후기 lexical registry; 개념 기원 근거에서 제외 |

mtime은 현재 corpus가 보존한 상대 순서다. 절대 작성 시각이나 개념의 최초 발명 시각을 단독으로 증명하지 않는다.

`SLEEP22`의 mtime은 `SAT22`보다 74초 빠르지만, 내용은 `SAT 패치`와의 결합을 직접 전제하고 `τ_cont`, `Θ`, safe-stopping을 사용한다 `[SLEEP22:L267–275]`. 따라서 내용 의존상 **SAT 본문의 이 개념들은 SLEEP22보다 먼저 존재했다**. 다만 `[SAT22:L190–202]`의 correction directive까지 SLEEP보다 앞섰는지는 알 수 없으므로 whole-file 순서를 `SAT22 → SLEEP22`로 확정하지 않는다.

### 0.2 QUAL13은 0121 당일 문서가 아니다

`QUAL13`은 제목에서 consolidated re-issue라고 밝히고 내부 작성일을 2026-01-13으로 둔다 `[QUAL13:L3–9]`. 이 장은 그것을 0121의 한 append block으로 취급하지 않는다.

다만 0121에서 `Π_view`와 `Φ`가 무엇을 잃고 무엇을 보존했는지 판단하려면 이 전사가 필요하다. 따라서 다음처럼 사용한다.

```text
QUAL13
= historical antecedent / backward lineage source
≠ 0121 event
≠ current QualiaMedium theory
```

### 0.3 RTO21은 네 지층이 한 파일에 붙은 vessel이다

`RTO21`은 하나의 clean addendum가 아니다.

```text
A  L4–128    Persona as Runtime Handle / 첫 Cross-Clock Lock
B  L134–274  Persona as Runtime Object / SelfOn 재작성
C  L289–458  UC+Q+GRAPH Draft Canon Sheet
D  L460–510  대화 기반 BIO Draft
```

A와 B는 중복 사본이 아니다. A가 Persona를 지속 계약과 handle로 정의한다면, B는 상태와 업데이트 규칙을 가진 runtime object로 바꾼다. D는 스스로 `(Draft)`와 `대화 기반`이라고 표시하므로 앞선 공리들과 동등한 clean canon으로 올리지 않는다 `[RTO21:L460–463]`.

### 0.4 UCXQ21도 한 번에 닫힌 정본이 아니다

`UCXQ21`은 세 덩어리로 나뉜다.

```text
A  L4–482      Operational Semantics + Definitions
B  L484–1187   대화형 continuation + Axioms/Theorems/Corollaries
C  L1191–1589  END 뒤 Symbol Registry·proof skeleton·attack catalog·traces
```

L484에는 `좋아. 이어서`라는 대화 잔여가 직접 남아 있고, 문서는 L1177에서 한 번 `END`를 선언한 뒤 다시 기술 부록을 append한다 `[UCXQ21:L484–485]` `[UCXQ21:L1177–1191]`. 제목의 `CANON`, `Integrated`, `Sealed`는 당시 문서의 자기 명명이지 현재 저장소의 canonical 승인 상태가 아니다.

### 0.5 OBJ22와 SAT22의 지위

`OBJ22`는 다수의 내부 객체가 proposal을 내고 하나의 `call`로 집계되는 Norm 내부 구현을 제안한다. 깨끗한 단일 addendum지만 Qualia나 정체성의 완성 정의는 아니다.

`SAT22`는 본문 뒤에 correction directive를 append한다.

```text
L4–186    SAT / CONT / TRK / DREAD 본문
L190–202  u_t 결정성, Φ의 역할, 연속 decoder, bill estimate 교정 지시
```

뒤 지시는 앞 정의를 자동 삭제하지 않지만, 직접 겨냥한 부분에서는 기능 교정으로 읽는다.

### 0.6 판정 표지

| 표지 | 뜻 |
|---|---|
| `[DIRECT]` | 원문이 직접 선언 |
| `[REWRITE]` | 앞 정의를 다른 역할·형식으로 다시 씀 |
| `[FUNCTIONAL CORRECTION]` | 뒤 지층이 앞의 누수·과잉을 실제로 좁힘 |
| `[REAL CONFLICT]` | 한 타입의 안정 정의로 동시에 유지하기 어려움 |
| `[ROLE DRIFT]` | 같은 이름이 output·state·policy 등 다른 역할로 이동 |
| `[TYPE GAP]` | 전이·저장·handoff 타입이 정의되지 않음 |
| `[OVER-CLOSURE]` | 보호 규칙이 합법적인 영향 경로까지 막을 위험 |
| `[OVERGENERALIZATION]` | 채택한 국소 모델을 인간 일반의 필연으로 확대 |
| `[MODEL ASSUMPTION]` | 증명 결과가 아니라 설계 가정 |
| `[RESIDUE]` | 중간에 등장했으나 통합본에서 기능이 빠지거나 미봉합 |
| `[CURRENT LENS]` | 현행 이론으로 비춘 비교이며 당시 정의가 아님 |
| `[BRIDGE]` | 이번 독해에서 새로 만든 연결 |
| `[OPEN]` | 후속 지층·반례에서 확인할 질문 |

### 0.7 핵심 소급 금지

```text
Q_t / Φ_t in QUAL13 ≠ current QualiaMedium
dynamic re-rendering ≠ durable plastic medium

Persona handle ≠ Persona runtime state
Persona runtime object ≠ Persona policy fixed point
SelfOn readout ≠ numerical identity
Cross-Clock Lock ≠ proven consciousness condition

internal committee ≠ multiple persons
α_t “reality-right” ≠ external authority
tracking hypothesis Θ_t ≠ autobiographical authorship
discontinuous active slice ≠ DID diagnosis

Continuity Tax ≠ normative debt
Safe-Stopping ≠ felt satisfaction
body modulation ≠ excuse / authority token
```

---

## 1. QUAL13 — 퀄리아를 신비가 아니라 안전한 표면으로 봉인하다

### 1.1 퀄리아는 상태가 아니라 view-only readout이다

`QUAL13`의 목적은 명확하다. Φ·Meta·Why-token을 신비나 주권이 아니라 이미 존재하는 지각 신호에서 계산되는 표면으로 닫고, 물리 상태·원장·Quench로 새는 마법 경로를 막는다 `[QUAL13:L23–28]`.

세 봉인은 더 직접적이다.

1. Φ는 SSOT 상태가 아니라 `view`의 산출물이다.
2. Φ·Meta·Why-token은 기존 신호에서 계산되는 결정론적 함수다.
3. 그 산출은 `Π_phys`, Spend, feasibility, Quench·Commit에 직접 들어갈 수 없다 `[QUAL13:L32–36]`.

```text
felt surface
≠ stored authority state
≠ evidence
≠ physical command
≠ commit trigger
```

여기서 퀄리아는 세계에 힘을 행사하는 별도 물질이 아니라, 지각계가 이미 만든 당김과 막힘을 한 번 더 읽게 하는 안전한 인터페이스다.

### 1.2 Q·Z·당김·제약 압력

현재상 `Z_t`만으로는 Φ 전체가 되지 않는다. 문서는 다음을 분리한다.

```text
Q_t  = 생각·상·이미지·의미를 포함하는 지각 덩어리
Z_t  = 현재 렌더
g_t  = 어느 방향으로 당기는가
p_t  = 당김의 총량
Λ_t  = 어느 제약이 빡빡한가
λ_t  = 제약이 실제로 잘라낸 총량
ξ_t  = 불일치
```

`Q_t`는 시각과 언어를 포함한 `생각/상(이미지/의미 덩어리)`로 직접 해석된다 `[QUAL13:L64–69]`. `Z_t`는 과거와 미래 사이에 렌더된 현재이고, Φ는 거기에 당김·장력·막힘의 촉감까지 더한 표면이다 `[QUAL13:L109–124]`.

따라서 이 시기의 Φ는 단순한 화면보다 넓다. 무엇이 보이는지뿐 아니라 무엇을 향하고, 어디서 잘리고, 왜 움직이지 못하는지가 함께 느껴지는 표면이다.

### 1.3 표면은 다음 tick을 바꾸지만 직접 쓰지는 못한다

Φ의 영향은 완전히 0이 아니다. 허용된 길은 하나다.

```text
current Φ
→ view re-expression
→ next-tick input / candidate change
→ next Φ
```

문서는 Φ의 영향이 `view 재표현 → 다음 tick 입력/후보 변화`로만 나타난다고 봉인한다 `[QUAL13:L117–125]`. 이성 역시 `Q_t`와 표상을 재배치·분해·재구성하여 다음 tick의 후보와 Φ를 유도할 뿐, 비용·제약·원장을 직접 바꾸지 못한다 `[QUAL13:L179–183]`.

이 점은 중요하다.

```text
Φ is dynamically re-rendered
≠ Φ is a durable mutable storage medium
```

형상은 매 tick 달라질 수 있지만, 그 변형이 어디에 얼마나 오래 남는지는 정의되지 않는다.

### 1.4 MetaFire와 Why-token — 막힘이 언어 손잡이로 떠오르다

Meta는 당김·절단·제약 압력·불일치를 다시 읽는 2차 readout이다 `[QUAL13:L128–140]`. 당김과 절단이 함께 크고 진전이 plateau에 걸리면 `MetaFire`가 성립한다.

```text
MetaFire_t ⇔ (p_t · λ_t ≥ Θ_meta) ∧ Plateau_t
```

그러나 MetaFire는 EventFire도, clock도, Quench trigger도 아니다. 이때 view에 생길 수 있는 최소 산출은 `Why-token`이다 `[QUAL13:L151–157]`.

Why-token도 설명이나 근거가 아니다. 그것은 view-only debug handle이며, 표현을 다시 매개해 진전 측정·후보 순서·불일치 구조를 바꿀 수 있을 뿐이다 `[QUAL13:L161–175]`.

```text
felt friction
→ Why-token
→ re-parameterization / candidate reordering

Why-token
≠ truth
≠ SSOT write
≠ language as a whole
```

### 1.5 변형의 필요량과 허용량

`QUAL13` 안에서 변형 한계를 직접 수식화한 항은 `FlexCost / Overstretch / Frustration`이다. 이는 현행 가소성 모델과의 `[CURRENT LENS]` 기능적 유비이지 `QualiaMedium`으로의 직접 계보는 아니다.

```text
Δθ_need = 모순을 피하고 불일치를 줄이는 데 필요한 변형
Δθ_max  = 현재 예산이 허용하는 최대 변형

Overstretch ⇔ ||Δθ_need|| > Δθ_max
Frustration ⇔ Overstretch ∧ Plateau
```

원문은 필요한 변형과 허용되는 변형의 차이를 직접 모델링한다 `[QUAL13:L220–233]`. 다만 변형 대상은 지속 매질이 아니라 lens·표상의 현재 조작량이다. 좌절도 원장을 바꿀 면허가 아니라 view/JOT 조작과 휴식 대기의 신호다.

앞의 `RoughFit / Consistency`도 같은 범위를 잠근다. 형상이 목표와 덜 비슷한 것은 틀릴 수 있는 후보로 남을 수 있지만, `K=false`인 모순은 우선 붕괴·재조합된다 `[QUAL13:L187–216]`. `틀림 허용`은 후보 유지 정책이지 비용·제약·원장을 바꿀 권한이 아니다 `[QUAL13:L237–242]`.

### 1.6 이 지층이 얻고 잃은 것

`QUAL13`은 퀄리아를 다음처럼 안전하게 만들었다.

```text
private vividness
without private authority

felt direction and blockage
without direct physical or ledger command
```

그러나 안전 장치가 강한 만큼 다음은 집을 얻지 못했다.

- 경험이 다음 경험 가능성 자체를 바꾸는 persistence-capable plasticity
- 언어 이전 동물 감각의 명시적 범위
- 생각 자체가 경험으로 축적되는 내부 trace
- 같은 단어와 다른 사적 형상 사이의 translation
- 퀄리아와 기억 저장 구조 사이의 handoff

이 항목들은 `QUAL13`이 명시한 목적 밖에 남는다. 문서가 직접 수행한 임무는 퀄리아의 생물학적 기원 설명이 아니라, 퀄리아가 사실·권한을 자체 발행하지 못하도록 readout 경로를 봉인하는 것이었다.

---

## 2. Persona as Runtime Handle — 동일성을 내용에서 계약으로 옮기다

### 2.1 기억 텍스트가 아니라 지속 핸들

`RTO21`의 첫 지층은 질문을 직접 바꾼다.

> ‘나(페르소나)’는 서사나 기억 텍스트의 내용이 아니라, 불변 계약과 갱신 규칙을 지키는 지속 핸들이다 `[RTO21:L16–23]`. `[DIRECT]`

그 계약은 네 조항으로 구성된다.

1. `Π_view`는 주소권이지 근거권이 아니다.
2. Access는 무비용 read가 아니라 사건이다.
3. 선명함은 근거가 아니고 비용은 귀속 토큰이 아니다.
4. 귀속·규칙·사회적 결합 변화는 Witness 경로로만 생긴다 `[RTO21:L18–23]`.

Chapter 08에서 현재의 나는 Archive 전체일 수 없었다. 여기서는 그 부정이 적극적인 정체성 정의로 바뀐다.

```text
같은 기억 내용
이 아니라
같은 접근·근거·귀속 계약
```

`TR1`은 기억과 서사 내용이 달라져도 계약과 갱신 규칙이 보존되면 핸들이 지속된다고 주장한다. 그래서 “나는 같은데 내가 낯설다”를 핸들은 유지되지만 runtime state가 달라진 상태로 설명한다 `[RTO21:L84–87]`. `[DIRECT] [REWRITE]`

다만 계약의 동일성이 곧 개체의 수적 동일성을 증명하지는 않는다. 같은 계약을 구현한 두 instance를 어떻게 가를지, 실제 handoff가 언제 성공했는지, 핸들의 생성·분기·종료 사건은 무엇인지 아직 없다.

### 2.2 Seed와 몸은 권한이 아니라 변조항이다

같은 지층은 몸·기질·느린 리듬을 자아 밖으로 밀어내지 않는다. Seed는 다음을 편향시킨다.

- Access 대역 예산
- 승격 압력 임계
- AddrSig·OpenEase·AfterCost
- 정책 `π`의 비용 반응성

하지만 Seed는 Witness 권한이 아니고 과거 귀속을 소급 수정할 수 없다 `[RTO21:L25–33]`.

심장·호흡·자율신경의 저주파 진동자 `t_b`도 근거가 아니라 Access 대역·포화·비용 체감·승격 임계를 연속적으로 흔드는 변조항이다 `[RTO21:L35–38]`.

```text
body changes what becomes easy, urgent, costly, or vivid
≠ body changes what counts as evidence
≠ body rewrites past attribution
```

원문은 비용 항목, ClaimSig·SourceTag, Seed·`t_b`가 모두 실재하거나 유용할 수 있어도 귀속을 옮기는 토큰은 아니라고 재봉인한다 `[RTO21:L40–48]`.

### 2.3 Selfness는 세 시계의 약한 잠금이다

초기 RTO의 가장 큰 새 제안은 일체감을 특정 저장소나 장기에 두지 않는 것이다. `AR5`는 `Selfness readout`, 즉 ‘나-켜짐’을 최소 세 시계가 약하게 잠길 때 나타나는 것으로 정의한다.

```text
t_b  몸의 느린 리듬이 Access를 안정화하거나 추적 가능하게 흔듦
t_e  주소를 따라 재수화와 정책 갱신이 실제로 수행됨
t_c  귀속과 기록이 소급 없이 비가역적으로 남음
```

이 세 조건은 직접 나열된다 `[RTO21:L50–56]`. 잠금 지표는 몸의 변조 안정성, 재수화, 미래 coverage 변화 가능성, 비가역 귀속의 동시 성립 정도이며 정확한 수식은 열어 둔다 `[RTO21:L60–78]`. `[DIRECT] [MODEL ASSUMPTION]`

여기서 ‘나’는 하나의 내용이 아니라 여러 시간 규모 사이의 작동 관계다. 그러나 계약이 보존되는 것과 시계가 잠기는 것은 아직 연결되지 않는다.

```text
IdentityHandle persists
≠ CrossClockLock currently holds
≠ SelfOn is currently felt
```

---

## 3. Runtime Handle에서 Runtime Object로 — ‘나-켜짐’을 상태화하다

### 3.1 두 번째 RTO는 같은 말을 반복하지 않는다

`RTO21`의 두 번째 지층은 페르소나를 시간에 따른 내부 상태와 업데이트 규칙을 가진 runtime object로 다시 정의한다 `[RTO21:L134–150]`. `[REWRITE]`

객체 `𝒫_t`에는 다음이 들어간다.

- 정책 상태 `π_t`
- 단서가 여는 이웃 분포 `AddrSig_t`
- Access 대역 `B_A(t)`
- 승격 압력 임계 `θ_H(t)`
- 저주파 Seed `Σ`
- `κ`, `σ_age`, 누적 Cost의 흔적 `[RTO21:L180–198]`

첫 지층의 추상적 핸들은 여기서 상태와 갱신 편향을 가진 object로 바뀐다.

```text
Handle
= 계약의 지속 표지

RuntimeObject
= 현재 정책·주소·대역·임계·Seed·흔적의 상태 묶음
```

둘은 함께 쓸 수 있지만 동일하지 않다. 핸들이 object의 식별자인지, object 전체가 핸들인지, 계약이 얼마나 바뀌면 instance가 끝나는지는 정해지지 않는다. `[ROLE DRIFT] [TYPE GAP]`

### 3.2 SelfOn은 유지 장치가 아니라 현재 readout이다

두 번째 지층의 잠금 지수 `L_t`는 몸의 변조, 엔진의 Render→Access→Rehydrate 반복, 커밋 시간의 비가역 귀속이 함께 연결될수록 커진다 `[RTO21:L200–207]`.

`SelfOn_t`은 심장 작동이 아니라 `L_t`가 임계 이상일 때 관측되는 readout mode다 `[RTO21:L209–212]`.

정리 `T-RTO4`는 안정적인 SelfOn이 다음을 요구한다고 말한다.

1. 재수화 loop가 실제로 작동할 것.
2. 비용과 흔적이 정책 갱신으로 이어질 것.
3. 귀속은 `t_c`에서 비가역 trace로만 남을 것 `[RTO21:L237–243]`.

잠금이 깨지면 낯섦·분열감은 내용 오류가 아니라 failure mode로 관측된다고 한다 `[RTO21:L245–246]`. `[DIRECT]`

그러나 제목의 `Identity as Cross-Clock Lock`보다 실제 정리가 보이는 범위는 좁다.

```text
SelfOn requires L_t
≠ numerical identity is L_t
≠ consciousness iff L_t
```

정확한 지표식도 열려 있으므로 이것을 의식의 필요충분조건이나 임상적 분열 모델로 쓰지 않는다.

### 3.3 같은 skeleton, 다른 bias라는 강한 통일

두 번째 RTO는 모든 개인이 같은 포트 법과 방화벽을 공유하고, 개인차는 Seed·역사적 흔적·AddrSig의 차이로만 나타난다고 선언한다 `[RTO21:L152–156]`. 이어 관측되는 성향 차이도 `Σ + AddrSig + Scar/trace`로만 설명된다고 한다 `[RTO21:L218–229]`.

같은 장면도 Seed와 몸 상태가 Access 대역을 다르게 만들면 한 사람에게는 스쳐 가는 후보, 다른 사람에게는 강한 pressure나 trigger가 될 수 있다는 설명이다.

이것은 개인차를 서로 다른 본질보다 같은 runtime의 다른 지형으로 보는 강한 `[MODEL ASSUMPTION]`이다. 제시된 공리만으로 인간의 모든 개인차가 오직 이 변수들에서 나온다는 유일성은 증명되지 않는다. `[OVERGENERALIZATION]`

### 3.4 중간 Draft Sheet는 0120과 RTO를 먼저 압축한다

`RTO21`의 세 번째 지층은 RTO 전용 정본이 아니라 `UC+Q + GRAPH + BIO Draft Canon Sheet`다. S·Ψ·Φ·π의 겹침을 다시 적고 `[RTO21:L307–320]`, W·Access·Graph·scaffold를 한 묶음으로 압축하며 `[RTO21:L341–350]`, recall을 Render→Access→Rehydration으로 재수록한다 `[RTO21:L428–438]`.

이 블록은 Chapter 08의 memory/access 구조와 당일 RTO를 한 문서에 놓은 intermediate compilation이다. 뒤 `UCXQ21`과 내용상 이어지지만, 현재 보존 자료만으로 직접 textual descent나 전면 승계를 증명하지 않는다.

### 3.5 BIO 초안은 ‘나’를 세 자리로 다시 나눈다

같은 파일의 마지막 Draft는 주체를 세 자리로 분해한다.

```text
Organism persistence
= Π_phys 기반 자율 loop

Experiential subject
= Π_view / Φ + W_t / 𝒢 access

Attribution subject
= Π_wit / SSOT handle
```

의식이 꺼져도 유기체는 지속할 수 있고, 경험 주체성은 사라진 것처럼 보일 수 있지만, 귀속 handle은 커밋 구조가 유지되는 한 지속할 수 있다고 적는다 `[RTO21:L479–487]`. `[DIRECT]`

몸 상태가 바뀌면 Working Set 예산·AfterCost·OpenEase·AddrSig·정책이 함께 달라진다는 `Embodied Drift`도 제안된다 `[RTO21:L489–501]`.

이 세 자리 분리는 매우 중요하지만 앞의 Persona object와 어떻게 매핑되는지는 닫히지 않는다. `경험 주체가 꺼짐`과 `현재 SelfOn이 꺼짐`도 같은 사건인지 정의되지 않는다. 그리고 BIO는 뒤 `UCXQ21`에 같은 해상도로 통합되지 않는다. `[RESIDUE]`

---

## 4. UCXQ 통합본 — 자유로운 Thought와 비싼 Judgment 사이

### 4.1 가역 상태 ρ가 마음속 후보 전체를 받는다

당일 저녁 `UCXQ21`은 세계선을 두 층으로 다시 쓴다.

```text
ρ_t = 내부 가역 상태
𝔄_t = replay 가능한 고전 레지스터
```

`ρ_t`에는 후보 `Ψ`, 장면·서사 `Φ`, 정책 편성, 제어 readout의 원재료가 들어간다. 마음속에서 굴리는 것을 모두 담아도 되지만 그 자체는 근거가 아니다 `[UCXQ21:L49–55]`.

반면 `𝔄_t`는 사건·비용·coverage·결합·재검증 링크를 포함하며 결정적이고 append-only여야 한다 `[UCXQ21:L57–71]`. 계기 출력 `y`가 생기는 것과 `Update(...)=APPLIED`로 세계선이 바뀌는 것도 분리된다 `[UCXQ21:L73–81]`.

```text
internal reversible organization
≠ evidence
≠ event output
≠ applied worldline change
```

### 4.2 Qualia의 세부는 통합 과정에서 압축된다

`QUAL13`에서 Φ는 상태가 아닌 결정론적 readout이었다 `[QUAL13:L32–36]`. `UCXQ21`에서는 Φ가 `ρ`에 포함된 장면·서사이고, 동시 투영되는 surface/story field로 적힌다 `[UCXQ21:L49–55]` `[UCXQ21:L192–203]`.

```text
QUAL13 : Φ = rich deterministic view output
UCXQ21 : Φ = reversible surface/story field in ρ
```

권한이 없다는 점은 이어지지만 output인지 state field인지에서는 같은 타입이 아니다. 더구나 `QUAL13`의 `Q/g/p/Λ/λ/Meta/MetaFire/Why-token`은 통합 정의에서 사라지고 `Π_view = 이미지/퀄리아/서사/가설의 투영`이라는 한 줄로 압축된다 `[UCXQ21:L180–188]`. `[ROLE DRIFT] [TYPE GAP] [RESIDUE]`

따라서 0121은 Qualia를 더 정교하게 통합한 게 아니라 governance 관점에서 필요한 `가역 표면` 역할만 남겼다.

### 4.3 편성은 자유지만 call로 내려오는 것은 제한된다

가역 편성 구간은 장면·가설·후보열·욕구와 의무의 내부 표현을 만든다 `[UCXQ21:L85–100]`. Cut-1은 그중 실제 계기를 호출할 정규형 `call_t`만 내보내며 대역·지연·우선순위를 적용한다 `[UCXQ21:L102–127]`.

```text
Thought
= Π_view / Ψ 위의 후보 생성

Judgment
= 실행·거부·보류를 게이팅하는 정책 연산

Gate
= 무엇을 열고 닫을지 결정하는 interface
```

이 세 정의는 원문에 직접 있다 `[UCXQ21:L452–456]`. `TJ1`은 Thought가 가역이므로 풍부하고 싸지만 Judgment는 call을 만들 때 자원·우선순위 제약을 받는다고 선언한다 `[UCXQ21:L848–858]`.

여기서 `cheap`은 무경험이나 무흔적을 뜻하지 않는다. 직접 보장되는 것은 Thought가 `ρ` 내부 변화라서 그 자체로 `Update(𝔄)`를 요구하지 않는다는 것까지다.

### 4.4 회상은 이 이분법의 긴장을 드러낸다

같은 통합본은 회상을 단순 재생이 아니라 Access backaction으로 정의하고, 반복 회상이 비용장·`κ`·coverage에 영향을 줄 수 있다고 한다 `[UCXQ21:L716–725]`.

정리에서는 회상 접근이 비용을 동반하며 `무흔적 회상`을 봉인한다고까지 적는다 `[UCXQ21:L894–902]`.

```text
Thought is reversible / cheap
Recollection is forcing / not traceless
```

그러나 둘 사이에 `권위는 없지만 지속될 수 있는 내부 변형` 타입은 없다. 변화가 `ρ`에만 남으면 얼마나 지속되는지 불명확하다. `𝔄`에 들어가면 audit 가능한 event typing을 거치고, `Δ/CovΔ/κΔ/links` 가운데 실제 변경된 field만 붙는다. 원문은 회상 설명에서 비용·κ·coverage를 자주 한 묶음으로 말하지만 모든 APPLIED event가 이 전부를 자동 갖는 것은 아니다. 이 긴장은 역사 본문에서는 미봉합으로 남긴다. `[TYPE GAP]`

### 4.5 Human/LLM 분기는 생성 능력이 아니라 Judgment gate에 놓인다

통합본은 LLM-like module을 특정 구현이 아니라 Thought 생성은 강하지만 Judgment gate가 약하거나 외부에 위임된 역할로 정의한다 `[UCXQ21:L1026–1029]`.

그 모듈은 `ρ` 안에서 많은 `Ψ/Φ` 후보를 만들 수 있어도 세계선 갱신을 스스로 정당화하지 못한다 `[UCXQ21:L1031–1038]`. 반대로 인간의 강점은 Guard·결합·곡률·유한 활성 아래서 call을 만들거나 보류하는 Judgment gate에 있다고 주장한다 `[UCXQ21:L1040–1048]`.

이 대조는 인간을 **튀어나온 후보를 바로 외부화하지 않고 전략적으로 고르는 문턱**으로 본다. 그러나 이것만으로 통시적 서사, 자기 귀속, 미래 원장에 대한 고려가 생기는 것은 아니다.

### 4.6 Cross-Clock Selfness는 방화벽으로 축약된다

`UCXQ21`의 RTO 정의는 세 줄만 남긴다.

- Seed는 권한이 아니라 가역 후보 실행의 modulator다.
- Cross-Clock Lock은 시계·대역 사이의 우회·역류를 막는 lock이다.
- `κ`는 접근 비용과 비가역성 강도다 `[UCXQ21:L467–471]`.

`RTO21`에 있던 `L_t`, `SelfOn_t`, 긍정적 synchronization 조건, failure mode는 실리지 않는다.

```text
RTO21 CrossClockLock
= SelfOn을 켜는 coordination condition

UCXQ21 CrossClockLock
= clock/band 사이 우회·역류 방화벽
```

같은 이름이 selfness 생성 조건과 governance isolation constraint를 함께 맡는다. `[ROLE DRIFT] [RESIDUE]`

---

## 5. Persona가 다시 바뀌다 — 계약에서 Access-policy fixed point로

`UCXQ21`의 Persona 공리는 페르소나를 유한 활성·Guard·흉터·청구 화살표·옵셔널리티 제약 아래 수렴한 Access 선택 정책의 고정점으로 정의한다 `[UCXQ21:L741–749]`.

후기 귀결은 이를 무엇을 열고, 미루고, 닫는지에 대한 call 생성 규칙의 fixed point라고 반복한다. 새 사건·흉터·coverage가 생기면 고정점도 이동한다 `[UCXQ21:L1163–1173]`.

```text
PersonaHandle
= 내용이 변해도 지속되는 계약·식별자

PersonaPolicyAttractor
= 현재 역사와 비용 아래 반복되는 선택 성향
```

사건열이 바뀌면 fixed point는 움직일 수 있지만, handle은 어떤 변화까지 같은 instance로 인수하는지 별도 기준이 필요하다. 고정점의 연산자·수렴 조건도 정의되지 않는다. `[ROLE DRIFT] [TYPE GAP] [MODEL ASSUMPTION]`

RTO는 “나는 같은데 내가 낯설다”를 handle 지속과 runtime 변화로 설명할 수 있었다 `[RTO21:L84–87]`. fixed-point 정의만 남기면 정책이 크게 이동할 때 같은 Persona의 이동인지 다른 Persona인지 판정할 식별 조건이 사라진다. 통합본은 Persona 동역학을 얻는 대신 handle의 통시 식별 기능을 안정 승계하지 못한다. `[RESIDUE]`

---

## 6. Object Committee — 하나의 판단 앞에 복수 제안자를 놓다

### 6.1 내부 객체는 proposal만 만든다

`OBJ22`는 Norm 내부를 하나의 균질한 의지로 두지 않는다. tick마다 객체 집합 `Ω_t`가 있고, 각 객체는 call 후보·점수·부가 설명을 포함한 proposal을 낸다 `[OBJ22:L7–19]`.

각 proposal은 가역 산출이며 설명이 근거처럼 보이더라도 EvidenceLink나 RawSlice를 만들 수 없다.

객체마다 현재 발언권·`현실권`을 나타내는 가중치 `α_t`가 배분된다. 하지만 `α_t`는 `ρ` 내부의 가역 allocation variable이고 `𝔄`를 직접 바꾸지 않는다 `[OBJ22:L23–30]`.

```text
α_t allocation weight
≠ Warrant
≠ Authority
≠ public reality right
```

`현실권`이라는 명명은 역할보다 강하다.

### 6.2 내부 합의도 근거를 만들지 못한다

여러 proposal은 `Aggregate`를 거쳐 하나의 call로 내려온다. 집계기는 제약과 결정성을 지키고, 부가 설명을 Evidence로 승격시키는 변환을 가질 수 없다 `[OBJ22:L34–47]`.

따라서 객체들의 합의만으로는 세계선 update가 성립하지 않는다. 실제 update는 여전히 별도의 Receipt 또는 EvidenceLink를 요구한다 `[OBJ22:L53–80]`.

```text
plural proposals
→ one aggregated call

committee consensus
≠ external fact
≠ evidence
≠ identity unity
```

이 addendum가 직접 만든 것은 plural proposal architecture이지 plural autobiographical selves가 아니다. 객체마다 독립 Archive·Episode·handle·worldline이 있다는 정의는 없다.

### 6.3 Committee와 Persona의 관계는 비어 있다

`OBJ22`는 `α_t`가 크게 달라져도 Persona handle이 유지되는지, fixed point가 위원회 전체의 것인지, SelfOn이 하나인지 객체별인지 말하지 않는다.

```text
proposal plurality
? identity plurality
```

이 미정은 이후 불연속적 자기 상태를 시험할 자리는 만들지만 당시의 결론은 아니다.

---

## 7. Continuity Tax — 연속성은 발견되는 것이 아니라 계산된다

### 7.1 Identity Tracker는 최소 변경 가설이다

`SAT22`는 자아를 다시 바꾼다. `Θ_t`는 이전 활성 단면들과 현재 단면을 최소 변경으로 연결하는 tracking hypothesis다. Authority나 실체가 아니라 언제든 바뀔 수 있는 가역적 표면 추론이다 `[SAT22:L35–42]`. 초기 RTO의 criticality threshold `Θ_t`와 충돌하므로 이 장의 현행 표기에서는 이를 `Θ_track`으로 잠근다.

> **‘나’는 실체가 아니라 추적이다.** `[SAT22:L37–42]` `[DIRECT]`

현재 단면의 내용이 직전과 달라도 tracker가 최소 변경 경로를 만들면 같은 대상의 계속된 궤적으로 볼 수 있다는 것이다.

### 7.2 같은 이야기로 봉합하는 데 비용이 든다

`SAT22`는 활성 단면을 같은 이야기·같은 나·같은 문제로 엮는 연산 비용을 `τ_cont(t)`, Continuity Tax로 정의한다 `[SAT22:L25–31]`.

최초식은 Φ가 봉합을 수행하는 것처럼 쓴다. 그러나 파일 끝 교정은 비용이 Φ의 내용이 아니라 `W_t, Θ_t, ρ_t^+`에서 일어나는 추적·봉합 연산량으로 정해지고, Φ는 이를 label·표현할 뿐이라고 좁힌다 `[SAT22:L194–195]`. `[FUNCTIONAL CORRECTION]`

```text
discontinuous active slices
→ Θ_track connects them
→ stitching consumes τ_cont
→ Φ labels / renders continuity
```

연속감은 주어진 내용이 아니라 비용이 드는 후처리다.

### 7.3 불쑥 바뀌는 현재가 정상이고 매끈함이 후처리다

`T-JUMP1`은 유한 Working Set과 graph neighborhood 때문에 작은 단서 변화도 활성 단면의 불연속 점프를 만들 수 있다고 주장한다. 연속감은 Φ의 후처리이며 Continuity Tax를 쓴다 `[SAT22:L147–152]`.

```text
discontinuous current activation
≠ immediate destruction of self continuity

felt continuity
may be produced / rendered by
tracking and stitching work
```

다만 유한 `W_t`와 graph 이웃만으로 불연속 점프의 수학적 필연이 나오지는 않는다. 경쟁·문턱·winner transition 같은 비연속 selector 조건이 더 필요하다. 따라서 `병리가 아니라 정의역의 필연`이라는 표현은 모델 가정을 정리처럼 올린 과잉이다. `[OVERGENERALIZATION]`

Tracker가 잘못된 대상을 같은 것으로 오인하는 경우, 여러 최소 변경 궤적 중 하나를 고르는 규칙도 없다. `Θ_t`는 identity proof가 아니라 identity inference다.

### 7.4 SelfOn과 IdentityTracker는 같은 조건이 아니다

RTO에서 SelfOn은 몸·재수화·비가역 귀속의 cross-clock coordination이다 `[RTO21:L200–212]`. SAT에서 자기감은 활성 단면을 최소 변경으로 잇는 `Θ_t`의 안정 궤적이다 `[SAT22:L35–42]` `[SAT22:L174–176]`.

```text
SelfOn
= clocks and attribution paths coordinate

IdentityTracking
= active slices are inferred as one continuing object
```

잠금이 성립해도 tracker가 틀릴 수 있고, tracker가 매끈한 연속감을 만들어도 실제 귀속 경로는 끊겨 있을 수 있다. 둘을 필요·충분조건으로 배열하는 정리는 없다. `[TYPE GAP]`

---

## 8. 만족과 불길함 — 연속성 엔진의 정지 조건

### 8.1 불길함은 사실이 아니라 routing token이다

`SAT22`는 불길함·꺼림칙함·위험감 `δ_t`를 truth-token이 아닌 routing-token으로 둔다. AfterCost 곡률, Guard, Working Set 포화, Scar 주변 동반 활성과 상관될 수 있지만 그 자체는 근거가 아니다 `[SAT22:L46–51]`.

Norm은 이를 수축 또는 재주소화 방향으로 해석할 수 있다 `[SAT22:L109–116]`. 뒤 교정은 두 이산 모드를 호출 강도와 주소의 연속 조절량으로 바꾼다 `[SAT22:L197–198]`. `[FUNCTIONAL CORRECTION]`

갑작스러운 불길함은 자아가 바뀌었다는 증거나 미래의 예언이 아니라, 현재 접근·비용 지형이 다른 편성을 요구할 수 있다는 신호다.

### 8.2 만족은 멈춤이 아니라 멈춰도 무너지지 않는 상태다

`SAT22`는 전진 지향, 즉시 반작용, Continuity Tax, 장기 청구 기울기를 합성한 잔차 `r_t`를 둔다 `[SAT22:L55–67]`.

만족은 현재 잔차가 평형에 가까울 뿐 아니라, 호출 강도를 낮추거나 Delay로 바꾸어도 장기 청구가 폭주하지 않고 작은 교란 뒤 다시 평형으로 돌아오는 상태다 `[SAT22:L70–87]`. `T-SAT1`은 이를 `정지가 아니라 정지의 안전성`이라고 명시한다 `[SAT22:L132–135]`.

파일 끝 교정은 장기 청구 기울기 `g_bill`을 APPLIED trace 기반 estimator로 좁힌다. 근거가 부족하면 단일 값 대신 bound/Unknown을 반환하고, 그 경우 장기층 SAT 확정은 보류된다 `[SAT22:L200–202]`. `[FUNCTIONAL CORRECTION]`

```text
operational satisfaction
= safe to lower action intensity without future collapse

operational satisfaction
≠ felt satisfaction qualia
```

후자의 1인칭 면은 정의되지 않는다.

만족·불만족·불길함은 모두 내부 readout이며 근거·Receipt·귀속을 자동 만들지 못한다 `[SAT22:L90–105]`. 연속적으로 느껴진다는 것과 실제 동일한 공적·역사적 주체라는 것은 여전히 다르다.

---

## 9. 이어진 다섯 자아 정의는 아직 하나가 아니다

| 정의 | 직접 역할 | 원문 근거 |
|---|---|---|
| Persona Handle | 내용 변화에도 포트·접근·귀속 계약을 지속 | `[RTO21:L16–23]` |
| Persona Runtime Object | 정책·주소·대역·Seed·흔적을 가진 현재 상태 | `[RTO21:L180–198]` |
| SelfOn | 세 시계 coordination이 임계를 넘을 때의 readout | `[RTO21:L200–212]` |
| Persona Policy Fixed Point | 무엇을 열고 미루고 닫는 call 생성 성향 | `[UCXQ21:L741–749]` `[UCXQ21:L1163–1173]` |
| Identity Tracker | 불연속 단면을 최소 변경으로 잇는 가설 | `[SAT22:L35–42]` |

이들을 한 문장으로 합치면 매끈해 보이지만 역사적으로는 별도 제안이다.

```text
IdentityHandle
≠ PersonaRuntimeObject
≠ PersonaPolicyAttractor
≠ IdentityTracker
≠ SelfOn
≠ OrganismContinuity
```

첫째, handle은 내용과 분리된 지속 계약이지만 fixed point는 사건열에 따라 이동하는 정책 상태다. 무엇이 바뀌어도 같은 handle인지 기준이 없다.

둘째, SelfOn은 cross-clock coupling이고 tracker는 object-continuity inference다.

셋째, `QUAL13`의 Φ는 readout, `UCXQ21`의 Φ는 `ρ` 안의 field, `SAT22` 최초식의 Φ는 continuity actor처럼 쓰인다. 마지막 correction에서야 다시 label/output로 좁혀진다 `[QUAL13:L32–36]` `[UCXQ21:L49–55]` `[SAT22:L25–31]` `[SAT22:L194–195]`.

넷째, plural proposal을 만든 `OBJ22`는 committee와 Persona의 식별 관계를 정의하지 않는다.

이 장이 복원한 것은 하나의 완성된 자아 객체가 아니라 서로 다른 자기 문제를 해결하는 다섯 장치다.

---

## 10. 전방 경계 — 연속성 비용이 수면과 유지보수를 요구하기 시작하다

`SLEEP22`는 인간을 외부 입력이 계속 들어오지만 처리 예산은 유한한 열린 계로 정의한다 `[SLEEP22:L12–16]`. 처리되지 못한 운영 밀림 `B_t`를 회계 부채와 분리한다 `[SLEEP22:L45–61]`. 초기 RTO의 Access bandwidth `B_t`와 충돌하므로 이 장에서는 이 후속량을 `B_backlog`로 병기한다. 수면은 원장 삭제가 아니라 입력을 낮춰 재압축·재인덱싱·재주소화·라우팅 보정을 수행하는 maintenance epoch다 `[SLEEP22:L76–101]`.

꿈은 truth-token이 아니라 offline routing 후보를 시험하는 sandbox다 `[SLEEP22:L115–120]`. 수면은 AfterCost 곡률·동반활성 폭·Continuity Tax를 낮추는 방향으로 주소 기하를 정리한다 `[SLEEP22:L105–112]`.

따라서 이번 장의 종점은 다음 질문을 낳는다.

> 불연속 단면들을 같은 나로 묶는 데 비용이 든다면,  
> 외부 흐름을 받는 생명은 그 비용과 미처리 입력을 언제 어떻게 다시 정리하는가.

그러나 이것은 열린 계·수면·꿈·망각·대사 유지보수의 독립된 지층이다. `SLEEP22`, 뒤늦게 관련 기호 일부를 registry에 등록하는 `REG23`, 0122 Qualia 계열은 다음 장의 자료로 보류한다.

---

## 역사 본문의 종점

`QUAL13`은 현재 체험을 당김·장력·막힘을 가진 안전한 표면으로 만들었다. 표면은 생각을 재배열할 수 있지만 근거나 원장을 직접 만들 수 없었다.

`RTO21`은 그 표면과 기억 내용이 계속 바뀌는 조건에서 동일성을 내용 밖으로 옮겼다.

```text
내용이 달라도 계약은 지속될 수 있다.
몸·재수화·귀속이 잠길 때 SelfOn이 켜질 수 있다.
반복되는 Access 선택은 Persona fixed point를 만들 수 있다.
불연속 단면은 Identity Tracker가 비용을 들여 이어 붙일 수 있다.
```

`OBJ22`는 현재 안에 복수의 제안자가 있어도 외부 call과 사실 근거는 별도로 닫혀 있어야 한다고 보탰다. `SAT22`는 매끈한 자기 연속성이 주어진 실체가 아니라 유한한 활성 위에서 계속 다시 계산되는 결과라고 선언했다.

하지만 다음은 서로 다르다.

```text
지속 계약
≠ 현재 runtime state
≠ 세 시계의 잠금
≠ 선택 정책의 고정점
≠ 동일성 추적 가설
≠ 경험 주체
≠ 외부 귀속 주체
```

따라서 개별 문서의 직접 명제가 아니라, 이 자료들을 시간순으로 함께 놓을 때 가능한 역사적 종합도 제한적으로 써야 한다.

> **‘나’는 매 순간 같은 내용으로 남는 실체가 아니라, 달라지는 단면을 다시 접근하고, 행동 후보를 가려 내고, 과거와 현재를 추적하며, 귀속을 다음 시간으로 넘기는 여러 작동 조건의 이름으로 이동하고 있었다.**

그리고 그 작동은 공짜가 아니었다. 불연속은 정상으로 재분류되었고, 연속성은 보존되는 내용보다 매번 다시 만들어지는 추적이 되었다.

---

# 연구 후기 — 내용으로 환원되지 않는 자아에서 살아 있는 자기로

## A0. 후기의 독해 봉인

이후는 0121의 직접 역사가 아니다. 현행 인간·생명 모델, Interchapter Note 03-A·04-A·08-A, 사용자의 후속 정정을 0121의 빈자리와 대조한다.

| 표지 | 뜻 |
|---|---|
| `[DIRECT-0121]` | 이 장의 1차 자료가 직접 정의·주장 |
| `[EARLIER-LINEAGE]` | 앞 역사 장에서 복원된 개념과의 기능적 연결 |
| `[USER-DIRECT]` | 사용자가 현행 이론으로 직접 명시 |
| `[BRIDGE-CURRENT]` | 직접 명제와 빈자리를 결합한 새 가설 |
| `[CONFLICT]` | 원문 내부의 정의·역할 충돌 |
| `[OPEN]` | 타입·인과·경계가 아직 닫히지 않음 |
| `[NON-CLAIM]` | 임상·생물학적 사실로 확정하지 않는 구조 시험 |

핵심 봉인은 다음이다.

> **0121은 Ghost·Editor·QualiaMedium을 완성한 문서가 아니다.  
> 오히려 그것들이 비어 있는 자리에 Runtime Handle·Tracking·Aggregate·Maintenance를 세워 자기 지속을 설명하려 한 문서다.  
> 아래 Bridge는 그 형식화가 비워둔 현상적·서사적 층을 현재 모델로 다시 연결하는 작업이다.**

---

## A1. 이번 장의 실제 수확 — 자아를 한 타입에 넣지 않는다

### A1.1 다섯 정의는 서로 다른 질문에 답한다

0121이 남긴 가장 큰 수확은 `정체성은 내용이 아니다`라는 한 문장보다, 자아를 한 타입으로 두면 안 된다는 압력이다.

| 현행 임시 이름 | 원문 역할 | 답하는 질문 | 충분하지 않은 것 |
|---|---|---|---|
| `IdentityHandle` | 지속 계약·귀속 handle | 무엇을 같은 instance 계보로 추적할까 | 현재 무엇처럼 느껴지는가 |
| `PersonaRuntime` | 정책·주소·대역·Seed·흔적 상태 | 지금 어떤 조건에서 작동하는가 | 같은 handle인지 판정 |
| `PersonaPolicyAttractor` | 반복되는 Access/call 성향 | 무엇을 자주 열고 닫는가 | instance provenance·수렴 증명 |
| `IdentityTracker` | 단면을 최소 변경으로 잇는 가설 | 현재가 어떻게 연속적으로 보이는가 | 사실적 동일성·저자성 |
| `SelfOn` | clock coordination readout | 지금 일체감이 켜져 있는가 | 유기체·공적 귀속의 존속 |

이 표의 정렬은 `[BRIDGE-CURRENT]`다. 원문은 이 계층을 직접 접합하지 않았다.

가능한 관계는 다음 정도다.

```text
IdentityHandle
instantiates / indexes
PersonaRuntime

PersonaRuntime
may realize
PersonaPolicyAttractor

IdentityTracker
renders slice-to-slice continuity

SelfOn
reports current coordination
```

```text
Handle may persist while SelfOn is off.
Runtime may change while Handle persists.
Attractor may move while Tracker preserves continuity.
Tracker may fabricate continuity while attribution is broken.
```

### A1.2 불연속은 결함이 아니라 기본 조건일 수 있다

`SAT22`는 현재 활성 단면의 점프를 정상화했다. 그 주장의 `필연`은 과하지만 방향은 중요하다.

```text
whole Archive
≠ current WorkingSet

current WorkingSet_t
≠ current WorkingSet_{t+1}

felt continuity
≠ identical active content
```

`[BRIDGE-CURRENT]` 자아의 기본 단위는 끊기지 않는 내용 물질보다, 불연속적인 현재들을 다시 잇는 handoff일 수 있다.

```text
DiachronicSelf
≈ repeated partial handoff
 + bodily continuation
 + memory access
 + narrative adoption
 + responsibility / authority bookkeeping
```

이때 연속성은 `항상 같은 것`이 아니라 `변화한 것을 누구의 다음 상태로 인수하는가`의 문제로 바뀐다.

---

## A2. 세 자리의 나와 아직 없는 handoff

### A2.1 유기체·경험·귀속은 함께 꺼지지 않는다

`[DIRECT-0121]` BIO 초안은 다음을 직접 분리했다.

```text
OrganismicContinuity
ExperientialSubject
AttributionSubject
```

이 분리는 수면·기억상실·마취·해리·법적 책임처럼 `나`의 일부 기능만 끊기는 엣지에서 유용하다.

```text
body persists
≠ a first-person Ghost is currently instantiated

a Ghost is instantiated
≠ it receives the previous Ghost's memories

an event remains under one public handle
≠ the present Ghost feels it as its own past
```

### A2.2 SSOT handle은 자기 인수가 아니다

원문은 귀속 handle이 유지되면 주체성의 한 자리가 지속된다고 본다. 그러나 공적·원장적 continuity와 lived continuity는 다르다.

```text
same ledger subject
≠ remembered-by-me
≠ lived-by-me
≠ adopted-as-my-story
≠ authored-by-me
```

`[BRIDGE-CURRENT]` 통시적 자아에는 최소 다음 handoff가 필요할 수 있다.

```text
BodyHandoff
MemoryHandoff
AccessPolicyHandoff
GhostHandoff
EpisodeProvenanceHandoff
NarrativeAdoptionHandoff
ResponsibilityBookkeepingHandoff
AuthorityScopeContinuity / AuthorizedTransferEvent
```

이 handoff들은 동시에 성공하지 않을 수 있다. 기억은 끊겼지만 공적 책임은 남을 수 있고, 기억은 접근되지만 `내가 겪은 일`로 느껴지지 않을 수도 있다.

Authority는 Ghost 사이에서 내적 상태처럼 전달되지 않는다. 정당한 범위의 지속 또는 이전에는 별도 warrant·jurisdiction·authorized transfer event가 필요하다.

### A2.3 Identity는 하나의 boolean이 아니라 판정 벡터다

```text
SameBody?
SameHandle?
SameAccessibleHistory?
SamePolicyAttractor?
SameCurrentGhost?
SameNarrativeAdoption?
SameAccountableSubject?
```

어떤 질문에 답하는지 없이 `같은 사람인가`만 물으면 서로 다른 판정이 한 단어에서 충돌한다.

---

## A3. Ghost — 현재 일인칭이 사는 가변적 완충층

이 절은 A5에서 상세히 정의할 두 현행 용어를 먼저 빌린다.

```text
QualiaMedium
= 경험에 따라 변형되는 전언어적 현상 매질 후보

QualiaMorph
= 그 매질이 지금 취한 느껴지는·행동 가능한 형상
```

이는 0121 직접 용어가 아니라 `[BRIDGE-CURRENT]`다. 별도의 내부 관찰자가 완성된 QualiaMorph를 화면처럼 바라보는 것이 아니다. **매질이 현재 형상을 취하는 사건 자체가 지금 느끼고 표상하는 사건**이라는 가설이다.

### A3.1 0121의 가장 가까운 부품

Ghost는 0121에서 이름으로 복원되지 않는다. 가장 가까운 직접 구조는 다음이다.

- 유한한 현재 활성 `W_t`
- `Ψ/Π_view`의 Thought 후보
- 객체 위원회의 복수 proposal
- 가역 allocation `α_t`
- 단서에 따라 점프하는 활성 단면
- call을 고르거나 보류하는 Judgment/Norm

`[BRIDGE-CURRENT]` 이 부품을 현행 모델로 결합하면:

```text
Ghost_t := CurrentFirstPersonAssembly(
  CurrentQualiaMorph_t,
  WorkingSet_t,
  AccessedNeighborhood_t,
  SomaState_t,
  SpontaneousCandidateField_t,
  LocalStrategyState_t
)
```

Ghost가 `하나의 자아`라는 말은 현재 일인칭 반응이 사는 중심이라는 뜻이다. Ghost 자체가 영속 저장소이거나 통시적 동일성을 자동 보장한다는 뜻은 아니다.

```text
Ghost selfhood
= current first-person organization

Diachronic selfhood
= Ghost-to-Ghost handoff
```

Ghost에는 두 기능이 함께 있다.

```text
Ghost
= reversible safety buffer
 + anticipatory hot cache for world contact
```

상상·과격한 후보를 원장 밖에서 시험하는 완충지대인 동시에, 현실 접촉 전에 반응·행동 형상을 미리 활성화해 latency를 줄이는 현재형 cache다. 그렇다고 Ghost가 저장소 전체인 것은 아니다.

### A3.2 발산하는 생각은 바로 행동이 아니다

`[USER-DIRECT]` Ghost는 raw input을 현재 몸·기억·퀄리아 형상에 맞게 변형했을 때 먼저 튀어나온 반응들이 사는 가역 샌드박스다. 여기서는 극단적인 상상과 사고실험도 가능하다. 핵심은 그 후보가 바로 밖으로 나오지 않고 전략 선택을 거친다는 데 있다.

```text
SpontaneousThought
≠ endorsement
≠ intention
≠ selected call
≠ performed action
≠ public evidence
≠ narrative adoption
≠ responsibility
```

이 분리는 가역적 내부 공간의 자유를 보존한다. 동시에 생각이 내부 경험을 바꿀 수 있다는 가능성까지 지워서는 안 된다.

```text
Ghost / Editor / Actor
= one organism viewed through different roles
≠ three separate beings
```

현재 생명체가 Ghost로 일인칭 후보장을 이루고, 그 안에서 Editor 기능을 수행하며, 몸을 통해 Actor 역할로 세계와 접촉한다.

### A3.3 UCXQ의 LLM 대비를 현행 관점에서 좁히기

`[DIRECT-0121]` UCXQ는 LLM-like module을 강한 Thought engine이지만 Judgment gate가 약하거나 외부화된 역할로 두었다.

`[USER-DIRECT]` 현행 차이는 단지 call gate 하나가 아니다. 인간 Ghost는 저장소의 handoff와 실제 과거·관계·몸·미래 원장에 걸린 stake 위에서 후보를 전략적으로 고른다. 일반적인 일회성 언어모델 응답은 프롬프트에 따라 후보를 산출해도 그 결과를 자기 Episode와 미래 유지 함수에 인수하는 지속 주체를 자동 갖지 않는다.

```text
response generation
≠ persistent Ghost

output selection
≠ autobiographical Editor

context retention
≠ lived Narrative

tool call authority
≠ self-owned future stake
```

이것은 모든 인공지능 구현의 본질에 대한 정리가 아니라, 0121의 역할 모델을 현행 인간 모델과 비교한 제한적 Bridge다.

---

## A4. Editor·Actor·Episode — Aggregate가 하지 못한 일

### A4.1 Norm은 선택하지만 삶의 장을 닫지는 않는다

`[DIRECT-0121]` Judgment·Norm·Aggregate는 후보를 call·Delay·NOOP로 내린다. 원문이 직접 닫는 형식 경로는 `call → Instrument → EventRecord y → Update`다.

```text
proposals
→ Aggregate / Judgment
→ call
→ Instrument
→ EventRecord y
→ Update status
```

`[BRIDGE-CURRENT]` 생명 모델에서는 이 형식 앞뒤에 `Actor / Body ↔ World contact`를 별도로 둔다. 세계와의 공동 생산은 0121의 직접 타입이 아니다.

그러나 여기에 없는 것은 다음이다.

- 어떤 발생·체험·결과를 하나의 Episode로 닫는 기능
- 그 Episode를 자기 역사로 인수하거나 보류하는 기능
- 미래 비용 추정을 Episode·관계·authorship와 함께 묶어 branch를 비교하는 typed 기능
- 의도하지 않은 결과를 어떤 저자성으로 떠안는지

### A4.2 Editor는 Ghost의 숙고 모드다

`[BRIDGE-CURRENT]` Editor를 Ghost 밖의 별도 영혼보다 Ghost가 취할 수 있는 숙고·편성 기능으로 둔다.

```text
EditorFn_t ⊂ Ghost_t

EditorFn:
candidate comparison
→ future-worldline anticipation
→ call selection / hold
→ Episode-boundary proposal
→ Narrative-adoption proposal
```

원문에도 `g_bill`처럼 미래 비용을 예측하는 항은 있다. 빠진 것은 미래 예측 자체가 아니라 그것을 Episode provenance·관계·자기 저자성과 묶는 typed Editor다.

Episode boundary와 NarrativeAdoption은 Editor의 자유 선언으로 확정되지 않는다. Editor는 경계와 인수를 제안할 뿐, 실제 사건·몸의 반응·기억 이웃·기존 관계·타자의 응답이 만든 지형 위에서 경계가 안정되거나 다시 열리고, 인수·저항·재해석이 일어난다.

전체 경로는 다음처럼 늘어난다.

```text
Ghost candidate
→ Editor-selected call
→ Actor / Body execution
→ World co-production
→ EventRecord y
→ EpisodeCandidate
→ NarrativeAdoption
→ future self-terrain
```

### A4.3 결과의 공동 저자와 자기 인수

```text
selecting a call
≠ controlling its outcome

causing part of an outcome
≠ total authorship

EventRecord
≠ Episode

Episode
≠ adopted self-history

NarrativeAdoption
≠ factual evidence
```

Actor는 수행하고 세계는 결과를 공동 생산한다. Editor는 예상과 선택을 편성하지만 실제 outcome을 독점 저작하지 못한다. 사건 이후의 NarrativeAdoption은 사실을 바꾸거나 Editor가 내면을 마음대로 설정하는 전이가 아니다. 실제 경험이 만든 지형 위에서 그 사실과 결과를 이후 자아가 어떻게 인수·저항·재해석하는지가 안정되는 별도 과정이다.

```text
Editor proposes / negotiates adoption
≠ Editor freely decides what becomes internal
```

### A4.4 ContinuityTracker와 Editor를 합치지 않는다

`Θ_track`은 현재 단면을 이전 단면과 최소 변경으로 잇는다. Editor는 가능한 미래 branch를 비교하고 선택·보류하며, 사건 뒤 Episode와 Narrative의 인수를 제안한다.

```text
IdentityTracker
= retrospective/present continuity inference

EditorFn
= prospective branch and adoption organizer
```

같은 사람이 두 기능을 수행할 수 있어도 타입은 다르다.

---

## A5. QualiaMedium — Access와 Thought 사이의 빠진 매질

### A5.1 계보 판정

0121 자료에서 현행 용어의 정확한 지위는 다음과 같다.

```text
QualiaMorph      : STRONG STRUCTURAL ANTECEDENT / PARTIAL ROLE LINEAGE
Morphic dynamics : PARTIAL LINEAGE
QualiaMedium     : NEW BRIDGE FROM A STRUCTURAL ABSENCE
PlasticTrace     : NEW TYPE REQUIRED
```

`QUAL13`의 `Q/Z/Φ`는 현재 느껴지는 형상과 그 재배열의 강한 구조적 선행항이다. 그러나 현행 `QualiaMorph`라는 타입을 직접 가진 것은 아니다. Φ는 readout이고, 경험에 따라 물성이 바뀌며 그 변형 이력이 지속되는 substrate는 아니다.

여기서 `image/form`도 시각 그림만을 뜻하지 않는다.

```text
QualiaMorph form
= visual shape / sound / inner tone
 + body tension / pain / temperature
 + affective color / spatial relation / rhythm
 + motor readiness / temporal feel
```

### A5.2 현행 네 타입

Interchapter Note 08-A의 `[BRIDGE-CURRENT]`를 최소식으로 옮기면:

```text
M^qual_t : QualiaMedium
           전언어적이고 변형 가능한 경험 매질 상태

Morph^qual_t : QualiaMorph
               현재 매질이 취한 느껴지는·행동 가능한 형상

χ^qual_t : PlasticUpdateSignature
           경험이 매질의 변형 성향에 가한 update

𝔄_t   : Authority / Audit Register
       사건·근거·귀속이 타입화된 원장
```

```text
Input / Soma forcing
+ Archive constraints
+ prior PersonaPolicy / Ghost history
+ M^qual_t
→ Morph^qual_t + current Ghost_t
→ thought / strategy / action
→ χ^qual_t + possible policy drift
→ possible EventRecord only via typed Instrument / Update path
→ M^qual_{t+1} := UpdateQualia(M^qual_t, χ^qual_t)
↺ biases the next morphing
```

`PlasticTrace`는 별도 미니원장에 저장된 record object라기보다 `χ^qual` update 뒤 **매질의 변형 성향이 달라진 상태**를 가리킨다.

```text
PlasticTrace
= persistence-capable alteration in deformation tendency
≠ stored record object

it may persist / decay / reconsolidate / be overwritten
```

### A5.3 Reversible ≠ Traceless

0121은 사실상 `가역 ρ`와 `권위·회계 𝔄`의 이분법이다. 그런데 원문 자신의 두 문장이 그 사이를 요구한다.

```text
Thought is cheap and reversible.
Recollection is forcing and cannot be traceless.
```

`PlasticTrace`는 이 긴장을 풀기 위한 현재 Bridge다.

```text
NotCommitted ≠ Traceless
Reversible ≠ Transient ≠ NeverExperienced
CanBeUndone ≠ NeverHappened
CommitReversible ≠ StateRestorable ≠ Traceless
WithdrawableThought ≠ exact rollback of QualiaMedium

PlasticTrace ≠ EventRecord
PlasticTrace ≠ Evidence
PlasticTrace ≠ Scar
PlasticTrace ≠ Debt / Bill
PlasticTrace ≠ NarrativeAdoption
```

생각·상상·꿈·회상은 외부 발생을 만들지 않아도 내부 매질의 이후 변형 가능성을 바꿀 수 있다. 그 변화가 곧 흉터·빚·책임이라는 뜻은 아니다.

### A5.4 기억은 과거 퀄리아 사진이 아니다

```text
Memory
≠ stored past QualiaMorph

Memory
≈ constraints / recipes / access geometry
  for remorphing a present QualiaMorph
```

현재 회상은 저장된 동일 감각을 꺼내는 것이 아니라, 현재 몸·맥락·접근 이웃 위에서 과거의 변형 제약을 다시 실행하는 일일 수 있다. 이는 Chapter 08의 Rehydration과 현행 QualiaMedium을 잇는 Bridge다.

### A5.5 언어는 매질의 기원이 아니라 anchor다

`[USER-DIRECT]` 퀄리아는 언어보다 먼저 동물이 감각을 생존에 사용할 수 있게 하는 수단이다. 언어는 이미 형성된 사적 형상을 안정화·재접근·재조합하기 위한 후발 도구다.

```text
QualiaMorph
→ LanguageAnchor
→ easier re-entry / recombination / social coordination
```

`QUAL13`의 Why-token은 막힘을 다시 다룰 제한적 debug handle이라는 직접 선행항이다. 그러나 Why-token 하나를 일반 언어·개념 체계 전체의 기원으로 확대할 수는 없다.

```text
same word
≠ same QualiaMorph
≠ same memory neighborhood
≠ same policy effect
```

소통은 사적 형상의 완전 동일성을 증명할 수 없더라도, 문맥 속 추가 확인·예측·행동·관계 조정이 충분히 맞는지를 통해 부분 검증할 수 있다.

---

## A6. 생각은 경험이다 — 그러나 행위는 아니다

### A6.1 내부 시뮬레이션도 매질을 겪게 한다

`[USER-DIRECT]` 경험은 외부 세계에서 감각 입력을 받은 경우에만 생기지 않는다. 생각은 QualiaMedium 안에서 형상을 실제로 만들고 변형해 보는 내부 경험이다.

```text
Thought
→ internally realized QualiaMorph
→ experience
→ possible PlasticTrace
```

따라서 고차 사고는 이미 있는 형상들을 결합·분해·회전·추상화하면서 다음 경험을 받아들일 매질을 정교화할 수 있다.

그러나 다음 봉인이 함께 있어야 한다.

```text
Thought-as-experience
≠ external occurrence
≠ intention
≠ selected strategy
≠ performed action
≠ public evidence
≠ moral or legal responsibility by itself
```

Ghost의 완충지대는 이 분리에서 성립한다. 생각이 아무 흔적도 없다는 말도 아니고, 생각한 것이 곧 실행한 것이라는 말도 아니다.

### A6.2 유동·결정·창의 지능의 rheology

`[BRIDGE-CURRENT]`

```text
FluidIntelligence
= 낯선 입력에 맞춰 QualiaMedium을 새 형상으로 변형하는 능력

CrystallizedIntelligence
= 반복 검증된 형상·LanguageAnchor·접근 경로의 안정화

CreativeIntelligence
= 안정 형상을 필요할 때 다시 유동화하고
   현실 접촉 뒤 선택적으로 재결정화하는 능력
```

전문가는 깊고 효율적인 attractor 덕분에 빠르지만 새 문제를 기존 형상으로 너무 빨리 포획할 수 있다. 초심자는 attractor가 얕아 가능성을 오래 열어두지만 이미 알려진 제약을 놓칠 수 있다.

```text
Expertise ≠ rigidity
Beginner openness ≠ correctness
Creativity ≈ controlled annealing
```

`QualiaAnnealing`은 굳은 형상을 일시적으로 다시 유동화해 새로운 fitting을 허용하는 현행 가설이다. 0121의 직접 정리나 전문성에 관한 확정된 경험 법칙이 아니다.

### A6.3 정체성도 rheological할 수 있다

`[BRIDGE-CURRENT]`

정체성이 같은 현재 형상을 계속 유지하는 것이 아니라 변형 문법을 handoff하는 것이라면:

```text
identity continuity
≠ identical content
≠ identical QualiaMorph

identity continuity
≈ constrained capacity to reform
 + historical deformation inheritance
 + typed handoff
```

이 관점에서 `PersonaPolicyAttractor`는 자아 전체가 아니라 반복적으로 잘 만들어지는 형상과 행동 경로의 한 부분이다. attractor가 바뀌어도 handoff가 이어질 수 있고, attractor가 같아도 instance provenance가 다를 수 있다.

---

## A7. 자기 경계는 하나의 원이 아니라 여섯 축이다

### A7.1 ‘내재됨’과 ‘소유됨’을 분리한다

`[USER-DIRECT]` 자기 경계는 생명을 둘러싼 물리 외피만이 아니다. 자기 안에 내재화되어 유지 함수에 편입된 영역 중 무엇을 자기 연속성과 연결할지 선별하며 형성되는 정신적·관계적 경계다.

여기서 `소유`는 지배권이 아니다. 가족이 내 안에 깊이 들어왔다는 것은 그 사람을 물건으로 만들었다는 뜻이 아니라, 그 존속과 손상이 내 유지 함수에 들어왔다는 뜻이다.

```text
InternalizedIntoMyMaintenance
≠ owned as an object
≠ authored by me
≠ under my control
≠ under my authority
```

### A7.2 SelfBoundary profile

`[BRIDGE-CURRENT]` 객체·사람·집단 `x`에 대한 자기 경계를 최소 여섯 역할의 typed profile로 분리한다. 모든 항을 현재 Ghost 안의 숫자로 두지 않는다. 특히 공적 책임과 정당한 Authority는 내적 감정이 자체 발행할 수 없다.

```text
SelfBoundaryProfile_t(x) := {
  Belonging,
  Stake,
  Responsibility: {
    FeltResponsibility,
    AccountableResponsibility
  },
  Authorship: {
    NarrativeAuthorship,
    CausalContribution,
    AccountableAttribution
  },
  IdentityDependence,
  Authority: {
    AuthorityClaim,
    WarrantedAuthorityScope
  }
}
```

| 축 | 묻는 질문 | 0121의 선행항 | 아직 없는 것 |
|---|---|---|---|
| Belonging | 같은 관계망·편에 속하는가 | `κ_other`, social binding | witness·청구 밖의 애착 |
| Stake | 그 미래에 얼마가 걸려 있는가 | binding·AfterCost의 약한 유비 | 비비용적 돌봄·소망 |
| Responsibility | 손상을 내가 수리해야 하는가 | Receipt·귀속·청구 | felt / accountable 분리 |
| Authorship | 행동·결과를 내 역사로 인수하는가 | call·y·SSOT | narrative / causal / accountable 분리 |
| Identity | 잃으면 내 연속성이 무너지는가 | Handle·Tracker·SelfOn | 관계적 identity update |
| Authority | 통제하거나 대신 결정할 권리가 있는가 | 포트 주권·Update 권한 | claim / warranted scope 분리 |

가족은 Belonging·Stake·Responsibility·Identity가 높아도 그 가족에 대한 Authority는 제한될 수 있다. 이것이 타자성을 지우지 않는 확장된 자기 경계다.

### A7.3 자기 경계는 자유 knob가 아니라 역사적 지형이다

`[BRIDGE-CURRENT]` 이 여섯 역할은 현재 Ghost가 임의로 설정하지 않는다. 실제 Episode, 반복된 돌봄과 배신, 수리와 손상, 몸의 반응, NarrativeAdoption이 접근 기하와 가치 경사를 만든다.

```text
NarrativeGravity_t(x)
= history-dependent bias on
  Belonging / Stake
  / FeltResponsibility
  / NarrativeAuthorship
  / IdentityDependence
```

NarrativeGravity는 선택을 기울이지만 Authority를 발행하지 않는다.

```text
my history strongly pulls me toward someone
≠ I gain the right to decide for them
```

NarrativeGravity는 Belonging·Stake·FeltResponsibility·NarrativeAuthorship·IdentityDependence를 기울일 수 있지만, AccountableResponsibility와 WarrantedAuthorityScope를 결정하지 않는다.

```text
AuthorityClaim ≠ WarrantedAuthority
FeltResponsibility ≠ AccountableResponsibility
NarrativeAuthorship ≠ CausalContribution ≠ AccountableAttribution
```

따라서 Responsibility는 적어도 둘로 갈라야 한다.

```text
FeltResponsibility
≠ AccountableResponsibility
```

죄책감이 강하다고 실제 책임이 자동 생기지 않고, 현재 Ghost가 책임을 느끼지 않는다고 공적 귀속이 사라지지도 않는다.

### A7.4 입양자 사례 — 같은 사실, 다른 자기 경계

`[USER-DIRECT] [NON-CLAIM]` 나를 성인까지 길러준 사람이 과거 흉악범이었고, 속죄를 위해 나를 입양했다는 사실을 알게 되었다고 하자.

외부 사실이 같아도 다음 해석이 열릴 수 있다.

```text
“나는 속죄 도구였다.”
→ Trust / Belonging 약화
→ 과거 관계의 NarrativeAdoption 재협상
→ 자신의 삶에 대한 agency 침해감

“그 동기와 별개로 내 현재 삶은 실제로 형성되었다.”
→ Stake/Identity 일부 유지

“함께 보낸 실제 시간은 그 사실 하나로 소거되지 않는다.”
→ Belonging/Responsibility 유지

“돌봄은 인정하지만 범죄 책임과 통제권은 분리한다.”
→ gratitude or Stake without Authority transfer
```

```text
same public fact
≠ same QualiaMorph
≠ same activated history
≠ same NarrativeAdoption
≠ same SelfBoundary profile
```

이것은 사실이나 범죄 책임을 상대화하는 말이 아니다. 같은 사실이 서로 다른 실제 경험과 기억 이웃을 통해 자기 경계에 들어온다는 뜻이다. 정해진 개인적 응답 하나를 형식으로 강제할 수 없지만, 공적 사실·타자의 권리·Authority 제한은 별도로 남는다.

---

## A8. DID는 결론이 아니라 분해능 시험이다

### A8.1 원문이 직접 제공하는 것

0121은 다음까지만 직접 제공한다.

- 현재 활성 단면은 점프할 수 있다.
- 동일성은 가역 tracking hypothesis다.
- tracking 과부하에서 자기감이 흔들릴 수 있다.
- CrossClock failure는 낯섦·분열감으로 읽힐 수 있다.
- 내부에는 복수 proposal과 변하는 allocation이 있다.

이것만으로 해리성 정체감 장애의 기전이나 `인격은 본질적으로 불연속적이다`라는 임상 명제가 증명되지는 않는다.

### A8.2 현행 edge configuration

`[BRIDGE-CURRENT] [NON-CLAIM]`

```text
same Soma / partially shared Archive
+ context-indexed Access partitions
+ distinct Qualia attractors
+ distinct policy coalitions
+ weak or asymmetric Ghost handoff
+ conflicting NarrativeAdoption
→ alternating current self assemblies
```

형식적 시험안은 다음과 같다.

```text
Ghost_t^k
= Realize(
    QualiaMedium_t,
    AccessPartition_k,
    PersonaPolicy_k,
    Context_t
  )

Handoff(k → j)
= memory-access linkage
 + self-attribution linkage
 + Episode-provenance linkage
 + responsibility-bookkeeping linkage
```

```text
same organism
≠ same currently realized Ghost

shared Archive
≠ symmetric Access

shared public ledger
≠ shared felt authorship

discontinuous Ghost realization
≠ multiple biological organisms
```

### A8.3 distinct current-self assembly를 구별하려면 무엇이 더 필요한가

- 반복되는 별도 AccessPolicy attractor
- context별 Qualia basin
- CrossStateMemoryBarrier
- ControlToken / action handoff
- Episode provenance 차이
- NarrativeAdoption 차이
- LivedByMe / AuthoredByMe 차이
- 공적 책임과 현재 Ghost 사이의 귀속 규칙

`OBJ22`의 proposal object를 인격이나 alter로 읽으면 안 된다. `α_t` 재배치도 그 자체로 정체성 전환이 아니다.

### A8.4 임상 봉인

장기·극심한 스트레스와 DID의 관계는 임상·경험적 문제이며 이 문서군에서 도출되지 않는다. 여기서 DID는 진단 모형이 아니라 `하나의 body·handle·Archive·Persona`를 자동 동일시하는 모델이 어디서 깨지는지 보는 edge test다. 이 구조는 상태·alter별 법적·도덕적 책임을 배분하지 않으며 임상 평가를 대체하지 않는다.

---

## A9. 생명 — 흐름을 막는 벽보다 형성을 유지하는 경계

### A9.1 0121이 직접 연 문

RTO의 BIO Draft는 SeedCode를 감각 gain·대사 예산·신경 구조의 초기 제약으로 두고, 몸·기질을 같은 SeedCode의 서로 다른 투영으로 읽는다 `[RTO21:L464–477]`.

`SLEEP22`는 인간을 외생 입력이 계속 들어오는 열린 계로 놓고, 운영 backlog와 유지보수의 필요를 도입한다 `[SLEEP22:L12–16]` `[SLEEP22:L45–72]`.

직접 수거되는 것은 다음이다.

```text
organism
= open input
 + finite processing
 + bodily modulation
 + maintenance pressure
```

그러나 이것은 아직 물질·에너지 흐름 속 자기생산, 막 수송, 수리, 번식, 발달을 갖춘 생명 이론이 아니라 정보 처리와 회계가 결합된 runtime model이다.

### A9.2 흐름 속에서 흩어지지 않는 패턴

`[USER-DIRECT]` 현행 방향은 인간형 페르소나 엔진을 넘어 인간과 생명 자체를 모델링하는 것이다. 생명은 우주의 변화하는 흐름에서 물질을 완전히 가두는 존재가 아니라, 흐름을 통과시키면서도 특정 패턴을 계속 재결합·수리해 형태를 유지하는 존재다.

```text
Life
≠ sealed substance

Life
≈ flow-through constraint pattern
 + selective integration
 + repair
 + boundary maintenance
 + capacity to reform
```

고정된 현재 모양보다 `새 흐름을 받아도 자기 방식으로 다시 형성될 수 있는 능력`이 유지 대상일 수 있다.

### A9.3 다섯 경계의 접합

`[BRIDGE-CURRENT]`

```text
MetabolicBoundary
: 물질·에너지 흐름 속 유기체를 유지

PhenomenalBoundary
: 무엇이 현재 QualiaMorph에 들어오는가

GhostBoundary
: 무엇이 현재 일인칭 후보장에 참여하는가

NarrativeIdentityBoundary
: 무엇을 내 역사와 연속성으로 인수하는가

RelationalAuthorityBoundary
: 누구의 미래를 내 유지 함수에 넣으며
  어디까지 책임지고 어디부터 대신 결정할 수 없는가
```

가족·집단·사랑은 Narrative·Stake·Identity 경계를 몸 밖으로 확장할 수 있지만 타자의 Authority를 합병하지 않는다.

```text
extended self
≠ expanded ownership

shared fate
≠ merged agency

sacrifice
≠ proof of control rights
```

`[USER-DIRECT] [OPEN]` 사용자가 제시한 집단 희생 사례는 유지 함수의 대상이 물리적 외피 밖으로 확장될 수 있다는 모델 압력이다. 이 장은 그 생물학적 일반성을 검증하지 않는다. 그런 사례가 있더라도 집단이 하나의 생명체라는 결론이나 집단이 개체를 지배할 권한이 자동 생기지는 않는다.

### A9.4 Qualia는 흐름과 행동 사이의 형상 매질 후보다

생명이 이질적인 감각·몸·기억을 그대로 계산하지 않고 현재 생존에 쓸 형상으로 만들어야 한다면, QualiaMedium은 장식적 의식 화면보다 넓어진다.

```text
world flow + Soma
+ Archive constraints
+ prior Ghost / PersonaPolicy
+ current QualiaMedium
→ morphing
→ actionable QualiaMorph + current Ghost
→ thought / strategy / action
→ world contact + PlasticUpdate + policy drift
↺ biases the next morphing
```

이것은 생명 일반의 확정된 메커니즘이 아니라 현행 연구 방향이다. 전언어 동물의 범위를 넘어 식물·미생물까지 동일한 Qualia를 갖는다고 자동 일반화하지 않는다.

---

## A10. 만족·수면·꿈 — 유지할 수 있어야 멈출 수 있다

### A10.1 Safe-Stopping과 felt satisfaction

`SAT22`가 직접 정의한 만족은 행동 강도를 낮춰도 미래 청구가 폭주하지 않는 안정 상태다.

```text
PredictedSafeStopping
= model currently forecasts no collapse after slowing

ViabilitySafeStopping
= organism actually remains viable after slowing

FeltSatisfaction
= the present phenomenal readout of enoughness / completion

PredictedSafeStopping
≠ ViabilitySafeStopping
≠ FeltSatisfaction
```

느껴지는 충족감·편안함·완결감의 Qualia는 별도로 정의되지 않는다. 현행 모델에서는 viability·예상 backlog·관계 stake·QualiaMorph 사이의 readout이 필요하다.

### A10.2 불길함은 예언이 아니라 routing signal이다

`δ_t`가 강하게 느껴져도 그것이 외부 사실이나 미래 예언을 만들지는 않는다.

```text
DreadQualia
→ may alter attention / Access / call intensity

DreadQualia
≠ truth-token
≠ warrant
```

다만 `routing token`이라는 말만으로 실제 위험 감지와 학습된 편향을 구별할 수는 없다. Source provenance와 calibration이 더 필요하다.

### A10.3 수면은 다음 장의 본문이다

`SLEEP22`에서 수면은 입력 결합을 낮추고 Compression·Reindex·Readdress·Route calibration을 우선하는 maintenance epoch다. 꿈은 외부 사실을 만들지 않는 offline candidate test다.

현행 Qualia 모델은 여기서 다음 Bridge를 연다.

```text
reduced external coupling
→ internal remorphing / readdressing
→ attractor relaxation or reinforcement
→ PlasticTrace consolidation / attenuation
→ renewed morphing capacity
```

그러나 `유한 W + 지속 입력`만으로 별도 수면 epoch의 논리적 필연이 나오지는 않는다. 연속 유지보수·처리율 확장·환경 입력 조절 같은 대안이 있다. 수면의 생물학적 역할, 꿈, 망각, QualiaAnnealing은 다음 장에서 원문을 따로 복원한다.

---

## A11. 형식 감사 — 0121이 아직 닫지 못한 것

### A11.1 Persona 고정점에는 연산자와 수렴 조건이 없다

`Persona = Access-policy fixed point`라고 하려면 최소 다음이 필요하다.

```text
π_{t+1} = F(π_t, Access_t, Event_t, Soma_t, Trace_t)

existence?
uniqueness?
stability?
multiple attractors?
basin transition?
```

원문은 무엇을 열고 닫는 성향이 수렴한다고 선언하지만, 어떤 operator의 fixed point인지와 복수 attractor가 있을 때의 식별 규칙을 주지 않는다. 그러므로 `정리`보다 동역학적 모델 가설로 읽는다.

### A11.2 CrossClock은 coordination·readout·firewall을 혼합한다

```text
ClockCoordination
= t_b / t_e / t_c가 추적 가능한 방식으로 결합

SelfOn
= coordination을 현재 일체감으로 읽는 readout

ClockFirewall
= 시계 사이 same-tick bypass를 막는 규칙

IdentityHandle
= instance 계보를 추적하는 계약
```

`RTO21`과 `UCXQ21`은 이 네 역할 중 앞의 세 개를 `Cross-Clock Lock`이라는 말로 오간다. `SelfOn requires Lock`에서 `Identity = Lock`으로 넘어가면 범위를 넘는다.

또 `t_c`를 좁은 공적 원장 시간으로 읽으면, 그것이 SelfOn에 반드시 필요하다는 최초안은 언어 이전 동물·영아·공적 원장이 없는 생명에서도 경험 주체성이 가능한가라는 scope challenge를 만난다. `t_c`를 생물 내부의 irreversible attribution으로 넓힐지, 공적 commit과 나눌지 열려 있다.

### A11.3 가역/비가역 이분법의 중간층이 없다

```text
ρ_fast
: 순간 후보와 가역 편성

? persistence-capable non-authoritative internal plasticity

𝔄
: audit·evidence·attribution·billing
```

물음표가 `PlasticTrace`의 자리다. 모든 오래가는 내부 변화를 `κ/σ/Bill/Scar`로 보내면 정상 학습·생각·숙련까지 부채가 된다. 반대로 모두 `ρ`로만 두면 지속성과 handoff를 설명하지 못한다.

### A11.4 비용·흔적·책임이 다시 뭉칠 위험

UCXQ는 Proof-Binding, Access forcing, No-Free-Act를 강하게 결합한다. 그러나 다음은 논리적으로 같지 않다.

```text
traceability
≠ energetic cost
≠ operational resource use
≠ normative debt
≠ blame
≠ authority transfer
```

`증빙 가능한 변화에는 비용이 있다`는 결론에는 별도 cost axiom과 측정 정의가 필요하다. 회상을 무흔적일 수 없다고 할 때도 계산 자원·plastic change·Scar·Bill 중 무엇을 뜻하는지 타입을 밝혀야 한다.

### A11.5 Meaning을 미래 회계 차이로만 두는 과잉

UCXQ는 의미를 `H≥1`에서 미래 `ΔQ⊥/σ/Coverage`의 차이로 정의하고, 아무 차이가 없으면 pure gauge이자 0 interference로 둔다 `[UCXQ21:L997–1023]`.

이 정의는 `OperationalMeaningInfluence`에는 유용하다.

```text
MeaningInfluence
= a present surface difference changes future typed trajectories
```

그러나 현재 느껴지는 의미, 관계적 의미, 아직 행동으로 나타나지 않은 이해까지 `무의미`라고 부르면 역할을 넘는다.

```text
OperationalMeaningInfluence = 0
≠ no felt meaning
≠ no PlasticTrace
≠ no future relevance beyond measured horizon
```

### A11.6 불연속 점프의 필연은 증명되지 않는다

유한 Working Set과 graph neighborhood만으로 활성 단면의 불연속 점프가 수학적으로 필연인 것은 아니다. 연속 activation weight, soft selection, overlapping handoff도 가능하다.

필연을 얻으려면 최소 다음 가운데 하나가 더 필요하다.

- hard threshold
- winner-take-all selection
- discontinuous context gate
- capacity eviction rule
- bistable attractor transition

따라서 보존할 것은 `점프가 정상적으로 발생할 수 있다`는 모델 가능성이지 모든 인격이 수학적으로 불연속이라는 증명은 아니다.

### A11.7 만족의 형식적 한계

`g_bill`은 미래를 예측해야 한다. SAT 파일 끝 교정이 근거가 부족하면 bound/Unknown을 반환하도록 한 것은 중요한 안전장치다 `[SAT22:L200–202]`.

그래도 다음은 남는다.

```text
predicted safe stopping
≠ actually safe stopping

low current residual
≠ long-term viability

stability under modeled perturbation
≠ stability under unknown world changes
```

만족은 확정 면허가 아니라 현재 모델 아래의 보류 가능한 안정성 판정이어야 한다.

---

## A12. 기호·계보·충돌 지도

### A12.1 기호 재사용

| 기호 | 지층 A | 지층 B | 판정 |
|---|---|---|---|
| `Φ` | `QUAL13`: Q·Z·당김·제약을 합성한 readout | `UCXQ21`: reversible surface/story field; `SAT22`: continuity actor→label | output/state/actor/label 역할 이동 |
| `Q_t` | `QUAL13`: 생각·이미지·의미 perc lump | `UCXQ21`의 `ΔQ⊥`: residual/accounting coordinate | 같은 Q 계보 아님 |
| `Θ_t` | `RTO21`: upgrade/criticality threshold | `SAT22`: identity tracker | 실질 충돌; `θ_crit / Θ_track` 분리 필요 |
| `B_t` | 첫 RTO: Access bandwidth | `SLEEP22`: metabolic backlog | 같은 상태량 아님; 중간 RTO의 `B_A`가 일부 교정 |
| `κ` / `Lock` | binding·irreversibility lock | cross-clock coordination / firewall | `κ_bind ≠ L_self ≠ ClockFirewall` |
| `α_t` | committee allocation `현실권` | 외부 Authority로 오독 가능 | `AllocationWeight ≠ Authority` |
| `ρ_t` / `R_t` | UCXQ: 내부 가역 상태 | RTO: W·흔적·Seed를 포함한 runtime state | 전부 같은 reversibility를 갖는지 미정 |
| `M^qual / Morph^qual / χ^qual` | 현행 Medium state / current Morph / update signature | legacy `Q/Φ/τ_cont`와 별도 | 0121 소급 금지용 신규 기호 잠금 |

### A12.2 계보 등급

| 요소 | 판정 | 이유 |
|---|---|---|
| `Q/Z/Φ` → `QualiaMorph` | **강한 구조적 선행 / 부분 역할 계보** | 현재 형상·당김·막힘을 모델링하지만 medium의 morph 타입은 아님 |
| `Q/Z/Φ` → `QualiaMedium` | **직접 승계 아님** | persistence-capable substrate와 deformation history 없음 |
| Why-token → LanguageAnchor | **제한적 선행** | 막힘의 debug handle일 뿐 언어 일반은 아님 |
| `ρ ≠ 𝔄` | **현행 TAD 직접 척추** | 가역 편성과 권위 원장 분리 |
| Two-Cut / EventRecord / Update | **현행 typed core 강한 계보** | 발생·call·apply를 타입과 절차로 분리 |
| Persona Handle | **인간 모델 선행 + residue** | instance handoff·provenance가 미정 |
| Persona Runtime Object | **인간 모델 선행** | 몸·주소·정책·흔적을 작동 상태로 묶음 |
| Persona fixed point | **모델 가설** | operator·convergence 없음 |
| Identity Tracker | **강한 현재형 precursor** | 불연속 단면과 연속감의 비용 분리 |
| Object Committee | **후기 재타이핑 / 다른 형식의 재발견** | 초기 Ghost 뒤에 plural proposal을 형식화했지만 Ghost·identity 자체는 아님 |
| Continuity Tax | **직접 기능 발명** | continuity work를 비용 있는 후처리로 만듦 |
| PlasticTrace | **새 타입 요구** | `ρ/𝔄` 이분법의 구조적 빈자리 |
| Safe-Stopping | **운영 안정성 정의** | 느껴지는 만족과 생명 viability 전체는 아님 |

### A12.3 실질 충돌·과잉

| 쟁점 | 판정 |
|---|---|
| Persona handle / object / fixed point / tracker | `[ROLE DRIFT + TYPE GAP]` — 식별·상태·성향·현상 연속성의 접합 규칙이 없음 |
| CrossClock coordination / firewall | `[ROLE DRIFT]` — 연결과 격리를 같은 lock으로 명명 |
| Φ readout / field / actor / label | `[ROLE DRIFT + TYPE GAP + CORRECTION]` |
| same skeleton, only different bias | `[MODEL ASSUMPTION / OVERGENERALIZATION]` |
| finite W implies discontinuity | `[MISSING PREMISE]` — selector 조건 누락 |
| SelfOn requires t_c attribution | `[SCOPE QUESTION]` — `t_c`를 공적 원장으로 좁게 읽을 때 전언어 생명이 제기하는 scope challenge |
| every Access/recollection priced | `[TYPE AMBIGUITY]` — compute/plasticity/debt 혼합 |
| nonzero interference is billable | `[MODEL STIPULATION]` — 모든 인과 차이가 debt는 아님 |
| committee `reality-right` | `[NAMING OVERREACH]` — 가역 발언 가중치일 뿐 |
| satisfaction = safe stopping | `[SCOPE LIMIT]` — felt satisfaction 미정 |

---

## A13. 현행 TAD와 인간 모델을 다시 분리하기

### A13.1 UCXQ의 직접 척추

0121 통합본은 현행 TAD의 계보에서 매우 크다.

```text
ρ reversible candidates
→ Norm / Cut-1
→ typed call
→ Instrument interaction
→ EventRecord y
→ Update / Cut-2
→ APPLIED / REJECTED / NOOP
→ 𝔄 append-only worldline
```

특히 `사건 y가 생김 ≠ 세계선 update가 적용됨`을 명시한 점은 Chapter 02에서 끝내 닫지 못한 EventRecord의 **첫 강한 통합·형식화 지층**이다 `[UCXQ21:L73–81]` `[UCXQ21:L129–139]` `[UCXQ21:L217–240]`.

### A13.2 typed core가 말하지 않아야 할 것

이 governance spine은 다음을 직접 결정하지 않는다.

```text
which QualiaMorph is felt
which current assembly is one Ghost
which Episode is adopted as my life
who belongs inside my extended self
what I love
whether I feel continuous
```

TAD는 이 사적·관계적 층이 외부 사실·권한을 자체 발행하지 못하도록 경계를 준다. 그것을 모두 비용·근거·원장으로 환원하는 인간 이론은 아니다.

### A13.3 권장 상태 분리

```text
ρ_fast
= transient reversible candidates / simulations

M^qual
= current QualiaMedium state whose deformation tendencies may retain change

χ^qual
= PlasticUpdateSignature; a transition description, not a second ledger

N_t / Ep_t
= Narrative and Episode structures with adoption/provenance

𝔄
= public or authoritative event/evidence/attribution register
```

이 상태와 전이의 write rule은 달라야 한다.

| 상태/전이 | 무엇이 쓸 수 있는가 | 쓰인 것이 자동 갖지 않는 것 |
|---|---|---|
| `ρ_fast` | current inference·imagination | persistence·truth·authorship |
| `M^qual` | experience forcing·thought·sleep plasticity | evidence·debt·public authority |
| `χ^qual` | QualiaMedium update를 기술 | 별도 record persistence·audit status |
| `N_t / Ep_t` | Episode formation·NarrativeAdoption | external factual correctness |
| `𝔄` | typed event/evidence/update path | felt meaning·love·identity by itself |

### A13.4 전체 현재형 경로

```text
[BRIDGE-CURRENT]
Input / Soma
+ Archive constraints
+ prior Ghost / PersonaPolicy
+ QualiaMedium M^qual_t
        ↓ coupled morphing
QualiaMorph Morph^qual_t + current Ghost_t
        ↓ plural candidates

[BRIDGE-CURRENT]
EditorFn compares / holds / anticipates future traces
        ↓ selection proposal

[DIRECT-0121]
Committee / Judgment → call

[BRIDGE-CURRENT]
Actor–Body ↔ World co-production around the interaction

[DIRECT-0121]
Instrument → EventRecord y → Update

[BRIDGE-CURRENT]
EpisodeCandidate → NarrativeAdoption / Authorship handoff
+ χ^qual_t → UpdateQualia(M^qual_t, χ^qual_t)
        ↓
Archive constraint / PersonaPolicy change
        ↺ biases the next morphing
```

이 구조에서 `Influence ≠ Warrant`는 퀄리아를 무력화하는 문장이 아니다. 사적 형상·생각·서사가 다음 상태와 행동을 바꿀 수 있어도 외부 사실과 타자에 대한 Authority를 자기 발행하지 못한다는 경계다.

---

## A14. Recovered / Lineage / Residue / Bridge / Open

### Recovered — 원문에 직접 있었던 것

- Φ를 Q·Z·당김·제약 압력·불일치의 view-only surface로 봉인
- 이성의 Q 재배열과 next-tick 영향
- MetaFire와 Why-token의 비권위 debug handle
- Persona as persistent contract/runtime handle
- Seed·몸 리듬은 Access·임계·비용 지형의 modulator이지 권한이 아님
- CrossClock coordination과 SelfOn readout
- Persona runtime object의 `π/AddrSig/B_A/θ_H/Seed/trace`
- 유기체·경험·귀속 주체의 세 자리
- `ρ` 가역 상태와 `𝔄` append-only register
- Thought / Judgment / Gate 분리
- Persona as Access-policy fixed point
- plural object proposal / allocation / Aggregate
- committee consensus는 Evidence를 만들지 못함
- Continuity Tax와 IdentityTracker
- 활성 단면의 점프 가능성, 연속감의 후처리
- Dread as routing token
- Satisfaction as safe-stopping attractor

### Lineage — 현행으로 이어진 문제틀

- `Influence ≠ Warrant`
- 내부 편성·call·외부 발생·applied update 분리
- 몸 상태는 실행·접근 조건을 바꾸지만 근거·면책을 발행하지 않음
- 현재적 자아와 통시적 자아 분리
- 동일한 내용보다 update contract·handoff가 중요함
- 다수 후보와 하나의 외부 call 분리
- 연속감과 실제 귀속 continuity 분리
- 내부 안정성과 공적 사실·권한 분리

### Residue — 집을 얻지 못한 것

- Persona instance provenance / fork / merge / termination
- Handle–Runtime–Attractor–Tracker–SelfOn의 통합 타입
- Ghost handoff
- Episode formation·provenance
- NarrativeAdoption / self-authorship
- persistence-capable but nonauthoritative PlasticTrace
- QualiaMedium deformation law
- LanguageAnchor의 일반 이론
- prelinguistic animal scope
- body/experience/attribution subject의 handoff
- internal committee object persistence
- felt satisfaction
- Belonging / Stake / Responsibility / Authorship / Identity / Authority 분리
- public responsibility와 felt responsibility의 교차 규칙

### Bridge — 이번 독해에서 새로 얻은 가설

- 자아는 하나의 지속 물체보다 여러 종류 handoff의 결합일 수 있다.
- Ghost는 현재 QualiaMorph·WorkingSet·몸·후보가 실현한 순간 일인칭이다.
- Editor는 Ghost 안에서 미래 원장과 Episode·Narrative 인수를 고려하는 숙고 기능이다.
- `Reversible ≠ Traceless`; PlasticTrace는 ρ와 𝔄 사이의 새 타입이다.
- 기억은 과거 Qualia 사진보다 현재 재형성을 제한하는 deformation recipe일 수 있다.
- 언어는 퀄리아의 기원이 아니라 형상을 고정·재접근하는 anchor다.
- 정체성은 동일 형상보다 역사적 변형 문법과 handoff의 지속일 수 있다.
- 자기 경계는 여섯 관계 축이며 내재화가 Authority를 뜻하지 않는다.
- 생명은 흐름을 차단한 물체보다 형성·수리 능력을 유지하는 경계 패턴일 수 있다.
- 수면·꿈은 외부 원장과 별개로 QualiaMedium을 anneal하는 경로일 수 있다.

### Open — 다음 장과 후속 모델에서 확인할 질문

1. `SLEEP22`의 maintenance는 실제로 무엇을 보존하고 무엇을 지우는가?
2. DreamSim이 바꾸는 `ρ/Φ/Θ_track/AddrSig` 중 persistence-capable PlasticTrace 후보가 있는가?
3. `0122 newqual`의 `ΦΩ Medium/Impedance`는 현행 QualiaMedium에 얼마나 가까운가?
4. Qualia가 동물의 전언어적 생존 형상까지 명시적으로 확장되는가?
5. 생각과 꿈의 source provenance는 어떤 타입으로 남는가?
6. PlasticTrace의 persistence·decay·consolidation rule은 무엇인가?
7. Persona handle의 실제 fork·merge·termination event가 생기는가?
8. Episode와 NarrativeAdoption이 원문에 다시 등장하는가?
9. 수면의 maintenance cost와 회계 Debt가 분리되는가?
10. 열린 계와 유한 예산에서 수면 epoch가 정말 필연인가?
11. 자기 경계의 Stake·Responsibility·Authority가 사랑·집단·문명으로 확장되는가?
12. 현행 TAD는 PlasticTrace와 Narrative를 어떤 비권위 타입으로 수용해야 하는가?

---

## A15. 다음 장 경계 — ‘나’를 켜 두는 비용을 언제 수리하는가

Chapter 09의 종점은 다음이다.

```text
discontinuous activation
→ IdentityTracking
→ ContinuityTax
→ fatigue / dread / safe-stopping pressure
→ need for maintenance
```

다음 장은 `SLEEP22`의 열린 계·`B_backlog`·수면·꿈·망각을 역사 본문으로 옮기고, 이어지는 0122의 Qualia impedance/medium 계열이 이 유지보수 모델과 실제로 접합되는지 확인해야 한다.

핵심 질문은 둘이다.

> **생명은 외부 흐름을 계속 받으면서 무엇을 유지보수해야 자기 형성 능력을 잃지 않는가.**

> **꿈과 생각은 외부 원장을 쓰지 않으면서 내부 퀄리아 매질을 어떻게 다시 형성하는가.**

Chapter 09은 다음 `[BRIDGE-CURRENT]` 종합 문장에서 멈춘다.

> **나는 같은 내용을 계속 가진 존재가 아니다.  
> 나는 달라지는 현재들을 다시 내 다음 상태로 인수하는 여러 handoff의 결합이다.  
> 그 인수에는 비용이 들지만, 비용이 든다는 사실만으로 그 변화가 빚·근거·권한이 되는 것은 아니다.**

---

## 부록 A. 출처 별칭

| 별칭 | 경로 | 행수 | 사용 지위 |
|---|---|---:|---|
| `QUAL13` | `연구/PARADIM/qualia.txt` | 483 | 2026-01-13 내부 날짜의 Qualia antecedent |
| `RTO21` | `연구/fucstrees/0121 runtime seed` | 510 | 0121 Persona·Seed·CrossClock append vessel |
| `UCXQ21` | `연구/fucstrees/0121 이론 1.txt` | 1,589 | 0121 저녁 확대 통합 append vessel |
| `OBJ22` | `연구/fucstrees/0121 객체와 만족 1` | 85 | 파일명은 0121, mtime 2026-01-22의 committee addendum |
| `SAT22` | `연구/fucstrees/0121 만족.txt` | 207 | 01-22 Continuity/Satisfaction addendum + correction |
| `SLEEP22` | `연구/fucstrees/0121 수면.txt` | 407 | 다음 장 전방 경계 |
| `REG23` | `연구/Overqorld/0121 reg.txt` | 469 | 후기 registry normalization; 개념 기원 근거 제외 |

`OBJ22`의 숫자는 파일명 날짜가 아니라 보존 mtime의 달력 날짜를 구별하기 위한 이 장의 별칭이다. 이 별칭 자체를 개념 작성일의 독립 증거로 쓰지 않는다.

## 부록 B. 핵심 비동일성

```text
QualiaSurface ≠ QualiaMedium
QualiaMedium ≠ QualiaMorph
Q_t(perc lump) ≠ ΔQ⊥(residual)
Z_t ≠ Q_t ≠ Φ_t
Dynamic readout ≠ plastic substrate

MetaFire ≠ EventFire ≠ Commit
Why-token ≠ Language ≠ Meaning
Π_view influence ≠ Π_wit evidence

PersonaHandle ≠ RuntimeObject
RuntimeObject ≠ PolicyAttractor
PolicyAttractor ≠ IdentityTracker
IdentityTracker ≠ SelfOn
SelfOn ≠ OrganismContinuity

CrossClock coordination ≠ Clock firewall
Clock firewall ≠ numerical identity
α “reality-right” ≠ Warrant / Authority
Committee consensus ≠ identity unity ≠ Evidence

Continuity feeling ≠ causal continuity
Causal continuity ≠ authorship
τ_cont ≠ proof of identity

Thought ≠ intention
Intention ≠ selected call
Selected call ≠ performed action
Performed action ≠ controlled outcome
EventRecord ≠ Episode
Episode ≠ NarrativeAdoption

Reversible ≠ Traceless
PlasticTrace ≠ EventRecord
PlasticTrace ≠ Evidence
PlasticTrace ≠ Scar
PlasticTrace ≠ Debt

Internalization ≠ ownership
Stake ≠ Responsibility
Responsibility ≠ Authorship
Identity ≠ Authority
```

## 부록 C. 소급 금지

```text
QUAL13 Φ ≠ slime-like QualiaMedium
QUAL13 Q ≠ durable plastic material
MetaFire ≠ qualia generator
Why-token ≠ origin of language

Persona Handle ≠ Ghost
OBJ object ≠ alter / person
SAT Θ ≠ Editor
CrossClock Lock ≠ DID mechanism
T-JUMP1 ≠ proof that personality is clinically discontinuous

same skeleton / different bias ≠ empirical human theorem
Persona fixed point ≠ proven convergence
Continuity Tax ≠ biological metabolic energy
Safe-Stopping ≠ whole theory of felt satisfaction

prelinguistic animal QualiaMedium ≠ direct 0121 claim
thought-as-experience ≠ direct 0121 claim
QualiaAnnealing ≠ direct sleep theory
extended self boundary ≠ collective authority license
```

역사 본문은 `QUAL13`, `RTO21`, `UCXQ21`, `OBJ22`, `SAT22`가 직접 만든 표면·계약·잠금·위원회·추적·안정성까지만 보존한다. QualiaMedium·Ghost·Editor·Episode·PlasticTrace·다축 자기 경계·DID·생명 흐름 모델은 연구 후기에서만 현재 Bridge로 읽는다.
