# Chapter 08 Terminology Intake — Scope

## 1. 조사 질문

Chapter 07은 부분 Coverage 아래에서 가역 후보장을 편성하는 0119의 구조를 추출했다. Chapter 08은 0120이 그 후보장에 저장된 과거와 경로 제한을 어떻게 연결했는지 조사한다.

이번 배치는 다음 두 축을 하나의 완성된 기억 시스템으로 합치지 않는다.

```text
경로·규칙 축
Port / Bandwidth / ClaimSig / Epoch / Hypothesis / MeaningFlux

접근·기억 축
Working Set / Field / Graph / Address / Access / Rehydration / Scar
```

중심 질문은 다음과 같다.

```text
route declaration은 무엇을 허가하며 무엇을 증명하지 못하는가?
ClaimSig는 서명·인증서인가, 귀속 이동의 경계조건인가?
Epoch는 버전값인가, 변경 사건인가, 승인된 migration인가?
Hypothesis는 사실 권한 없이 어떻게 행동을 조향하는가?

저장된 구조와 현재 활성 상태는 어떻게 갈리는가?
주소·접근·활성·Working Set admission은 같은 사건인가?
Rehydration은 재생인가, 재구성인가, 현재 체험인가?
생생함·친숙함·출처 귀속·근거 자격은 어떻게 갈리는가?
회상 backaction은 무엇을 바꾸며 무엇을 소급 저작하지 못하는가?
Scar는 저장 내용인가, 접근 기하인가, 정책 압력인가?
Persona는 자아인가, 반복 접근 attractor인가?
```

이번 intake의 최상위 비동일성은 다음이다.

```text
Stored
≠ Addressable
≠ Accessible
≠ Activated
≠ Admitted to current Working Set
≠ Rehydrated
≠ Vivid
≠ Familiar
≠ Source-attributed
≠ Evidential
≠ Lived-by-me
≠ Self-adopted
≠ Authored-by-me
```

## 2. 연대기·판본 독해 원칙

### 2.1 0120 자료 ledger

Chapter 08이 복원한 1차 자료는 다음과 같다.

```text
EMPTY20
→ MAIN20
→ PATCH20-A
→ PATCH20-B
→ PATCH20-C
→ PATCH20-D
→ PATCH20-E
→ PATCH20-F
```

- `EMPTY20`은 0바이트 placeholder다. 파일명과 보존 시각만 기록하며 내용 근거로 사용하지 않는다.
- `MAIN20`은 UC+Q Integrated Clean · Living Dynamics를 자칭하는 0120 통합 본문이다.
- `PATCH20`은 하나의 clean addendum가 아니라 여섯 self-contained block이 이어 붙은 문서다.

`PATCH20` 내부 block은 다음과 같이 분리한다.

```text
A  SIG / EPOCH / HYP / κ_other / MeaningFlux
B  WSET / FIELD / ACCESS / COMP
C  GRAPH / IMG-SCAFFOLD / TRIGGER / REHYDRATION
D  SCAR / LESSON / PROPULSION 최초식
E  SCAR / LESSON / PROPULSION Refined
F  CLAIM-SIG / CHART-INVARIANCE / WSET /
   GRAPH·IMG-SCAFFOLD / ACCESS / BACKACTION 재컴파일
```

뒤 block이 앞 block의 모든 명칭과 정의를 자동 승계했다고 보지 않는다.

- E는 제목과 내용상 D의 명시적 refinement다.
- F는 A~E 전체를 대체한 최종 clean canon이 아니라 선택된 역할을 재컴파일한 block이다.
- `F_t`, Persona, Rehydration은 중간 block에 직접 등장하지만 F에서 이름 그대로 재수록되지 않는다.
- 재수록되지 않았다는 이유로 폐기라고 단정하지 않는다.
- 중간 발명이라는 이유로 최종 안정 타입이라고도 단정하지 않는다.

### 2.2 후기 거울

다음은 2026-03-07에 보존된 후기 자료다.

```text
BASE-MIRROR20
MAIN-MIRROR20
```

- `MAIN-MIRROR20`은 MAIN20 동일성 검증에만 사용한다.
- `BASE-MIRROR20`은 후기 편집 차이와 별도 baseline을 확인하는 보조 자료다.
- 둘을 0120 당일 최초 정의 근거로 사용하지 않는다.

### 2.3 직전·전방 경계

- Chapter 07의 `π@STORY19`, `A@LENS19`, `W@LENS19`, `F@VITALITY19`를 0120의 동철자와 자동 동일시하지 않는다.
- Chapter 09의 Qualia Surface·Persona runtime handle·Cross-Clock Selfness·Continuity Tax·Identity Tracking을 0120의 숨은 완성형으로 소급하지 않는다.
- Chapter 08 연구 후기의 Ghost·self-adoption·DID edge model은 0120 직접 타입이 아니다.

## 3. 선행 입력

이 프로젝트는 최신 `main`의 다음 결과를 선행 입력으로 사용한다.

```text
research/terminology/projects/chapter-01/
research/terminology/projects/chapter-02/
research/terminology/projects/chapter-03/
research/terminology/projects/chapter-04/
research/terminology/projects/chapter-05/
research/terminology/projects/chapter-06/
research/terminology/projects/chapter-07/
research/terminology/projects/current-research/
```

기존 concept 상태는 다음과 같다.

```text
C0001 KEEP  행동 경로 선택
C0002 KEEP  외부 occurrence
C0003 HOLD  결과 상태 후보군
C0004 KEEP  occurrence record
C0005 KEEP  현재 체험 표면
C0006 KEEP  비권위적 인과 영향
C0007 HOLD  수행 활동 후보군
C0008 KEEP  실제 자원 지출
C0009 HOLD / SUBJECT-FIELD SPLIT
```

이번 배치는 기존 판정을 변경하지 않는다. `touched-concepts.md`는 비교 위치와 후속 cluster 목적지만 기록한다.

## 4. 주 입력

- `chapters/chapter-08-finite-present-access-rehydration-scar-0120.md`

Chapter가 복원한 흐름을 다음 순서로 읽는다.

```text
Port / Bandwidth
→ ClaimSig
→ Epoch
→ Hypothesis
→ MeaningFlux 정의 이동
→ finite Working Set W_t
→ accumulated Field F_t
→ Memory Graph 𝒢_t
→ Image / Phenomenal Scaffold ℐ
→ Trigger / Cue
→ Access A_t
→ activation / Working Set admission
→ Rehydration in Ψ
→ vividness / evidence separation
→ recall backaction
→ Unknown / Forgetting
→ Scar
→ OpenEase / AfterCost
→ LessonGradient
→ Propulsion / Contraction / Readdressing
→ Persona attractor
→ 자기 인수·저자성 공백
```

## 5. 출처별 주장 권한

| 출처 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| Chapter 08 역사 본문 | 0120 명칭이 어떤 역할을 맡았고 PATCH block 사이에서 어떻게 교정·잔류했는가 | 해당 구조가 인간 기억의 보편적·경험적으로 검증된 모듈임 |
| Chapter 08 연구 후기 | 역사 지층의 타입 공백·과잉·현행 문제와의 구조적 연결 | Bridge를 0120 원문의 직접 정의로 소급 |
| Chapter 07 배치 | 0119의 View/Fog/Ψ/Reporter/기호 epoch 선행 경계 | 0120 Access·Memory Graph가 이미 0119에 있었다고 주장 |
| Chapter 06 배치 | Witness/Grounds/Receipt/σ/Bill·evidence gap 선행 경계 | ClaimSig·memory report를 기존 EvidenceLink로 자동 동일시 |
| 기존 C-ID | 이미 분석된 occurrence·surface·influence·work·spend·record 경계 | 0120의 모든 entity·process·relation을 기존 C-ID에 흡수 |
| 후기 거울 | 동일성 검증과 후기 편집 차이 | 당일 최초 발명·정의 시점 확정 |

Chapter 08의 사례·수식·엣지 모델은 저장소 내부 코퍼스다. 독립 관측 자료나 임상 증거로 표시하지 않는다.

## 6. 핵심 비동일성

### 6.1 경로·권한

```text
Port declaration
≠ route authorization
≠ payload integrity
≠ evidence sufficiency
≠ Warrant
≠ application authority

ClaimSig completeness
≠ truth
≠ evidence
≠ certification
≠ authority

Epoch identifier
≠ authorized epoch change
≠ migration
≠ rollback / revocation
```

### 6.2 후보·인과

```text
Hypothesis
≠ Evidence

Hypothesis motivates action
≠ Hypothesis becomes true

MeaningInfluence
≠ BeneficialMeaning / Repair
≠ AccessGeometryChange
≠ NarrativeAdoption
```

### 6.3 저장·현재 활성

```text
F_t
≠ 𝒢_t
≠ W_t

archive persistence
≠ current causal availability

W_memory
≠ W_scene
≠ W_candidate
≠ W_evidence
≠ W_control
```

### 6.4 접근·회상

```text
Cue
≠ Address scaffold
≠ Access request
≠ Access selection
≠ local activation
≠ Working Set admission
≠ Rehydration

Rehydration
≠ accurate replay
≠ evidence
≠ self-adoption
```

### 6.5 체험·근거·자기귀속

```text
Vividness
≠ Evidence strength

external pointer exists
≠ claim is true

Remembered
≠ Familiar
≠ Source-attributed
≠ Lived-by-me
≠ Self-adopted
≠ Authored-by-me
```

### 6.6 흔적·비용·의무

```text
AccessTrace
≠ MetabolicCost
≠ AttentionCost
≠ LearningUpdate
≠ ScarUpdate
≠ Receipt
≠ σ
≠ Bill
≠ NormativeDebt
```

### 6.7 흉터·정책

```text
OpenEase
≠ AfterCost
≠ Evidentiality
≠ Identity importance

Pain / AfterCost
≠ blame
≠ valid attribution

Scar
≠ clinical diagnosis
≠ identity
```

## 7. 우선 대조할 선행 후보

### Chapter 07

- `X-CH07-009~014` — Coverage와 persistent CovState
- `X-CH07-015~018` — Story/Φ/MeaningFlux와 C0006 관계
- `X-CH07-034~040` — Fog/Ψ/Reporter/Ego Compression
- `X-CH07-041~047` — M1–M3와 projection/positive evidence gap
- `X-CH07-048~053` — Two-Cut·action/outcome 공백
- `X-CH07-061~066` — optionality cost·immediate influence
- `X-CH07-067~069` — Ghost/self-adoption/authorship 공백
- `X-CH07-072~075` — π/A/W/F 전방 기호 재사용

### Chapter 06

- `X-CH06-021~028` — WitnessSchema·positive evidence issuance gap
- `X-CH06-030~038` — Grounds/Influence·same-commit 경계
- `X-CH06-012~020` — Receipt/σ/Bill·cost/obligation 과적재

### Chapter 03·04

- `X-CH03-008~014` — Ψ/JOT/SSOT/current scene·future draft
- `X-CH03-019` — 권한 없는 durable residue
- `X-CH04-015` — delayed causal lane
- `X-CH04-023~024` — work-coupled update와 actual Spend

### Chapter 01

- access lock / reconsolidation / Reflex Buffer / History / Scene / Editor / Plasticity 후보

## 8. 추출 묶음

`extraction-map.md`는 최소 다음 묶음으로 구성한다.

1. 판본·source authority·PATCH block
2. Port·Bandwidth·ClaimSig·Epoch
3. Hypothesis·MeaningFlux·비권위적 인과
4. Working Set·Field·Graph·저장 타입 공백
5. Address scaffold·Cue·Access·activation
6. Rehydration·vividness·evidence·source attribution
7. Backaction·Unknown·Forgetting
8. Scar·OpenEase·AfterCost·LessonGradient
9. Propulsion·Contraction·Readdressing·다중 정책 반응
10. Persona·Ghost·자기 연속성·authorship 공백
11. κ_other·관계 경계·의무/권한 과적재
12. 기호·타입 epoch와 Chapter 09 전방 질문

후보 수는 미리 고정하지 않는다. 각 후보는 하나의 중립 책임·관계·충돌·공백만 소유한다.

## 9. relation·판정 규율

- 모든 새 후보의 기본값은 `HOLD`다.
- 같은 runtime 흐름에 있다는 이유로 동일 concept라고 판정하지 않는다.
- 같은 특성 `persistent + non-authoritative`를 공유해도 genus가 다르면 별도 후보로 둔다.
- entity와 그 entity가 참여하는 causal relation을 구분한다.
- transition 후보를 state/entity concept에 병합하지 않는다.
- `MERGE`는 동일 genus·동일 본질/차별 특성·동일 외연·치환 가능성이 확인된 synonymy에만 사용한다.
- 이번 intake에서는 `MERGE`를 수행하지 않는다.

## 10. 산출물

```text
research/terminology/projects/chapter-08/
├─ scope.md
├─ extraction-map.md
├─ basic-term-list.md
└─ touched-concepts.md
```

오늘의 연구 일기도 같은 PR에 추가한다.

```text
research/diary/2026-07-29/
└─ 저장된-과거는-아직-현재의-나가-아니다.md
```

## 11. 이번 배치에서 하지 않는 것

- 새 C-ID 발급
- 기존 C-ID 정의·특성·판정 변경
- synonym `MERGE`
- Archive/Graph/Access/Rehydration 정본 ontology
- Working Set 하위 concept 선발급
- ClaimSig를 Warrant·EvidenceLink·EventRecord로 승격
- Rehydration을 정확한 replay로 승인
- Scar를 trauma·임상 진단으로 소급
- Persona를 Ghost·self와 동일시
- Access cost를 obligation으로 자동 cast
- Chapter 09 intake
- Bridge 기반 Ghost/self/DID 모델 정본화
- glossary·current-use rename
- runtime/model/code 변경

## 12. 완료 조건

- 모든 추출 ID가 연속적이다.
- 모든 basic-term-list 명칭이 extraction-map 후보로 연결된다.
- PATCH20 A~F의 역할 이동과 residue가 보존된다.
- MeaningFlux의 복수 정의가 하나의 안정 concept로 압축되지 않는다.
- `F_t / 𝒢_t / W_t` 관계가 미확정으로 남는다.
- Unknown의 근거 공백·접근 불가·전략적 보류가 분리된다.
- Access trace·cost·learning·scar·obligation이 분리된다.
- Rehydration·vividness·evidence·self-adoption이 분리된다.
- Scar의 OpenEase와 AfterCost가 분리된다.
- Persona·Ghost·archive continuity·diachronic self가 분리된다.
- π/A/W/F/κ/S의 0120 epoch가 기록된다.
- 새 C-ID·MERGE·concept 판정 변경·runtime 변경이 없다.
