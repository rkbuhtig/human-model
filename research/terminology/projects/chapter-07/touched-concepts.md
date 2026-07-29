# Chapter 07 — Touched Concepts

이 문서는 Chapter 07 intake가 기존 C-ID와 후속 cluster를 어디에서 건드렸는지 기록한다. 이번 배치는 concept 파일·판정·정의를 수정하지 않는다.

- 후보 설명의 단일 권위: `extraction-map.md`
- 명칭 색인: `basic-term-list.md`
- concept 정의와 현재 판정: `../../termbase/concepts/`
- 형제 후보의 실제 분석: `../../termbase/clusters/`

## 1. 기존 concept 대조 — 판정 변경 없음

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH07-035~039` — Fog·Ψ·Reporter·Polarizer·Ego Compression
  - `X-CH07-048` — Cut-1
  - `X-CH07-052~053` — Reporter/Editor 및 body/action gap
- 유지 판정: `KEEP`
- 보존한 경계:

```text
candidate field exists
≠ candidate is selected
≠ current scene is compressed
≠ strategy is adopted
≠ body authorizes execution
≠ action is performed
```

- 관계 후보:
  - `Cut-1 RELATED-TO C0001`, 상태 `HOLD`
  - Reporter frame selection은 C0001을 사용할 수 있는 선행 편성 과정일 수 있으나 synonym이 아니다.
  - EgoCompression은 선택 결과·선택자·행동 path 자체와 동일하지 않다.
- 다음 cluster:
  - selection / strategy authorship / Cut-1 relation
- 주의:
  - Ψ·Reporter·Cut-1을 C0001의 하위 유형으로 선판정하지 않는다.

### C0002 — 외부 occurrence

- 사용한 후보:
  - `X-CH07-049~053` — Cut-2와 body/action/outcome 중간층
  - `X-CH07-060` — Observation Jump
- 유지 판정: `KEEP`
- 보존한 경계:

```text
internal Cut-1
≠ irreversible application
≠ performed action
≠ external outcome
≠ someone observed
≠ occurrence record
```

- 관계 후보:
  - `PerformedAction NARROWER-CANDIDATE-OF C0002`, 기존 `HOLD` 유지
  - Cut-2는 C0002의 synonym이 아니다.
  - public exposure나 Observation Jump가 있다는 사실만으로 C0002 occurrence의 정확한 type이 정해지지 않는다.
- 다음 cluster:
  - `CL0003-action-outcome.md`
  - body / execution / outcome cluster

### C0003 — 결과 상태 후보군

- 사용한 후보:
  - `X-CH07-051`, `X-CH07-053`, `X-CH07-060`
- 유지 판정: `HOLD`
- 보존한 경계:

```text
external outcome
≠ observed reflection
≠ outcome observation
≠ social irreversibility
≠ evidence support
≠ settlement status
```

- 관계 후보:
  - `ExternalOutcome RELATED-OR-NARROWER-CANDIDATE-OF C0003`, 기존 `HOLD` 유지
  - Observation Jump는 outcome 자체가 아니라 타인의 관측·기록이 만든 사회적 비가역성일 수 있다.
- 재개 조건:
  - realized world outcome, relational outcome, observation status, settlement status의 대비 사례

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH07-049~051` — Cut-2 / external record 압축
  - `X-CH07-057~060` — Binding / Witness / Observation Jump
- 유지 판정: `KEEP`
- 보존한 경계:

```text
occurrence happened
≠ record persisted
≠ evidence link is valid
≠ event was certified
≠ state was applied
≠ another person remembers
```

- 관계 후보:
  - Commit-Cut의 trace attribution은 C0004와 `RELATED`, 상태 `HOLD`
  - `performed-action record NARROWER-CANDIDATE-OF C0004`, 기존 `HOLD` 유지
  - `B_other`와 Observation Jump는 social persistence를 보여주지만 occurrence record의 정확성·scope를 자동 보증하지 않는다.
- 주의:
  - vA0.3 Binding axis를 하나의 record concept로 복구하지 않는다.

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH07-001`, `X-CH07-008~010`
  - `X-CH07-017~018`
  - `X-CH07-039~040`
- 유지 판정: `KEEP`
- 코퍼스 확인 대비:

```text
현재 Φ·놀람·권태·행복·활력이 주어짐
≠ 외부 사실의 Grounds가 확보됨

현재 접근 가능한 범위가 좁음
≠ 세계에 증거가 없음
≠ 그 증거가 false임

현재 장면이 압축되어 주어짐
≠ 통시적 자아가 그 장면의 과거를 인수함
```

- 관계 후보:
  - `Π_view`, `ViewOut`, `d_cov`는 runtime projection·slot·readout이며 C0005와 synonym이 아니다.
  - EgoCompression은 current surface의 형성 과정과 관련될 수 있으나 self/identity 전체가 아니다.
- 다음 cluster:
  - current surface / current scene / compression relation
  - self / identity / authorship cluster

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH07-002~003`
  - `X-CH07-016~017`, `X-CH07-021`
  - `X-CH07-024`, `X-CH07-032~033`
  - `X-CH07-064`
- 유지 판정: `KEEP`
- 유지한 본질 경계:

```text
source state / representation / signal
→ later or immediate routing·attention·search·candidate influence

but

↛ self-issued Grounds
↛ Warrant
↛ irreversible writer authority
```

- 중요한 해석:
  - C0006은 `ViewOut`, `StoryField`, `MeaningFlux`, `Φ`, `Γ`, `Reporter`를 모아놓는 entity category가 아니다.
  - 이 source entity들이 권한 없이 변화를 일으키는 **인과 관계**를 소유한다.
- 관계 후보:
  - `StoryField RELATED-TO C0006`, 상태 `HOLD`
  - `MeaningFlux RELATED-TO C0006`, 상태 `HOLD`
  - `Γ / relationship terrain RELATED-TO C0006`, 상태 `HOLD`
  - `M4@MORNING19`는 C0006의 역사적 runtime 규율 대조이며 synonym이 아니다.
- H0001 유지:
  - next-tick은 필수 특성이 아니라 역사적 안전 구현이다.
  - `X-CH07-064`는 immediate nonauthoritative routing과 same-commit authority cast를 분리해야 한다는 후속 교정을 제공하지만, Chapter 후기 Bridge만으로 concept 정의를 수정하지 않는다.

### C0007 — 수행 활동 후보군

- 사용한 후보:
  - `X-CH07-012` — scan·compare work
  - `X-CH07-061~062` — optionality maintenance와 compute work
- 유지 판정: `HOLD`
- 확인된 경계:

```text
coverage expansion is desired
≠ scan/compare activity is performed
≠ resource is expended
≠ work is recorded
≠ deferred obligation is created
```

- 관계 질문:
  - scan과 compare는 수행 활동의 종개념인가?
  - candidate generation·rehearsal은 하나의 처리 과정의 부분인가?
  - attention switching은 수행 활동과 associative relation인가?
- 재개 조건:
  - generic / partitive / associative 관계를 가르는 코퍼스 대비
- cluster:
  - `CL0004-work-accounting-cardinality.md`

### C0008 — 실제 자원 지출

- 사용한 후보:
  - `X-CH07-012`, `X-CH07-019`, `X-CH07-027`
  - `X-CH07-061~062`, `X-CH07-066`
- 유지 판정: `KEEP`
- 코퍼스 확인 대비:

```text
F_out capacity
≠ F_use actual use

candidate generation work exists
≠ actual resource expenditure is measured

compute cost exists
≠ debt exists
≠ normative obligation exists
```

- 관계 후보:
  - `Spend_scan`·`Spend_cmp`는 actual expenditure role 대조 후보이며 이번 intake에서 C0008 synonym으로 승인하지 않는다.
  - `Budget_phys`는 derived slack이지 actual expenditure가 아니다.
- 다음 cluster:
  - performed cognitive activity / metabolic cost / attention cost / actual expenditure

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보:
  - `X-CH07-057~060`
  - `X-CH07-061~066`
- 유지 판정: `HOLD / SUBJECT-FIELD SPLIT`
- 강화된 이유:
  - vA0.3 Binding은 SSOT record, Witness, debt, other record를 하나의 강도 축으로 묶었다.
  - Optionality Cost는 performed work, cost attribution, debt, obligation을 같은 귀속식 주변에 모았다.
  - 이들은 하나의 accounting record concept가 아니라 서로 다른 표상 대상과 relation이다.
- 분리 유지:

```text
work-performance record
≠ expenditure record
≠ evidence artifact
≠ claim-specific EvidenceLink
≠ obligation record
≠ external occurrence record
≠ social memory
```

- cluster:
  - `CL0004-work-accounting-cardinality.md`
  - evidence / obligation cluster

## 2. 후속 cluster 입력

### 2.1 Evidence / observation / claim support

- 후보:
  - `X-CH07-023`, `X-CH07-028~033`
  - `X-CH07-034`, `X-CH07-041~047`
  - `X-CH07-050~051`, `X-CH07-055`, `X-CH07-059~060`
- 비교해야 할 것:

```text
world contact
≠ source projection
≠ observation method
≠ observation artifact
≠ Witness input
≠ claim-specific Grounds relation
≠ EvidenceLink
≠ Warrant
≠ Certification
≠ Application
≠ Truth
```

- 새로 추가된 압력:
  - same world contact가 여러 projection에 들어가는 것과 Grounds를 공유하는 것은 다르다.
  - closed input port만으로 positive evidence issuance가 완성되지 않는다.
  - Observation Jump의 사회적 비가역성은 method validity나 claim support를 보증하지 않는다.
  - Hallucination/elevation pressure는 candidate content보다 illicit evidence cast를 문제 삼는다.
- 현재 상태: `HOLD`

### 2.2 Persistent non-authoritative material

- 후보:
  - `X-CH03-010`, `X-CH03-019`
  - `X-CH07-010`, `X-CH07-056`, `X-CH07-063`
  - Chapter 08의 `PlasticTrace`, `M^plast` 대기
- 비교해야 할 것:

```text
unresolved durable record
≠ persistent perceptual/access state
≠ repeated-experience trace
≠ adaptation trace
≠ memory/plasticity state
```

- 공통 질문:

```text
persistence
⊥
authority
```

- 주의:
  - `durable non-authoritative material`은 cluster 질문이지 승인된 concept 이름이 아니다.
- 현재 상태: `HOLD`

### 2.3 Body / authorization / execution / outcome

- 후보:
  - `X-CH07-048~053`
  - Chapter 01 `X-CH01-031~036`
  - Chapter 06 `X-CH06-034~036`
- 비교해야 할 것:

```text
candidate selected
≠ Cut-1
≠ strategy adopted
≠ body permission/veto
≠ motor actuation
≠ performed external action
≠ external outcome
≠ outcome observation
≠ Cut-2 application
```

- 현재 상태:
  - `BodyAuthorization`: `HOLD`
  - `PerformedAction`: C0002 narrower candidate, `HOLD`
  - `ExternalOutcome`: C0003 relation candidate, `HOLD`
  - `OutcomeObservation`: evidence cluster, `HOLD`

### 2.4 Work / cost / obligation

- 후보:
  - `X-CH07-012`, `X-CH07-019`
  - `X-CH07-031`, `X-CH07-044`
  - `X-CH07-061~066`
- 비교해야 할 것:

```text
activity performed
≠ metabolic compute cost
≠ attention cost
≠ actual expenditure
≠ accounting trace
≠ deferred repair
≠ transferred burden
≠ normative obligation
```

- 새로 추가된 압력:
  - `No Unpriced Act`는 M1~M3의 순수 정리로 나오지 않고 별도 cost/obligation generation rule을 요구한다.
- 현재 상태: `HOLD`

### 2.5 Self / identity / authorship

- 후보:
  - `X-CH07-037~040`
  - `X-CH07-052`
  - `X-CH07-067~069`
- 비교해야 할 것:

```text
frame selection
≠ current scene compression
≠ current first-person runtime
≠ strategy authorship
≠ Episode binding
≠ Narrative adoption
≠ memory rehydration
≠ self-adoption
≠ diachronic identity
≠ authority over others
```

- 현재 상태: 전부 `HOLD`
- 주의:
  - Chapter 후기의 Ghost synthesis와 self-boundary five-layer는 Bridge다.
  - 새 identity C-ID는 Chapter 08~09와 독립 대비 사례를 함께 분석하기 전 열지 않는다.

## 3. 역사·runtime 역할

이번 intake는 아래 항목을 concept로 판정하지 않는다.

### provenance / epoch artifact

- `MORNING19`, `NIGHT19`
- `SLOT19`, `LINK19`, `NORM19`, `VESSEL19`, `CLEAN19`, `LOG19`
- `MIRROR19`

### runtime contract / checker 후보

- Phenomenology Payload Slots
- Linker Signatures
- LINT / TEST
- `Π_wit`, `Π_phys`, `Π_view`, `Π_ctrl`
- policy-latched `g_t / g_{t+1}`

### model assumption / model choice

- Observation = Control
- Default Fog를 모든 행동의 필수 조건으로 보는 주장
- attenuation-only Polarizer
- Reporter를 M1~M3의 필연 귀결로 보는 주장

### Bridge / current-lens 후보

- immediate nonauthoritative routing
- phenomenal geometry / adjudication metric 분리
- Ghost functional synthesis
- self-adoption / authorship handoff
- Belonging / Stake / Responsibility / Identity / Authority의 다중 자기 경계

## 4. symbol epoch

Chapter 07은 다음 의미를 고정하고 Chapter 08의 동철자와 분리한다.

```text
M1@MORNING19 ≠ M1@NIGHT19
M2@MORNING19 ≠ M2@NIGHT19

π@STORY19 ≠ π@POLICY20
A@LENS19 ≠ A@ACCESS20
W@LENS19 ≠ W_t@WORKING-SET20
F@VITALITY19 ≠ F_t@ARCHIVE20

g_t@LATCH19 ≠ g@GROUND19
κ@LINT19 ≠ κ@BIND19
```

동일 철자는 `basic-term-list.md`에서 서로 다른 추출 ID와 epoch로 연결한다. 이 작업은 synonymy나 직접 lineage 판정이 아니다.

## 5. 판정 요약

```text
C0001: KEEP 유지; Cut-1/Reporter relation 후보 HOLD
C0002: KEEP 유지; PerformedAction narrower 후보 HOLD
C0003: HOLD 유지; outcome/observation/social irreversibility 분해
C0004: KEEP 유지; Commit-Cut/Observation Jump relation 후보 HOLD
C0005: KEEP 유지; ViewOut/Π_view/EgoCompression synonymy 금지
C0006: KEEP 유지; source entity와 causal relation 비동일성 명시
C0007: HOLD 유지; scan/compare/optionality generic-partitive 미판정
C0008: KEEP 유지; capacity/use/compute/debt 분리
C0009: HOLD / SUBJECT-FIELD SPLIT 유지

새 C-ID: 없음
MERGE: 없음
기존 concept 판정 변경: 없음
새 cluster 판정: 없음
```
