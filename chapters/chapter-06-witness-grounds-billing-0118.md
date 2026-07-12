# Chapter 06 — 증언과 빚의 탄생

## 무엇이 판정의 근거가 되며, 완화의 차익은 어떻게 미래 청구가 되었는가

> **상태:** 역사 복원 + 연구 후기 v1.0  
> **범위:** 2026-01-18 `머하고잇엇지`·Rationale 03–05·STG06–062부터 `대통합 헌법`·`그릇`까지  
> **직전 장:** Chapter 05 — 문서는 아직 런타임이 아니다  
> **전방 경계:** 0119 이후의 인간형 재통합, 0121의 압축 통합, 0122의 Qualia 매질 메트릭 재분리는 다음 장들로 보류

---

## 들어가며 — 다르게 느낄 자유와 사실을 정할 권리는 다르다

Chapter 05의 공장은 문장을 실행 계약으로 바꾸었다. 키마다 reader와 writer를 정하고, current와 next를 가르고, 표에 없는 경로를 닫았다. 그러나 닫힌 실행기는 아직 두 질문에 답하지 못했다.

```text
외부에서 들어온 것 중 무엇을 판정의 근거로 삼을 것인가?

사람이 주의·표현·기대·마취로 현재의 부담을 줄였을 때,
줄어든 체감과 줄지 않은 문제의 차이는 어디에 남는가?
```

0118은 이 두 질문을 한꺼번에 붙잡는다. 첫 질문에서는 `Raw / Perc / Witness / View`를 분리하고, 두 번째 질문에서는 `pledge / Receipt / σ / Bill`을 만든다.

처음에는 둘이 다른 문제처럼 보인다.

- Witness 계열은 무엇을 믿을 수 있는가의 문제다.
- Billing 계열은 미뤄진 비용을 어떻게 보존할 것인가의 문제다.

하지만 둘의 밑바닥에는 같은 공포가 있다.

> 지금의 체감이나 표현을 바꾸는 능력이  
> 과거의 흔적과 미래의 부담까지 공짜로 다시 쓰게 해서는 안 된다.

그래서 0118의 가장 중요한 발명은 `Witness`라는 객체 하나도, `Bill`이라는 계정 하나도 아니다. **체험이 다음 행동에 영향을 주는 경로와, 판정이 사실을 확정하는 근거 경로를 서로 다른 계약으로 가른 것**이다.

후기 헌법은 마침내 이를 두 단어로 부른다.

```text
Grounds   : 판정이 사실을 확정할 때 참조하는 입력
Influence : 다음 변화에 반영되도록 전달되는 입력
```

그러나 이 장은 성공담으로만 닫히지 않는다. 증거 오염을 막으려 만든 벽은 1인칭 체험의 사실성까지 밀어냈고, 미뤄진 부담을 보존하려 만든 회계는 한때 모든 표면 완화와 연결을 빚으로 만들었다. `pledge`는 서약에서 자동 영수증으로 변했지만 실제 행동보다 먼저 발행되었고, `ActionOut` 뒤의 몸·세계 결과는 끝내 돌아오지 않았다.

따라서 이 장의 중심 질문은 이것이다.

> **느낌이 사실을 사칭하지 못하게 하면서도 느낌을 지우지 않고,  
> 미뤄진 부담을 보존하면서도 모든 변화에 죄목을 붙이지 않으려면  
> 어떤 타입들이 더 필요했는가?**

---

# 역사 본문 — 0118 하루 동안 벌어진 분리와 과잉

## 0. 범위·판본·독해 규율

### 0.1 파일명이 아니라 보존 mtime과 내부 교정을 따른다

0118군은 하나의 완성 논문이 아니라 같은 날 여러 번 다시 쓰인 실험군이다. 앞 문서의 문장이 뒤 문서에 재등장해도 의미와 read scope가 달라질 수 있다. 이 장은 파일시스템의 보존 mtime을 판본 순서의 보조 증거로 사용하되, 표시된 timezone을 저자의 실제 작성 timezone으로 단정하지 않는다.

| 순서 | 보존 시각 | 별칭 | 문서 | 이 장에서의 역할 |
|---:|---:|---|---|---|
| 1 | 01:13 | `MEM18` | `공장2/0118 머하고잇엇지` | 0117 공장 이후 문제 재호출 |
| 2 | 01:46 | `R03` | `공장2/0118 rationale03` | Pressure–Repair–Relief·RiskCarry |
| 3 | 02:46 | `R04` | `공장2/0118 rationale 04` | Witness/Control/Storage/Bill 최초 완형 |
| 4 | 03:00 | `R05` | `공장2/0118 rationale 05` | Cosmetic/True Relief·policy-free Bill 교정 |
| 5 | 03:54 | `STG0` | `공장2/0118 STG06` | 첫 실행화 |
| 6 | 04:24 | `STG1` | `공장2/0118 STG061` | Receipt-only와 payload firewall 강화 |
| 7 | 05:26 | `STG2` | `공장2/0118 STG 062` | WitnessSchema·core 분리·단일 전이 |
| 8 | 13:13 | `RSUM` | `공장2/0118 rationale 05 1` | allowlist 필요성과 설계 의도 회고 |
| 9 | 13:23 | `LINK18` | `공장2/0118 linker` | World 두 경계·Control/Receipt 두 bus |
| 10 | 14:38 | `AX18` | `공장2/0118 공리 정리 1` | 공리 압축 |
| 11 | 16:56 | `JOIN18` | `공장2/0118 접합용 문사` | 접합용 재서술 |
| 12 | 17:53 | `TEM18` | `공장2/0118 temo` | Conn→Imprint 보편화 실험 |
| 13 | 18:41 | `PATCH18` | `공장2/0118 append patch` | AXH vA0.1/.2/.4 누적 bundle; vA0.3 부재 |
| 14 | 19:22 | `FULL18` | `공장2/0118 full06 1` | 후기 실행 합성 |
| 15 | 20:23 | `RUN18` | `공장2/0118 통합 1.txt` | v0.6-STG+AXH 실행 종점 |
| 16 | 20:55 | `THEORY18` | `공장2/0118 통합1 이론1.txt` | 실행 구조의 이론 재해석 |
| 17 | 22:57 | `CON06` | `MAYnilat/0118 대통합 헌법` | Grounds/Influence 명시 분리 |
| 18 | 23:17 | `CON01` | `MAYnilat/0118 대통합 헌법 01` | v0.6 뒤에 작성된 최소 헌법 재추출 |
| 19 | 23:40 | `VES18` | `MAYnilat/0118 그릇` | Evidence/Ledger/σ 역할과 load slot |

`공장2/0118 통합 1용 설명문서`는 이름상 0118군이지만 보존 mtime이 2026-03-07이다. 이 장에서는 `EXPL18`이라 부르고 **후기 설명 거울**로만 사용한다. 0118 당일 최초 정의의 근거로는 쓰지 않는다.

당일 19개 파일은 모두 서로 다른 SHA-256을 가진다. 완전 중복 합본은 없으며, 이름이 비슷하다고 동일 판으로 처리할 수 없다.

특히 밤의 헌법 두 판은 이름과 시간 순서가 반대처럼 보인다.

```text
22:57  대통합 헌법 v0.6
23:17  대통합 헌법 01 v0.1
```

따라서 `v0.1 → v0.6`의 진보 계보로 쓰면 역사 오류다. `CON01`은 시간상 후기의 최소 헌법 재추출 branch로 읽으며, 내부 번호가 작다고 `CON06`을 자동 supersede한다고 보지 않는다.

### 0.2 선언은 append-only, 실제 편집은 full rewrite다

여러 문서가 append-only 정신을 선언하지만 파일 계보는 대부분 재발행과 전면 rewrite다.

```text
R04 → R05
개념 승계 + 전면 재작성

STG0 → STG1 → STG2
큰 동일 블록을 보존하면서 계속 구조 교체

STG2 → FULL18 → RUN18
AXH 흡수 뒤 다시 full rewrite
```

따라서 앞 판본의 폐기된 허용과 뒤 판본의 금지를 모두 최종 규칙처럼 합치지 않는다. 실제 append log에 가장 가까운 `PATCH18`에도 별도 provenance 문제가 있다.

- `CONTROL-OBS FIREWALL ... vA0.1`
- `RUN/ATTACH PROJECTION ... vA0.1`

서로 다른 두 패치가 `vA0.1`이라는 이름을 재사용한다. 이 장에서는 필요할 경우 각각 `AXH-vA0.1`, `RUN/ATTACH-vA0.1`로 구분한다. 또한 `PATCH18`의 vA0.4는 vA0.3을 supersede한다고 선언하지만 보존된 0118 파일군에는 vA0.3 본문이 없다. 이는 실제 provenance gap이다.

### 0.3 이 장의 표지

| 표지 | 뜻 |
|---|---|
| `[DIRECT]` | 해당 원문이 직접 선언 |
| `[REWRITE]` | 앞 정의를 새 용어·구조로 재서술 |
| `[FUNCTIONAL CORRECTION]` | 뒤 판본이 앞 판본의 누수나 모호성을 실제로 좁힘 |
| `[REAL CONFLICT]` | 함께 정본으로 유지하기 어려운 정의 |
| `[OVER-CLOSURE]` | 오염을 막는 범위가 넓어 정당한 경로도 함께 닫힘 |
| `[OVERGENERALIZATION]` | 국소 직관을 보편 법칙으로 확장 |
| `[SIDE BRANCH][HOLD]` | 탐색 가치가 있으나 현행 코어로 곧장 승계하지 않음 |
| `[TYPE RESIDUE]` | 구분의 필요는 보였으나 독립 타입이 생기지 않음 |
| `[LINEAGE]` | 현행 이론과 직접 또는 강한 문제 계보 |
| `[RESIDUE]` | 형식화하며 빠지거나 집을 얻지 못한 것 |
| `[BRIDGE]` | 원문과 현행 이론을 함께 읽어 이번에 얻은 가설 |
| `[OPEN]` | 다음 지층에서 확인할 질문 |

### 0.4 소급 금지

이 장의 `RawSlice`는 생명체가 해석하기 전에 받는 organismal raw와 같지 않다. 이미 `GateRaw`와 헌법 검사를 거쳐 판정 계약에 받아들여진 조각이다.

```text
organismal raw
≠ 0118 RawSlice
≠ Witness
≠ Grounds relation
≠ Qualia
```

또한 0118의 `Witness`는 현행 TAD의 `EvidenceArtifact`, `EvidenceLink`, `ObservationEvent`, `CertifiedEvent` 중 어느 하나와도 동일하지 않다.

```text
Witness ≠ Truth ≠ Warrant
Receipt ≠ EvidenceLink
ActionOut ≠ performed action ≠ world outcome
```

이 비동일성은 연구 후기에서 다시 등급화한다.

---

## 1. 출발점 — 완화가 문제를 없앤 것처럼 보일 때

### 1.1 0117의 공장이 남긴 빈 입구

Chapter 05의 실행기는 어떤 모듈이 무엇을 읽고 쓸지 닫았지만 외부 입력의 진위를 판정할 독립 port를 만들지 못했다. 후기 STG branch의 `PercIn`은 policy-shaped 변환을 거쳐 후보·물리 신호·Commit으로 들어갈 수 있었다.

즉 같은 표현 조작이 두 역할을 동시에 가질 위험이 남았다.

```text
현재를 덜 괴롭게 보이게 함
+ 판정할 잔여 자체도 줄어든 것처럼 만듦
```

`R03`은 이 문제를 아직 Witness로 풀지 않는다. 먼저 인간적 언어로 압력·수리·완화를 나눈다.

### 1.2 Pressure–Repair–Relief

`R03`의 출발점은 몸과 시스템이 감당해야 할 압력이다.

- Pressure는 예상 수리 요구와 현재 여유의 충돌이다.
- Repair는 이미 생긴 불일치를 재압축·격리·복구하는 작동이다.
- Relief는 현재 느끼고 대응하는 부담을 낮춘다.

`[R03:L66–85]`

이때 Relief는 악이 아니다. 살아 있는 시스템은 모든 압력을 같은 강도로 의식할 수 없고, 주의와 전망을 조절하지 않으면 행동 자체를 못 할 수 있다.

문제는 완화가 비용의 존재까지 다시 쓰는 경우다.

### 1.3 RiskCarry — 미래로 옮긴 차액

`R03`은 policy가 Forecast를 낮춰 당장의 여유 `hr`을 높이면 그 차액을 `RiskCarry`에 계상한다 `[R03:L90–137]`.

```text
낮아진 현재 전망
→ 커진 현재 여유
→ 사라지지 않은 위험 차액
→ RiskCarry
```

여기에는 이후 `σ`와 닮은 문제틀이 있다. 그러나 `R03`의 RiskCarry는 동일 tick의 `dm/ConstraintMargin`에 보상 계상될 뿐, Store나 `t+1` 지속식으로 시간 경계를 건너는 상태는 아니다 `[R03:L114–115]`.

> **[STRUCTURAL PRECURSOR]** “현재 완화의 차액을 다른 축에 남긴다”는 압력은 이어지지만, RiskCarry를 곧바로 초기 `σ`라고 부르지는 않는다.

또한 아직 판정식에 policy가 직접 들어가고 `Canon_phys` 역시 이미 변환된 `PercIn`에서 만들어진다 `[R03:L270–293]`.

> **[TYPE RESIDUE]** 미뤄진 부담을 별도 상태로 보존해야 한다는 직관은 생겼지만, 무엇이 policy-independent한 손상이며 무엇이 체감된 위험인지 아직 타입으로 갈리지 않았다.

---

## 2. 네 층의 발명 — Witness / Control / Storage / Bill

### 2.1 흔적과 조종간을 가르다

`R04`는 문제를 네 층으로 재구성한다.

```text
Witness : 몸과 환경에 남은 흔적을 판정 쪽에 제공
Control : 주의·표현·전망·대응을 바꿈
Storage : 아직 해소되지 않은 차액을 시간 너머로 보존
Bill    : 보존된 부담이 실제 비용·제약으로 귀속되는 청구
```

`[R04:L32–43]`

장 전체를 관통하는 문장은 초반에 이미 나온다.

> 표현과 지각을 바꿀 수는 있어도, 그 차이는 몸과 세계의 흔적에 남는다.

`[R04:L10–14, 의역]`

이 문장은 “마음은 거짓이고 몸만 진실”이라는 이원론이 아니다. 오히려 사람이 현재를 다르게 경험하고 전략을 바꿀 자유를 인정하면서, 그 자유가 판정과 비용을 공짜로 삭제하지 못하게 하려는 설계다.

### 2.2 GateRaw와 두 개의 입구

`R04`는 외부 접촉을 처음으로 두 경로로 가른다.

```text
Ŝ      := Π_wit(S)
RawIn  := GateRaw(X, Mark, Ŝ)
PercIn := TR(S, RawIn, policy)
```

`[R04:L134–192]`

- `RawIn`은 policy가 개입하지 못하게 하려는 판정 후보다.
- `PercIn`은 주의·표현·프레이밍이 작용할 수 있는 체험·대응 입력이다.
- `Witness`는 raw와 policy 비가시 상태에서 구성되는 판정용 묶음이다.

> **[REWRITE: 후기 THEORY18의 언어]** 같은 세계 접촉이 두 번 존재한다는 뜻이 아니라, 한 접촉에서 무엇을 묻는가가 달라진다.

```text
이 접촉이 나에게 무엇처럼 주어지는가?
≠
이 판정에서 무엇을 근거로 읽도록 허용할 것인가?
```

### 2.3 초기 Witness의 과장

`R04`는 Witness를 “반박 불가능한” 몸·환경 흔적처럼 강하게 묘사한다 `[R04:L36–43, L406–411]`.

하지만 바로 뒤의 `R05`는 이를 낮춘다.

> Witness는 객관적 진리 자체가 아니라 몸과 환경에 남은 흔적이다.

`[R05:L159–167, 의역]`

이 교정은 작지 않다.

```text
세계 그 자체
≠ 센서가 남긴 흔적
≠ schema가 허용한 증거 묶음
≠ 그 묶음으로 정당화되는 특정 claim
```

0118은 첫 번째와 두 번째의 차이를 감지했지만, 세 번째와 네 번째를 claim-specific relation으로 만들지는 못한다.

---

## 3. Raw와 Eff — 줄어든 사실과 줄어든 체감

### 3.1 두 잔여

`R04–R05`는 잔여를 두 갈래로 나눈다.

```text
ΔQ⊥_raw
= Witness / Coverage_wit로 계산하는 판정용 잔여

ΔQ⊥_eff
= 현재 policy·표현·주의를 통과해 체감되고 대응되는 잔여
```

`[R04:L196–206; R05:L183–196]`

이에 따라 다음도 갈린다.

```text
Coverage_wit ≠ Coverage_view
raw residual ≠ experienced residual
판정 ≠ 대응
증거 ≠ 조종간
```

이 분리의 직접 목적은 간단하다.

> 낙관적으로 표현했다고 미해결 문제가 해결된 것으로 계산하지 말 것.

### 3.2 CosmeticRelief와 TrueRelief

`R05`는 완화를 두 종류로 명명한다.

```text
CosmeticRelief
= 낙관·둔감·주의 재배치·표현 전환으로 eff 부담을 낮춤

TrueRelief
= raw residual 감소
  또는 σ 감소
  또는 lock 완화
  또는 constraint margin 회복
```

`[R05:L41–53]`

또 `ForecastBase`와 `ForecastCosmetic`을 나누고, 둘의 차액을 pledge에 넣는다 `[R05:L91–112]`.

이때 “cosmetic”은 처음에는 **판정 잔여를 줄이지 않은 완화**라는 기술적 뜻이다. 그러나 후기 문장에서는 “가짜 변화”라는 가치 판단으로 쉽게 미끄러진다. 이 미끄러짐은 후기 Qualia와 현재형 자아 모델을 다시 읽을 때 중요하다.

### 3.3 raw도 세계 그 자체는 아니다

`ΔQ⊥_raw`는 policy-independent하게 만들려 했지만 절대적 현실량은 아니다. 정확한 뜻은 다음에 가깝다.

> 현재 등록된 WitnessSchema와 coverage 안에서, policy의 표현 조작 없이 계산할 수 있는 잔여.

관측되지 않은 현실, 잘못 교정된 센서, schema 밖 사건은 이 값에 잡히지 않을 수 있다. 따라서:

```text
policy-independent under schema
≠ complete
≠ infallible
≠ ontologically raw
```

---

## 4. pledge에서 Receipt로 — 서약이 자동 흔적으로 바뀌다

### 4.1 초기 pledge는 미래에 대한 자기 서약이었다

`R04`의 pledge는 `겉완화 − 실완화`의 차이를 미래 `σ`에 적재하겠다는 전략 명세다 `[R04:L222–241]`.

이 단계의 뉘앙스는 인간적이다.

```text
나는 지금 이 부담을 덜 느끼는 전략을 쓴다.
그러나 그것이 실제 해결이 아니라면
그 차액이 미래에서 다시 계산되도록 남긴다.
```

다만 이것은 행위자가 speech act로 직접 발행한 자기신고가 아니다. `PolicyUpdateFn`이 `(policy_{t+1}, pledge_{t+1})`를 함께 생성한다 `[R04:L222–241]`. 따라서 “서약”은 원문의 의미론적 비유이고, 구현상으로는 controller가 선택한 회피·직시·프레이밍 전략의 명세에 가깝다.

### 4.2 정책이 청구 법칙까지 바꾸는 누수

초기 `R04`에서는 `obs_gain`이 즉시비용뿐 아니라 `σ`의 소산 확률·계수에도 관여할 여지가 있다 `[R04:L245–260]`.

이는 현재의 관측·표현 전략이 다음을 동시에 할 수 있다는 뜻이다.

```text
체감을 낮춤
+ 적재량을 바꿈
+ 나중에 청구될 방식도 바꿈
```

`R05`는 이 누수를 고친다.

- `obs_gain`은 즉시 비용과 Store 적재량까지만 관여한다.
- Bill 규칙은 policy가 읽거나 조작하지 못한다.
- soft/hard dissipation은 결정론적으로 정의한다.

`[R05:L229–265]`

> **[FUNCTIONAL CORRECTION]** 지금의 coping strategy는 자신이 남긴 부담의 청구 법률까지 다시 쓸 수 없다.

### 4.3 실행본에서 pledge는 자동 Receipt가 된다

STG 계열을 지나며 pledge의 지위가 변한다.

```text
초기 pledge
= “이 전략의 차액을 미래에 남기겠다”는 서약

후기 Receipt
= 고정된 knob configuration과 cosmetic delta에서
  자동 산출되는 전략-설정 영수증
```

`Receipt`라는 별칭과 Receipt-only 규율의 최초 명시는 `STG1`이다.

- `Receipt(=pledge payload)`라는 이름이 등장한다 `[STG1:L355–361]`.
- pledge는 `StoreFn` 전용이며 Bill·Damage·Residual이 직접 읽지 못한다 `[STG1:L411–421]`.
- `AttachMeta`가 pledge를 단일 원천으로 자동 산출한다 `[STG1:L574–591]`.

`STG2`는 이를 승계해 knob와 auto-mint를 더 안정화한다.

- Receipt의 개념 역할을 다시 고정한다 `[STG2:L373–379]`.
- `PledgeFn`은 전체 policy가 아니라 허용된 고정 knob만 읽는다 `[STG2:L383–405]`.
- pledge는 `StoreFn`만 읽을 수 있고 Bill·Damage·ResidualRaw가 직접 읽을 수 없다 `[STG2:L420–426]`.
- `pledge_next`는 `CtrlSolve`의 자유 출력이 아니라 자동 산출된다 `[STG2:L612–624]`.

시간 인덱스는 완전히 봉인되지 않는다. `STG1`은 state 안의 이전 산출물을 `pledge_t`처럼 처리하지만 `[STG1:L552–570]`, `STG2`는 같은 역할을 `pledge_{t-1}`로 표기한다 `[STG2:L542–579]`. state 시점 기준과 산출 tick 기준이 바뀐 것일 수 있으나 명시 규약이 없어 잠재적 double-delay가 남는다.

서약이 자동 영수증으로 바뀐 이유는 명확하다. controller가 자신이 선택한 조작 좌표를 임의로 축소 신고할 수 없게 하려는 것이다. 그러나 이 Receipt는 그 조작이 몸과 세계에서 실제 수행되었다는 증명은 아니다.

그러나 이름이 유지되면서 서로 다른 두 타입이 한 계보처럼 보이게 됐다.

```text
declared intention
≠ chosen strategy configuration
≠ performed action receipt
≠ external outcome evidence
```

이 구분은 아직 완성되지 않는다.

---

## 5. σ와 Bill — 사라지지 않은 것이 시간을 건너는 방식

### 5.1 σ는 경로를 가진 미해결 상태다

`R04`는 `σ`를 미해결 응력·미지급 수리 요구가 누적된 벡터 상태로 둔다 `[R04:L210–218]`.

`σ_age`도 단순한 시계가 아니다. 오래된 정도가 소산 양상과 반응 방식을 바꾸는 경로 의존 요약이다.

```text
같은 양의 미해결 부담
+ 다른 경과 시간·반복·고착
→ 다른 반응 profile
```

따라서 `σ_age`를 “늦으면 무조건 이자가 붙는다”로만 읽으면 원래 뉘앙스를 잃는다. 더 가까운 뜻은:

> 오래되면 같은 양도 다른 방식으로 몸과 선택을 구속할 수 있다.

### 5.2 Store와 Bill

`R04–R05`에서 흐름은 다음과 같다.

```text
Cosmetic / deferred relief
→ pledge 또는 Receipt
→ Store
→ σ, σ_age
→ soft 또는 hard dissipation
→ Spend / heat / lock / margin 변화
```

`[R04:L264–290; R05:L244–265]`

여기서 Bill은 한 뜻으로 안정되지 않는다.

1. 앞으로 내야 할 청구액
2. 몸·환경에서 실제로 나타난 후과
3. 그 후과가 원장에 게시된 line item

이 세 의미가 섞이면 “빚이 존재함”, “청구가 발행됨”, “결과가 발생함”, “상환이 끝남”이 하나가 된다.

```text
Obligation
≠ BillIssued
≠ ConsequenceRealized
≠ Settlement
```

위 구분은 0118 원문의 완성 타입이 아니라 후대 분석에서 필요한 교정이다.

### 5.3 raw repair와 σ settlement

당일 후기 `CON06`은 둘을 분리한다.

- raw residual과 `σ`는 서로 직접 상쇄하지 않는다.
- `σ` 감소는 등록된 settlement/repayment 경로로만 가능하다.

`[CON06:L81–104]`

이는 중요한 교정이다.

```text
현재 문제를 실제로 고침
≠ 과거에 부담을 옮긴 책임이 자동 소멸함

과거 의무를 정산함
≠ 현재의 물리 문제가 자동 해결됨
```

둘은 같은 사건에서 함께 일어날 수 있지만 같은 관계는 아니다.

반대로 2026-03-07의 후기 설명 거울 `EXPL18`은 `PaidRepair`라는 표현으로 raw 감소와 `σ` 감소를 다시 가깝게 묶는다 `[EXPL18:L341–397]`.

> **[LATE REGRESSION]** 시간상 `CON06`이 `EXPL18`을 교정한 것이 아니다. 당일 헌법이 먼저 분리를 닫았고, 3월 설명본이 그 모호성을 부분적으로 되살렸다.

### 5.4 미룸의 여러 종류가 아직 한 σ에 뭉친다

0118에는 다음을 구분하는 독립 타입이 없다.

```text
정당한 보류
예약된 정산
부분 상환
무지급
상환 불능
타자의 자발적 인수
면제·용서
회복 불가능한 손실
```

`pledge→σ→Bill`이 이 모두를 하나의 “나중에 돌아오는 부담”으로 압축한다.

> **[TYPE RESIDUE]** 지속된 불일치는 잘 포착했지만, 책임의 근거·부담자·수혜자·면제 권한·정산 조건은 아직 없다.

---

## 6. STG06–062 — 철학을 실행 계약으로 만들다

### 6.1 STG의 입력과 출력

`STG2`는 외부 입력 `X`, mark, state를 받아 여러 projection·candidate·policy·commit·action을 산출하는 단일 전이를 만든다 `[STG2:L149–159, L640–760]`.

Chapter 05의 공장이 배선 문법을 만들었다면, 0118 STG는 그 위에 다음 코어를 얹는다.

```text
EvidenceCore
LedgerCore
SigmaCore
CtrlSolve
Commit
```

하지만 이 이름들이 현행 타입과 같다는 뜻은 아니다. 특히 `EvidenceCore`가 claim-specific EvidenceLink를 발행하지 않고, `LedgerCore`가 실제 world outcome을 받지도 않는다.

### 6.2 subtract에서 allowlist로

초기 `Π_wit`는 policy·view·story 같은 금지 필드를 빼는 subtract 방식에 가깝다. 곧 문제가 생긴다.

```text
새 field가 생김
→ 금지 목록에는 아직 없음
→ 의도치 않게 Witness에 섞일 수 있음
```

`STG2`는 이를 `WitnessSchema` allowlist와 default deny로 바꾼다.

```text
Π_wit(S) := ProjectBySchema(S, WIT_SCHEMA[version])
```

- 등록되지 않은 새 필드는 증거가 아니다 `[STG2:L163–179]`.
- 판정 연산자는 `Π_wit + RawSlice/Witness`만 읽는다 `[STG2:L183–191]`.
- `GateRaw`와 `TR_perc`는 독립 경로다 `[STG2:L211–248]`.
- Witness 밖의 것을 추가 근거로 읽지 못한다 `[STG2:L252–270]`.

`RSUM`은 이 변화의 이유를 명시한다.

- subtract-only로는 부족하다.
- Registry와 HardExclude가 함께 필요하다.
- Witness 충분성은 함수 금지 목록이 아니라 데이터 계약이어야 한다.

`[RSUM:L171–190]`

> **[LINEAGE]** Witness는 더 이상 “현실의 본질”이 아니라 버전이 고정된 admissible evidence contract가 된다.

### 6.3 PayloadFirewall과 read-cap

`STG1–STG2`는 Receipt payload가 원장·손상·raw residual의 근거로 역류하지 못하도록 전용 경로를 만든다. `EvidenceCore`, `SigmaCore`, `LedgerCore`도 읽을 수 있는 payload를 제한한다 `[STG2:L550–608]`.

이는 Chapter 05의 key-level closure를 의미론에 적용한 것이다.

```text
값이 존재함
≠ 모든 함수가 읽을 수 있음

오래 저장됨
≠ 판정 근거가 됨
```

여기서 Chapter 02에서 발견한 `Persistence ≠ Authority`가 새 형태로 돌아온다.

### 6.4 LedgerCore 안에서 운영비와 raw 판정이 다시 만난다

`STG2`의 `LedgerCore`가 `PercIn`과 policy를 읽는 것 자체가 곧 위반은 아니다. 실제 처리 비용·Spend·운영 제약은 사람이 선택한 policy와 지각 처리에 따라 달라질 수 있다.

문제는 같은 `LedgerCore`가 그 입력들을 읽으면서 `Spend/h/e/ΔQ/q_lock/q_rate`뿐 아니라 `ΔQ⊥_raw`까지 함께 갱신한다고 적힌 점이다 `[STG2:L585–595]`.

> **[ROLE AMBIGUITY][CONDITIONAL CONFLICT]** operational cost가 policy 영향을 받는 것과 evidence-derived raw residual이 policy-independent해야 한다는 것을 한 writer signature에 섞었다. policy/PercIn read 자체는 합법일 수 있지만, 그 입력으로 raw를 재계산하거나 판정 근거처럼 기록하면 충돌한다. `OperationalCostCore ≠ OutcomeLedgerCore ≠ EvidenceCore ≠ ObligationCore`가 아직 타입으로 갈리지 않았다.

> **[INFERENCE]** 이 field-level 혼합은 후기 헌법이 `Grounds`와 `Influence`를 역할 관계로 다시 정의할 필요를 보여주는 압력으로 읽힌다. 직접 발명 원인으로 문서화되었다는 뜻은 아니다.

---

## 7. 부정적 폐쇄의 성공과 양의 증거 경로의 부재

### 7.1 0118이 잘 닫은 것

0118은 다음 역류를 강하게 막는다.

```text
View / Story / policy
↛ Witness
↛ raw residual
↛ same-commit ledger grounds

Receipt payload
↛ Evidence
↛ external fact
```

이는 “내가 그렇게 느낀다”가 곧바로 “외부 세계가 그렇다”가 되는 것을 막는다.

### 7.2 무엇을 새 Evidence로 발행하는가는 비어 있다

하지만 default deny는 합법 입력을 스스로 만들지 못한다. 0118에는 다음이 충분히 타입화되어 있지 않다.

```text
어떤 claim을 확인하려는가?
누가 observation을 호출했는가?
어떤 instrument와 method를 썼는가?
source provenance는 무엇인가?
coverage와 uncertainty는 얼마인가?
artifact가 어느 claim을 어떤 scope에서 지지하는가?
누가 이를 인증했고 언제까지 유효한가?
```

현행 문법으로 쓰면 빠진 경로는 이렇다.

```text
subjective signal
→ Observation Call
→ instrumented collection
→ ObservationEvent(
     EvidenceArtifact,
     EvidenceLink[s],
     method,
     source provenance,
     coverage,
     uncertainty
   )
→ Certification
→ Application
```

0118은 Raw와 일부 상태 요약을 Witness라는 넓은 판정 입력 묶음으로 모은다. 그러나 Call·Artifact·EvidenceLink·Certification·Application을 그 안에 실제로 표현하지는 않는다. 이 단계들은 압축되었다기보다 부재하거나 다른 함수명 속에 흩어져 있다.

따라서 **누가 들어오지 못하는가**는 잘 말하지만 **새로운 증거가 어떻게 claim-specific하게 들어와 인증·적용되는가**는 닫지 못한다.

### 7.3 schema gap

allowlist는 오염을 막지만 살아 있는 시스템에는 다른 위험을 만든다.

```text
등록되지 않은 현상
→ 증거가 아님
→ false로 취급될 위험
→ 새로운 손상·체험·환경 변화를 영원히 못 봄
```

정확한 봉인은 다음이어야 한다.

```text
unregistered ≠ false
undefined ≠ disproved
schema gap → observation / schema-update proposal
```

0118에 schema 변화의 흔적이 전혀 없는 것은 아니다.

- `STG2`는 addendum-only version event를 둔다 `[STG2:L176–180]`.
- `LINK18`은 schema version event를 말한다 `[LINK18:L102–113]`.
- `TEM18`은 monotonic·nonretroactive 변경과 calibration debt를 시도한다 `[TEM18:L153–165]`.

그러나 issuer, 필요한 evidence, 승인 Warrant, certification, application 전이를 끝까지 묶지는 않는다. 즉 **schema versioning은 있으나 lawful schema issuance는 미완성**이다.

> **[OPEN]** 스키마 변경 자체를 proposal–evidence–certification–application 전이로 다루는 구조는 후대에 필요해진다.

---

## 8. View를 막다가 Influence까지 잃다

### 8.1 느린 도핑의 의심

`LINK18`에서는 아직 다음 경로가 보인다.

```text
View / SelectWitness
→ CtrlSolve
→ policy_next
```

`[LINK18:L209–219]`

이후 `PATCH18`은 세 단계로 이 경로를 좁힌다.

1. `AXH-vA0.1`은 `ViewOut` 직접 참조를 차단하지만 아직 `S/PercIn` 직접 입력과 미래 `Bill/Record` 참조를 남긴다.
2. vA0.2는 미래참조를 `bill_posted_{t-1}` 쪽으로 고친다.
3. vA0.4는 앞 판을 supersede하며 `CtrlSolve`를 handle-only 쪽으로 밀어붙인다 `[PATCH18:L390–490]`.

이유는 풍부한 View가 낮은 대역의 policy knob를 통해 천천히 Evidence/ledger를 오염시키는 측면채널이 될 수 있기 때문이다.

### 8.2 과잉 봉인

이 패치가 모든 체험 신호를 지운 것은 아니다. 통증·공포가 이미 `PercIn/PhysSig`에 부호화되어 있다면 upstream 보호 신호로 남을 수 있다.

지워질 위험이 큰 것은 풍부한 `ViewOut`에서 새로 형성된 고차 의미·서사·자기해석의 직접 제어 경로다.

- “이 상황은 예전과 같은 위협이다”라는 자기해석
- 관계 의미가 탐색 순서를 바꾸는 것
- 감정의 명명으로 휴식·거리두기·도움 요청을 고르는 것
- 이야기 전체의 맥락이 전략을 재배치하는 것

이들은 외부 사실의 근거가 아니지만 실제 causal influence다.

> **[OVER-CLOSURE]** `Qualia is not Grounds`를 지키려다 View에서 새로 형성된 의미가 합법적 Influence로 번역되는 길까지 막을 위험이 생겼다.

### 8.3 저대역 Control bus로 남은 Influence를 형식화하다

bounded `CtrlCtx`의 최초 구성은 `PATCH18` vA0.4와 이를 흡수한 `FULL18`에 있다 `[PATCH18:L513–542; FULL18:L587–607]`. `RUN18`은 `CTX_SCHEMA`, 양자화, bit cap을 더 명시해 강화한다 `[RUN18:L785–829]`.

```text
rich narrative/view
↛ direct control

bounded features
→ CtrlCtx
→ policy_next
```

이로써 남아 있던 체험 신호는 제한된 channel capacity를 가진 Influence로 형식화된다. 그러나 무엇이 합법 feature인지, 사람의 의미가 압축 중 얼마나 손실되는지는 별도 문제로 남는다.

더 큰 충돌도 있다. `RUN18`의 `CtrlObsHandle`은 `RawSlice / Witness / ΔQ⊥_raw / dm_phys`에서 직접 mint되어 policy 쪽으로 전달된다 `[RUN18:L741–743]`. bounded handle이라도 Grounds digest를 포장해 Control로 옮기면 두 관계가 다시 결합할 수 있다.

후기 `VES18`은 이를 더 엄격하게 교정한다.

- policy feature가 Raw/Witness를 직접 참조하면 hidden evidence path로 실패한다 `[VES18:L147–149]`.
- 필요하면 등록된 `Raw→View` 단방향 요약을 사용한다 `[VES18:L168–172]`.

> **[REAL CONFLICT][FUNCTIONAL CORRECTION]** 합법 Influence는 Grounds를 작은 handle로 포장한 것이 아니라 별도 계약의 influence feature여야 한다.

---

## 9. ActionOut의 역설 — 실행 영수증이 행동보다 먼저 생긴다

### 9.1 후보와 행동 출력은 있다

`STG2`에는 후보 생성, 선택, `ActionOut`이 있다 `[STG2:L447–477]`.

겉으로 보면 pledge/Receipt가 실제 행동의 비용을 기록할 수 있을 것 같다. 그러나 단일 전이 순서를 따라가면 문제가 드러난다.

```text
이전 tick lane:
pledge_{t-1}
→ SigmaCore / Store
→ σ / Bill / core Commit

현재 tick lane:
current knob / Witness / eff
→ pledge_next mint
→ Attach(next-tick payload)

두 lane의 Commit/Attach가 끝난 뒤
→ ActionOut 산출
```

`[STG2:L612–624, L640–760]`

현재 `pledge_next`가 같은 tick의 Store로 곧장 들어가는 것은 아니다. Store가 읽는 것은 이전 `pledge_{t-1}`이고, 새 payload는 다음 tick용으로 Attach된다. 그러나 **현재 Receipt mint가 ActionOut보다 먼저**라는 결손은 그대로다. Commit/Attach 역시 몸과 세계의 결과를 받기 전에 끝난다.

### 9.2 이 Receipt가 증명할 수 있는 것

따라서 후기 pledge/Receipt가 보증할 수 있는 범위는 좁다.

```text
이 knob 구성을 선택했다
또는
이 전략을 실행하도록 시스템을 설정했다
```

다음을 보증하지는 못한다.

```text
몸이 실제로 허가했다
행동이 수행되었다
외부 세계에 도달했다
의도한 결과가 발생했다
그 결과가 독립적으로 관측되었다
```

즉:

```text
Choice
≠ StrategyAdoption
≠ BodyAuthorization
≠ PerformedAction
≠ ExternalOutcome
≠ ObservedOutcome
```

### 9.3 몸의 부재

원문은 몸을 Witness의 핵심 매질로 자주 부르지만 실행 구조에는 독립 `BodyState`, body veto, motor execution, pain, recovery가 없다.

`dm_phys`도 실제 조직 손상 자체라기보다:

```text
max(0, RepairLowerBound − RepairBudget)
```

에 가깝다 `[STG2:L352–360]`.

> **[BRIDGE: 현행 재명명]** 그러므로 이름은 Damage보다 `UnmetRepairDemand`가 더 정확하다.

> **[TYPE RESIDUE]** 몸은 진실을 남기는 매질로 호출되지만 실제 허가·수행·후과를 가진 actor로 구현되지 않았다.

> **[BRIDGE/INFERENCE]** 이 결손은 구조상 typed `EventRecord`, execution receipt, outcome observation을 요구한다. 직접 문서 승계가 확인되었다는 뜻은 아니다.

---

## 10. 이론 재서술 — Projection은 서로 다른 질문이 된다

### 10.1 같은 접촉에 여러 질문을 던지다

`THEORY18`은 실행 projection들을 단순 접근제어가 아니라 질문의 분리로 재해석한다.

```text
Π_phys : 비용·제약에 대해 무엇을 묻는가
Π_perc : 의미·감정에 대해 무엇을 묻는가
Π_view : 인간에게 어떻게 보이는가
Π_wit  : 무엇을 증거로 인정하는가
Π_ctrl : 운영에 필요한 요약은 무엇인가
```

`[THEORY18:L73–91]`

이 재서술은 중요한 진전이지만 이 판본은 같은 입력을 비용 질문과 의미 질문이 공유하면 붕괴한다고까지 말한다 `[THEORY18:L88–91]`.

후기 `CON06`은 이를 더 정확하게 고친다. 같은 세계 접촉에서 여러 projection이 나오는 것은 가능하지만, **입력을 공유한다고 Grounds를 공유하는 것은 아니다** `[CON06:L139–145]`.

```text
same source contact may feed multiple projections
≠ one projection may borrow another projection's grounds
```

오류는 출처 접촉의 공유 자체가 아니라 한 projection의 결과를 다른 역할로 무검사 cast하는 것이다.

### 10.2 0118에서의 임피던스 재명명

같은 문서는 `Φ`를 다음처럼 설명한다.

> 내가 세계에 닿는 느낌의 임피던스 표면.

`[THEORY18:L350–357, 의역]`

이는 Qualia의 최초 탄생이 아니다. 0113 `연구/PARADIM/qualia.txt`에 이미 전용 Qualia Surface 정의가 있었고, 0118은 그 현상을 Witness/Billing 헌법 안에서 **비권위적 임피던스 표면으로 재배치**한다. 이후 0121은 이를 인간 런타임 안에 압축 통합하고, 0122 `연구/fucstrees/0122 newqual.txt`는 다시 매질 메트릭으로 분해한다.

> **[CURRENT LENS]** 아래 번역은 0118의 직접 Ghost 공식이 아니라 최신 자아 모델로 이 표현을 다시 읽은 것이다.

```text
세계/몸/기억의 접촉
→ Ghost가 접근할 때 생기는 마찰·가까움·무게·색조
→ 행동 후보와 의미 지형을 바꿈
```

하지만 이 표면은 외부 사실을 확정하는 Witness가 아니다.

```text
Qualia may cause Influence.
Qualia does not self-issue Grounds or Authority.
```

### 10.3 “표면은 원인이 아니다”라는 과장

`THEORY18`은 한편으로 표면·의미가 원인이 아니라고 말하고 `[THEORY18:L124–133]`, 다른 곳에서는 표면과 의미가 행동·정책을 바꾼다고 말한다 `[THEORY18:L312–345]`.

> **[REAL CONFLICT]** “비원인”은 너무 강하다. 살아남을 봉인은 “비근거·비권위”다.

### 10.4 PhysSig의 역할 모호성

같은 문서는 `PhysSig := Π_phys(S, PercIn)`을 ledger ground처럼 두는 구간이 있다 `[THEORY18:L202–215]`. 그러나 `PercIn`은 policy-shaped 성분을 포함한다.

`PhysSig`가 policy가 만든 실제 운영비·행동 효과를 전달하는 causal input이라면 합법 Influence일 수 있다. 외부 사실이나 `ΔQ⊥_raw`의 최종 Grounds로 cast될 때 같은 문서의 Witness-only closure `[THEORY18:L221–228]` 및 후기 헌법 M2와 충돌한다.

> **[ROLE AMBIGUITY][CONDITIONAL CONFLICT]** 당시 “근거”가 evidentiary grounds와 causal input을 함께 뜻한다. `PhysSig(PercIn)`을 최종 Grounds로 채택할 때에만 raw/eff 분리가 무너진다.

---

## 11. Grounds와 Influence — 관계의 이름이 생기다

### 11.1 명시적 분리

`Grounds`라는 용어는 초기 공장2 문서가 아니라 후기 `CON06`에서 명시적으로 등장한다.

```text
Grounds
= 판정이 사실을 확정할 때 참조하는 입력

Influence
= 다음 변화에 반영되도록 정책에 전달되는 입력
```

`[CON06:L23–34]`

그리고 둘을 독립 검사하라고 명시한다.

```text
Grounds 규칙을 잘 지켰다고 Influence channel을 늘릴 수 없다.
Influence 규격을 잘 지켰다고 Grounds를 완화할 수 없다.
```

이것은 현행 `Influence ≠ Warrant`의 가장 직접적인 **선행 문제틀**이다. 다만 동일 명제는 아니다. 0118의 Grounds는 아직 claim·scope·epoch·jurisdiction에 묶인 relation이 아니고, Warrant도 독립 타입으로 완성되지 않는다.

### 11.2 M1–M4

후기 헌법군은 대체로 네 가지 봉인을 세운다.

```text
M1  비가역 SSOT 갱신은 Commit-only
M2  등록된 Raw/Witness만 Grounds에 참여
M3  Receipt→σ→Bill과 law/state·settlement 경로 봉인
M4  지연·저대역·감사 가능한 control Influence
```

`[CON06:L36–123; CON01:L16–112; VES18:L64–156]`

same-commit surface backflow 금지는 M1 하나의 본체가 아니라 M1+M4의 귀결이다.

판본마다 M3/M4의 세부 표기가 완전히 일치하지는 않는다. 특히 Receipt bus를 별도 world-crossing trace로 둔 `LINK18`과 “유일한 influence는 policy_next”처럼 읽히는 후기 M4 사이에는 범위 긴장이 있다.

> **[SCOPE CONFLICT]** M4의 Influence를 `control influence`로 한정하면 Receipt는 M3의 별도 accounting-imprint lane으로 공존할 수 있다. 그러나 “표면이 세계선에 닿는 유일한 길”이라는 넓은 문장은 Receipt와 충돌한다. `Control Influence / Accounting Imprint / Grounds`를 서로 다른 관계로 명시해야 한다.

### 11.3 same-tick 금지의 정확한 범위

후기 헌법의 강한 봉인은 다음이다.

> 같은 commit epoch에서 생긴 표면·정책 출력이 그 commit의 Grounds·ledger·commit decision을 다시 쓰지 못한다.

`[CON06:L36–39; VES18:L164–166]`

same-commit 조항 자체는 모든 즉시 비권위 반응을 금지하지 않는다.

- 내부 후보 재배치
- 주의 전환
- 보호 반응
- 가역적 전략 변경
- 비권위 행동 출력

> **[BRIDGE: 현행 생명 런타임 교정]** 위 반응까지 다음 tick으로 미루면 생명 런타임은 위험에 반응하지 못한다. 금지 대상은 **즉시 영향 전체**가 아니라 **같은 irreversible commit의 근거·권한 역류**여야 한다.

다만 원문 M4의 `policy_{t+1} only`를 문자 그대로 적용하면 즉시 `View→Action` 영향은 여전히 닫힐 수 있다. 즉시 보호 반응의 허용은 원문에서 완성된 회수가 아니라 현행 교정이다.

### 11.4 Authority의 자리도 좁아진다

초기 이론문은 `phys / ledger / constraint`가 Authority를 가진다고 영역 중심으로 말한다. 후기 헌법은 비가역 갱신을 실제 수행하는 `t_c Commit`만 SSOT write authority를 가진다고 좁힌다.

```text
physical or evidentiary role
≠ irreversible write capability
```

> **[FUNCTIONAL CORRECTION]** Authority는 “물리적인 것”이 본질적으로 가진 속성이 아니라, 특정 전이를 SSOT에 비가역 적용할 수 있는 capability가 된다. Witness는 Grounds를 제공할 수 있지만 write authority를 갖지 않는다.

---

## 12. 보편 청구로의 팽창 — 모든 연결은 비용을 남기는가

### 12.1 좁고 강한 직관

0118이 보존해야 할 핵심은 다음이다.

> 현재의 이득이 실제 미해결 비용을 미래·몸·타자에게 옮겨 얻어진 것이라면, 그 이월은 흔적 없이 사라질 수 없다.

이 명제는 생명·책임·회계에 모두 유용하다.

### 12.2 모든 표면 완화가 빚이 되는 순간

팽창은 한 번에 일어나지 않는다.

```text
R05:L45–52
CosmeticRelief로 분류된 완화가 pledge를 남김
— 아직 좁은 규칙

THEORY18:L17–24
CON06:L81–84
VES18:L104–107
표면 조작 일반이 Receipt→σ→Bill로 넓어짐

EXPL18:L378–391
2026-03-07 후기 설명에서 raw/eff 차액 공식으로 강하게 재서술
```

후기 판본으로 갈수록 raw가 그대로인데 eff가 좋아지면 거의 자동으로 debt가 생기는 방향으로 확장된다.

그러면 다음도 모두 의심스러운 채무가 된다.

- 외부화되지 않은 가역적 사고실험
- 정확한 재해석
- 안전 확보 뒤의 안도
- 학습으로 줄어든 마찰
- 정당한 휴식
- 주의의 정상 조절
- 단순히 달라진 Qualia

이것은 완충지대를 없앤다.

```text
Qualia 변화
= Grounds 변화 아님
= 외부 현실 변화 아님
≠ 가짜 변화
≠ 자동 부채
```

### 12.3 Conn→Imprint side branch

`TEM18`은 문제를 모든 연결로 넓힌다.

```text
Conn
→ Imprint(C / R / S)
→ flux × resistance
→ 최소 비용·담보·잔여
```

`[TEM18:L198–233, L256–305]`

연결이 흔적을 남긴다는 직관은 생명 경계 연구에 매력적이다. 그러나 `ConnFlux × Resistance`가 보편 청구 하한이라는 주장은 코어 공리에서 자동으로 나오지 않는 새 물리 가정이다.

> **[SIDE BRANCH][HOLD]** “모든 접촉에는 변환 비용이 있다”와 “모든 접촉은 채무를 낳는다”를 구분해야 한다.

최소한 다음은 갈라야 한다.

```text
MetabolicCost
RepairDemand
DeferredObligation
TransferredBurden
IrreversibleLoss
NormativeResponsibility
```

비용이 존재한다는 것과 누군가에게 빚을 졌다는 것은 같지 않다.

---

## 13. 역사 본문의 결론 — 자기기만은 가능하지만 지속 가능하지 않게

0118은 인간이 자신을 속일 수 없다고 가정하지 않는다. 오히려 상상·주의·표현·전망을 바꾸는 능력을 Control/View 쪽에 남긴다.

그 대신 다음을 시도한다.

```text
표면을 바꿀 자유는 보존
판정 근거를 자가 발행할 권한은 차단
미뤄진 실제 부담은 별도 상태로 보존
현재 policy가 미래 청구 법칙을 바꾸는 것은 차단
```

그래서 이 장을 가장 압축하면:

> **자기조작은 가능하되, 자기조작이 자신의 증거와 청구 법률을 동시에 다시 쓰지는 못하게 한다.**

이 설계는 큰 성공을 거둔다.

- raw와 eff가 갈린다.
- Witness와 View가 갈린다.
- Receipt와 Evidence가 갈린다.
- 현재 체감과 미래 부담이 갈린다.
- Grounds와 Influence가 처음 이름을 얻는다.

그러나 네 개의 빈자리를 남긴다.

1. 1인칭 체험 자체의 제한된 사실성
2. 새로운 evidence를 합법적으로 발행하는 양의 경로
3. 몸의 허가·실제 행동·외부 결과·관측 결과의 분리
4. 비용·수리 요구·연기·전가·책임을 가르는 typed obligation

이 빈자리가 이후 인간 모델과 현행 TAD가 다시 만나야 할 자리다.

---

# 연구 후기 — 현행 이론으로 역조명하되 소급하지 않기

## A1. 이번 장의 실제 수확

### A1.1 Influence와 Grounds는 서로 다른 관계다

0118의 가장 큰 수확은 “감정은 믿으면 안 된다”가 아니다.

```text
어떤 것이 행동을 바꿀 수 있음
≠ 그 값이 외부 사실을 확정할 근거임
≠ 그 값이 irreversible write 권한을 가짐
```

Qualia·서사·공포·사랑은 실제 행동을 바꿀 수 있다. 그것을 비원인으로 만들 필요는 없다. 다만 자신이 촉발한 판정을 스스로 인증해서는 안 된다.

### A1.2 Persistence와 Authority 사이에 Receipt가 들어온다

Chapter 02의 JOT는 오래 남지만 권위가 없는 흔적이었다. 0118 Receipt도 마찬가지로 저장되지만 Evidence는 아니다.

```text
durable
≠ authoritative
≠ evidentiary
≠ debt by itself
```

여기에 새 구분이 추가된다.

> 내부 control 조작·strategy configuration 기록이 오래 남는 것과, 실제 행동이 수행되었거나 그 조작이 부담 전가를 만들었다는 판정은 각각 별도다.

### A1.3 obligation은 보존량이 아니라 typed relation이어야 한다

`σ`의 장점은 이월된 불일치가 시간을 건너며 경로 의존성을 가진다는 점이다. 약점은 그것을 하나의 보편 부채처럼 다룬다는 점이다.

현행 관점에서는:

```text
Obligation(
  source,
  actor,
  historical_author,
  beneficiary,
  current_bearer,
  stake_scope,
  responsibility_scope,
  authority_scope,
  identity_impact,
  consent_or_acceptance,
  settlement_condition,
  evidence,
  expiry_or_end_condition
)
```

같은 관계가 필요하다. 다만 SelfBoundaryProfile의 Stake·Identity·Belonging은 obligation을 자동 생성하는 원장이 아니라 `ObligationAssessment`가 읽는 문맥이다.

이는 원문에 없던 `[BRIDGE]`다.

---

## A2. 현행 TAD v7-dev4 typed candidate와의 비교

아래 비교 대상은 승인된 final canon이 아니라 현재 보존된 `v7-dev4 TYPED-CANDIDATE`다. `Ω_wit / Ω_ops / Ω_bill` 역시 보편 보존량이나 승인 정본으로 읽지 않는다.

### A2.1 비동일성 표

| 0118 개념 | 현행에서 가장 가까운 역할 | 동일하지 않은 것 |
|---|---|---|
| `RawSlice` | gate를 통과한 evidence candidate payload | organismal raw, world truth |
| `Witness` | admissible evidence bundle | EvidenceLink, EventRecord, CertifiedEvent |
| `Grounds` | claim을 지지하는 관계의 선행 문제틀 | Warrant 자체 |
| `View / Qualia` | private influence-bearing surface | external evidence by default |
| `pledge` 초기형 | strategy declaration | performed receipt |
| `Receipt` 후기형 | control-operation/configuration mint trace의 전조 | performed-action receipt, EvidenceLink, outcome evidence |
| `σ` | carried mismatch / obligation precursor | 모든 residue, 모든 debt |
| `Bill` | obligation realization·posting 전조 | settlement 자체 |
| `Commit authority` | irreversible write capability | truth, certification |

### A2.2 현행 외부 사실 경로

현행 TAD가 0118보다 더 잘 가른 경로는 다음이다.

```text
source
→ EvidenceArtifact
→ claim-specific EvidenceLink
→ ObservationEvent
→ CertifiedEvent
→ AppliedRecord
```

그리고:

```text
Receipt ≠ EvidenceLink
Candidate ≠ Call
Call ≠ EventRecord
EventRecord ≠ CertifiedEvent
CertifiedEvent ≠ AppliedRecord
```

0118 Witness를 이 전체의 직접 선조라고 쓰면 과장이다. 정확한 판정은 **강한 문제 선행 + 일부 domain precursor**다.

### A2.3 Grounds도 claim-specific relation이어야 하며, Warrant와 동일하지 않다

0118은 어떤 값이 Witness에 들어가면 여러 판정에 두루 쓰일 수 있는 것처럼 보인다. 현행 Bridge에서는 같은 artifact도 claim에 따라 지위가 달라야 한다.

```text
Grounds(
  artifact,
  claim,
  scope,
  method,
  coverage,
  uncertainty
)
= 이 artifact가 이 claim을 어느 범위에서 지지하는가

Warrant(
  grounds_ref,
  rule,
  epoch,
  jurisdiction,
  authority_scope
)
= 그 Grounds를 바탕으로
  누가 무엇을 말하거나 판정할 권한을 얻는가
```

이 관계화는 0118 원문 정의가 아니라 `[BRIDGE]`다. 0118의 Grounds는 아직 “판정이 읽도록 허용된 입력 역할”에 더 가깝다.

예를 들어 심박 상승은:

- “심박이 상승했다”에는 강한 ground일 수 있다.
- “그 사람이 공포를 느꼈다”에는 제한된 간접 근거다.
- “외부 위협이 실제로 존재했다”에는 충분하지 않다.

### A2.4 current Ω와 σ의 관계

현행 temporal sustain은 obligation을 적어도 다음처럼 가른다.

```text
Ω_wit   : 필요한 witness·verification
Ω_ops   : 운영·용량·유지 의무
Ω_bill  : 비용·정산 의무
```

이는 0118 `σ`의 직접 이름 변경이 아니다.

- 직접 domain precursor: unresolved state가 time boundary를 건넌다.
- 구조적 유비: obligation은 typed하게 유지·감소된다.
- 현행 교정: obligation migration은 보존법칙이 아니다.

의무는 증빙, 용량 회복, 합법적 scope 종료, claim 철회, 조건 변화로 닫힐 수 있다. 모든 감소가 “같은 양을 갚았다”는 뜻은 아니다.

---

## A3. 1인칭 체험의 사실성 — Witness closure가 놓친 것

### A3.1 세 문장은 다르다

0118의 전면적 `View→Evidence` 금지는 다음을 충분히 구분하지 못한다.

```text
나는 통증을 느꼈다.
내 몸에 조직 손상이 있었다.
나는 통증이 있다고 말했다.
```

- 발화 기록은 “그가 통증을 보고했다”를 ground할 수 있다.
- 생체 계측은 “조직 손상 징후가 있었다”를 ground할 수 있다.
- 둘 다 “그 Ghost에게 통증이 무엇처럼 주어졌다”를 완전히 대신하지 못한다.

주관 체험을 외부 세계의 보편 증거로 승격하면 안 된다. 그렇다고 체험이 발생했다는 사실까지 0으로 만들 수도 없다.

### A3.2 PrivateExperienceEvent / Trace / SelfReport

따라서 하나의 Trace가 체험을 자동 인증하게 하지 말고, 최소한 세 역할을 갈라야 한다.

```text
PrivateExperienceEvent
= 현재 Ghost-state 안에서 발생한 1인칭 phenomenal exposure

PrivateExperienceTrace
= phenomenal exposure가 local store에 등록된 evidence candidate

SelfReportReceipt
= 당사자가 그 체험을 그렇게 보고했다는 수행 기록

Public EvidenceLink
= 보고·계측 artifact가 특정 public claim을
  어느 scope에서 지지하는가
```

`PrivateExperienceTrace`는 선언된 first-person claim profile 안에서 experience-occurrence를 제한적으로 지지할 수 있다. 그러나 외부 원인·타인의 의도·공적 세계 상태·후대 Ghost의 자기 인수를 자동 보증하지 않는다.

이는 0118 원문에 없는 `[BRIDGE]`다.

중요한 것은 “주관도 진실이다”라는 무제한 승격이 아니라 claim scope를 좁히는 것이다.

```text
experience occurrence
≠ experience interpretation
≠ external cause
≠ public fact

PrivateExperienceTrace stored
≠ later Ghost can access it
≠ later Ghost remembers it
≠ later Ghost adopts it as “my experience”
```

### A3.3 Ghost의 합법 경로

사용자의 최신 Ghost 정의를 붙이면 경로는 다음처럼 보인다.

```text
organismal raw
→ Ghost의 가역적 변형
→ Qualia / candidate / strategy
→ bounded Influence
→ 행동·질문·관측 요청
```

그리고 외부 claim을 ground하려면 한 번 더 세계로 나가야 한다.

```text
subjective signal
→ observation Call
→ independent contact
→ artifact + method + provenance
→ claim-specific EvidenceLink
```

0118은 첫 경로의 `Raw/Perc/View` 구조적 윤곽과 넓은 `Witness` 종점을 보았지만, organismal transduction·Ghost·Call·artifact·claim-specific link는 만들지 못했다.

---

## A4. Ghost와 부채 — 완충지대를 살리는 교정

### A4.1 현재형 자아인 Ghost의 변화는 실제지만 비권위적일 수 있다

Ghost는 완충 기능 하나의 이름이 아니라, 지금 들어오는 raw를 어떻게 변형해 받아들이고 어떤 후보와 전략을 외부화할지 고르는 **현재형 자아**다. 그 내부의 가역적 sandbox에서는 극단적 사고실험도 가능하다. 그 사고가 존재했다는 것과 외부 행동·원장 사건이 일어났다는 것은 다르다.

```text
Ghost_t
= IntakeTransform_t
 + ReversibleCandidateField_t
 + StrategySelection_t
 + FirstPersonSurface_t

DiachronicSelf
= Ghost_t
 ⊗ StorageAccess_t
 ⊗ ContinuityBinding_t
```

다만 Ghost의 통시적 자아성은 스스로 영구한 실체라서 생기지 않는다.

```text
현재 Ghost
→ 저장소에 흔적을 남김
→ 다음 Ghost가 기억·서사·의무를 재수화
→ 앞선 인수를 자기 것으로 handoff
```

이 연결이 기억 상실·격리·분리로 끊기면 새 Ghost가 같은 몸에서 나타나도 앞선 자아의 연속성을 자동으로 갖지 않는다. 그러므로 **Ghost는 국소적으로 자아이고, 저장소와 인수 사슬이 그 자아의 통시성을 만든다.** 완충지대는 본체가 아니라 그 자아가 가진 기능이다.

```text
stored trace
≠ current Ghost access
≠ recall
≠ self-adoption
≠ authorship inheritance

same body and public worldline
≠ same memory access
≠ same phenomenal authorship
≠ same Ghost continuity
```

여기서 Ghost가 받는 organismal raw와 0118의 `RawSlice`도 다시 구별해야 한다. 전자는 현재 자아가 해석하기 전의 감각·몸 신호이고, 후자는 특정 판정을 위해 이미 gate와 schema를 통과한 evidence-side 입력이다.

0118의 이분법은 이런 변화를 둘 곳이 부족하다.

```text
단순 view gauge
또는
authoritative σ debt
```

그 사이에 다음 층이 필요하다.

> 지속할 수 있지만 비권위적이고, 실제이지만 반드시 채무는 아닌 내부 지형.

재프레이밍이 기억 접근·후보 선택·행동 가능성을 바꾸면 실제 내부 변화다. 다만 그 변화만으로 외부 사실이나 debt가 되지 않는다.

### A4.2 Receipt가 필요한 조건

모든 Ghost 변형에 Receipt를 발행할 필요는 없다.

```text
reversible sandbox transform
→ 기본적으로 debt Receipt 없음

ordinary regulation
→ 실제 사용한 대사·주의 자원만 cost로 기록 가능

deferral / burden shift
→ typed Receipt와 obligation assessment 필요

actual repair / settlement
→ 서로 다른 감소 경로
```

`Receipt → Obligation`은 자동 cast가 아니다. 등록된 obligation rule이 actor·action·outcome·scope·bearer에 적용될 때에만 특정 obligation이 성립한다.

현재 이득 없이도 피해, 약속 위반, 역할 책임, 실패한 행동으로 의무가 생길 수 있다. 아래 조건은 모든 debt가 아니라 0118이 직접 다루던 **ReliefDeferralObligation** subtype에만 해당한다.

```text
ReliefDeferralObligation ⇔
  present relief realized
  ∧ unresolved burden displaced
  ∧ bearer and scope identified
  ∧ applicable obligation rule exists
  ∧ causal provenance is bound
```

즉 configuration Receipt는 obligation assessment의 한 입력일 뿐 debt 그 자체가 아니다.

### A4.3 새 흐름

0118을 현행 인간 모델로 다시 쓰면 다음 정도가 적절하다.

```text
organismal contact / afferent signal
→ Ghost transformation / Qualia
→ StrategyCandidate
→ Body authorization / veto
→ PerformedAction
   ├─→ PerformedActionReceipt
   └─→ external OutcomeEvent
       → ObservationEvent + EvidenceLink
→ ObligationAssessment
   ├─ NONE
   ├─ ImmediateCost
   ├─ RepairDemand
   ├─ DeferredObligation
   └─ TransferredBurden
→ Settlement / Default / Loss
```

이 흐름 전체는 원문에 있지 않다. 0118의 결손이 무엇을 요구하는지 보여주는 `[BRIDGE]`다.

---

## A5. 생명과 자기 경계 — σ를 누구의 부담으로 볼 것인가

### A5.1 생명은 미해결 불일치를 운반한다

생명을 우주의 변화 흐름 속에서 형태를 유지하는 존재로 보면 `σ`는 도덕적 빚보다 넓게 읽을 수 있다.

> 생명 경계를 유지하기 위해 아직 통합·수리·배출하지 못하고 시간 너머로 운반 중인 불일치.

이 해석은 유용하지만, 다시 모든 불일치를 한 부채로 만들면 안 된다.

### A5.2 부담자와 수혜자

같은 형태 유지도 부담의 위치가 다르다.

```text
현재 몸이 부담
미래의 내가 부담
가족·집단에 전가
환경이 흡수
타인이 자발적으로 인수
복구 불가능한 손실로 전환
```

0118의 단일 `S_t`에는 `beneficiary`와 `burden_bearer`가 없다. 그래서 자기 경계가 넓어질 때 책임과 권한을 구분하지 못한다.

### A5.3 내재화는 지배권이 아니다

가족의 존속과 손상이 내 유지 함수에 들어올 수 있다. 그러나 그것이 가족을 내 소유물로 만들지는 않는다.

```text
Belonging
Stake
Responsibility
Authorship
Identity
Authority
```

이 축들은 서로 다르다.

가족에 대한 `Stake / Responsibility / Identity`가 높아도, 그 사람을 대신 결정할 `Authority`는 제한될 수 있다.

0118식 obligation에 이를 붙이면:

```text
내가 그 부담을 인수함
≠ 내가 그 타자의 Grounds를 대신 정의함
≠ 내가 그 타자의 선택권을 소유함
```

> **[BRIDGE]** 확장된 자기 경계는 obligation bearer를 넓힐 수 있지만 jurisdiction을 자동 확장하지 않는다.

### A5.4 살아 있는 경계에는 두 intake와 한 escalation이 필요하다

Chapter 05에서 제안한 두 intake는 0118에서 더 선명해진다.

1. policy-independent evidence intake
2. Qualia·의미·주의를 바꾸는 influence intake

그리고 0118의 default deny를 보완하려면 세 번째 작동이 필요하다.

3. schema 밖 신호를 false로 만들지 않고 새 observation/schema proposal로 올리는 escalation

```text
Evidence intake
Influence intake
Schema-gap escalation
```

완전 개방은 형태를 흩뜨리고, 완전 폐쇄는 학습과 수리를 굶긴다. 생명 경계는 선택적 투과뿐 아니라 **새 종류의 접촉을 합법화하는 학습 절차**를 가져야 한다.

---

## A6. 계보 등급

| 0118 요소 | 판정 | 이유 |
|---|---|---|
| `Grounds ≠ Influence` | **직접 domain precursor** | 후기 헌법이 두 역할을 명시적으로 독립 검사 |
| Raw/Eff 분리 | **직접 domain precursor** | 판정용 잔여와 체감·대응용 잔여 분리 |
| Witness closure | **강한 문제 선행** | 현행 claim-specific evidence chain은 아직 없음 |
| Receipt ≠ Grounds | **직접 domain precursor** | configuration mint trace의 증거 역류 차단 |
| `σ`의 시간 지속·경로 의존 | **구조적 선행** | typed Ω와 동일 객체는 아니지만 문제 구조가 이어짐 |
| `Bill` | **부분 선행 + 과잉** | 이월 부담 보존은 유효, 모든 표면 변화 채무화는 폐기 |
| same-commit backflow 금지 | **강한 직접 선행** | 현재 influence/warrant 방화벽의 좁은 핵심 |
| Authority의 Commit capability화 | **직접 domain precursor** | phys 영역의 속성에서 irreversible write 권한으로 축소 |
| Qualia impedance surface | **재배치 지층** | 0113 전용 정의를 Witness/Billing 헌법 안의 비권위 surface로 재서술 |
| `Conn→Imprint` | **SIDE BRANCH/HOLD** | 연결 흔적 직관은 유용하나 보편 청구 하한은 미증명 |
| PrivateExperienceTrace | **새 Bridge** | 원문에 없는 1인칭 claim 타입 |
| typed obligation bearer/scope | **새 Bridge** | 원문의 단일 σ를 최신 자기 경계와 결합 |

---

## A7. 형식화하며 얻은 것과 잃은 것

| 얻은 것 | 약해지거나 빠진 것 |
|---|---|
| Witness/View 분리 | 1인칭 체험 발생의 제한된 사실성 |
| Raw/Eff 분리 | eff 변화의 실제 내적 가치 |
| WitnessSchema allowlist·version event | schema update의 issuer·evidence·approval·application |
| Evidence/Ledger/Sigma read-cap | claim·method·coverage가 묶인 Warrant |
| 자동 Receipt | 의도·선택·수행·결과의 차이 |
| policy-free Bill | 면제·불능·부분 상환·책임 scope |
| σ와 σ_age | 부담자·수혜자·타자성 |
| same-commit 봉인 | 즉시 보호 반응과 합법 Influence의 풍부함 |
| 저대역 CtrlCtx | 인간 의미가 압축 중 손실되는 방식 |
| 단일 전이 F | 몸·행동·world outcome의 독립 actor |

---

## A8. 충돌·교정 지도

| 쟁점 | 판정 |
|---|---|
| `R03` Canon_phys가 policy-shaped PercIn에서 생성 | `[TYPE RESIDUE]` — 분리 문제는 발견했으나 입력 타입 미완 |
| `R04`의 “반박 불가능한 Witness” | `[OVERCLAIM]` — `R05`가 객관적 진리 자체가 아니라고 완화 |
| `R04` obs_gain이 σ 소산 계수까지 영향 | `[FUNCTIONAL CORRECTION]` — `R05`가 Bill을 policy-free로 제한 |
| pledge의 약속 의미론과 Receipt 자동 mint | `[REAL TYPE SHIFT]` — 같은 이름 아래 promise semantics/configuration trace 혼재 |
| `pledge_t`와 `pledge_{t-1}` 표기 변화 | `[OPEN]` — state 기준/산출 tick 기준 인덱스가 섞여 double-delay 가능 |
| `STG2` LedgerCore가 PercIn·policy를 읽으며 `ΔQ⊥_raw`도 갱신 | `[ROLE AMBIGUITY][CONDITIONAL CONFLICT]` — operational-only면 안전, raw 재계산/기록이면 충돌 |
| Receipt가 ActionOut보다 먼저 생성 | `[TYPE RESIDUE]` — strategy configuration만 증명 가능 |
| `THEORY18`이 서로 다른 질문의 동일 입력 공유를 금지 | `[OVER-CLOSURE][FUNCTIONAL CORRECTION]` — `CON06`이 input 공유와 Grounds 공유를 분리 |
| `THEORY18` PhysSig가 PercIn에서 생성 | `[ROLE AMBIGUITY][CONDITIONAL CONFLICT]` — causal input이면 합법, external Grounds로 cast하면 M2 위반 |
| “표면은 원인이 아니다” | `[OVER-CLOSURE]` — 비원인이 아니라 비근거·비권위 |
| `PATCH18`의 ViewOut 전면 차단 | `[OVER-CLOSURE]` — 고차 의미의 direct Influence 손실 위험 |
| `PATCH18/FULL18` bounded CtrlCtx와 `RUN18` schema 강화 | `[FUNCTIONAL CORRECTION]` — 남은 signal의 저대역 Influence 계약 |
| `RUN18` CtrlObsHandle이 Raw/Witness digest를 Control로 운반 | `[REAL CONFLICT][FUNCTIONAL CORRECTION]` — `VES18`이 registered Raw→View 요약만 허용 |
| raw와 σ 상쇄 | `[FUNCTIONAL CORRECTION]` — 후기 헌법이 Repair/Settlement 분리 |
| `EXPL18` PaidRepair가 raw 감소와 σ 감소를 다시 접근시킴 | `[LATE REGRESSION]` — 당일 `CON06` 분리 뒤 3월 설명에서 재혼합 |
| M4 policy-only와 Receipt bus | `[SCOPE CONFLICT]` — Control Influence와 Accounting Imprint의 범위 미명시 |
| 모든 eff 개선·연결의 채무화 | `[OVERGENERALIZATION][HOLD]` |
| 서로 다른 두 addendum의 `vA0.1` 재사용 | `[PROVENANCE CONFLICT]` — AXH와 RUN/ATTACH 패치 구분 필요 |
| `PATCH18`이 supersede한다는 vA0.3 부재 | `[PROVENANCE GAP]` |

---

## A9. Recovered / Lineage / Residue / Bridge / Open

### Recovered — 원문에 직접 있었던 것

- Pressure–Repair–Relief와 RiskCarry
- Witness/Control/Storage/Bill 네 층
- `GateRaw`와 policy-shaped `TR`
- `Coverage_wit ≠ Coverage_view`
- `ΔQ⊥_raw ≠ ΔQ⊥_eff`
- CosmeticRelief와 TrueRelief
- pledge·Store·`σ`·`σ_age`·Bill
- policy가 Bill 법칙을 바꾸지 못한다는 교정
- pledge를 자동 Receipt로 바꾸는 시도
- WitnessSchema allowlist와 default deny
- schema version event와 monotonic/nonretroactive 변경 시도
- Receipt payload firewall
- EvidenceCore/LedgerCore/SigmaCore read-cap
- bounded `CtrlCtx`
- `VES18`의 Raw/Witness→policy direct digest 금지와 registered Raw→View 요약
- Qualia를 임피던스 표면으로 보는 표현
- `Grounds ≠ Influence`
- same-commit surface backflow 금지
- Authority를 Commit-only write capability로 좁힌 것
- raw와 σ settlement의 분리

### Lineage — 현행으로 이어진 것

- Influence가 있다고 Warrant가 생기지 않는다.
- 체험·서사·policy는 자신의 evidence를 자가 발행할 수 없다.
- Receipt는 external fact evidence가 아니다.
- 지속되는 상태는 권위와 별개다.
- current surface는 같은 irreversible commit의 grounds로 역류할 수 없다.
- evidence reader와 ledger writer는 capability로 제한되어야 한다.
- obligation은 사라지지 않되 typed reduction 경로가 필요하다.
- observation과 execution outcome은 독립 provenance를 가져야 한다.

### Residue — 아직 집을 얻지 못한 것

- organismal raw와 evidence raw의 명시 분리
- `PrivateExperienceTrace`
- lawful Observation Call
- method/source/calibration/coverage/uncertainty
- claim-specific EvidenceLink
- Body authorization/veto
- performed action과 external outcome
- burden bearer·beneficiary·responsibility scope
- deferral/default/incapacity/forgiveness/loss
- 지속하지만 비권위이고 비채무인 Ghost 지형
- schema gap과 lawful schema update

### Bridge — 이번 독해에서 새로 얻은 가설

- Qualia는 Ghost의 세계 접촉 임피던스 표면이고 Witness는 판정의 증거 계약이다.
- 둘은 같은 접촉에서 생길 수 있지만 서로를 대체하지 않는다.
- 1인칭 trace는 선언된 first-person claim profile 안에서 체험 발생을 제한적으로 지지할 수 있지만 외부 원인이나 공적 사실을 자동 인증하지 않는다.
- Receipt가 debt가 되려면 부담 전가·부담자·scope·규칙·provenance가 별도 판정되어야 한다.
- 자기 경계의 확장은 obligation bearer를 넓힐 수 있지만 Authority jurisdiction을 자동 확장하지 않는다.
- 생명 경계에는 Evidence intake, Influence intake, Schema-gap escalation이 함께 필요하다.

### Open — 다음 장에서 확인할 질문

1. 0119–0120에서 인간형 Ghost·Editor·Episode가 Witness/Receipt 구조에 다시 들어오는가?
2. 1인칭 체험과 외부 사실의 claim type이 분리되는가?
3. body veto와 실제 수행, world outcome을 받는 lane이 생기는가?
4. `σ`는 언제 대사 비용·수리 요구·도덕적 책임으로 갈라지는가?
5. lawful observation Call과 claim-specific EvidenceLink가 실제 타입으로 나타나는가?
6. Qualia는 “cosmetic surface”에서 독립적인 인간 현실로 복구되는가?
7. self boundary와 responsibility scope가 ledger에 연결되는가?
8. 0121은 0113 전용 정의와 0118 임피던스 재배치를 어떤 인간 런타임으로 압축하는가?
9. 기억 접근이 끊긴 현재 Ghost는 과거 Receipt와 obligation을 어떤 의미에서 인수하는가?
10. 신체적 부담자·공적 인격·과거 저자·현재 Ghost를 어떤 타입으로 분리하는가?

---

## A10. 다음 장 경계 — 0119–0120의 접합을 건너뛸 수 없는 이유

Qualia는 0113에서 이미 전용 정의를 얻었고, 0118 말미에는 “세계에 닿는 느낌의 임피던스 표면”으로 Witness/Billing 구조 안에 다시 배치된다. 0121은 최초 본편이 아니라 여러 인간 요소를 한 런타임에 압축하는 지층이며, 0122는 매질 메트릭을 다시 분리한다.

따라서 바로 0121로 점프하면 다음 재접합 과정이 사라진다.

그 사이 문서에서 확인해야 할 것이 있다.

```text
Witness / Grounds 방화벽
→ 인간형 Ghost·Editor·Episode와 어떻게 다시 접합되는가
→ 몸·행동·자기 경계가 어디까지 복구되는가
→ 그 뒤 0121 압축 통합이 무엇을 보존·혼합하는가
→ 0122가 왜 Qualia 매질을 다시 갈라야 했는가
```

따라서 다음 장은 우선 0119–0120의 접합 지층을 확인해야 한다. 문서가 실질적으로 짧은 다리라면 하나의 전이 장으로 압축하고, 별도 돌연변이가 있다면 독립 장으로 확장한다.

Chapter 06의 종점은 이 문장이다.

> **다르게 느낄 자유는 남았고, 그 느낌이 사실을 자가 발행할 권한은 차단됐다.  
> 이제 남은 문제는 그 느낌 자체가 인간에게 어떤 현실이며,  
> 그것이 몸·행동·서사와 어떻게 합법적으로 이어지는가이다.**

---

## 부록 A. 출처 별칭

| 별칭 | 경로 | 행수 | 핵심 역할 |
|---|---|---:|---|
| `MEM18` | `연구/공장2/0118 머하고잇엇지` | 207 | 전날 문제 재호출 |
| `R03` | `연구/공장2/0118 rationale03` | 352 | Pressure/Repair/Relief·RiskCarry |
| `R04` | `연구/공장2/0118 rationale 04` | 419 | W/P/Storage/Bill 최초 완형 |
| `R05` | `연구/공장2/0118 rationale 05` | 394 | Cosmetic/True Relief·Bill 교정 |
| `STG0` | `연구/공장2/0118 STG06` | 603 | 첫 실행화 |
| `STG1` | `연구/공장2/0118 STG061` | 739 | Receipt-only·firewall 강화 |
| `STG2` | `연구/공장2/0118 STG 062` | 804 | WitnessSchema·core split·단일 F |
| `RSUM` | `연구/공장2/0118 rationale 05 1` | 233 | allowlist 설계 회고 |
| `LINK18` | `연구/공장2/0118 linker` | 293 | world boundary·Control/Receipt bus |
| `AX18` | `연구/공장2/0118 공리 정리 1` | 182 | 공리 압축 |
| `JOIN18` | `연구/공장2/0118 접합용 문사` | 261 | 접합용 재서술 |
| `TEM18` | `연구/공장2/0118 temo` | 404 | Conn→Imprint side branch |
| `PATCH18` | `연구/공장2/0118 append patch` | 665 | AXH vA0.1/.2/.4 누적; vA0.3 provenance gap |
| `FULL18` | `연구/공장2/0118 full06 1` | 895 | 후기 실행 합성 |
| `RUN18` | `연구/공장2/0118 통합 1.txt` | 1307 | v0.6-STG+AXH 실행 종점 |
| `THEORY18` | `연구/공장2/0118 통합1 이론1.txt` | 492 | 이론 재서술·Qualia 임피던스 재배치 |
| `CON06` | `연구/MAYnilat/0118 대통합 헌법` | 190 | Grounds/Influence·M2/M3 |
| `CON01` | `연구/MAYnilat/0118 대통합 헌법 01` | 159 | v0.6 뒤의 최소 헌법 재추출 branch |
| `VES18` | `연구/MAYnilat/0118 그릇` | 298 | Evidence/Ledger/σ·load slot |
| `EXPL18` | `연구/공장2/0118 통합 1용 설명문서` | 439 | 2026-03-07 후기 설명 거울 |

## 부록 B. 핵심 비동일성

```text
organismal raw ≠ RawSlice
RawSlice ≠ Witness
Witness ≠ Truth
Witness ≠ EvidenceLink
Grounds ≠ Warrant
Influence ≠ Grounds
Influence ≠ Authority

Qualia ≠ external fact
Qualia ≠ fake
Qualia ≠ automatic debt

pledge intention ≠ automatic Receipt
Receipt ≠ Evidence
Receipt ≠ obligation
obligation ≠ BillIssued
BillIssued ≠ ConsequenceRealized
ConsequenceRealized ≠ Settlement

Choice ≠ BodyAuthorization
BodyAuthorization ≠ PerformedAction
PerformedAction ≠ ExternalOutcome
ExternalOutcome ≠ ObservedOutcome

Repair ≠ Settlement
Cost ≠ Debt
Responsibility ≠ Authority
Stake ≠ Jurisdiction
```

## 부록 C. 소급 금지

```text
0118 Witness ≠ 현행 EventRecord
0118 Grounds ≠ 완성된 Warrant
0118 Receipt ≠ external action proof
0118 σ ≠ 현행 Ω 전체
0118 Bill ≠ 보편 도덕 회계
0118 RawSlice ≠ Ghost 이전 감각 raw
0118 View ≠ 완성된 Qualia theory
0118 CtrlCtx ≠ 인간 의미 전체
0118 ActionOut ≠ world outcome
Conn→Imprint ≠ 채택된 우주 법칙
PrivateExperienceTrace ≠ 원문 정의
typed self-boundary obligation ≠ 원문 정의
```

역사 본문은 0118이 직접 만든 분리와 실패를 보존한다. 현행 TAD·Ghost·자기 경계와의 결합은 연구 후기의 계보·잔차·Bridge로만 읽는다.
