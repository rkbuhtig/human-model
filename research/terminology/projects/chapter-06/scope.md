# Chapter 06 Terminology Intake — Scope

## 1. 조사 질문

Chapter 05의 factory가 문서·key·socket의 실행 참여 경로를 닫은 뒤에도 남긴 두 공백을 Chapter 06이 어떻게 다루었는지 추출한다.

```text
외부 입력이 내부 계산에 들어옴
≠ 판정의 근거가 됨

현재 체감·전망이 완화됨
≠ 실제 문제·부담이 해소됨
```

Chapter 06은 이 두 공백을 각각 다음 계열로 푼다.

```text
Raw / Perc / Witness / View
→ 무엇이 판정에 참여할 수 있는가

pledge / Receipt / Store / σ / Bill
→ 현재 완화 뒤 남은 부담이 어떻게 지속·귀속되는가
```

그러나 이번 intake는 이를 완성된 네 층 ontology나 현행 정본 타입으로 승인하지 않는다. 중심 질문은 다음과 같다.

```text
Witness는 무엇을 보존했으며 어디서 Truth처럼 과장되었는가?
Grounds는 값의 종류인가, 특정 판정에서의 입력 역할인가?
Influence는 Grounds와 어떻게 갈리고 어디서 다시 섞였는가?
Receipt는 전략 설정·행동 수행·세계 결과 중 무엇을 실제로 증명하는가?
σ는 미해결 상태인가, 비용인가, 의무인가, 채무인가?
Bill은 청구 예정·후과 발생·원장 게시·정산 중 무엇인가?
```

## 2. 연대기 독해 원칙

파일명과 내부 버전 번호를 직선 발전 계보로 읽지 않는다. 2026-01-18 하루 동안 같은 문제를 여러 번 전면 재작성했고, 후기 최소 헌법의 내부 버전이 앞선 대통합 헌법보다 작다.

주요 상대 순서는 다음과 같다.

```text
MEM18
→ R03
→ R04
→ R05
→ STG0
→ STG1
→ STG2
→ RSUM
→ LINK18
→ AX18
→ JOIN18
→ TEM18
→ PATCH18
→ FULL18
→ RUN18
→ THEORY18
→ CON06
→ CON01
→ VES18
```

다음 자료는 별도로 취급한다.

- `EXPL18`은 2026-03-07의 후기 설명 거울이며 0118 당일 최초 정의의 근거가 아니다.
- `CON01`은 시간상 `CON06` 뒤에 작성된 최소 헌법 재추출 branch다. 내부 버전 번호가 작다는 이유로 `CON06`의 선행판이나 자동 superseder로 보지 않는다.
- `TEM18`의 Conn→Imprint는 보편 청구 가설을 확장한 side branch로 읽으며 core 공리로 자동 채택하지 않는다.
- `PATCH18`의 AXH vA0.4가 vA0.3을 supersede한다고 선언하지만 보존된 vA0.3 본문은 없다. 이를 provenance gap으로 기록한다.
- 같은 `vA0.1` 이름을 쓴 서로 다른 patch는 동일 artifact로 합치지 않는다.

앞 판본의 허용과 뒤 판본의 금지를 모두 최종 규칙처럼 합치지 않는다. 각 후보는 언제 등장했고 어떤 누수를 고치며 역할이 바뀌었는지 기록한다.

## 3. 선행 입력

이 프로젝트는 최신 `main`의 다음 결과를 선행 입력으로 사용한다.

- `projects/chapter-02/`
- `projects/chapter-03/`
- `projects/chapter-04/`
- `projects/chapter-05/`
- `projects/current-research/`
- `termbase/concepts/C0001.md` — 행동 경로 선택
- `termbase/concepts/C0002.md` — 외부 occurrence
- `termbase/concepts/C0003.md` — 세계 결과 상태
- `termbase/concepts/C0004.md` — occurrence record
- `termbase/concepts/C0005.md` — 현재 체험 표면
- `termbase/concepts/C0006.md` — 비권위적 미래 편성 영향
- `termbase/concepts/C0007.md` — 실제 탐색·비교 노동
- `termbase/concepts/C0008.md` — 실제 자원 지출
- `termbase/concepts/C0009.md` — 수행·지출 회계 기록 (`ENGINE-ONLY`)

이번 배치는 Chapter 06 후보가 기존 concept를 어떻게 비추는지 기록할 수 있지만 새 C-ID를 열거나 기존 concept 정의를 자동 수정하지 않는다.

## 4. 주 입력

- `chapters/chapter-06-witness-grounds-billing-0118.md`

Chapter가 복원한 다음 문제 흐름을 따른다.

```text
Chapter 05 evidence port 공백
→ Pressure / Repair / Relief
→ RiskCarry
→ Witness / Control / Storage / Bill
→ RawIn / PercIn 이중 경로
→ raw / eff residual
→ CosmeticRelief / TrueRelief
→ pledge
→ Receipt-only
→ Store / σ / σ_age / Bill
→ WitnessSchema allowlist
→ EvidenceCore / LedgerCore / SigmaCore
→ bounded CtrlCtx
→ Grounds / Influence 명시 분리
→ 보편 debt 팽창과 교정 요구
```

## 5. 보조 입력

다음 파일은 선행 경계와 현재 사용을 대조하는 데만 사용한다.

- `research/terminology/projects/chapter-05/extraction-map.md`
- `research/terminology/projects/chapter-05/basic-term-list.md`
- `research/terminology/projects/chapter-04/extraction-map.md`
- `research/terminology/projects/chapter-04/touched-concepts.md`
- `research/terminology/projects/chapter-03/extraction-map.md`
- `research/terminology/projects/current-research/extraction-map.md`
- `research/terminology/termbase/concepts/C0002.md`
- `research/terminology/termbase/concepts/C0003.md`
- `research/terminology/termbase/concepts/C0004.md`
- `research/terminology/termbase/concepts/C0005.md`
- `research/terminology/termbase/concepts/C0006.md`
- `research/terminology/termbase/concepts/C0008.md`
- `research/terminology/termbase/concepts/C0009.md`

Chapter 07 이후의 Fog·Reporter·Two-Cut, Chapter 11의 authorityless causal layer, 현행 TAD의 EvidenceArtifact·EvidenceLink·ObservationEvent·Certification은 Chapter 06 후보의 숨은 완성형으로 소급하지 않는다.

## 6. 출처별 주장 권한

| 출처 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| Chapter 06 역사 본문 | 0118 명칭이 어떤 판정·제어·저장·회계 역할을 맡았고 판본 사이에서 어떻게 교정됐는가 | 해당 구조가 인간 내부의 독립 모듈로 경험적으로 검증됨 |
| Chapter 06 연구 후기 | 당일 지층의 누수·과잉·현행 문제와의 구조적 연결 | 후기 bridge를 0118 원문의 직접 정의로 소급 |
| Chapter 05 배치 | input admission·closure·record·action/outcome 공백의 선행 문제 | Witness·Grounds가 Chapter 05에 이미 존재했다고 주장 |
| Chapter 04 배치 | Influence·actual work·Spend·accounting의 선행 경계 | X/R/U/A를 Chapter 06 정본 schema로 복구 |
| current-research | 현행 evidence·receipt·authority 경계가 요구되는 위치 | 현행 타입을 역사적 Witness·Receipt와 자동 동일시 |
| 기존 C-ID | 이미 분석된 occurrence·surface·influence·work·record 경계 | Chapter 06의 모든 후보를 기존 ID에 흡수 |

Chapter 06의 인간적 장면과 이론 사례는 저장소 내부 코퍼스다. 독립 관측 자료나 인간 일반에 대한 경험적 검증으로 표시하지 않는다.

## 7. 핵심 비동일성

### 7.1 Witness 계열

```text
organismal raw
≠ RawSlice
≠ Witness
≠ Grounds relation
≠ Truth
≠ Warrant
```

- `RawSlice`는 생명체가 해석하기 전의 절대 raw가 아니라 `GateRaw`와 schema를 통과한 판정 후보 입력이다.
- `Witness`는 초기에는 반박 불가능한 흔적처럼 과장되지만 뒤 판본에서 몸·환경에 남은 trace로 낮아진다.
- `Grounds`는 하나의 물질 종류가 아니라 판정이 참조하도록 허용된 입력 역할에 가깝다.
- Witness가 있다는 사실은 특정 claim을 어느 scope에서 지지하는지 자동 결정하지 않는다.

### 7.2 View·Influence 계열

```text
Qualia / View
≠ external fact grounds
≠ 비원인

Control Influence
≠ Grounds
≠ Accounting Imprint
≠ irreversible write authority
```

`View→Grounds`를 차단하면서 풍부한 체험·서사·자기해석이 미래 행동을 바꾸는 합법 경로까지 지우지 않았는지 추적한다.

### 7.3 Receipt 계열

```text
declared intention
≠ chosen strategy configuration
≠ strategy-setting Receipt
≠ performed action receipt
≠ external outcome evidence
```

0118의 후기 Receipt는 knob configuration과 cosmetic delta에서 자동 생성되는 controller-side 기록이다. 몸의 허가, 실제 행동 수행, 외부 결과, 독립 관측을 증명하지 않는다.

### 7.4 σ·Bill 계열

```text
unresolved state
≠ resource cost
≠ repair demand
≠ deferred obligation
≠ transferred burden
≠ normative debt
```

```text
Obligation
≠ BillIssued
≠ ConsequenceRealized
≠ Settlement
```

`σ`가 시간을 건너는 미해결 상태라는 수확은 보존하되, 모든 완화·연결·지속 차이를 채무로 만드는 팽창은 별도 과잉으로 기록한다.

## 8. 우선 대조할 선행 후보

- `X-CH04-015` — delayed causal lane
- `X-CH04-019` — influence provenance·warrant 공백
- `X-CH04-023` — actual-work 결박 지연 갱신
- `X-CH04-024` — No-discount·Throttle·Spend
- `X-CH04-030` — outcome record·observation receipt·EvidenceLink 공백
- `X-CH05-028` — ExternalIn을 VIEW로 제한한 over-closure
- `X-CH05-029` — policy-shaped PercIn 경로
- `X-CH05-030` — input admission과 evidence 분리
- `X-CH05-031` — policy-independent evidence port 부재
- `X-CH05-035` — Decision / ActionOut / occurrence / outcome 분리
- `X-CH05-036` — spec closure와 verified implementation closure 분리
- `C0002` — 외부 occurrence와 Witness·ActionOut의 경계
- `C0003` — world outcome과 Bill·σ·internal residual의 경계
- `C0004` — occurrence record와 Receipt·Witness bundle의 경계
- `C0005` — 현재 체험 표면과 Perc/View/Grounds의 경계
- `C0006` — 비권위적 미래 편성 영향과 CtrlCtx·policy operation의 경계
- `C0008` — 실제 자원 지출과 deferred burden·Bill의 경계
- `C0009` — 기술 회계 기록과 Receipt·Bill line item의 경계

## 9. 특별 처리 규칙

### Witness

- `Witness`를 `Truth`, `EvidenceArtifact`, `EvidenceLink`, `ObservationEvent`, `CertifiedEvent`와 자동 동일시하지 않는다.
- 초기 “반박 불가능” 표현과 후기 trace 교정을 별도 후보·재압축 이력으로 보존한다.
- schema allowlist가 무엇을 제외하는지뿐 아니라 새로운 증거를 어떻게 합법 발행하는지가 비어 있음을 기록한다.

### Grounds / Influence

- 두 용어가 명시적으로 등장하는 후기 `CON06`의 위치를 기록한다.
- 두 relation을 독립 검사한다는 규칙을 보존한다.
- `Grounds`가 claim-specific relation이나 Warrant type까지 완성했다고 과장하지 않는다.
- `Influence`를 control bus 하나로 축소하지 않고 accounting imprint와 구분한다.

### Receipt

- pledge의 자기서약 의미와 후기 자동 configuration receipt 역할을 분리한다.
- Receipt-only firewall을 기록하되 receipt 존재가 debt·action·outcome을 자동 승인하지 않음을 명시한다.
- `pledge_t` / `pledge_{t-1}` 표기 변화에서 double-delay 가능성을 별도 시간 잔차로 남긴다.

### σ / Bill

- `RiskCarry`를 초기 σ로 자동 개명하지 않는다.
- raw repair와 σ settlement를 별도 transition으로 보존한다.
- Bill의 청구 예정·실현 후과·원장 게시 의미를 한 concept로 승인하지 않는다.
- Conn→Imprint 보편 청구는 `SIDE BRANCH / HOLD`로 유지한다.

## 10. 조사 원칙

1. Witness를 현실 그 자체나 claim truth로 승격하지 않는다.
2. policy-independent under schema를 완전성·무오류성과 합치지 않는다.
3. unregistered를 false 또는 disproved로 바꾸지 않는다.
4. default deny와 positive evidence issuance를 분리한다.
5. View가 Grounds가 아니라는 이유로 causal Influence까지 제거하지 않는다.
6. bounded handle이 Grounds digest를 Control로 포장하는 hidden path가 될 수 있음을 확인한다.
7. current strategy가 자신의 미래 Bill 법칙을 바꾸지 못하게 한 교정을 보존한다.
8. configuration Receipt와 performed action receipt를 분리한다.
9. ActionOut을 actual occurrence나 world outcome과 동일시하지 않는다.
10. raw residual repair와 σ settlement를 자동 상쇄하지 않는다.
11. actual cost와 normative debt를 분리한다.
12. 모든 연결이 흔적을 남길 수 있다는 가설과 모든 연결이 채무를 낳는다는 주장을 구분한다.
13. same-commit 금지를 모든 즉시 보호 반응의 금지로 확대하지 않는다.
14. Authority를 phys 영역의 본질 속성이 아니라 특정 irreversible write capability로 읽되 현행 정본으로 자동 승격하지 않는다.
15. 후보 설명의 단일 권위는 `extraction-map.md`다. `basic-term-list.md`는 명칭 색인만 제공한다.

## 11. 산출물

- `extraction-map.md`: Chapter 06에서 추출한 중립 후보와 관계
- `basic-term-list.md`: 역사적 명칭·기호에서 추출 ID로 들어가는 색인

이번 배치에서는 다음을 만들지 않는다.

- 새 C-ID
- 기존 C0001~C0009 수정
- KEEP / MERGE / ENGINE-ONLY 판정
- Witness/Grounds/Receipt/σ/Bill 정본 ontology
- 현행 EvidenceArtifact·EvidenceLink 타입의 소급 적용
- harmonization 기록
- glossary
- current-use rename
- scenario suite·checker·status registry
- runtime/model/code 변경

## 12. 완료 조건

- Chapter 05의 evidence port 공백에서 Witness 계열이 왜 생겼는지 추적 가능하다.
- RawIn·PercIn·Witness·View의 역할과 한계를 구분할 수 있다.
- 초기 Witness의 truth 과장과 후기 trace 교정을 확인할 수 있다.
- raw residual과 experienced residual을 분리할 수 있다.
- pledge가 Receipt로 바뀐 의미 변화와 read-cap firewall을 추적할 수 있다.
- σ의 지속·경로 의존성과 obligation 과압축을 함께 보존한다.
- Bill의 세 의미와 settlement를 분리해야 할 이유가 드러난다.
- WitnessSchema allowlist와 positive evidence issuance 공백이 함께 보인다.
- Grounds·Control Influence·Accounting Imprint를 서로 다른 관계로 대조할 수 있다.
- View over-closure와 hidden grounds-to-control path를 모두 확인할 수 있다.
- Choice·strategy configuration·ActionOut·performed action·world outcome이 분리된다.
- universal debt와 Conn→Imprint side branch가 core 수확과 구분된다.
- Chapter 07 이후 용어를 Chapter 06의 숨은 정답으로 소급하지 않는다.
