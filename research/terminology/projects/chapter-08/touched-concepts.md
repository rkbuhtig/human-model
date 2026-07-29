# Chapter 08 — Touched Concepts

이 문서는 Chapter 08 배치가 기존 C-ID와 대조한 위치, C-ID를 열지 않은 인접 후보의 관계·목적지를 기록한다. 정의는 `termbase/concepts/`, 후보 설명은 `extraction-map.md`, 형제 비교는 후속 `termbase/clusters/`가 소유한다.

이번 intake는 기존 concept 정의·특성·판정을 변경하지 않는다.

## 1. 기존 concept 대조

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH08-021` Hypothesis→policy 조향
  - `X-CH08-043~046` AddressCandidate / AccessRequest / AccessSelection / Access bundle
  - `X-CH08-064` Deferred access
  - `X-CH08-075~079` scar 주변 policy pressure와 반응 분기
- 유지한 경계:

```text
주소 후보가 생김
≠ 접근 요청이 생김
≠ 접근 경로가 선택됨
≠ trace가 활성화됨
≠ 현재 Working Set에 편입됨

Hypothesis가 policy를 기울임
≠ 행동 경로가 선택됨
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - `AccessSelection RELATED-OR-NARROWER-CANDIDATE-OF C0001`, 상태 `HOLD`.
  - `Deferred_access`는 접근 불능이 아니라 현재 비접근 선택일 수 있으나 C0001과 동일 concept인지 미확정이다.
- 주의:
  - memory retrieval의 내부 selection을 일반 행동 경로 선택과 synonym MERGE하지 않는다.
  - scar policy pressure를 선택 결과 자체로 읽지 않는다.

### C0002 — 외부 occurrence

- 사용한 후보:
  - `X-CH08-022` 가설 기원 행동의 사후 흔적 요구
  - `X-CH08-036` archive/record boundary
  - `X-CH08-060~061` recollection backaction
  - `X-CH08-088` HistoricalActionAuthorshipAssessment
- 유지한 경계:

```text
과거 occurrence가 성립함
≠ 그 occurrence가 기억 graph에 남음
≠ 현재 회상함
≠ 현재 해석이 바뀜
≠ 현재 자아가 저자성 claim을 수락함
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - 회상 backaction은 access state update 후보이며 과거 occurrence가 아니다.
  - HistoricalActionAuthorshipAssessment는 actor relation 판정 후보이며 occurrence 자체가 아니다.
- 주의:
  - 현재 기억의 재구성이 과거 외부 사건을 소급 변경하지 않는다.
  - 기억이 생생하거나 self-attributed라는 사실로 performed action을 증명하지 않는다.

### C0003 — 결과 상태 후보군

- 사용한 후보:
  - `X-CH08-021~022` hypothesis-origin action과 사후 후과
  - `X-CH08-023~027` 미래 궤적 변화·Repair·MeaningInfluence
  - `X-CH08-073~079` AfterCost와 policy response
- 유지한 경계:

```text
미래 궤적이 달라짐
≠ 외부 world outcome이 실현됨
≠ repair가 성공함
≠ 현재 AfterCost가 생김
≠ 결과가 관측·정산됨
```

- 판정: `HOLD` 유지.
- 보류 이유:
  - MeaningInfluence는 인과적 trajectory difference이며 world outcome status와 동일하지 않다.
  - AfterCost는 활성 뒤의 내부 후과 후보이며 C0003의 외부·관계적 결과 후보군과 경계가 닫히지 않았다.
- 주의:
  - Chapter 08은 C0003의 genus·differentia를 닫을 독립 대비를 추가하지 않는다.

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH08-011~014` ClaimSig route metadata
  - `X-CH08-022` post-action trace requirement
  - `X-CH08-034~036` Memory Graph와 archive/record boundary
  - `X-CH08-057~058` external pointer와 recollection report
  - `X-CH08-060~061` Backaction
- 유지한 경계:

```text
occurrence record
≠ ClaimSig
≠ Memory Graph
≠ recollection report
≠ access/backaction trace
≠ external evidence pointer 그 자체
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - public evidence pointer는 occurrence record를 가리킬 수 있지만 pointer 자체와 record는 다르다.
  - ArchiveTrace·Memory Graph의 node가 occurrence를 표상할 수 있어도 모든 node가 occurrence record인 것은 아니다.
- 주의:
  - ClaimSig에는 claim body·event target·evidence reference가 없으므로 C0004와 병합하지 않는다.
  - 현재 회상 보고는 과거 occurrence record를 새로 mint하지 않는다.

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH08-037~041` conscious working memory·phenomenal scaffold·address vividness
  - `X-CH08-050~056` activation·Rehydration·Vividness
  - `X-CH08-059` familiarity/source/confidence 공백
  - `X-CH08-073~074` AfterCost와 체감 축
  - `X-CH08-086` PhenomenalMine-ness
- 유지한 경계:

```text
현재 회상 장면이 생생함
≠ 기억이 정확함
≠ 외부 evidence가 강함
≠ 출처가 맞음
≠ 그 기억이 내 과거라고 귀속됨

현재 AfterCost를 느낌
≠ 실제 자원이 그만큼 지출됨
≠ scar node가 객관적으로 존재함
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - RehydratedExperience·Vividness·PhenomenalMine-ness는 C0005와 가까운 surface 후보지만 process·content·mine-ness가 서로 다른 genus일 수 있어 `HOLD`한다.
  - Working Set은 current surface가 아니라 surface를 포함하거나 조건 짓는 active runtime set일 수 있다.
- 주의:
  - C0005를 모든 current activation·working memory·recollection content의 상위 바구니로 만들지 않는다.
  - familiarity와 confidence를 현재 체험의 질감 사례로 기록할 수 있어도 source truth와 동일시하지 않는다.

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH08-020~027` Hypothesis·MeaningInfluence
  - `X-CH08-037` implicit active causal state
  - `X-CH08-042~049` cue·context·Access·implicit influence
  - `X-CH08-060~061` recall backaction
  - `X-CH08-075~080` scar/lesson policy pressure
  - `X-CH08-081~085` Persona·Archive conditioning·κ_other
- 유지한 경계:

```text
Hypothesis
Story / MeaningFlux
Cue
Scar
Persona
Archive / Graph

≠ C0006

위 entity·state·content가
권위 없이 다음 access·policy·행동을 바꾸는 causal relation
= C0006과 대조할 위치
```

- 판정: `KEEP` 유지.
- 확인된 대비:
  - Hypothesis는 policy를 조향해도 Π_wit을 생성하지 않는다.
  - MeaningInfluence는 미래 trajectory를 바꿀 수 있어도 좋은 변화·truth·NarrativeAdoption을 보증하지 않는다.
  - recall backaction은 access geometry를 바꿀 수 있어도 과거 occurrence를 다시 쓰지 않는다.
  - Persona attractor는 무엇이 쉽게 활성화되는지를 조건 지을 수 있어도 현재 선택·권한·자아 전체가 아니다.
- 관계 후보:
  - `Hypothesis-source --C0006 relation--> policy/access change`, 상태 `HOLD`.
  - `Scar/Persona/Archive conditioning --C0006 relation--> current activation`, 상태 `HOLD`.
- 주의:
  - Chapter 08 entity를 C0006에 병합하지 않는다.
  - `next-tick`, `through W_t`, `through Access`를 C0006의 보편 필수 특성으로 올리지 않는다.

### C0007 — 수행 활동 후보군

- 사용한 후보:
  - `X-CH08-043~048` address generation·AccessSelection·Access-as-Forcing
  - `X-CH08-050~054` activation·Rehydration processing
  - `X-CH08-066` scaffold weakening·reweighting
- 유지한 경계:

```text
접근이 요청됨
≠ 접근 경로가 선택됨
≠ 실제 retrieval/activation 작업이 수행됨
≠ Rehydration이 수행됨
≠ resource가 지출됨
≠ trace가 기록됨
```

- 판정: `HOLD` 유지.
- 보류 이유:
  - address generation, retrieval, graph traversal, activation, re-expansion이 수행 활동의 종개념인지 하나의 recall process의 부분인지 미확정이다.
  - Access-as-Forcing은 operation과 cost/trace를 함께 압축한다.
- 후속 cluster 질문:

```text
Access는 하나의 수행 활동인가?
AccessSelection과 graph traversal은 같은 activity의 단계인가?
Rehydration은 retrieval의 일부인가 별도 reconstruction activity인가?
```

- 주의:
  - 실제 연산을 요구한다는 이유만으로 모든 후보를 C0007 아래 새 C-ID로 발급하지 않는다.

### C0008 — 실제 자원 지출

- 사용한 후보:
  - `X-CH08-047~048` Access-as-Forcing과 비용 분해
  - `X-CH08-073~076` AfterCost·LessonGradient
- 유지한 경계:

```text
AccessTrace
≠ MetabolicCost
≠ AttentionCost
≠ felt AfterCost
≠ LearningUpdate
≠ ScarUpdate
≠ NormativeDebt
```

- 판정: `KEEP` 유지.
- 관계 후보:
  - MetabolicCost·AttentionCost는 C0008의 NARROWER 후보일 수 있으나 실제 지출량과 자원 stock 대비가 없어 `HOLD`한다.
  - AfterCost는 체감·σ·κ 변화가 혼합된 후과라 C0008에 자동 포함하지 않는다.
- 주의:
  - 모든 Access가 state trace를 남길 수 있다는 주장과 모든 Access가 실제 자원 지출 또는 Bill을 발생시킨다는 주장을 분리한다.
  - 고통·주의 소모·대사 지출을 한 scalar로 합치지 않는다.

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보:
  - `X-CH08-011~014` ClaimSig metadata
  - `X-CH08-022` post-action trace
  - `X-CH08-036` archive/record boundary
  - `X-CH08-048` AccessTrace
  - `X-CH08-057~058` public pointer·recollection report
  - `X-CH08-060` Backaction trace
- 판정: `HOLD / SUBJECT-FIELD SPLIT` 유지.
- 확인된 기록 후보:

```text
route metadata record
access occurrence trace
working-set admission trace
learning/backaction trace
archive provenance record
public evidence pointer
recollection report
```

- 보류 이유:
  - 각 표상 대상과 정확성 조건이 다르다.
  - ClaimSig는 route constraint tuple이고 event·work·evidence record가 아니다.
  - Memory Graph는 저장 구조이며 모든 node가 audit record인 것은 아니다.
- 주의:
  - Chapter 08 기록 후보를 C0009 subject-field에 다시 한꺼번에 넣지 않는다.

## 2. 기존 C-ID 밖의 주요 HOLD 후보군

### 2.1 Route metadata / authority / configuration change

대상:

- `X-CH08-008~019`

형제 후보:

```text
interface Port
scope / Bandwidth
route declaration
route authorization
ClaimSig metadata
constraint completeness
SourceTag
Epoch identifier
Epoch change event
authorized migration
Evidence admission
Warrant
write capability
```

현재 상태:

- 전부 `HOLD`.
- ClaimSig는 synonym MERGE 대상이 아니라 route metadata inventory다.
- Epoch change는 event화되지만 proposal·writer·migration·rollback이 없다.
- `Authority Port`와 `B_wit`은 admission과 writer/binding을 다시 혼동한 역사적 conflict다.

### 2.2 MeaningInfluence / Repair / access geometry / adoption

대상:

- `X-CH08-023~027`

형제 후보:

```text
MeaningInfluence
BeneficialMeaning / Repair
future generation-rate change
AccessGeometryChange
NarrativeAdoption
```

현재 상태:

- 전부 `HOLD`.
- 같은 이름 아래 다른 질문이 들어간 것으로 판정한다.
- 새 C-ID는 열지 않는다.

### 2.3 Bounded activation / Working Set family

대상:

- `X-CH08-028~038`

형제 후보:

```text
active causal state
consciously reportable working memory
PerceptualWorkingSet
MemoryWorkingSet
CandidateWorkingSet
EvidenceReviewSet
ControlWorkingSet
```

현재 상태:

- 전부 `HOLD`.
- W_t는 하나의 concept라기보다 세 역할이 같은 철자를 공유한 후보다.
- generic/partitive/associative relation을 후속 cluster에서 판단한다.

### 2.4 Archive / Graph / Address / Access / Activation / Rehydration

대상:

- `X-CH08-031~054`

핵심 전이 후보:

```text
persistent background / archive potential
→ graph structure
→ address candidate
→ access request
→ access selection
→ local activation
→ Working Set admission
→ Rehydration
```

현재 상태:

- 전부 `HOLD`.
- 이 사슬을 하나의 `memory` concept로 압축하지 않는다.
- state/entity와 transition/process를 분리한다.
- `F_t ≠ 𝒢_t` 관계는 미확정이다.

### 2.5 Memory report / evidence / source attribution

대상:

- `X-CH08-055~059`

핵심 경계:

```text
Vividness
≠ Familiarity
≠ Confidence
≠ SourceAttribution
≠ EvidenceArtifact
≠ EvidenceLink
≠ Warrant
≠ Fact
```

현재 상태:

- 전부 `HOLD`.
- public pointer는 검증 가능한 연결 후보이지 truth 판정이 아니다.
- RecollectionReport는 EvidenceLink가 아니지만 방법·provenance·claim-specific relation 아래 evidence candidate가 될 수 있다는 후속 질문을 남긴다.

### 2.6 Backaction / persistent non-authoritative update

대상:

- `X-CH08-060~061`

핵심 경계:

```text
current access path reweighted
≠ past occurrence changed
≠ historical record rewritten
≠ current self authored the past
```

현재 상태:

- `HOLD`.
- C0006 relation과 관련되지만 update target·writer·timing이 미확정이다.
- JOT residue·CovState·PlasticTrace·M^plast와 같은 genus라고 가정하지 않는다.

### 2.7 Unknown / Forgetting failure positions

대상:

- `X-CH08-062~068`

분리한 후보:

```text
Unknown_external
Inaccessible_archive
Deferred_access
address/scaffold weakening
encoding failure
storage damage/deletion
rehydration failure
source-attribution loss
self-attribution loss
```

현재 상태:

- 전부 `HOLD`.
- Unknown은 하나의 concept가 아니라 epistemic/access/policy state 충돌이다.
- 0120 Forgetting은 접근 실패형 모델로 범위를 제한한다.

### 2.8 Scar / access geometry / cost / policy pressure

대상:

- `X-CH08-069~080`

분리한 축:

```text
stored/path-dependent history
node coupling
OpenEase
AfterCost
Evidentiality
identity importance
LessonGradient
policy response
```

현재 상태:

- 전부 `HOLD`.
- Scar를 하나의 scalar·기억 내용·임상 진단으로 승인하지 않는다.
- D→E refinement는 OpenEase/AfterCost 분리와 readdressing을 보존한다.
- approach/avoidance 이분법 밖의 반응 목록은 구성 후보이며 concept 판정이 아니다.

### 2.9 Persona / current Ghost / diachronic self / authorship

대상:

- `X-CH08-081~088`

핵심 경계:

```text
Persona attractor
≠ current Working Set
≠ current Ghost realization
≠ Archive / Graph
≠ diachronic self

Remembered
≠ Lived-by-me
≠ NarrativeAdopted
≠ Authored-by-me
```

현재 상태:

- 전부 `HOLD`.
- 0120은 Persona attractor와 접근 구조를 제안하지만 self-adoption·Episode provenance·authorship handoff를 만들지 않는다.
- identity/self 영역은 Chapter 09 intake 뒤 별도 cluster에서만 판단한다.

### 2.10 Relation / belonging / responsibility / authority

대상:

- `X-CH08-014`, `X-CH08-076`, `X-CH08-085`

핵심 경계:

```text
SourceTag
≠ blame

AfterCost / hurt
≠ responsibility truth

κ_other
≠ Belonging
≠ Stake
≠ Responsibility
≠ Identity
≠ ValidAuthority
```

현재 상태:

- 전부 `HOLD`.
- Chapter 08의 사회 결합 scalar를 확장 자기 경계 ontology로 사용하지 않는다.

## 3. 기호 epoch

Chapter 07에서 잠근 0119 의미와 Chapter 08의 0120 의미를 다음처럼 분리한다.

```text
π@STORY19          ≠ π@POLICY20
A@LENS19           ≠ A@ACCESS20
W@LENS19           ≠ W_t@WORKING-SET20
F@VITALITY19       ≠ F_t@FIELD20
κ@BIND19           ≠ κ@BINDING20 stable succession 미확정
S@WORLDLINE19      ≠ S@SSOT-LEDGER20 범위 미확정
```

- 기호 재사용은 concept MERGE가 아니다.
- Chapter 09에서 같은 철자가 다시 등장하면 0120 epoch를 선행 대조로 사용한다.

## 4. 후속 cluster 큐

이번 intake 뒤 가능한 cluster는 다음과 같다. 순서는 아직 확정하지 않는다.

### Route / ClaimSig / Epoch

- route metadata와 authority/evidence/configuration change 관계

### Archive / Graph / bounded activation

- F_t / 𝒢_t / W_t cardinality와 relation

### Access / Activation / Rehydration

- transition 분해와 실패 위치

### Memory report / evidence

- vividness·source attribution·public pointer·claim-specific support

### Persistent non-authoritative update

- backaction·JOT residue·CovState·PlasticTrace의 genus 비교

### Scar / access geometry / cost

- OpenEase·AfterCost·resource expenditure·policy pressure

### Persona / self / continuity / authorship

- attractor·current realization·Archive continuity·self-adoption·handoff

### Meaning

- MeaningInfluence·Repair·AccessGeometryChange·NarrativeAdoption

다음 cluster는 Chapter 08 review와 Chapter 09 intake 결과를 본 뒤 하나만 구체화한다.

## 5. 판정 요약

```text
C0001: KEEP 유지
C0002: KEEP 유지
C0003: HOLD 유지
C0004: KEEP 유지
C0005: KEEP 유지
C0006: KEEP 유지
C0007: HOLD 유지
C0008: KEEP 유지
C0009: HOLD / SUBJECT-FIELD SPLIT 유지

새 C-ID: 없음
MERGE: 없음
기존 concept 판정 변경: 없음
runtime/model/code 변경: 없음
```
