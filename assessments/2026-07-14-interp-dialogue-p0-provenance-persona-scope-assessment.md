# INTERP-DIALOGUE-001P0 provenance와 persona scope에 대한 외부 평가

| 항목 | 값 |
|---|---|
| Document type | External non-peer assessment |
| Canonical status | **NON-CANONICAL** |
| Adoption status | 이 문서에서는 판정하지 않음 |
| Evaluated artifact | PR #15 — `INTERP-DIALOGUE-001P0-v0` |
| Evaluated merge commit | `05d946590a605a76e1bbe89fceab8b556c2d37cf` |
| Source provenance | 2026-07-14 사용자 제공 피드백과 병합된 저장소 상태의 구조화된 기록 |

> 이 문서는 외부 평가를 보존한다. 여기에 적힌 제안은 채택된 주장, 구현 상태,
> 실행 결과 또는 인간 메커니즘의 증거가 아니다. 채택 판정은
> [별도 adoption record](../research/adoption-records/2026-07-14-interp-dialogue-p0-provenance-persona-scope.md)에 있다.

## 총평

평가자는 PR #15를 중단하거나 갈아엎을 대상으로 보지 않는다. PR #15의 목적은
범용 인간 측정 infrastructure가 아니라, 동결된 개발용 elicitation script를 exact
scripted replay로 재현하고 raw payload와 schedule provenance를 손실 없이 보존하는 데
있다.

```text
scripted replay
!= actual participant/model acquisition
!= latent-state observation
!= persona measurement
!= human-mechanism support
```

이번 평가의 핵심은 PR #15의 목적을 바꾸는 것이 아니라, 이후 연구가 그 범위를
과승격하지 못하도록 관측과 해석의 경계를 더 정확히 기록하는 것이다.

## 1. `First Failure`보다 먼저 필요한 관측 경계

`afterneu` 계보에서 제안된 `First Failure + Recovery`는 페르소나 연구의 유력한 아이디어
후보다. 그러나 현재 P0의 vignette judgment와 scripted replay가 직접 관측하는 것은
내부 기능의 최초 변화가 아니다.

```text
first latent change
!= first detected surface deviation
```

내부 변화와 표면 사이에는 다음이 개입할 수 있다.

- role contract
- transient gate state
- expression permission
- mask / leak policy
- compensation
- observation-channel sensitivity

따라서 응답 표면에서 먼저 보인 단답, 멈칫, 회피 또는 불일치는 내부 기능의 최초
변화나 실패 순서를 인증하지 않는다. 변화 순서 역시 total order일 필요가 없으며,
동시 변화, 미관측 변화, interval censoring과 unknown order를 허용해야 한다.

현재 안전한 연구 대상은 `ProtectedFunctionSet`이나 `SelectiveAdaptationGrammar`가 아니라
조건부 표면 변화의 후보 signature다.

```text
SelectiveTransitionSignature
-> held-out perturbation prediction
SelectiveTransitionGrammarCandidate
-> functional preservation/outcome criterion
SelectiveAdaptationGrammarCandidate
-> role/state/session-stable replication
PersonaSpecificGrammarCandidate
```

이 승격 사다리는 미래의 longitudinal PERS 연구에 속하며 P0/P1의 측정 대상이 아니다.

## 2. 역할과 페르소나를 분리

과거 runtime 문서는 역할과 페르소나를 다르게 두었다.

```text
RoleContract
= 외부 인터페이스, 책임, 금기와 기대

Persona candidate
= 역할을 받아들이고, 충돌시키고, 벗어나는 방식에 남는 안정 후보
```

따라서 역할 계약 자체를 persona 구성요소로 넣어서는 안 된다. 미래 persona 연구에서
고려할 수 있는 것은 다음과 같은 조건부 문법이다.

```text
RoleUptakeGrammar
RoleConflictGrammar
RoleExitGrammar
```

이들 역시 현재는 경쟁 가설일 뿐이다.

## 3. 현재 24개 시나리오의 범위

현재 24개 cell은 현실 영역의 functional-jurisdiction vignette다. 참가자는 가상 상황을
보고 응답한다.

```text
participant vignette judgment
!= vignette actor persona
!= participant persona
!= Human runtime trace
```

현재 trace oracle이 등록한 matched-future authority는 세 pair에 한정된다.

```text
rel-000  <-> rel-100
work-000 <-> work-100
risk-000 <-> risk-100
```

24개 cell은 initial presentation에 사용할 수 있지만, 나머지 cell에 future option을
붙였다는 사실만으로 PR #13 matched-future oracle authority가 생기지 않는다.

현재 horizon에서 얻을 수 있는 것은 frozen mapping이 생긴 뒤의 immediate/later surface
후보뿐이다. 다음은 현재 자료로 판정할 수 없다.

```text
actual first failure
recovery order or time
durable residual
cross-domain trait
persona identity
```

PERS 연구는 P0의 컬럼 확장이 아니라 다중 session, perturbation ramp, recovery probe와
held-out domain prediction을 가진 별도 longitudinal study여야 한다.

## 4. 응답 제출과 내부 응답 생성 과정을 분리

`ResponseProductionOccurrence`라는 표현은 답을 만드는 내부 인지 과정을 관측한 것처럼
읽힐 수 있다. 실제 acquisition에서 직접 기록할 수 있는 것은 보통 다음이다.

```text
ResponseSubmissionOccurrence
ResponseReceivedOccurrence
RawResponseReceipt
```

UI가 실제 interaction start를 기록한다면 `InputInteractionStarted`를 남길 수 있지만,
그것도 생각이 시작된 시각은 아니다.

```text
response submitted before later prompt
-> later trajectory를 바꾸었을 가능성

but
-> 어떤 내부 처리로 바뀌었는지는 관측하지 않음
```

따라서 미래 schedule 비교도 mediation을 미리 주장하지 않고 노출 조건으로 명명한다.

```text
NO_INTERMEDIATE_ELICITATION
PRIOR_FREE_RESPONSE_EXPOSURE
PRIOR_STRUCTURED_RESPONSE_EXPOSURE
```

`response-mediated`는 실제 mediation design과 분석 뒤에만 사용한다.

## 5. 질문과 답변은 단순 관찰이 아니라 사건일 수 있음

P0 schedule에서 immediate prompt와 scripted response record는 later prompt보다 앞에 있다.
실제 인간 또는 모델 acquisition에서는 질문을 받고 응답을 제출하는 행위가 rehearsal,
commitment, self-perception 또는 attention change를 만들 수 있다.

```text
E0 vignette
-> E1 immediate prompt
-> R1 response submission/receipt
-> E2 future option
-> E3 later prompt
-> R2 later response
```

따라서 O10과 같은 later surface는 자연적·무개입 trajectory가 아니라 prior elicitation
exposure 뒤의 표면이다. 양 arm에 같은 질문을 주는 것만으로 interaction effect가 제거된다고
가정할 수 없다.

후속 `PROMPT-REACT-001`은 다음 schedule을 비교해야 한다.

```text
no intermediate elicitation
free response exposure
structured response exposure
```

그 전까지 prior-response-exposed later surface를 unprompted latent persistence로 해석해서는
안 된다.

## 6. P0/P1 provenance에서 관측 가능한 것

PR #15는 고정 schedule과 exact payload provenance를 성공적으로 분리한다. 그러나 현재
scripted event log는 범용 acquisition ledger가 아니며 실제 occurrence time, participant
identity, consent 또는 withdrawal을 표현하지 않는다.

P1은 scripted development run이므로 이것이 blocker는 아니다. P1의 범위는 다음으로
제한해야 한다.

```text
frozen v0 replayability
instrument/schema/language defect inspection
raw response and missingness preservation
mapping-vocabulary limitation discovery
revision proposal issuance
```

P1이 판정하지 않는 것:

```text
participant/model latent mechanism
persona
functional placement winner
D2a recursion
human empirical support
revision effectiveness
```

## 7. Raw response, mapping과 observation을 분리

```text
RawResponseReceipt
!= DevelopmentMappingAttempt
!= DevelopmentMappingCandidate
!= O5/O10 observation
!= internal trace
```

`OUT_OF_MODEL`은 runner가 raw text에서 직접 발행할 값이 아니다. frozen mapping이 응답을
수용하지 못하고 instrument failure도 배제된 뒤의 evaluator/analyst 판정이어야 한다.

응답이 현재 vocabulary에 들어가지 않는 경우도 곧바로 문항 결함이 아니다.

```text
OUTSIDE_CURRENT_VOCABULARY
may mean:
- vocabulary가 좁음
- perspective가 모호함
- 복수 행위가 함께 있음
- mapping이 아직 underspecified
- response가 현재 scope 밖임
```

## 8. `NO_SELF_CERTIFICATION`

과거 runtime 결함들에는 내부에서 만든 파생물이 독립 source처럼 되돌아와 자신을
지지하는 공통 위험이 있다.

```text
prediction-shaped encounter
-> prediction accuracy support

reconstructed memory
-> source fact support

repeated explanation
-> independent evidence support
```

같은 자료를 재평가하거나 내부 모델을 다시 사용하는 것 자체는 금지할 수 없다.

```text
EvidenceBaseDelta = 0
AssessmentDelta != 0
```

은 가능하다. 금지해야 하는 것은 같은 source closure의 후손을 독립 source로 다시 세어
자기 자신을 인증하는 것이다.

> No claim gains additional independent-source support solely from descendants
> whose claim-relative source closure contains no new source receipt.

정상 통제 사례:

- 기존 receipt의 오류 교정이나 새 판정 규칙은 evidence base를 늘리지 않고 assessment를
  바꿀 수 있다.
- prediction이 질문을 유도하고 상대가 새로 답하면 새 occurrence가 생길 수 있다.
  다만 leading, selection과 source independence는 별도 판정이다.
- 내부 놀람 occurrence는 놀람 자체의 source일 수 있지만 외부 대상의 위험성에 대한 독립
  source는 아니다.

이 원칙은 연구 헌법 후보로 채택할 수 있지만 P0/P1 evaluator 구현이나 새 claim support로
즉시 승격해서는 안 된다.

## 9. View/access 중간층은 후속 과제

다음 구분은 이론적으로 중요하다.

```text
EvidenceReceiptRegistry
AccessEligibleEvidenceRefs
CurrentlyAccessedEvidenceRefs
AttendedEvidenceRefs
SubjectiveSupportAppraisal[claim]
UsedInAdjudicationRefs
ReportedSupportContent
```

그러나 P0/P1이 고정할 수 있는 것은 다음 부정적 경계뿐이다.

```text
응답에서 근거가 언급되지 않음
!=> 근거가 접근되지 않았음
!=> 근거가 존재하지 않음
```

실제 access, attention, subjective appraisal과 adjudication 분해는 별도 `ACCESS-001`에서
경쟁 구조와 함께 열어야 한다.

## 10. 더 강한 persona 경쟁 모델

미래 PERS preregistration에서는 단순 static trait나 global load만 비교해서는 안 된다.
최소 challenger는 다음과 같아야 한다.

```text
M4 shared runtime + transient state/gate
M5 same internal deformation + different observation mask
M6 unstructured stable individual difference
M7 structured selective-transition grammar
```

M7은 같은 자료를 더 잘 설명하는 것만으로 살아남지 않는다. domain/session 1에서 추정한
문법이 보지 않은 domain, session 또는 perturbation trajectory를 예측해야 한다.

Trait candidate는 먼저 post-run derived readout이어야 한다.

```text
observed repeated pattern
!= stored internal trait rule
```

행동에서 trait를 추론하고 그 trait로 동일 행동을 설명하는 순환을 피해야 한다.

## 11. 권장 순서

```text
P0-v0                 merged / frozen / unexecuted
P1 preregistration    separate docs freeze
P1-v0                 immutable scripted development pilot
P0-v1                 conditional proposal decision
P1-v1                 conditional re-pilot
ACQ0                   actual occurrence/provenance contract
PROMPT-REACT-001       elicitation-reactivity study
source-specific freezes
human / LLM / D2a execution
longitudinal PERS program
```

## 최종 판정

PR #15는 범용 인간 측정 infrastructure가 아니라 개발용 elicitation instrument를 손실
없이 시험할 수 있는 고정 지그다. 다음 단계는 그 지그를 확장하거나 persona 이론을 넣는
것이 아니라, exact v0를 한 번 실행하여 결함과 수정 제안만 남기는 P1이어야 한다.

```text
질문·응답·순서 provenance
-> P0/P1에서 다룸

surface != latent
role != persona
NO_SELF_CERTIFICATION
-> 연구 경계 후보

selective adaptation / persona grammar / generalization lattice
-> 후속 경쟁 가설
```

이 문서는 이 구분을 외부 평가로 보존하며 구현 완료나 인간 경험적 지지를 주장하지 않는다.
