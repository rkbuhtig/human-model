# Chapter 01 Touched Concepts

## 0. 판정 범위

이 문서는 Chapter 01 추출 후보가 기존 termbase에 실제로 어떤 영향을 주는지 기록한다.

이번 배치는 누락 보정이다. 기존 concept를 Chapter 01의 초기 명칭으로 소급하지 않으며 새 C-ID와 synonym `MERGE`를 만들지 않는다. 직접 복원된 대비는 provenance와 경계 질문으로 연결하고, `LINEAGE`·`BRIDGE`는 `PRECURSOR / RELATED / HOLD`로만 기록한다.

## 1. 요약

| 대상 | Chapter 01 대조 | 이번 결과 |
|---|---|---|
| C0001 행동 경로 선택 | Brain 판정, Body Veto, Scene 편집 | 정의 변경 없음; authorization·actuation·option-space modification은 HOLD |
| C0002 외부 occurrence | Measurement output, speech act, performed action | 정의 변경 없음; expressed act와 performed action은 NARROWER/RELATED 후보 |
| C0003 결과 상태 | Output–Reflection 관계 결과, 후속 자기 변화 | 기존 HOLD 유지; outcome·observation·relational state 분해 필요 |
| C0004 occurrence record | Reflex Buffer→History, History log | KEEP 유지; History는 PRECURSOR/RELATED이며 synonym 아님 |
| C0005 현재 체험 표면 | Reflex signal, subjective time, E_gap | KEEP 유지; felt occurrence와 external cause의 비동일성 보강 후보 |
| C0006 비권위적 인과 영향 | Flux, 질문, DREAM, Reflex, Anti-Masquerade | KEEP 유지; 강한 precursor지만 발화 타입과 인과 관계를 MERGE하지 않음 |
| C0007 실제 수행 노동 | Active Sensing, Scene 편집 | 기존 HOLD 유지; generic/partitive/associative 미판정 |
| C0008 실제 자원 지출 | Speech Stake, Claim Debt, Body cost | KEEP 유지; 관계 판돈·부담·손상과 실제 지출을 분리 |
| C0009 기록 subject field | History, Claim Debt, contract store | 기존 HOLD/SUBJECT-FIELD SPLIT 유지 |
| Evidence cluster | Evidence_Span, Cov, O_k, μ, receipt scope | 후속 cluster input; 현재 EvidenceLink/Warrant로 소급 금지 |
| Body/action cluster | Brain Commit, Body Veto, actuation | 후속 cluster input; BodyAuthorization C-ID 선발급 금지 |

## 2. C0001 — 행동 경로 선택

사용한 후보:

- `X-CH01-001`: 닫히지 않은 내부 가능성장
- `X-CH01-030`: Brain의 Claim/유보 판정
- `X-CH01-031`: Body Veto
- `X-CH01-036`: 말할 수 있음과 실행 가능성의 비동일성
- `X-CH01-043`: Scene/Editor의 환경 지형 변경
- `X-CH01-054`, `X-CH01-058`: Body Mediation·Geometry Freedom Bridge

판정:

```text
private candidate coexistence
≠ path selection
≠ claim authorization
≠ body authorization
≠ performed action
≠ option-space modification
```

Chapter 01의 `Brain Commit`은 선택·단정 허가·표현을 충분히 분리하지 않았으므로 C0001의 synonym이 아니다. `Body Veto`는 선택 이후 별도 실행 조건이 필요하다는 직접 대비를 주지만 독립 BodyAuthorization concept를 확정하지 않는다.

`Scene/Editor`는 후보 중 하나를 고르는 것보다 후보 지형을 바꾸는 개입일 가능성이 있다. C0001과 `RELATED` 후보로 남기며 generic/partitive 판정은 보류한다.

결과: **C0001 KEEP 유지, 정의 변경 없음.**

## 3. C0002 — 외부 occurrence

사용한 후보:

- `X-CH01-002`: Measurement의 외부화
- `X-CH01-020`: 비Claim 발화의 관계 사건성
- `X-CH01-035`: 내부 반응과 역사 기록의 비동일성
- `X-CH01-036`: 말할 수 있음과 실행 가능성의 비동일성
- `X-CH01-053`: Expression Ladder Bridge

판정:

Chapter 01의 `Measurement`는 출력·발화·행동·커밋을 한쪽에 모아 놓았기 때문에 C0002와 동일한 concept로 사용할 수 없다. 다만 외부로 실제 놓인 표현 행위는 generic external occurrence의 `NARROWER-CANDIDATE`일 수 있다.

```text
internal reflex
≠ expressed act
≠ performed bodily action
≠ world response
```

비Claim 발화가 관계 사건이라는 Chapter synthesis는 expressed act가 warrant 없이도 occurrence일 수 있다는 관계 후보를 주지만, 모든 발화를 C0002로 승인하거나 발화 내용의 진실까지 보증하지 않는다.

결과: **C0002 KEEP 유지. expressed act / performed action 관계는 HOLD.**

## 4. C0003 — 결과 상태

사용한 후보:

- `X-CH01-004`, `X-CH01-005`: Output–Reflection 관계적 Self와 지연
- `X-CH01-020`: 발화가 관계 경계와 미래 비용을 바꿈
- `X-CH01-042`: 외부 태도와 내부 믿음의 불일치
- `X-CH01-053`, `X-CH01-054`: expression/outcome Bridge

판정:

Chapter 01은 출력 뒤 돌아오는 반사가 관계·자기 상태를 바꾼다는 선행 장면을 제공한다. 그러나 다음이 아직 한 concept인지 판정할 수 없다.

```text
world outcome
relational outcome
observed reflection
internal interpretation
future-option change
```

따라서 Chapter 01은 C0003을 다시 KEEP으로 올리는 근거가 아니라, 현재 HOLD 사유를 강화한다.

결과: **C0003 HOLD 유지.**

## 5. C0004 — occurrence record

사용한 후보:

- `X-CH01-033`: Reflex Buffer
- `X-CH01-034`: History 승격
- `X-CH01-035`: 내부 반응과 역사 기록 분리
- `X-CH01-037`: History log
- `X-CH01-038`: History Receipt scope Bridge
- `X-CH01-021~023`: 기억 내용·접근·재공고화 분리

판정:

Reflex가 즉시 History가 되지 않고 Brain 관측·Body 결과·반복·쇼크 같은 추가 조건을 요구한다는 직접 대비는 occurrence와 durable record를 분리해야 했던 선행 압력이다.

하지만 초기 `History`는 발화·반사·태도·장기 기억을 넓게 포함하므로 C0004의 synonym이 아니다.

```text
temporary reflex buffer
≠ durable occurrence record
≠ current interpretation
≠ belief
≠ truth
```

`History is Stance, not Belief`와 receipt-scope Bridge는 기록이 행동 성립을 지지해도 내면 믿음·명제 진실까지 인증하지 않는다는 후속 evidence cluster 질문을 연다.

결과: **C0004 KEEP 유지. History는 PRECURSOR/RELATED, MERGE 금지.**

## 6. C0005 — 현재 체험 표면

사용한 후보:

- `X-CH01-014`, `X-CH01-029`: Reflex의 ALERT/TENSION/FLINCH
- `X-CH01-040`, `X-CH01-041`: 주관시간과 waiting/flow/shock/boredom
- `X-CH01-042`: E_gap과 내부 상태
- `X-CH01-055`: Scoped first-person warrant Bridge

판정:

Chapter 01은 경보·긴장·움찔과 주관시간 차이를 외부 사실 판정 이전에 나타나는 현재 현상으로 보존한다. 이는 C0005의 다음 경계를 지지하는 선행 사례다.

```text
felt occurrence
≠ external cause
≠ exact interpretation
≠ other person's intention
```

다만 `BRIDGE.SCOPED-QUALIA`의 제한된 1인칭 Claim은 Chapter 01 원문의 직접 개념이 아니므로 C0005의 정의나 evidence 권한을 변경하지 않는다.

결과: **C0005 KEEP 유지; provenance candidate 추가, 정의 변경 없음.**

## 7. C0006 — 비권위적 인과 영향

사용한 후보:

- `X-CH01-011~015`: Flux·질문·DREAM·Reflex·Anti-Masquerade
- `X-CH01-020`: 비Claim 발화의 관계 사건성
- `X-CH01-027`: 이중 보존 Bridge
- `X-CH01-043`: Scene/Editor
- `X-CH01-047`: 표현층 How→Decision 제한

판정:

Chapter 01에는 사실 단정 권한이 없지만 다음 탐색·행동·관계에 영향을 미치는 후보가 반복해서 나타난다.

```text
Flux
question
hypothesis / metaphor
reflex signal
tone
scene modification
```

이는 C0006이 다루는 문제의 강한 precursor다. 그러나 초기 항목은 발화 유형·신호·환경 개입·구현 금지로 서로 다른 범주이며, C0006의 인과 관계 concept와 synonym이 아니다.

Anti-Masquerade와 표현층의 직접 결정 개입 금지는:

```text
causal influence
≠ warrant
≠ decision authority
```

라는 경계가 왜 필요해졌는지 보여준다.

결과: **C0006 KEEP 유지; PRECURSOR/RELATED만 기록.**

## 8. C0007 — 실제 수행 노동

사용한 후보:

- `X-CH01-012`: Active Sensing
- `X-CH01-023`: reconsolidation edit
- `X-CH01-043`: Scene/Editor
- `X-CH01-048`: HookCompiler

판정:

질문·기억 편집·환경 재배치·컴파일은 모두 어떤 처리 활동처럼 보이지만 다음 관계가 닫히지 않았다.

```text
탐색 노동의 종개념
vs
더 큰 과정의 부분 단계
vs
관련된 별도 활동
vs
엔진 절차
```

Chapter 01은 C0007의 generic/partitive/associative 질문을 늘리지만 단일 genus와 차별 특성을 제공하지 않는다.

결과: **C0007 HOLD 유지.**

## 9. C0008 — 실제 자원 지출

사용한 후보:

- `X-CH01-016`: Speech Stake
- `X-CH01-019`: Claim Debt
- `X-CH01-032`: Body의 에너지·열·손상 정산
- `X-CH01-042`: 불일치가 남기는 열·그림자·폭발

판정:

Chapter 01의 비용 언어는 관계 판돈, 예측된 부담, 신체 손상, 은유적 열을 함께 사용한다. 이들을 실제 자원 지출로 자동 합치면 안 된다.

```text
speech stake
≠ claim debt
≠ felt pressure
≠ body damage
≠ actual resource expenditure
≠ normative obligation
```

Body의 실제 에너지 사용은 C0008과 `RELATED`할 가능성이 있지만, Chapter 01의 물리 은유만으로 측정 가능한 actual expenditure를 확정하지 않는다.

결과: **C0008 KEEP 유지; negative boundary 보강.**

## 10. C0009 — 기록 subject field

사용한 후보:

- `X-CH01-019`: Claim Debt
- `X-CH01-034`, `X-CH01-037`: History promotion/log
- `X-CH01-045`, `X-CH01-046`: Ω writer / Write-Derive
- `X-CH01-050`: 6-slot contract의 store
- `X-CH01-051`: symbol epoch

판정:

Chapter 01에도 History, debt bookkeeping, writer trace, store contract가 함께 나타나지만 이들은 하나의 기록 concept가 아니다. 이는 C0009의 `SUBJECT-FIELD SPLIT`을 되돌리지 않고 오히려 강화한다.

결과: **C0009 HOLD / SUBJECT-FIELD SPLIT 유지.**

## 11. Evidence / observation / claim-support cluster

입력 후보:

```text
X-CH01-006 Claim
X-CH01-007 Evidence_Span
X-CH01-008 O_k
X-CH01-009 μ
X-CH01-010 UNKNOWN/BLUR/COMMIT_OK
X-CH01-038 History receipt scope
X-CH01-055 scoped first-person warrant
```

보존할 경계:

```text
observation contact
≠ observability score
≠ output permission
≠ observation artifact
≠ claim-specific support
≠ warrant
≠ truth
```

`Evidence_Span/Cov/O_k/μ`는 출력 전 Claim gate이고, Chapter 06 Witness나 현행 EvidenceLink는 다른 파이프라인 위치와 표상 대상을 가진다. `PRECURSOR` 이상으로 승격하지 않는다.

결과: **후속 evidence cluster로 이동.**

## 12. Body / authorization / execution cluster

입력 후보:

```text
X-CH01-028 IRB time scales
X-CH01-030 Brain adjudication
X-CH01-031 Body Veto
X-CH01-032 body cost/damage
X-CH01-036 authorization ≠ execution
X-CH01-054 Body Mediation
```

보존할 경계:

```text
claim adjudication
≠ path selection
≠ call authorization
≠ body permission/veto
≠ motor actuation
≠ external occurrence
≠ observed outcome
≠ pain/damage/recovery
```

Chapter 01은 BodyAuthorization 결손에 대한 선행 자료를 제공하지만 `Body Veto` 하나로 전체 body ontology를 확정할 수 없다.

결과: **BodyAuthorization·BodyVeto·actuation 후보 모두 HOLD.**

## 13. Governance / terminology method

입력 후보:

- `X-CH01-045~050`: Single Writer, Write/Derive, 표현층 경계, HookCompiler, glossary/contract
- `X-CH01-051`: symbol epoch
- `X-CH01-052`: 물리 은유의 권위 차용 위험

판정:

0103-A와 0103-B의 차이는 용어 설명과 실행 계약이 다른 산출물이라는 직접 사례다. 6-slot 계약은 현재 terminology concept schema가 아니라 엔진 책임 계약의 역사적 전신 후보다.

Chapter 01의 기호 재사용 목록은 `basic-term-list.md`가 단어만이 아니라 epoch/역할을 함께 색인해야 한다는 운영 근거를 제공한다. 그러나 이번 PR에서 전역 schema나 checker를 추가하지 않는다.

## 14. 이번 배치에서 바뀌지 않는 것

- 새 C-ID 없음
- synonym `MERGE` 없음
- C0001·C0002·C0004·C0005·C0006·C0008의 현재 판정 유지
- C0003·C0007·C0009의 HOLD 유지
- H0001~H0003 수정 없음
- Chapter 01 Bridge를 concept 근거로 사용하지 않음
