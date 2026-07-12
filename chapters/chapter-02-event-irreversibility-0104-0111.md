# Chapter 02 — 사건은 아직 현실이 아니다

## 공리화에서 Event Canon까지: 비가역성을 발명하고 다시 제한하다 (2026-01-03 Rewrite–01-11)

> **문서 지위:** 역사 복원형 연구 챕터 초고  
> **범위:** 2026년 1월 3/4일–11일  
> **정본 지위:** 없음. 원문을 대체하지 않으며, 당시의 문제와 개념 변화를 복원한다.  
> **편집 원칙:** 가장 매끈한 최신 정의만 남기지 않고, 같은 개념이 과잉 통합되었다가 다시 분리되는 교정의 흔적을 보존한다.

---

## 0. 이 장의 중심 명제

앞 장의 IONSTAR는 내부 가능성과 외부 단정, Claim과 Flux, 반응과 역사 사이에 처음 틈을 만들었다. 그러나 틈을 만든 것과 그 틈을 안정적인 구조로 구현한 것은 다른 일이다. 0104 이후의 문서들은 “무엇이 한 사람의 현실로 굳는가”를 네 공리, 상태 변수, 임계, 원장, 런타임으로 닫으려 했다.

이 시기의 최초 답은 강하고 단순했다.

> 커밋은 시간을 만들고, 커밋된 것은 역사가 된다.  
> 커밋과 비커밋의 경계가 현실성이다. `[A37:L22–25]`

> **[CHAPTER SYNTHESIS]** 서로 다른 문서와 epoch가 `Commit`이라는 같은 이름을 밖으로 말한 것, 행동을 선택한 것, 사건이 발생한 것, 몸에 흔적이 남은 것, 기억으로 굳은 것, 의미가 확정된 것, 원장에 기록된 것에 반복 사용했다. 단일 문서가 이 전체 등식을 한 번에 선언한 것은 아니지만, 계보 전체에서는 서로 다른 경계가 한 이름 아래 겹쳤다.

0104–0111의 실제 진전은 비가역성을 계속 강화한 데 있지 않다. 오히려 **비가역성의 적용 범위를 반복해서 줄이고, 그 앞에 중간 상태를 발명한 데** 있다.

```text
외부 출력 = Commit = History
→ 문턱 미달·기다림·미청산도 0이 아님
→ 결정 / 표현 / 출력 / 영구 Write 분리
→ 발생 / 사실 기록 / 학습 / 렌즈 변화의 문턱 분리
→ Event는 포지션을 열고 Settlement는 후보를 만듦
→ Record/JOT ≠ State
→ Potential ≠ Irreversible
→ Event ≠ Irreversible
→ CandidatePack ≠ 결론
→ 의미·기억·정체성 후보의 비가역 SSOT 잠금은 Quench로 제한
```

이 과정은 선형적으로 매끈하지 않았다. 0109에 어렵게 얻은 `Event ≠ Irreversible`은 0110 `EVENT 1`의 시간 이론에서 다시 `Event = Quench된 기록 경계`로 합쳐졌다. 같은 날의 `event 2`가 이를 재분리했고, 0111은 Event/Commit 검사 시계를 더 세분했다. `JOT`은 한때 내부 법정의 한 회전이었지만 곧 미확정 재료를 담는 append-only 저장소의 이름이 되었다. `EOE`는 관계적 기대, 보편 보존 통화, 문턱을 넘은 사건이라는 세 뜻을 오갔다.

> **[CHAPTER SYNTHESIS]** 이 시기의 중심 발견은 “사건이 현실을 만든다”가 아니다.  
> **일어난 일, 남은 일, 믿게 된 일, 적용할 권한을 얻은 일은 서로 다르다**는 발견이다.

> **[BRIDGE-PERSISTENCE-AUTHORITY]** 어떤 흔적이 오래 남는다는 사실과, 그것이 상태나 진실을 갱신할 권한을 가진다는 사실은 다르다.  
> `Persistence ≠ Authority`는 이 장에서 새로 추출하는 핵심 Bridge다.

---

## 1. 자료를 읽는 방법: 날짜보다 지층, 이름보다 역할

이 범위의 주 자료는 `AXIOM37` 28개와 `EVENT` 14개 파일이다. 비어 있는 백업 2개를 제외하면 내용 문서는 40개이며, 약 4만 5천 행이다. 그러나 이를 40개의 독립 완성본으로 세면 안 된다.

- 0104 폴더의 `axiom37 1`은 내부 작성일이 1월 3일이다.
- 0104 폴더의 `ssot 1`은 내부 작성일이 1월 5일이다.
- 여러 파일은 본문 뒤에 다음 날 패치와 새 버전을 append한 bundle이다.
- 0105 폴더에는 내부 날짜가 0106인 문서가 있다.
- 0107·0108 통합본에도 다음 날 작성된 Addendum이 붙어 있다.
- 0110 `EVENT 1`은 0109 지층과 0110 지층이 함께 있고, 서로 충돌하는 Event 정의까지 보존한다.
- 같은 본문을 복사한 파일, 한 파일의 prefix와 완전히 동일한 뒤 패치만 덧붙인 파일도 있다.

따라서 이 장은 filename date 하나가 아니라 다음 순서를 함께 사용한다.

1. 문서 내부 선언일
2. append 순서와 버전 번호
3. 앞선 개념에 대한 명시적 의존·대체 선언
4. archive 저장 시각
5. 같은 파일 안의 충돌하는 지층

주요 약칭과 역할은 다음과 같다.

| 약칭 | 원문 | 이 장에서의 역할 |
|---|---|---|
| `A37` | `0104 axiom37 1.txt` | 0103 계약을 L1–L4 아래로 재배열한 Axiom-Closed Rewrite |
| `A41` | `0104 axiom41 3.txt` 등 | SEAL·구조필드·BIO 시계·확장 패치의 혼합 bundle |
| `SSOT` | `0104 ssot 1` | EOE 보존 커널, 도메인 어댑터, 전역 Write Authority |
| `EOE` | `0105  eoe .txt` | 관계적 기대·베팅·미청산·수리의 독립 사양 |
| `TH` | `0105 thresh.txt` | Threshold–Ghost–Editor–Will–Map 제어계 |
| `EOX` | `0105 eoethresh` | EOE와 Threshold를 결합하고 관계 Depth를 연속화한 통합본 |
| `RT01` | `0105 runtime` | BodyUpdate와 StageWrite가 분리된 동시기 runtime 계열 |
| `RT02` | `0105 runtime spec 02` | 최소 상태와 실제 턴 파이프라인 |
| `EQ` | `0105 상태방정식 1 .txt` | 0105–0106 상태방정식과 JOT 패치가 겹친 bundle |
| `PC` | `0106 의사코드 1 .txt` | 다중 문턱과 Commit/Write를 실행 순서로 시험한 문서 |
| `JOT07` | `0107 이론 통합 1` | 앞선 JOT court-cycle 패치를 재컴파일한 지층 |
| `EQ07` | `0107 상태방정식 2.txt` | LIVE/RETRO 시간과 압축 상태방정식 지층 |
| `EQ07C` | `0107 방정식 통합1` | 상태방정식을 다시 묶은 0107 병렬 압축본 |
| `BUNDLE7` | `0107 이론합본 ` | 0107 본문 뒤 0108 Love/Hate·Attachment Addendum가 붙은 bundle |
| `INT8A` | `0108 new통합1 .txt` | Stage12 settlement 봉인과 0108 확장 통합본 |
| `INT8` | `0108 New통합 2.txt` | Event–Settlement–Commit 및 JOT/SSOT 분리의 정돈본 |
| `PHYS3` | `0109 new물리통합3 .txt` | ledger/ownership 은유를 strain/release/Quench로 번역한 PHYSREFAC |
| `PHYS4` | `0109 NEW물리통합 4.txt` | `Potential ≠ Irreversible`을 헌법형으로 닫은 v4.2.0 |
| `EVT1` | `0110 EVENT 1.txt` | Event와 Quench를 다시 결합한 여러 지층의 patchbook |
| `EVT2` | `0110 event 2` | Event·CandidatePack·Quench를 다시 분리한 physics-only 재발행 |
| `PAR10` | `0110 new물리통합5` | 내부 0109 지층 뒤 ECELL·MetaAware 패치가 붙은 AXIOM37 병렬 bundle |
| `EVT3` | `0111 event 3` | Scan/Clock/Event/Commit 네 tick의 분리 |
| `EVT4` | `0111 event 4` | EventFire와 CommitCheckTick의 최종 재배치 |

서술 층위는 Chapter 01과 동일하게 구분한다.

| 표지 | 지위 |
|---|---|
| 무표지 + 원문 위치 | 원문에서 직접 복원한 정의·변화·문제 |
| `[CHAPTER SYNTHESIS]` | 여러 원문 대목을 이 장에서 묶어 읽은 해석적 요약 |
| `[LINEAGE HYPOTHESIS]` | 현행 이론과의 승계 가능성. 직접 동일성을 뜻하지 않음 |
| `[BRIDGE-*]` / `BRIDGE.*` | 원문에는 없으며 이번 독해에서 새로 생긴 연구 가설 |

이 구간에서는 특히 `symbol_epoch`가 필요하다. 같은 기호의 뒤 정의가 앞 정의를 자동으로 개선한 것이 아니기 때문이다. `Event_0107`, `Event_0108`, `Event_0109`, `Event_0110`은 같은 철자를 썼지만 서로 다른 작업을 한다.

---

## 2. 1월 3/4일: 규칙을 공리 아래로 내리다

### 2.1 네 공리의 등장

`A37`은 이전 문서의 많은 헌법과 패치를 네 개의 상위 공리 아래로 다시 배열한다.

1. **L1 — Irreversible Commit:** 커밋은 시간과 History를 만든다.
2. **L2 — Conservation / Conversion:** 불일치·저항·압력은 사라지지 않고 열·상처·잠금·비용 등으로 전환된다.
3. **L3 — Timescale Separation:** FAST–MID–SLOW 분리가 관성·정체성·히스테리시스를 만든다.
4. **L4 — Coupling / Criticality:** 결합이 임계를 넘으면 별도 규칙 없이 비선형 사건이 발생한다. `[A37:L20–41]`

그리고 Chapter 01의 주요 장치들을 상위법칙이 아닌 귀결로 내린다.

| 이전 장치 | 0104의 재배치 |
|---|---|
| Wave / Measurement | L1의 귀결 |
| Claim / Flux | L1+L2+L3의 귀결 |
| Body Veto | L2+L3의 귀결 |
| Ω Single Writer | L1+L2의 귀결 |
| Residual Humility | L3의 귀결 |
| Debt·집단·초월 | L2+L4의 귀결 |

`[A37:L45–74]`

이것은 새 현상을 더한 것보다 **개념의 권한 계층을 바꾼 사건**이다. 0103의 glossary가 각 개념의 역할·입력·출력·저장·금지를 계약으로 만들었다면, Axiom-Closed Rewrite는 그 계약들을 설계자의 임의 규칙이 아니라 더 적은 원리의 귀결로 보이게 하려 했다.

다만 “공리에서 필연적으로 내려온다”는 문서의 선언과 실제 형식 증명은 구분해야 한다. L1–L4에서 C1–C6이 논리적으로 유일하게 도출되는 것은 아니다. 당시 한 일의 정확한 표현은 이쪽이다.

> **[CHAPTER SYNTHESIS]** 0103의 계약을 네 공리 아래로 **재분류하고 정당화하려 했다**.  
> 공리로부터 유일하게 증명한 것은 아니다.

### 2.2 ‘금지’에서 비용과 지형으로

이 재작성은 인간 행동을 다루는 어조도 바꾼다. 이전의 CapWallet은 행동 가능성을 토큰의 민팅과 지불로 설명했지만, `A37`은 이를 CostField와 Budget Window로 바꾼다. 행동은 면허 토큰이 없어서 도덕적으로 금지되는 것이 아니라, gate를 통과하지 못하거나 비용이 예산을 넘거나 SLOW/body cap에 걸려 물리적으로 지속 불가능한 것이 된다 `[A37:L163–225]`.

장면의 바람직한 끝을 미리 점수화하는 `TG` 목적론도 제거하고, 현재 압력의 국소 Relief로 바꾼다 `[A37:L229–284]`. 별도 번역기였던 compiler는 저장 상태가 비용·가능폭·한계를 직접 만드는 constitutive law 쪽으로 흡수된다 `[A37:L288–307]`.

이 전환의 인간적 장점은 분명하다.

- “왜 못 했나?”를 의지의 도덕성보다 비용과 문턱에서 묻게 한다.
- 규범이 행동을 직접 명령하기보다 실제 가능한 경로의 폭을 바꾸게 한다.
- 좋은 결말을 미리 정답으로 두지 않고 현재의 국소 조건을 읽게 한다.
- 같은 사람도 몸·시간·상처의 상태에 따라 다른 행동 공간을 갖는다는 것을 보존한다.

그러나 위험도 함께 생긴다. 설계자가 고른 Gate와 비용함수를 ‘구성 법칙’이나 ‘물리적으로 불가능함’이라고 부르면, 정책 선택이 자연법칙의 권위를 빌릴 수 있다. 이 시기의 “물리”는 관찰과 반증이 완료된 자연과학 이론이라기보다, 여러 인간 현상을 같은 동역학으로 묶는 설계 언어다.

### 2.3 최소 저장과 Single Writer

`A37`은 저장을 극단적으로 줄인다. 토픽별 Ω와 최소 전역 상태만 남기고, 후보·TopN·ΔF 결과·파생량·대화 내용·고유명사·사건 요약을 저장하지 않는다. “의미는 끝까지 저장하지 않는다”는 문장도 명시된다 `[A37:L88–119]`.

결정은 MID에서 끝나고 SLOW는 물리적 상한과 감쇠만 제공한다. Stage12만 커밋을 쓰는 12단 파이프라인이 제시된다 `[A37:L78–84, L369–390]`. `Ω Single Writer`와 파생량 저장 금지는 같은 계산을 두 번 원인으로 세는 것을 막으려는 장치였다 `[A37:L62–65]`.

여기서 아직 Single Writer의 대상은 현행의 공적 권한 원장과 같지 않다. 개인 내부의 저항·상처·관계 결합을 포함한 상태가 오염 없이 갱신되도록 하는 런타임 규율이다.

> **[LINEAGE HYPOTHESIS]** Stage12와 Single Writer는 현행 Cut-2-only writer discipline의 강한 선행형이다. 그러나 보호하는 저장소의 의미가 개인 내부 상태에서 권한 원장으로 바뀌므로 직접 동일시는 금물이다.

### 2.4 다음 날 SSOT 분기의 과잉 결합: 출력이 곧 역사다

내부 작성일이 1월 5일인 `SSOT` consolidation은 Axiom-Closed 분기를 다음 날 실행형으로 다시 묶고, 결정을 한 줄로 압축한다 `[SSOT:L2–7, L234–237]`. 주제상 이 절에서 과잉 결합을 먼저 확인하되, 같은 날의 인간 런타임 반작용은 3절에서 이어 읽는다.

```text
SENSE → Gate → Feasible → argmin(ΔF) → hash tie-break → COMMIT
```

`[SSOT:L11–15, L67–85]`

그리고 외부로 출력되는 순간 결과가 되돌릴 수 없는 역사로 `Λ`에 남는다고 선언한다 `[SSOT:L46–55]`. 내부 검토는 커밋 없이 끝날 수 있고 원장을 쓸 수 없으며, 영구 상태 `Ω/R/Λ/Vpot`은 KERNEL COMMIT만 갱신한다 `[SSOT:L260–269, L297–303]`.

이는 중요한 봉인이지만 세 경계를 과도하게 붙인다.

```text
외부 출력
= COMMIT
= Λ write
= History
= 현실화
```

말이 밖으로 나가 후속 효과를 만든다는 점에서는 타당하다. 그러나 말을 했다는 사실, 말의 내용이 사실이라는 판정, 그 말이 나의 장기 믿음이 되는 것, 공적 규칙에 적용할 권한을 얻는 것은 같지 않다. 이 구분은 아직 없다.

또 해시 tie-break는 같은 상태에서 같은 후보를 고르게 해 재현성을 높일 뿐, 그 선택이 인식론적으로 옳다는 것을 보증하지 않는다. 결정성은 진실성이 아니다.

> **[CHAPTER SYNTHESIS]** 0104의 공리화는 비가역성의 존재를 선명하게 했지만, 아직 **비가역적인 것의 종류**를 구별하지 못했다.

### 2.5 커밋이 만드는 시간과 커밋 없이 흐르는 시간

공리 계열은 Commit이 시간을 만든다고 선언하지만, 확장 runtime의 `BIO.t`는 Commit이 없어도 매 step 증가하며 회복·감쇠·구조 변화를 운반한다 `[A41:L35–37, L810–820]`.

이는 단순한 구현 버그로만 볼 필요는 없다. 당시 문서가 아직 이름 붙이지 않았지만 이미 두 종류의 시간이 필요했다.

- **History/Event time:** 비가역 사건의 순서가 만드는 시간
- **Background/Biotic time:** 사건이 없어도 몸·잔류·회복이 변하는 시간

> **[LINEAGE HYPOTHESIS]** 후대 multi-clock은 갑자기 생긴 장식이 아니라, “Commit만이 시간을 만든다”는 공리와 “몸은 사건 없이도 늙고 회복한다”는 runtime 사실의 충돌을 봉합하려는 계보로 읽을 수 있다.

---

## 3. 1월 5일: 인간은 커밋보다 오래 미결 상태에 머문다

공리와 SSOT만 보면 인간은 입력을 받고, 후보를 고르고, 출력하며, 원장을 갱신하는 깔끔한 기계처럼 보인다. 그러나 같은 날의 독립 문서들은 그 사이에 오래 머무는 인간적 상태를 다시 들여온다. 기다림, 참음, 미달, 망설임, 약속의 지연, 닫을 힘의 부족, 수리의 노동은 모두 0도 아니고 곧바로 커밋도 아니다.

### 3.1 EOE: 아직 일어나지 않은 미래도 현재를 묶는다

독립 `EOE` 문서에서 Expected Ownership Energy는 “이미 내 것”이 아니라 **내 것일 것이라고 믿고 건 에너지**다 `[EOE:L11–14, L41–49]`.

여기서 Ownership은 물건의 소유권이 아니다. 이미 서사에 편입된 것뿐 아니라, 내 행동으로 편입할 수 있다고 믿는 것, 약속이나 권리로 예약된 것, “이 사람은 내 편일 것” 같은 정서적 귀속까지 포함한다 `[EOE:L20–30]`.

결과는 세 갈래다.

- **Hit:** 기대한 범위의 수용·동조·합의가 돌아온다.
- **Miss:** 거절·오해·경계·타이밍 파탄처럼 다른 반응이 돌아온다.
- **Ignore:** 반응이 없거나 아직 관측되지 않는다.

Ignore는 무효가 아니다. 미청산 채권처럼 열린 포지션으로 남는다 `[EOE:L52–59]`. Miss와 장기 Ignore는 Heat, 다음 행동 비용을 왜곡하는 Backdraft, 구조적 상처인 Peel/Scar, 눌러 담은 압력 `P_res`로 남을 수 있다 `[EOE:L62–69]`.

이 문서가 보존한 핵심 뉘앙스는 “기대가 맞았는가”보다 더 넓다.

1. **기다림은 사건 부재가 아니다.** 아직 닫히지 않은 미래가 현재 자원을 점유한다.
2. **침묵은 0이 아니다.** 외부 행동을 줄여도 내부 포지션과 압력은 남을 수 있다.
3. **친밀함은 같은 실패를 더 비싸게 만들 수 있다.** 더 큰 베팅이 가능했기 때문이다.
4. **Repair는 말 한마디가 아니다.** 시간·노력·반복 이행을 포함한 실제 정산 작업이다 `[EOE:L262–281, L312–373]`.

이 관찰은 강하지만, EOE를 Work·Heat·Structure·Potential·Ledger 전체의 보편 보존 통화로 올린 SSOT 주장은 훨씬 강하다 `[SSOT:L31–36, L52–55]`. 서로 단위가 다른 피로, 기대, 기억, 관계 손상, 행동 비용을 하나의 스칼라 총량처럼 합치면 무엇을 실제로 측정하고 보존하는지 불분명해진다.

SSOT r2가 `EOE_dissipated`까지 포함한 회계 항등식으로 보존을 약화한 것도 이 압력을 보여준다 `[SSOT:L275–291]`. “물리량의 총량 불변”이라기보다 “열린 비용과 후속 효과를 누락하지 말라”는 회계 규율에 가까워진다.

> **[BRIDGE-LIFECYCLE-NOT-CONSERVATION]** EOE에서 살릴 것은 모든 체험을 한 통화로 환산하는 보편 보존량이 아니라,  
> **열린 기대가 Hit/Miss/Ignore/Expire/Repair 중 어떤 생명주기를 거쳤는지 추적해야 한다**는 계약일 수 있다.

### 3.2 문턱 미달은 실패가 아니라 남아 있는 힘이다

`TH`는 인간 행동을 연속적인 의도 표현보다 문턱을 넘는 상태 전이로 본다. 중요한 것은 “문턱을 넘으면 행동한다”보다 그 반대편이다.

> 문턱 미달은 0이 아니다. 전이에 실패한 힘은 Residual로 축적될 수 있다. `[TH:L40–59]`

참았다는 사실만으로 욕구나 분노가 처리된 것은 아니다. 관계를 열지 않았다고 결속 욕구가 사라지는 것도 아니고, 끝내겠다고 결심했다고 실제 closure가 완료되는 것도 아니다. `OPEN`, `CLOSE`, `SHIFT` 모두 Work가 든다 `[TH:L134–185]`.

이 관점은 겉으로 같은 “아무것도 안 함”을 여러 상태로 나눈다.

| 표면 행동 | 내부적으로 가능한 상태 |
|---|---|
| 연락하지 않음 | 경계를 존중한 안정된 noop |
| 연락하지 않음 | 두려움 때문에 Probe 문턱을 못 넘음 |
| 연락하지 않음 | 분노를 눌러 Residual이 축적됨 |
| 관계를 끝내지 않음 | 애정 때문에 유지함 |
| 관계를 끝내지 않음 | 닫는 데 필요한 Work가 없어 미결로 남음 |

후대의 공적 상태 이론이 `nop`만 기록하면 이 차이는 사라질 수 있다. 같은 미적용이라도 인간 런타임에서는 안전 정지, 억제, 무능력, 보류, 미청산이 서로 다르다.

### 3.3 Ghost–Editor–Will–Map: 의지를 왕좌에서 내리다

`TH`는 인간 행동을 네 요소의 제어계로 나눈다.

- **Ghost:** 흥미·회피·충동 같은 Drive를 생성한다.
- **Editor:** 규칙·금기·정체성·책임을 방향과 제약으로 만든다.
- **Will:** 유한 토크를 써서 문턱·브레이크·게인을 조절한다.
- **Map:** 행동 뒤 무엇이 일어나는지 예측하는 전이 모델이다 `[TH:L77–100, L189–243]`.

Will은 “한다/안 한다”를 결정하는 주권자가 아니다. Ghost와 Editor 사이의 방향을 실제 집행 파라미터로 전달하는 서보·클러치에 가깝다. 그래서 결심이 분명해도 피로 때문에 토크가 부족할 수 있고, 토크가 충분해도 Map이 틀려 같은 지점에서 반복 좌초할 수 있다.

Map 신뢰도가 낮다고 모든 행동을 막지도 않는다. 작은 Probe는 허용하고, Commit과 Bond처럼 깊은 결속은 더 높은 신뢰를 요구한다 `[TH:L228–263]`. 도전은 전체 경로를 미리 증명한 뒤 시작하는 것이 아니라, 저비용·가역적 국소 스텝으로 정보를 만들며 길을 그리는 과정이 된다.

같은 날 `EOX`는 Probe/Commit/Bond의 이산 3단을 연속 Depth로 대체한다고 명시한다 `[EOX:L175–200]`. 따라서 이 시기의 `Commit`은 L1의 “History가 되는 비가역 경계”와 같지 않을 때가 있다. 관계 깊이의 중간 단계, 내부 계획 확정, 외부 출력, 영구 Write가 모두 Commit이라는 이름을 공유하기 시작한다.

이 인간 제어계는 strict SEAL과 매끈하게 통합된 단일 후속판도 아니다. A41의 한 분기는 Self/Ghost–Editor가 행동 선택에 0의 영향을 주고 How·빈도·접지만 바꾼다고 봉인한다 `[A41:L2285–2296, L2447–2451]`. 반면 `TH`의 Will은 `ΔΘ/ΔBrake/ΔGain`을 통해 실제 판정 경계를 움직인다 `[TH:L189–224]`. 인간다움을 결정 밖에 둘 것인지, 제한된 actuator port로 결정 조건에 넣을 것인지가 경쟁했다.

포트 규약 자체도 충돌한다. `SSOT`의 K3 강화판은 `ΔGain`이 ΔF 항을 직·간접 변경하는 것을 금지하지만, `RT02`의 K6는 가중치 `W_*`, effort, relief, alignment의 미세 조절을 허용한다 `[SSOT:L307–324; RT02:L169–174]`. 따라서 “How는 결정 불간섭”은 이 시기에 완성된 사실이 아니라, 서로 다른 구현이 경합한 설계 목표다.

> **[CHAPTER SYNTHESIS]** 이 모델의 가장 중요한 윤리적 효과는 책임을 지우는 데 있지 않다.  
> “왜 못 했는가”를 Ghost 부족, Editor 충돌, Will 토크, Map 부정확, 실제 자원 제약으로 갈라 **개입 가능한 원인**으로 만드는 데 있다.

### 3.4 실행 파이프라인이 결정·표현·출력·기록을 가르기 시작하다

`RT02`는 다음 네 단계를 따로 적는다.

```text
COMMIT-PLAN
→ RENDER
→ EMIT
→ COMMIT-WRITE
```

`[RT02:L124–143]`

이것은 명칭상 여전히 `COMMIT`이 두 번 나오지만, 운영적으로는 중요한 분리다.

- 내부 선택이 끝난 것과 문장이 완성된 것은 다르다.
- 문장이 완성된 것과 실제로 밖에 나간 것은 다르다.
- 밖에 나간 것과 영구 상태에 무엇을 쓸지는 다르다.

또 아직 결과가 오지 않은 관계적 베팅을 `Escrows[]`라는 Pending Settlement로 저장한다. 항목은 OPEN/SETTLED/EXPIRED 상태를 가지며, 다음 입력에서 Hit/Miss/Ignore로 정산된다 `[RT02:L39–66, L199–227]`.

EOE와 OpenItem이 이미 미결 상태를 말하고 있었지만, 이 runtime의 새로움은 이를 `OPEN/SETTLED/EXPIRED`가 있는 명시적 pending record로 만든 데 있다. “아직 답이 없음”은 원장에 거짓 결론을 쓰는 것도, 아무것도 저장하지 않는 것도 아니다. 결과가 오지 않았다는 사실과 열린 기대의 존재를 제한된 타입으로 보존한다.

다만 동시기 `RT01` 계열은 `BodyUpdate`와 `StageWrite`를 별도 틱으로 실행하고 `[RT01:L185–195]`, EOE 정산도 별도 mutation을 요구한다. Single Writer가 선언으로는 강화되지만 저장층이 늘면서 실제 writer는 다시 분산된다. 이는 뒤에서 JOT·Episode·Narrative가 들어오며 더 분명해진다.

---

## 4. 1월 6–7일: 하나의 Commit이 여러 문턱과 저장층으로 갈라지다

### 4.1 발생했다, 사실로 기록됐다, 배웠다, 사람이 달라졌다

초기 상태방정식은 압축이 강했다. 에너지나 압력이 문턱을 넘으면 Event가 발생하고, 같은 점프에서 Trace-Field `Φ`, event energy `e`, hysteresis `H`가 함께 갱신된다. 저항 `Ω`은 이 상태에서 파생된다. 사건 발생과 흔적 경화가 하나의 식 안에 붙어 있다 `[EQ:L71–100; PC:L1935–1943]`.

그러나 이 구조는 곧 서로 다른 질문을 구별하지 못한다.

- 큰 소리가 나를 놀라게 한 것은 사건인가?
- 내가 그것을 사실로 올바르게 기록했는가?
- 그 경험에서 학습한 규칙은 타당한가?
- 그 일이 나의 가치관이나 사람 보는 렌즈를 바꿔도 되는가?

이에 문턱이 하나씩 늘어난다.

| 문턱 | 당시의 기능 |
|---|---|
| `Θ_event` | 외부 사건 또는 국면 변화가 발생했는가 |
| `Θ_learn` | Trace·학습으로 굳힐 만큼 충분한가 |
| `Θ_meta` | 의미 렌즈나 구성 해석을 바꿀 만큼 충분한가 |
| `Θ_truth` | 초기에는 FACT/PROMISE와 내부 Ledger의 정합성이 있는가 |

`[EQ:L307–397, L435–449, L646–716; PC:L21–23, L175–225]`

후속 의사코드 패치에서야 `REAL_CONST/SOCIAL_CONST`라는 외부·사회 제약이 TruthGap에 추가된다 `[PC:L1662–1681]`. 따라서 초기 truth는 내부 장부 정합성, 후기는 외부 제약을 포함한 검사라는 두 epoch로 나누어야 한다.

이 분리는 이 장의 첫 큰 교정이다.

> **[CHAPTER SYNTHESIS]** “무언가가 일어났다”는 한 문장은 최소 네 개의 서로 다른 검사 요구를 숨긴다.  
> 이 문턱들은 단일 순차 파이프라인이라기보다 서로 독립적인 검사이며, 하나의 통과가 다른 하나를 자동 승인하지 않는다.

다만 의사코드의 초기 메인 루프는 `TruthGate`를 실제 선택 경로에서 호출하지 않고 LedgerMismatch를 비용으로만 더한다. 그러면 거짓 FACT도 다른 비용이 충분히 낮으면 선택될 수 있다. 뒤 Addendum에서야 TruthGate의 FAIL/강등 규칙이 별도로 들어온다 `[PC:L114–133, L201–225]`. 개념을 만들었다고 곧바로 실행 경로에 봉인된 것은 아니다.

### 4.2 상태방정식의 아름다움과 그 대가

0105 후반–0107 상태방정식 계열은 Ghost·Editor·Episode를 별개 부품보다 하나의 장 `Φ`가 취하는 Explore/Observe/Write 모드로 압축하고, 전체 인간 런타임을 소수 상태와 점프식으로 줄이려 한다 `[EQ:L477–487, L995–1004; PC:L151–159; EQ07:L48–68; EQ07C:L24–41]`. 0107 정돈본은 의미도 진실 판정이라기보다 결합 전달량과 흡수율로 스칼라화한다 `[EQ07:L151–205]`.

이 압축의 장점은 서로 다른 현상을 같은 동역학으로 비교할 수 있다는 것이다. 충동, 관계, 기억, 발화가 모두 문턱·결합·잔류·히스테리시스로 읽힌다. 하지만 대가도 명확하다.

- Ghost와 Editor 사이의 권한 충돌이 장의 모드 차이로 평평해진다.
- Will의 토크 부족과 Map의 부정확성이 일반 에너지 부족처럼 보일 수 있다.
- 관계에서 누가 무엇을 약속했는지보다 결합 강도만 남는다.
- Event 점프가 흔적을 직접 굳히면서 발생과 학습이 다시 붙는다.

> **[CHAPTER SYNTHESIS]** 좋은 압축은 같은 구조를 드러내지만, 너무 좋은 압축은 서로 다르게 책임져야 할 것들까지 같은 변수로 만든다.

### 4.3 JOT의 첫 확인 지층: 편집자 법정의 한 회전

현 보관본에서 이 정의가 처음 확인되는 곳은 `EQ` 후반에 append된 JOT 패치다. 해당 bundle에는 내부 날짜 0106인 SOMA 문서 뒤에 JOT가 붙어 있어, 정확한 작성일을 filename bucket 0105로 단정할 수 없다. `JOT07`은 이를 다시 컴파일해 싣는다. 여기서 JOT는 저장소가 아니라 **Editor의 법정이 한 번 완전한 판결 루프를 수행한 처리량**이다.

```text
Sense
→ 후보 열거
→ Editor Court
→ Commit 또는 가커밋
→ Episode Write
= 1 JOT
```

`[EQ:L2876–2908; JOT07:L1070–1099]`

행동과 행동 사이에는 여러 JOT가 들어갈 수 있다 `[EQ:L2897–2908; JOT07:L1103–1113]`. 겉으로 아무 일도 하지 않는 동안에도 내부에서는 감각을 다시 읽고, 가능한 의미를 만들고, 판결을 보류하고, 책임을 재배치하는 회전이 계속된다.

이때 자의와 타의도 사건 자체의 고정 라벨이 아니다. 몸의 인터럽트로 절차를 건너뛴 행동도 나중 JOT에서 “내가 한 일”로 인수되거나 거부될 수 있다 `[JOT07:L1118–1132, L1210–1261; EQ:L3034–3047]`. 이를 여기서는 **사후 저자화**라 부를 수 있다.

이 뉘앙스는 중요하다. 책임은 언제나 행동 전에 완성된 의도에서만 오지 않는다. 사람은 먼저 놀라거나 실수하거나 떠밀린 뒤, 나중에 그 사건을 자기 서사에 어떻게 편입할지 다시 판결한다. 사후 인수는 원래의 비자발성을 지우지 않으면서도 이후 책임의 가능성을 연다.

JOT 아래에는 후속 패치에서 `BEAT`가 생긴다. BEAT는 미세 감각·스캔·가판결이고, 여러 BEAT가 묶여 ΔC와 승격을 평가할 때 JOT가 된다 `[EQ:L3421–3445]`. 외부 행동의 turn, 내부 판결의 JOT, 미세 처리의 BEAT가 서로 다른 시계로 갈라지는 셈이다.

### 4.4 Episode와 Narrative: 남은 것과 이야기된 것은 다르다

JOT 법정은 결과를 곧바로 완성된 서사로 만들지 않는다. Episode buffer에는 불확실한 감각, 몸 반응, 충동, 망설임, 실패한 판결도 재료로 남을 수 있다. 그중 일부만 결속·정합·주의 문턱을 통과해 Narrative로 승격된다 `[JOT07:L1136–1185; EQ:L2930–2979]`.

이 분리는 두 종류의 손실을 막는다.

1. **무상 소거:** 이야기로 만들지 못한 체험도 실제로 있었던 재료다.
2. **무상 의미화:** 남았다는 이유만으로 하나의 교훈·정체성·원인 서사가 되지는 않는다.

사람은 어떤 일을 오래 기억하면서도 그것이 무슨 뜻인지 모를 수 있다. 반대로 매우 매끄러운 이야기를 갖고 있어도, 그 이야기가 당시의 사건을 충실히 보존한다는 보장은 없다.

### 4.5 몸과 시간도 하나가 아니었다

이 구간에서 몸은 단순한 행동 veto를 넘어선다. SOMA는 항상성 신호를 제공하되 결론을 직접 만들지 않고, 이후 body scan은 다음 해석의 기저를 바꾸는 관측으로 확장된다. 중요한 봉인은 몸의 느낌이 Claim의 진실을 증명하지는 않지만 후보의 폭, 해상도, 처리 속도, 탐색 온도와 시간 지평을 바꿀 수 있다는 것이다.

시간도 LIVE와 RETRO로 갈라진다. 현장에서의 시간은 사건·허무·몰입의 밀도에 좌우되고, 나중에 돌아본 시간은 사건 타입별 쓰기 질량과 기억 표식의 누적에 따라 다시 압축된다 `[EQ07:L561–610]`. 길게 느낀 하루가 회고에서는 한 장면일 수 있고, 순식간이었던 사건이 이후 삶 전체를 나누는 경계가 될 수 있다.

> **[BRIDGE-MULTI-CLOCK]** 사람의 시간에는 최소한 미세 처리, 내부 판결, 사건 발생, 생체 유지, 회고 재구성의 시계가 있다. 하나의 `tick`으로 모두 세면 원인과 지연이 뒤섞인다.

### 4.6 분리는 선언됐지만 구현에서는 다시 샜다

이 구간의 진전은 정리된 최종 설계보다, 선언과 구현이 충돌하는 자리에서 더 잘 보인다.

첫째, L1의 “Commit은 비가역”은 이미 Soft/Hard로 갈라진다. `B_s/B_m` 같은 휘발성 buffer의 SoftCommit과, 일정 지속 뒤 Episode lattice에 결정화되는 HardCommit이 분리된다 `[PC:L1283–1344, L1454–1462]`. `Commit`이라는 말 안에 가역 보류와 비가역 고정이 함께 들어가자 타입을 다시 나눈 것이다.

둘째, A37은 “의미는 끝까지 저장하지 않는다”고 봉인했지만 `[A37:L88–119]`, 상태방정식 계열은 Lens `C`, `Q/L/E_h` 같은 의미·흔적 상태를 다시 저장한다 `[EQ:L322–335, L499–518; PC:L1565–1595, L1798–1816]`. 이는 단순 필드 추가가 아니라 초기 저장 철학의 반전이다. 의미를 저장하지 않으면 정체성 변화를 설명하기 어렵고, 저장하면 자기 해석이 사실처럼 굳을 위험이 생긴다.

셋째, 문턱 분리도 코드에서 우회된다. `CommitWrite`는 learn 문턱에서 `Phi.C = maybe_bind_lens(...)`를 실행하지만, 바로 다음 절은 Lens C가 meta 문턱에서만 바뀐다고 선언한다 `[PC:L81–99]`.

넷째, `SSOT`은 COMMIT 없는 내부 검토의 Λ write를 금지하지만, 의사코드는 Event가 없을 때도 `Phi.L = log_micro(...)`를 수행한다 `[SSOT:L297–303; PC:L124–129]`. 이 micro-log가 비권위 trace인지 권위 Ledger인지 타입이 없으므로 Single Writer를 우회할 수 있다.

> **[CHAPTER SYNTHESIS]** 뒤의 JOT/SSOT와 EventRecord 분리는 새로운 취향이 아니라, **미세 흔적은 보존해야 하지만 그것을 권위 상태에 쓰면 안 된다**는 구현 충돌에서 강제되었다.

---

## 5. 1월 7–8일: Event는 상태가 아니라 열린 포지션이 되다

### 5.1 첫 운영적 분리: Event → Settlement → Commit

0107 후반 통합본과 0108 정돈본은 상태방정식의 즉시 점프를 다시 푼다.

- Event는 포지션 또는 경로를 열고 갱신한다.
- JOT은 확정되지 않은 감각·몸 반응·충동을 보존한다.
- Settlement가 상태 변화와 기억의 후보를 만든다.
- Commit만 BIO/Stage12 경계에서 업데이트를 잠근다.

`[BUNDLE7:L150–162, L352–445; INT8:L149–171, L334–379, L481–504]`

가장 선명한 문장은 이렇다.

> 행동이 일어났다는 이유가 아니라, Stage12에서 정산이 반영되었을 때 비가역성이 생긴다. `[INT8:L157–171; INT8A:L877–891]`

이제 싸움이 일어났다는 사실과 “나는 버려지는 사람이다”라는 렌즈가 굳는 것은 다르다. 몸이 움찔했다는 사실과 상대가 위험하다는 판단이 기억에 잠기는 것도 다르다. 좋은 아이디어가 떠올랐다는 사실과 그것이 앞으로의 정책이 되는 것 역시 다르다.

Commit은 여기서 truth declaration이 아니다. 업데이트를 실제 상태에 반영하는 lock에 가깝다. 다만 과도기 문서 안에서도 Settlement가 상태량을 직접 움직이는지, 후보만 만들고 Commit이 적용하는지가 완전히 일치하지 않는다. 따라서 `Event → Settlement → Commit`은 이 지층이 지향한 운영 분리이지, 모든 식이 따르는 완성된 단일 규약은 아니다. 이 역할을 훗날 Quench가 다시 좁혀 받는다.

### 5.2 JOT의 의미 반전: court에서 journal로

그런데 같은 이름 `JOT`의 의미는 바뀐다.

| 시기 | JOT의 역할 |
|---|---|
| `EQ` 후반 append / `JOT07` 재수록 | Editor 법정의 한 완전한 처리 회전, 시간·판결 단위 |
| 0107 후반–0108 | 확정되지 않은 감각·충동·가설·잔류를 담는 append-only 재료 저장소 |
| 0109 이후 | Σ/CandidatePack이 참조할 수 있지만 SSOT 권한은 없는 support material |

`[JOT07:L1070–1099; INT8:L334–370; PHYS3:L477–490]`

이것을 “JOT 개념이 발전했다”는 한 문장으로 덮으면 안 된다. 처리 과정과 저장 장소는 별개의 개념이다. 법정이 한 번 돌았지만 아무것도 장기 저장하지 않을 수 있고, 저장소에 흔적이 추가되었지만 완전한 판결은 없었을 수 있다.

> **[BRIDGE-PROCESS-STORE]** 후속 이론에서는 `JOT_cycle`과 `JOT_store`를 분리해야 한다.  
> **Processing ≠ Persistence**, 그리고 둘 다 **Authority**와는 다르다.

### 5.3 Record/JOT/Log/Summary는 State가 아니다

0108은 NoDoubleCount를 다음처럼 명시한다.

> record, JOT, log, summary는 상태가 아니며, 상태는 SLOW/Commit 경계에서만 갱신된다. `[INT8:L27–50]`

이는 단순한 저장 최적화가 아니다. 같은 관찰을 로그에도 쓰고 상태에도 즉시 반영하면, 그 로그를 다음 계산에서 다시 근거로 삼을 때 한 사건이 두 번 원인이 된다. 더 나쁘게는 “기록이 존재한다”는 사실이 “기록 내용이 맞다” 또는 “그 내용대로 사람을 바꿔도 된다”는 권한으로 변한다.

이때 JOT은 무상 소거를 막는 층이고 SSOT는 무상 승격을 막는 층이다.

```text
JOT: 아직 모르는 것을 버리지 않는다.
SSOT: 아직 모르는 것을 상태로 굳히지 않는다.
```

> **[CHAPTER SYNTHESIS]** Chapter 01의 이중 규율—공짜 진실 금지와 공짜 소거 금지—가 처음으로 서로 다른 저장층을 얻는다.

### 5.4 인간적 의미: 일어났지만 아직 ‘내가 된’ 것은 아닌 것

Event가 포지션만 연다는 정의는 사람의 체험을 세밀하게 보존한다.

- 충격은 몸과 주의를 흔들지만 아직 하나의 교훈이 아닐 수 있다.
- 반복되는 생각은 JOT에 남지만 믿음이나 정체성은 아닐 수 있다.
- 관계의 Miss는 흔적을 남기지만 상대의 의도에 대한 판결은 아닐 수 있다.
- 창의적 장면은 다음 후보를 바꾸지만 실행 정책은 아닐 수 있다.

공적 권한의 관점에서 “원장에 적용되지 않음”은 아무 일도 없었다는 뜻이 아니다. 인간 런타임의 관점에서 **비승격 잔류**는 다음 후보 공간과 체감 시간, 몸의 경계를 계속 바꿀 수 있다.

### 5.5 사랑·미움·친밀·애착: 결박과 방향을 처음 갈라내다

0107 bundle 뒤에 붙은 0108 Addendum은 Event–Settlement 구조를 관계에 적용한다. 첫 선언은 도발적이다.

> Love/Hate는 모두 Casting과 Binding이다. `[BUNDLE7:L2060–2077]`

이 문장을 사랑과 미움이 같다는 정서적 명제로 읽으면 과장이다. 직접 정의에서 공통인 것은 대상이 내 서사의 등장인물로 편입되고 주의 예산을 점유한다는 점이다. 좋아함과 싫어함 모두 생각·비교·재호출을 만들 수 있고, 누적된 주의는 결박 `b_j`를 만든다 `[BUNDLE7:L2088–2107]`.

차이는 결박의 존재보다 **그 관계가 다음 챕터에서 어느 방향으로 정산되는가**에 있다. `σ_j`가 회복·의미 쪽으로 닫히는지, 손실·오염·회피 쪽으로 굳는지가 Love/Hate를 가른다 `[BUNDLE7:L2120–2131]`. 후속 패치는 이를 더 분명하게 `BIND`와 `VAL`로 나눈다. 높은 결박은 긍정과 부정 어느 쪽에도 남을 수 있다.

이 구분에서 두 개의 별도 관계량이 생긴다.

- **애착:** 좋아함이 아니라 제거비용 `RemoveCost`가 큰 상태. 그래서 싫어도 떼지 못할 수 있다.
- **친밀:** 감정 강도가 아니라 오독과 복구비가 낮고 ChapterSettle 성공률이 높은 결박 `[BUNDLE7:L2352–2370]`.

중독·강박도 단순 쾌락보다 “값싼 vividness 공급”으로 설명한다. 즉시 살아 있음을 높이지만 의미 정산은 빈약한 행동이 반복되면 주의와 결박을 납치할 수 있다 `[BUNDLE7:L2372–2384]`.

여기서 살릴 뉘앙스는 사랑의 강도를 하나의 결합계수로 재는 것이 아니다.

```text
얼마나 자주 호출되는가
≠ 얼마나 긍정적인가
≠ 얼마나 떼기 어려운가
≠ 얼마나 함께 운영하기 쉬운가
```

다만 “사랑은 실체감을 값싸게 얻는 유지 기제”라는 문장은 사랑의 타자성·돌봄·상대의 권한을 기능적 효율로 환원할 위험이 있다 `[BUNDLE7:L2161–2168]`. 또 내 주의와 결박은 상대의 상호성을 증명하지 않는다. 원문 자체도 짝사랑을 “내 원장에만 존재하는 결박”으로 구분한다 `[BUNDLE7:L2395–2400]`.

> **[LINEAGE HYPOTHESIS]** 후대 사랑 런타임에서 `private BIND`, 관계 valence, 상호 `κ`를 분리해야 했던 이유가 여기서 생긴다. 결박은 호출과 제거비용을 설명하지만, 타자의 독립적 상호 사건이나 공동 미래를 만들지는 못한다.

---

## 6. 1월 9일: 원장을 버리고 Quench를 발명하다

### 6.1 PHYSREFAC: 관계의 회계어를 물성어로 번역하다

`PHYS3`은 ledger, position, ownership, settlement, bet이라는 경제·법적 은유를 명시적으로 제거한다. 그 자리를 basin, binding, strain, injection, relaxation/release, Quench가 대신한다 `[PHYS3:L1–36, L883–895]`.

변환은 대략 다음과 같다.

| 이전 언어 | PHYSREFAC 언어 |
|---|---|
| 열린 position | 활성 basin·분지 |
| ownership / bond | binding `κ_bind` |
| bet / stake | allocation·injection |
| 미청산 debt | strain·residual |
| settlement | relaxation / release |
| commit 기능 | Quench로의 치환을 시도하되 후반 Addendum에는 기존 최종 Commit도 잔존 |

이 전환의 이점은 감정과 관계를 도덕적 채무나 소유권으로 선결정하지 않는 데 있다. 사랑, 불안, 집착, 상처가 반드시 “누가 누구에게 빚졌다”는 형식일 필요는 없다. 몸과 기억의 경로의존성만으로도 결속과 제거비용, 잔류와 재점화를 설명할 수 있다.

그러나 손실도 있다. 회계·원장 언어에는 “누가 무엇을 약속했고, 어떤 반응이 아직 오지 않았으며, 누가 수리 책임을 졌는가”라는 행위자와 범위가 남아 있었다. strain과 basin만으로 번역하면 책임과 증빙보다 상태 변화가 전면에 온다.

> **[BRIDGE-LEDGER-SCOPE]** 사적 체험의 잔류에는 물성·trace 언어가 더 안전할 수 있고, 공적 약속·권한·책임에는 receipt·ledger 언어가 필요할 수 있다.  
> Ledger를 전 영역에 일반화하거나 전 영역에서 제거하기보다 **적용 범위를 타입으로 제한**해야 한다.

### 6.2 Event–Release–Quench

PHYSREFAC에서 Event는 분지를 활성화하고 strain·binding·injection을 바꾸는 국면 변화다. 그러나 구조 변화는 SLOW/Quench에서만 확정된다 `[PHYS3:L209–243]`.

Release는 업데이트 후보를 만든다. Quench는 그 후보를 비가역 상태에 잠그는 연산으로 도입된다. 다만 후반 Addendum에는 Quench 조건을 통과한 결과도 후보이고 기존 Commit이 최종 확정한다는 이전 규약이 남아, 치환은 완전하지 않다. JOT은 미흡수 입력·몸의 경보·불확실한 잔류를 보존하며, 아직 정식 명칭이 닫히지 않은 update-candidate package의 재료가 될 수 있지만 상태는 아니다 `[PHYS3:L453–503]`. `CandidatePack`이라는 이름과 schema는 `PHYS4`에서 형식화된다.

Quench에 붙은 가장 중요한 봉인은 다음이다.

> Quench는 진실 선언이 아니라 update lock이다. `[PHYS3:L495–503]`

어떤 기억이나 정체성이 안정적으로 굳었다는 것은 그것이 참이어서일 수도 있지만, 반복·공포·습관·환경 폐쇄 때문에 안정된 것일 수도 있다. 비가역성은 사실성의 증명이 아니다.

### 6.3 `Potential ≠ Irreversible`

`PHYS4`는 이 분리를 헌법의 첫 문장으로 올린다.

> ISG·CBUF의 출력은 view/JOT이며, SSOT update는 별도의 Σ·safe·tick·stable 조건에서만 가능하다.  
> `Potential ≠ Irreversible.` `[PHYS4:L24–30]`

행동을 고르는 `ΔF-Select`와 어떤 의미 후보를 계속 살려둘지 고르는 `FELT-Select`도 분리된다. 창의적 생성이 넓어질수록 확정은 오히려 더 보수적이어야 하며, 불안정·불안전 상태에서는 JOT만 허용한다 `[PHYS4:L34–59]`.

이는 창의성과 안전을 서로 반대되는 양으로 두지 않는 구조다.

```text
탐색 폭 ↑
→ 후보 다양성 ↑
→ 불확실성과 상호충돌 ↑
→ 승격 문턱도 ↑
```

자유로운 생성이 강할수록 믿기 쉬워지는 것이 아니라, **더 많이 생성했기 때문에 더 조심해서 굳혀야 한다**.

> **[BRIDGE-EXPLORATION-CONSERVATISM]** 생성기의 자유와 승격기의 보수성은 같은 축의 타협값이 아니라 서로 독립적으로 강화될 수 있다.

### 6.4 CandidatePack은 결론이 아니다

`Σ`는 JOT·Trace·SceneSpec 등의 재료를 묶어 proposed deltas, support keys, safety snapshot, stability hint를 가진 CandidatePack을 만든다 `[PHYS4:L440–479, L791–817]`.

이 Pack은 정돈되어 있고 출처 참조도 갖지만 결론은 아니다. 특히 support key에는 생성된 SceneSpec도 들어갈 수 있으므로, 현행 의미의 증거 링크나 receipt로 읽을 수 없다. 잘 구조화된 제안과 실제 결과 기록은 다르다.

`stable_count`도 truth가 아니다. 일정 기간 유지되었음을 나타낼 뿐, 사실성·안전성·상호성·정당성을 증명하지 않는다. 안정된 오류와 오래된 집착도 가능하다.

> **[CHAPTER SYNTHESIS]** 0109에 이르면 생성 기원과 사건 기원이 Quench 앞에서 만날 수 있는 구조가 선명해진다. 다만 아래는 역할별 가능한 경로이지 모든 경우의 단일 필수 순서가 아니다.

```text
Generate / view → JOT·SceneSpec ┐
                                ├→ Σ / CandidatePack → QuenchTry
Execute / Event → trace·JOT   ┘
```

이것이 0110에서 다시 흔들린다.

---

## 7. 0110–0111 보관 bucket: Event를 시간으로 만들었다가 다시 풀다

### 7.1 0110의 재결합

`EVT1`은 하나의 완성본이라기보다 내부 날짜 0109–0110의 여러 Event 이론이 append된 patchbook이다. 앞 지층에서 EventTick은 선택 파이프라인을 호출하고 곧바로 `Gate → Feasible → ΔF → Quench`로 간다 `[EVT1:L196–227, L665–728]`.

시간은 “Quench로 잠긴 Event pulse”의 순서로 정의되고, 후반에는 Event 자체가 `Irreversible Record Boundary`로 다시 정의된다 `[EVT1:L456–498, L1229–1242]`.

같은 파일 안에서 Event는 적어도 세 역할을 한다.

1. 선택 파이프라인을 호출하는 펄스
2. Quench로 잠긴 episode/time point
3. 비가역 record boundary

이 재결합의 동기는 이해할 수 있다. 연속적인 내적 장에서 무엇이 “한 사건”으로 세어지고, 그 사건점들이 어떻게 한 사람의 세계선과 시간을 만드는지 설명하려 했다. 그러나 Event를 시간의 원자로 만들기 위해 Quench를 정의 속에 넣자, 0109에 얻은 `Event ≠ Irreversible`이 사라진다.

별도의 AXIOM37 0110 병렬 bundle `PAR10` 후반 ECELL 패치에서는 셀 전이, FELT 임계 초과, MetaAware scan까지 Event에 포함된다 `[PAR10:L2908–2924, L2999–3025]`. 그러면 Quench가 없는 전이와 스캔도 Event가 된다. 같은 보관 bucket의 병렬 트랙 사이에서 Event 존재론이 다시 갈라진다.

> **[CHAPTER SYNTHESIS]** 0110은 실패한 우회로라기보다, **사건과 시간이 왜 같은 말이 되어서는 안 되는지 드러낸 압력 시험**이다.

### 7.2 0110 `event 2`: 분리를 다시 세우다

같은 날의 후속 재발행 `EVT2`는 다시 명시한다.

- Potential과 view/JOT는 SSOT가 아니다.
- Event는 `e ≥ Θ_event`인 국면 변화일 뿐 비가역이 아니다.
- `Σ`는 CandidatePack 생성기이지 결론이 아니다.
- Quench는 truth declaration이 아니라 update lock이다.
- Stage12만 SSOT를 쓴다.

`[EVT2:L28–40, L422–438, L726–815, L1195–1244]`

Event에서 시작하는 한 가능한 경로의 역할 순서는 다음에 가깝다. CandidatePack은 반복 패턴·meta threshold·BIO/Clock 경계에서도 생길 수 있으므로, 이것이 유일한 필수 파이프라인은 아니다.

```text
Event: 경로를 흔듦
→ JOT/Residual: 미확정 재료를 남김
→ Σ/CandidatePack: 변경 제안을 구성
→ safe/tick/stability 검사
→ Quench: SSOT 업데이트 잠금
```

### 7.3 0111: Event clock과 Commit clock의 분리

`EVT3`는 네 개의 시간을 분리한다.

| 시간 경계 | 기능 |
|---|---|
| `ScanStep` | 감각·내부 상태를 읽는 미세 처리 |
| `ClockTick` | 배경 감쇠·회복·유지 경계 |
| `EventTick` | 문턱을 넘은 국면 변화의 발생 순서 |
| `CommitTick` | Quench를 검사할 수 있는 적용 경계 |

`[EVT3:L27–36]`

`EVT3`에서 Event는 `τ`를 증가시키지만 비가역 update는 아니다 `[EVT3:L48–66, L352–376]`. 즉시 JOT trace는 `EVT4`에서 추가된다. `stable_count`는 Clock/Commit 경계에서 세며, 사건이 많이 발생했다는 사실이나 진실성을 뜻하지 않는다 `[EVT3:L634–679]`.

`EVT4`는 `EventFire = current_pressure ≥ Θ_event`를 사건 발생의 기준으로 올리고, EventFire가 일어나면 EventTick과 “팡!” JOT trace를 남긴다. 그러나 SSOT update와 CommitCheckTick은 여전히 별개다 `[EVT4:L78–118, L361–384]`.

여기서 얻은 구조는 단순한 지연이 아니다.

> **[BRIDGE-EVENT-CLOCK-COMMIT-CLOCK]** 사건이 발생한 시간과, 장기 상태 적용을 검사하는 경계를 구분할 수 있다.  
> 다만 `EVT3`는 EventTick과 같은 tick에 CommitTick을 열 수도 있으므로, 이 구분 자체가 same-tick 승격을 금지하지는 않는다. 자동 승격을 막으려면 `CommitCheck > EventTick` 또는 현행의 별도 delay 봉인이 추가로 필요하다.

### 7.4 끝내 생기지 않은 EventRecord

이 계열의 역사를 현재에서 보면 `EventRecord`의 초기형을 찾고 싶어진다. 그러나 사료는 반대 결론을 지지한다.

- `EVT1` 후반은 Event 자체를 irreversible record boundary라고 부른다.
- `EVT2` 이후 raw occurrence는 JOT 재료로 간다.
- CandidatePack은 proposed deltas와 support refs를 가진 update 제안이다.
- Quench는 SSOT 적용 잠금이다.
- EventFire trace는 생기지만 receipt·provenance·outcome을 묶은 독립 typed record는 없다.

즉 발생, 지속 흔적, 변경 제안, 비가역 적용이 서로 갈라졌지만 **그 사이를 운반하는 증빙 결박된 1급 객체**는 끝내 안정되지 않았다.

> **[LINEAGE HYPOTHESIS]** 현행 `y = EventRecord`의 직접 조상이 이 시기에 완성된 것이 아니다.  
> 오히려 이 네 층을 한 타입 계약으로 닫지 못한 실패가 후대 `y`를 필요하게 만든 강한 발생 압력이다.

### 7.5 Event Canon이 남긴 내부 모순

0111의 최신판도 완전히 닫히지는 않는다.

1. `EVT4` 앞부분은 EventFire가 없으면 결정·잠금·의미 확정이 없다고 하지만, 뒤 Quench 식은 EventFire 없이 기존 CandidatePack을 잠글 수 있게 읽힌다.
2. 최종 runtime 순서에는 절대 기준이라고 한 EventFire 판정 단계가 빠져 있다.
3. 문서 부제는 `Generate → FELT-Select → Σ → Quench`인데 runtime은 Σ와 FELT의 순서를 바꾼다.
4. `Σ`는 operator/generator인데 Quench 조건에서는 boolean처럼 쓰인다.
5. `COMMIT`은 외부 행동 이름과 SSOT 저장 연산의 이름을 함께 가진다.
6. Event가 없어도 FAST microstate는 변할 수 있는데, “Event 없이는 state change 없음”이라는 문장이 범위를 구분하지 않는다.

특히 `SSOT_update ⇔ (Σ ∧ safe ∧ tick ∧ stable)`라는 쌍조건은 너무 강하다. 조건을 통과한 후보가 반드시 적용되어야 하는지, `reject`나 `nop`가 가능한지, 실제 결과와 증거가 어디서 묶이는지가 없다. 지속성과 안전만으로 warrant가 생기지도 않는다.

이 모순들은 장의 실패 목록이 아니라 다음 형식화를 요구한 정확한 빈자리다.

---

## 8. 본문 결론 — 비가역성을 제한하는 것이 현실성을 높였다

0104의 첫 공리는 커밋이 시간을 만들고 History가 된다고 선언했다. 이것은 Chapter 01의 흐릿한 `Wave/Measurement` 경계를 실제 writer와 저장 상태로 만들었다. 그러나 한 번의 출력·사건·기록·학습·정체성 변화가 모두 같은 Commit에 들어가면서, 현실성은 강해진 대신 너무 많은 것이 너무 빨리 현실이 되었다.

그 뒤 일주일은 그 과잉을 풀어내는 과정이었다.

- EOE는 일어나지 않은 미래도 현재를 점유한다는 것을 보였다.
- Threshold는 미달과 침묵이 0이 아님을 보였다.
- Ghost–Editor–Will–Map은 결심과 실행 사이의 서로 다른 병목을 갈랐다.
- Runtime은 계획·렌더·출력·Write를 분리했다.
- 다중 문턱은 사건·사실·학습·렌즈 변화를 갈랐다.
- JOT와 Episode는 미확정 재료를 지우지 않으면서 상태 승격을 막았다.
- Settlement와 CandidatePack은 변화 후보를 실제 적용 앞에 놓았다.
- Quench는 비가역성을 진실 선언이 아닌 update lock으로 낮췄다.
- EventTick과 CommitTick은 발생 시간과 적용 가능 시간을 갈랐다.

이 장의 역사적 연쇄를 가장 짧게 쓰면 다음과 같다.

```text
Commit이 현실을 만든다
→ 그러나 미커밋도 사람을 흔든다
→ 흔들림을 보존하되 상태로 자동 승격하지 않는다
→ 사건은 후보를 만들 뿐이다
→ 적용에는 별도 경계와 writer가 필요하다
```

> **[CHAPTER SYNTHESIS]** 현실적인 인간 모델은 모든 체험을 즉시 현실로 굳히는 모델이 아니다.  
> **아직 무엇인지 모르는 흔적이 남아 있으면서도, 그 흔적이 자기 자신을 진실·정체성·권한으로 승격하지 못하게 하는 모델**이다.

이 지점에서 Chapter 01의 두 규율은 더 구체적인 네 문장으로 확장된다.

```text
No Free Promotion: 발생했다고 사실이 되지 않는다.
No Free Erasure: 확정되지 않았다고 없던 일이 되지 않는다.
No Free Persistence: 남았다는 이유만으로 장기 상태가 되지 않는다.
No Free Authority: 장기 상태가 되었다고 공적 적용 권한이 생기지 않는다.
```

마지막 두 문장은 이 장의 원문에 그대로 있는 공리가 아니라, 0104–0111의 반복 교정을 읽어 추출한 Bridge다.

---

## Chapter 02 Research Afterword

### A1. 현재 이론으로 역조명한 계보

현행 형식은 `rho`라는 가역 후보장과 `a`라는 비가역 권위 원장을 분리한다. `rho`는 `a`를 직접 쓸 수 없고, 원장 갱신은 오직 Cut-2 `update(a,y)`에서만 일어난다. `inst(rho,call,a)`가 typed event record `y`를 만들며, `update` 결과에는 `[app]`, `[rej]`, `[nop]`가 있다. 적용된 업데이트는 receipt 또는 EvidenceLink와 결박되어야 한다 `[NOW:L375–410, L624–650]`.

또 certified한 도구적 성공은 applied와 같지 않고, claim은 오직 `compile(y,v)`에서 나온다 `[NOW:L526–529, L1055–1069]`. 따라서 초기 문서의 `Commit`, `Quench`, `CandidatePack`, `EventFire`를 현행 spine에 그대로 대입해서는 안 된다.

| 초기 구조 | 현행과의 판정 | 이유와 금지되는 동일시 |
|---|---|---|
| `Potential ≠ Irreversible` | **STRONG PRECURSOR** | 후보·view가 SSOT를 직접 쓰지 못한다는 문제와 규율이 연속된다. 단, 초기 Potential은 현행 `rho` 타입과 동일하지 않다. |
| view/JOT 자동 승격 금지 | **STRONG PRECURSOR** | 현행 S-NOUP/No-Promotion의 강한 선행 문제틀. JOT은 때로 court, 때로 store이므로 `phi`나 `ops` 하나로 고정할 수 없다. |
| Stage12 Single Writer | **STRONG PRECURSOR** | Cut-2-only writer discipline의 선행형. 초기 writer는 개인 내부 SSOT를, 현행 writer는 권위 원장 `a`를 보호한다. |
| `Event ≠ Irreversible` | **STRONG PRECURSOR** | 발생과 적용을 분리해야 한다는 핵심 문제의 연속. 초기 EventFire는 내부 threshold event이고 현행 `y`가 아니다. |
| `CandidatePack ≠ 결론` | **STRONG PRECURSOR** | structured proposal이 자동 적용되지 않는다는 규율. Pack은 결과 record나 evidence가 아니라 Cut-1 proposal 쪽에 가깝다. |
| Quench = update lock, not truth | **STRUCTURAL PRECURSOR** | 적용 경계와 명제 진실을 분리한다. proof-binding·typed `y`·`rej/nop`가 없으므로 `update(a,y)`와 직접 동일하지 않다. |
| stable_count ≠ truth | **STRONG PRECURSOR** | 지속성·확신·반복을 warrant로 쓰지 않는 non-tokenization 규율의 선행형. |
| EventTick ≠ CommitTick | **STRUCTURAL ANALOGY** | 발생 경계와 적용 검사 경계를 따로 생각하게 한다. 같은 tick 검사도 허용하므로 자동 승격 금지의 선행 규칙은 아니다. |
| EOE open/settle/expire | **DOMAIN PRECURSOR** | 열린 약속·기대의 생명주기 추적에 유용. 보편 스칼라 보존량은 계승하지 않는다. |
| EVENT의 SSOT | **ANALOGY ONLY** | 기억·정체성·압력·문턱을 포함한 개인 상태다. 현행 authority ledger `a`와 다르다. |
| JOT/Trace support key | **NOT EVIDENCE** | 생성 SceneSpec과 내부 trace도 참조하므로 EvidenceLink·Receipt가 아니다. |
| Joint Quench / JEID | **ANALOGY ONLY** | 동조된 사적 기억 링크다. paired/cross-linked receipt를 요구하는 것은 현행 core의 직접 규정이 아니라 이 장의 관계-domain 추가 가설이다. |

현행 spine과 가장 안전하게 대응시키면 다음 정도다.

```text
view / JOT material
≈ rho·phi·ops의 강한 선행 문제틀

Gate → Feasible → ΔF → Execute
≈ norm과 inst의 행동 선택·집행 앞부분과의 구조적 유비
(실제 outcome/provenance를 묶어 y를 만드는 record formation은 부재)

CandidatePack
≈ Cut-1 proposal envelope의 선행형

EventFire / JOT trace
≈ typed record 이전의 occurrence material

Quench / Stage12
≈ 단일 적용 경계의 선행 규율
```

반드시 유지해야 할 비동일성은 다음과 같다.

```text
EventFire ≠ y(EventRecord)
CandidatePack ≠ y
CandidatePack support_keys ≠ EvidenceLink / Receipt
Quench ≠ update(a,y)
EVENT SSOT ≠ authority ledger a
FELT select ≠ truth / certification
EOE의 e ≠ 현행 evidence section e
Certified ≠ Applied
```

> **[LINEAGE HYPOTHESIS]** 현행 Two-Cut은 0104의 공리 하나에서 직선으로 나온 것이 아니라, Event와 Commit을 여러 번 붙였다 떼고 JOT·Settlement·CandidatePack·Quench 같은 중간층을 시험한 뒤 남은 **선택적 압축으로 읽을 수 있다**.  
> 실제 인과 계보는 0112–0121의 중간 문서를 읽은 뒤 검증해야 한다.

### A2. `symbol_epoch`: 같은 이름 아래 서로 다른 이론

이 시기의 기호 충돌은 단순 편집 오류가 아니다. 해결하려는 문제가 바뀔 때마다 익숙한 단어를 새 역할에 다시 사용했다. 현재의 정의를 과거 파일에 소급하면 개념 계보가 거짓으로 매끈해진다.

| 개념 | 초기 epoch | 중간 epoch | 후반 epoch | 동일시 금지 |
|---|---|---|---|---|
| `Event` | 0106–07: 문턱 점프와 흔적 경화가 겹침 | 0107–08: 열린 position, Settlement 대기 | 0109: 비가역 아닌 국면 변화; 0110: 다시 Quench된 시간점; 0111: EventFire/JOT trace | `Event_hardening ≠ Event_position ≠ Event_phase ≠ Event_timepoint ≠ y` |
| `Commit` | History를 만드는 외부 비가역 커밋 | Probe/Bond 사이 관계 깊이, JOT 판결·가커밋, COMMIT-PLAN/WRITE | Quench의 동의어이자 Stage12 lock; 동시에 행동 이름에도 잔존 | 행동 선택·외부 출력·저장 잠금을 섞지 않는다. |
| `JOT` | `EQ` 후반 append에서 확인되고 `JOT07`에 재수록된 Editor 법정의 처리 회전 | 미확정 재료를 담는 append-only journal | CandidatePack이 참조하는 support material | `JOT_cycle ≠ JOT_store ≠ SSOT` |
| `EOE/e` | 기대에 건 관계적 상태량 | Work/Heat/Ledger의 보편 통화 | Budget에서 배치되어 문턱을 넘는 event energy | 어느 epoch에서도 epistemic evidence가 아니다. |
| `SSOT` | 최소 영구 상태를 고르는 저장 원칙 | “이 문서가 유일 권위”라는 문서 지위 | 개인의 FAST/SLOW/기억/정체성 상태 | 현행 권위 원장 `a`와 동일하지 않다. |
| `Ledger` | Claim·Promise·Correction 정합성 장부 | position·ownership·settlement의 관계 회계 | PHYSREFAC에서 제거 후 event trace 의미로 재등장 | 내부 회계, 공적 증빙, 권위 원장을 구분한다. |
| `Potential` | 후보·잠재장 일반 | ISG output의 비권위 생성물 지위 | 0110 localization/field potential | 타입 지위와 물리장 값을 섞지 않는다. |
| `Quench` | Event 점프 안에 암묵적으로 포함 | Release 뒤 비가역 update lock | Event를 시간점·세계선으로 만드는 연산으로 확대 | 0109의 Event 뒤 Quench와 0110의 Quench 포함 Event를 같은 식에 넣지 않는다. |
| `Σ` | summary/refocus kernel | CandidatePack generator | Quench 조건의 boolean처럼도 사용 | operator, output Pack, 승인 predicate를 분리한다. |
| `Φ` | 전체 내부장·상태 tuple | Trace/CBUF/phenomenal surface | 현행 `phi`는 근거 아닌 phenomenal readout | 동일 철자는 직접 승계를 보증하지 않는다. |
| `Λ` | 개인의 History·약속·상처·후회 원장 | 일부 문서에서 event partial order | 현행 `a`는 authority ledger | private memory와 public authority를 구분한다. |

이 표에서 특히 JOT의 의미 반전과 Event의 재결합은 별도 표준화가 필요하다. 후속 편집에서는 기호 뒤에 epoch 또는 역할을 붙이는 편이 안전하다.

```text
JOT.cycle / JOT.material
Event.occ / Event.trace / EventRecord
Commit.plan / Emit / Commit.apply
Ledger.private / Ledger.promise / Ledger.authority
```

### A3. 현재 형식화에서 빠지기 쉬운 인간적 뉘앙스

#### A3.1 마지막 폭발보다 그 전의 ‘비사건적 미달’

참다가 작은 일에 터질 때 최종 트리거만 Event로 기록하면, 그 전에 반복해서 문턱에 미달한 힘이 사라진다. 원문에서 미달은 `R`로 남고 반복 WAIT가 쌓여 Burst를 만든다 `[TH:L153–158, L387–391]`.

이는 모든 불만을 보존해야 한다는 뜻이 아니다. **발생하지 않은 행동도 다음 행동의 조건을 바꿀 수 있다**는 뜻이다.

#### A3.2 결심과 집행 가능성

닫고 싶은 Drive가 충분해도 BioCredit이 비용보다 작으면 closure는 일어나지 않는다. Will도 유한 TorqueBudget을 쓰는 중재기다 `[TH:L179–185, L213–224]`.

현행 `norm → call → inst`가 공적 절차를 정확히 분리하더라도, 인간 런타임에서는 “정당한 방향을 안다”, “결심했다”, “첫 동작을 시작할 토크가 있다”, “경로를 유지할 자원이 있다”가 다시 갈라져야 한다.

#### A3.3 Probe는 결론의 약한 버전이 아니라 지도를 사는 행동

Map 신뢰가 낮을 때 작은 Probe를 허용하는 이유는 확신이 조금 있어서가 아니다. 행동 결과를 관찰해 Map 자체를 만드는 정보 가치 때문이다 `[TH:L228–288]`.

낮은 Bet의 탐색은 “Commit을 덜 세게 한 것”이 아니라 목적과 성공 기준이 다른 행동 타입이다.

#### A3.4 침묵과 WAIT

Ignore는 미청산 포지션을 남기고, WAIT는 외부 Bet을 줄이는 대신 일부 압력을 내부화한다 `[EOE:L250–281]`. 공적 Event가 없더라도 인간 런타임에는 열린 기대와 노화하는 불확실성이 있을 수 있다.

따라서 모든 silence를 `nop`으로 해석해서는 안 된다. 건강한 경계 존중, 정보 대기, 두려움에 의한 억제, 수동 공격, 안전 정지는 표면이 같아도 다른 내부 생명주기를 가진다.

#### A3.5 Repair는 문장이 아니라 반복 이행

“미안하다”는 정보만으로 Peel이나 관계 손상이 직접 줄지 않는다. 시간, 불편 수용, 반복 약속, 보상 행동 같은 실제 후속 지불이 필요하다고 원문은 말한다 `[EOE:L361–373]`.

사과 Claim의 적절성, 사과 발화 receipt, 상대의 수용, 손상 회복, 재발 방지 규칙의 반복 이행은 서로 다른 사건이다.

#### A3.6 안전해진 뒤에도 바로 풀리지 않는 Mask

Mask는 외부 마찰을 낮추는 대신 내부 strain을 살 수 있다. 오래 유지하면 안전한 공간으로 돌아와도 Core로 즉시 전환되지 않아 멍함·말투 혼선·어색함이 남는다 `[A41:L2475–2486, L2565–2591]`.

Persona를 How/render 설정으로만 보면 이 전환 지연과 회복 비용이 사라진다.

#### A3.7 행동 사이의 법정과 사후 저자화

외부 행동이 없는 동안에도 여러 JOT가 돌 수 있다. 몸이 먼저 한 반사 행동도 이후 법정에서 인수·수리·거부의 대상이 될 수 있다 `[JOT07:L1103–1132, L1210–1261; EQ:L3034–3047]`. 이 뉘앙스는 책임을 “행동 전 완전한 의도”로만 환원하지 않는다.

#### A3.8 수면은 값의 단순 감쇠가 아니다

초기 문서는 수면과 Dream/VOID를 낮에 처리하지 못한 MaskStrain·Residual·상처를 상징·재연·재배열해 다음 날 prior를 바꾸는 구간으로 본다 `[A41:L2595–2619]`.

정리되지 않은 감정을 삭제하거나 진실을 생성하는 것이 아니라, 활성 간섭과 접근 지형을 다시 배치한다는 뉘앙스는 후대 maintenance epoch에서 살릴 가치가 있다.

#### A3.9 ‘일어난 일’과 ‘내가 된 일’의 거리

Event가 Quench되지 않았다고 영향이 없는 것은 아니다. 반대로 Quench되어 기억·정체성으로 굳었다고 그 해석이 참인 것도 아니다. 인간은 이 둘 사이에서 오래 산다.

### A4. 내부 긴장과 정본으로 올릴 수 없는 주장

#### A4.1 보편 EOE 보존

기대, 피로, 열, 상처, 관계 부채, 구조 변화는 서로 다른 단위와 관측 절차를 가진다. 이를 하나의 총량으로 보존한다고 주장할 근거는 없다. 살릴 수 있는 것은 “후속 효과를 누락하지 말라”는 lifecycle/accounting 규율이다.

#### A4.2 물리라는 이름의 권위

공리·구성방정식·상전이 언어는 다양한 현상을 압축하는 데 강하다. 그러나 Gate, 비용함수, tie-break, 안전 조건은 설계 선택일 수 있다. 이를 자연법칙처럼 부르면 정책의 가정과 반증 범위가 숨는다.

#### A4.3 hash determinism

해시 tie-break는 같은 입력의 재생 가능성을 준다. 선택이 옳거나 공정하거나 증거에 결박되었다는 보증은 아니다. `Deterministic ≠ Warranted`다.

#### A4.4 strict SEAL의 간접 누수

ISG/FELT가 ΔF 점수를 직접 바꾸지 않아도 후보집합을 바꾸면 argmin 결과가 달라진다. body scan이 `P_res`를 바꾸고 그것이 Gate 입력이면 역시 간접 영향이 있다. “직접 입력 금지”와 “결정 불간섭”은 같은 규율이 아니다.

따라서 완전 비간섭을 주장하기보다 영향 가능한 port와 금지되는 warrant 승격을 타입으로 명시해야 한다.

#### A4.5 안정성의 자기 정당화

`stable_count`와 반복은 유지 가능성을 측정할 수 있지만 truth를 만들지 않는다. 폐쇄된 환경, 공포, 습관, 상호 강화도 높은 안정성을 만든다.

#### A4.6 Event 중심 존재론의 사각지대

사건 사이에도 FAST drift, 회복, 노화, 유지보수, 약한 누적이 일어난다. “Event 없이는 의미 있는 변화가 없다”는 문장은 비가역 적용이나 공적 topology 변경처럼 범위를 좁혀야 한다.

#### A4.7 append-only의 보존 비용

JOT과 Trace를 무기한 append-only로 두면 사생활, 망각, 접근권한, retention, expiry 문제가 생긴다. 무상 소거를 막는 것과 영구 보존을 명령하는 것은 다르다.

#### A4.8 `SSOT_update ⇔ conditions`

안전·tick·stability·CandidatePack 존재가 모두 참이라고 반드시 업데이트해야 하는 것은 아니다. 현재 형식의 `[app]/[rej]/[nop]`와 proof-binding의 trace 필요조건은 이 부족을 줄이지만, 그것도 명제 진실의 충분조건은 아니다. 조건은 적용 자격의 일부이지 적용 의무나 진실 보증이 아니다.

#### A4.9 몸과 FELT의 자기 인증

몸과 퀄리아는 후보 우선순위와 탐색 폭을 바꿀 수 있지만 외부 원인이나 사실성을 인증하지 않는다. 강렬함, 불길함, 편안함, 반복 호출은 influence일 수 있으나 warrant는 아니다.

### A5. 이번 장에서 새로 열린 Bridge 가설

아래 Bridge는 현행 타입의 직접 기원을 주장하지 않는다. EVENT 계열이 남긴 미해결 분리 문제를 현재 언어로 다시 표현한 연구 가설이다.

#### BRIDGE.OCCURRENCE-ADOPTION — 발생과 채택

```text
Occurrence
→ runtime perturbation / trace
→ proposal
→ typed outcome record
→ kernel disposition [app|rej|nop]
→ adoption은 [app]일 때만
```

Event가 경로를 흔드는 것과 그 사건 해석을 장기 상태나 공적 원장에 채택하는 것은 다르다. `a`가 바뀌지 않아도 `rho/phi/ops`는 흔들릴 수 있다. 단, 내부 EventFire를 현행 `y`로 부르지는 않는다.

#### BRIDGE.PERSISTENCE-AUTHORITY — 지속성과 권한

이 장에서는 두 칸짜리 `rho/a`만으로는 가려질 수 있는 중간층이 보인다.

| 층 | 지속 가능 | 권위 있음 | 예시 |
|---|---:|---:|---|
| transient view | 아니오 | 아니오 | 순간 퀄리아·후보 |
| durable non-authoritative trace | 예 | 아니오 | JOT material, Episode residue |
| structured proposal | 예 | 아니오 | CandidatePack |
| authoritative applied state | 예 | 예 | proof-bound update 뒤의 `a'` (status `[app]`) |

> **가설:** `rho` 내부 또는 annex에 **durable-but-nonauthoritative** subtype을 명시하면, “원장에 없으니 영향 없음”과 “남았으니 권위 있음”이라는 두 오류를 함께 막을 수 있다.

#### BRIDGE.MISSING-RECORD-MIDDLE — 빠진 Record 중간층

초기 계열은 occurrence, trace, proposal, lock을 분리했지만 typed EventRecord를 만들지 못했다. 현행에서 `inst`의 역할을 다음처럼 더 명시할 수 있다.

```text
call을 실행한다
→ 실제 outcome·receipt·provenance를 묶는다
→ y(EventRecord)를 만든다
```

CandidatePack은 이 `y`가 아니라 실행 전 proposal envelope에 놓인다.

#### BRIDGE.PROCESS-STORE — 처리와 저장

`JOT_cycle`은 내부 판결의 처리 단위, `JOT_material`은 미확정 재료 저장소다. 둘을 구분하면 반추가 많지만 저장 흔적이 적은 상태, 흔적은 많지만 판결은 멈춘 상태를 따로 모델링할 수 있다.

#### BRIDGE.TWO-SELECTORS — 행동과 의미 후보

```text
Action selector: 지금 무엇을 실행할 것인가
Meaning-retention selector: 어떤 해석 후보를 다음 tick까지 살려둘 것인가
```

퀄리아와 FELT는 두 번째 selector에 영향을 줄 수 있지만 truth/certification selector가 아니다. 어떤 의미를 계속 생각하게 만드는 것과 그 의미대로 행동하거나 믿을 권한은 다르다.

#### BRIDGE.EVENT-CLOCK-COMMIT-CLOCK — 사건시계와 적용시계

Occurrence ordering과 authority-eligibility window를 별도 시계로 두는 것만으로는 same-tick 자동 승격이 막히지 않는다. `CommitCheck > EventTick` 같은 추가 순서 계약이 있을 때만 차단된다. 현재의 `delay(vis(a)) ≥ 1`과 직접 동일시하지 않고, 인간 런타임용 multi-clock 가설로 유지한다.

#### BRIDGE.PERSISTENCE-NON-TOKEN — 지속성은 토큰이 아니다

반복·안정·확신·오래됨은 maintenance와 scheduling의 readout이 될 수 있다. evidence, safety, mutuality, proof-binding을 대체하는 토큰으로는 사용할 수 없다.

#### BRIDGE.UNCOMMITTED-RESIDUE — 미커밋 잔류

JOT·Episode residue는 warrant 없이도 다음 후보와 비용 지형을 바꿀 수 있다.

```text
No Warrant ≠ No Influence
Influence ≠ Write Authority
```

이는 인간 런타임에서 `Influence ≠ Warrant`를 저장 구조로 구현하는 후보가 된다.

#### BRIDGE.SHARED-EPISODE-SHARED-AUTHORITY — 공동 체험과 공동 권한

동시에 겪고 강하게 동조했으며 같은 JEID를 가진다는 사실은 correlated private episode를 만들 수 있다. 현행 core의 좁은 필요조건은 각 update에 `Receipt OR EvidenceLink`가 동반되는 것이다. 양쪽의 독립적이거나 cross-linked된 receipt를 더 요구하는 것은 공동 사건·상호성 domain을 위해 이번 장에서 추가로 제안하는 가설이다.

```text
shared vividness
≠ paired receipt
≠ shared authority
```

#### BRIDGE.LEDGER-SCOPE — 원장의 적용 범위

사적 감정·퀄리아에는 strain/trace가, 약속·수리·공적 권한에는 receipt/ledger가 더 적절할 수 있다. 하나의 원장 은유를 인간 전체에 씌우지 말고, writer와 witness의 범위를 타입으로 제한한다.

#### BRIDGE.EXPLORATION-CONSERVATISM — 자유 생성과 보수 승격

생성 폭을 넓히는 정책과 승격 문턱을 높이는 정책은 동시에 강화할 수 있다. 이것은 창의성을 줄이지 않고도 환각성 확정을 줄이는 인간·AI 공통 런타임 원리 후보이다.

### A6. 상태별 연구 판정

| 항목 | 현재 판정 | 다음 조치 |
|---|---|---|
| L1 `Commit → History` | **역사적 핵심, 범위 과대** | 출력·기록·학습·적용을 분리한 채 기원 문장으로 보존 |
| L2 No Free Conversion | **강한 직관, 보편 스칼라 정리 아님** | 구체적 lifecycle·receipt·residual로 도메인별 검증 |
| L3 Timescale Separation | **유지 가치 큼** | FAST/MID/SLOW 외에 JOT/Event/BIO/Commit clock의 타입화 |
| L4 Coupling/Criticality | **모델 가설** | 관측량·단위·반례가 있는 domain model로 한정 |
| Threshold–Will–Map | **인간 런타임 핵심 후보** | 반사실 개입으로 병목 식별 가능성 시험 |
| EOE 기대 포지션 | **도메인 모델 후보** | scalar energy 대신 open/settled/expired/repaired lifecycle로 재작성 |
| EOE 보편 보존 통화 | **비정본** | 단위와 측정 계약이 생기기 전 canon 승격 금지 |
| JOT cycle | **복원 가치 큼** | journal 의미와 분리해 내부 처리 시계로 재도입 |
| JOT material | **복원 가치 큼** | retention/expiry/privacy와 no-authority 봉인 추가 |
| Event → Settlement → Commit | **강한 운영 선행형** | occurrence/trace/proposal/record/application 타입으로 재정의 |
| PHYSREFAC no-ledger | **부분 채택** | 사적 trace에는 사용, 공적 약속/책임에는 ledger 복원 |
| `Potential ≠ Irreversible` | **강한 선행 문제틀 후보** | 0112–0121의 실제 승계가 확인될 때까지 No-Promotion의 직접 전제로 단정하지 않음 |
| `Event ≠ Irreversible` | **강한 계보 자산** | EventFire와 현행 EventRecord의 비동일성을 함께 봉인 |
| CandidatePack | **연구형 proposal schema** | Cut-1에만 두고 evidence/receipt와 분리 |
| Quench | **구조적 선행형** | truth가 아닌 update lock이라는 뉘앙스만 계승 |
| Event-based time | **탐색 가설** | scan/live/retro/commit/public time을 하나로 합치지 말 것 |
| Joint Quench / JEID | **관계 동역학 가설** | paired/cross-linked receipt 요구는 이 장의 domain 추가 가설로 분리 |

이 장에서 실제로 수거된 가장 큰 새 관점은 하나의 새로운 변수라기보다 **네 단계의 분리**다.

> **일어난 것은 남을 수 있다.  
> 남은 것은 아직 제안이 아닐 수 있다.  
> 제안된 것은 아직 증빙된 사건 레코드가 아니다.  
> 증빙된 사건 레코드도 적용되기 전에는 권위 상태가 아니다.**

---

## 부록 A. 핵심 원문 위치

| 약칭 | 경로 | 주제 |
|---|---|---|
| `A37` | `연구/AXIOM37/0104 axiom37 1.txt` | L1–L4, corollary 재배치, 최소 저장, 비용 지형 |
| `A41` | `연구/AXIOM37/0104 axiom41 3.txt` | SEAL, W field, BIO time, Mask/Core, Dream patch |
| `SSOT` | `연구/AXIOM37/0104 ssot 1` | EOE conservation, minimal state, Kernel COMMIT writer |
| `EOE` | `연구/AXIOM37/0105  eoe .txt` | Expected Ownership, Hit/Miss/Ignore, WAIT, Repair |
| `TH` | `연구/AXIOM37/0105 thresh.txt` | Threshold, Ghost, Editor, Will, Map, Probe/Commit/Bond |
| `EOX` | `연구/AXIOM37/0105 eoethresh` | EOE×Threshold, continuous relation Depth |
| `RT01` | `연구/AXIOM37/0105 runtime` | BodyUpdate and StageWrite split |
| `RT02` | `연구/AXIOM37/0105 runtime spec 02` | persistent state, escrow, plan/render/emit/write |
| `EQ` | `연구/AXIOM37/0105 상태방정식 1 .txt` | EOE×Θ, 다중 문턱, JOT/BEAT, Episode/Narrative |
| `PC` | `연구/AXIOM37/0106 의사코드 1 .txt` | TruthGate, Event/Commit pseudocode, Soft/Hard Commit |
| `JOT07` | `연구/AXIOM37/0107 이론 통합 1` | recompiled JOT court cycle, authorship, Episode buffer |
| `EQ07` | `연구/AXIOM37/0107 상태방정식 2.txt` | LIVE/RETRO time, compressed field equations |
| `EQ07C` | `연구/AXIOM37/0107 방정식 통합1` | parallel field-equation consolidation |
| `BUNDLE7` | `연구/AXIOM37/0107 이론합본 ` | 0107 body + 0108 Love/Hate, Attachment, Intimacy Addendum |
| `INT8A` | `연구/AXIOM37/0108 new통합1 .txt` | Stage12 settlement, extended integration patches |
| `INT8` | `연구/AXIOM37/0108 New통합 2.txt` | NoDoubleCount, Event position, Settlement, Commit, CBUF |
| `PHYS3` | `연구/AXIOM37/0109 new물리통합3 .txt` | no-ledger refactor, Release, Quench, body scan |
| `PHYS4` | `연구/AXIOM37/0109 NEW물리통합 4.txt` | Potential/Event/CandidatePack/Quench 헌법 |
| `EVT1` | `연구/EVENT/0110 EVENT 1.txt` | EventTick→Quench, Event time, irreversible record boundary |
| `EVT2` | `연구/EVENT/0110 event 2` | Event≠Irreversible, CandidatePack, Quench/Stage12 |
| `PAR10` | `연구/AXIOM37/0110 new물리통합5` | internal 0109 strata + ECELL/MetaAware parallel patches |
| `EVT3` | `연구/EVENT/0111 event 3` | Scan/Clock/Event/Commit tick 분리 |
| `EVT4` | `연구/EVENT/0111 event 4` | EventFire, JOT trace, CommitCheckTick |
| `NOW` | `current_lens/monograph_edition_0_1_5_humanstack_v3_2_atlas_ats_v0_1.md` | 현행 Two-Cut·Proof-Binding·EventRecord·status spine |

원자료의 기준 루트는 이 작업본에서 `research_utf8/연구/`다. 행 번호는 해당 UTF-8 변환본을 기준으로 한다.

## 부록 B. 편집 상태

- 이 장은 원문 40개를 하나의 최신 스펙으로 병합하지 않았다.
- 중복 사본은 별도 증거로 중복 계상하지 않았다.
- 내부 작성일과 filename bucket이 다른 경우 둘을 분리해 기록했다.
- append된 후속 지층은 앞 본문을 자동 폐기한다고 가정하지 않았다.
- 직접 복원, chapter synthesis, lineage hypothesis, bridge를 표지로 구분했다.
- 현행 TAD와의 대응은 `STRONG PRECURSOR`, `STRUCTURAL PRECURSOR`, `STRUCTURAL ANALOGY`, `DOMAIN PRECURSOR`, `ANALOGY ONLY`, `NOT EVIDENCE`처럼 강도를 구분했다.
- 이 장의 Bridge와 상태 판정은 canon이 아니라 다음 장 이후 재검증할 연구 제안이다.
