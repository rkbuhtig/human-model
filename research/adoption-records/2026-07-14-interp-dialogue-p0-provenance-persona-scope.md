# Adoption Record — INTERP-DIALOGUE P0 Provenance and Persona Scope

| 항목 | 값 |
|---|---|
| Date | 2026-07-14 |
| Source | [External non-peer assessment](../../assessments/2026-07-14-interp-dialogue-p0-provenance-persona-scope-assessment.md) |
| Evaluated artifact | PR #15 / merge commit `05d946590a605a76e1bbe89fceab8b556c2d37cf` |
| Decision | `ADOPTED WITH REVISIONS` |
| Implementation | P0-v0 `FROZEN / UNEXECUTED`; this record changes no runtime or frozen artifact |
| Human-empirical status | `OPEN` |

`ADOPTED`는 연구 경계의 채택이지 P0 실행, latent-state 측정, persona 이론의 채택,
인간 경험적 참 또는 새 claim support를 뜻하지 않는다.

## Adopt

| ID | 결정 | 현재 지위 |
|---|---|---|
| A-01 | `Surface observation != latent transition` | 연구 경계 `ADOPTED`; latent mapping `OPEN` |
| A-02 | Scenario judgment는 vignette actor나 participant의 persona를 인증하지 않음 | `ADOPTED` |
| A-03 | Response submission/receipt는 내부 response-production mechanism 관측이 아님 | `ADOPTED` |
| A-04 | `RoleContract != Persona` | `ADOPTED`; role-conditioned persona study `HOLD` |
| A-05 | `Scripted replay != actual acquisition` | P0-v0 contract와 일치 |
| A-06 | `RawResponseReceipt != DevelopmentMappingAttempt != oracle observation != internal trace` | P0-v0 contract와 일치 |
| A-07 | Prior-response-exposed later surface는 natural/unelicited trajectory가 아님 | `ADOPTED`; prompt-reactivity identification `OPEN` |
| A-08 | 동일 source closure의 파생물은 새 source receipt 없이 독립 source support를 추가할 수 없음 | 연구 원칙 후보 `ADOPTED`; claim/defect implementation `HOLD` |
| A-09 | Trait/persona는 held-out longitudinal prediction 전에는 derived hypothesis로 유지 | `ADOPTED` |
| A-10 | P1은 exact frozen-v0 scripted development pilot과 proposal-only output으로 제한 | P1 preregistration에 적용 |

## Adopted boundary statements

### Surface is not latent state

```text
FirstDetectedSurfaceDeviation
!= FirstLatentTransition
```

role, transient gate, mask, expression permission, compensation과 observation sensitivity가
표면과 내부 변화 사이에 존재할 수 있다. P0/P1 응답만으로 internal failure order,
recovery order 또는 causal residence를 발행하지 않는다.

### Role is not persona

```text
RoleContract
!= PersonaSpecificGrammarCandidate
```

역할 자체는 conditioning variable다. 미래 연구에서 persona와 관련될 수 있는 것은
역할을 받아들이고, 충돌시키고, 벗어나는 방식의 안정 후보이며 현재는 구현하지 않는다.

### Submission receipt is not response-generation mechanism

실제 acquisition에서 직접 기록 가능한 event 이름은 관측 권한에 맞춰 제한한다.

```text
ResponseSubmissionOccurrence
ResponseReceivedOccurrence
RawResponseReceipt
```

`ResponseProductionOccurrence`는 내부 생성 과정을 직접 관측한 경우가 아니면 사용하지
않는다. UI interaction start 역시 thinking-start timestamp가 아니다.

### P0/P1 schedule is an elicited path

```text
prior prompt + response exposure
-> later surface에 영향을 줄 가능성

but
-> effect size, mediation 또는 latent mechanism은 미측정
```

O10을 natural/unprompted trajectory로 부르지 않는다. 실제 prompt reactivity는 별도
schedule comparison을 요구한다.

### No self-certification

> No claim gains additional independent-source support solely from descendants
> whose claim-relative source closure contains no new source receipt.

이 원칙은 동일 자료의 재평가를 금지하지 않는다.

```text
EvidenceBaseDelta = 0
AssessmentDelta != 0
```

은 합법일 수 있다. 금지되는 것은 prediction, reconstructed memory, subjective encounter,
repeated explanation 등의 내부 파생물을 새 독립 source처럼 계산해 원래 주장을 자기
인증하는 것이다.

현재 defect schema는 repository-local source excerpt와 upstream git blob provenance를
요구한다. 외부 `afterneu` archive를 정식 defect case로 등록하려면 external-source
provenance contract 또는 source corpus freeze가 먼저 필요하다. 따라서 이 record는 새
`HM-DEFECT-*` case나 claim registry support를 생성하지 않는다.

## Revise

### R-01 — 이론 명칭을 단계적으로 승격

`Selective Adaptation Grammar`는 적응 기능과 보호 목적을 미리 가정한다. 다음 사다리를
사용한다.

```text
SelectiveTransitionSignature
-> held-out perturbation prediction
SelectiveTransitionGrammarCandidate
-> functional preservation/outcome criterion
SelectiveAdaptationGrammarCandidate
-> role/state/session-stable replication
PersonaSpecificGrammarCandidate
```

초기 자료에서 안전한 용어는 `ObservedPreservedSurfaceSet` 또는
`PerturbationRelativeInvariantSurfaceCandidate`다. 겉으로 유지된 표면은 실제 내부
불변, mask, 비사용, 대체 출력 또는 검출 문턱 아래 변화와 모두 양립한다.

### R-02 — 노출 조건을 mediation보다 먼저 기록

```text
NO_INTERMEDIATE_ELICITATION
PRIOR_FREE_RESPONSE_EXPOSURE
PRIOR_STRUCTURED_RESPONSE_EXPOSURE
```

를 사용한다. `response-mediated trajectory`는 mediation design과 분석을 통과한 뒤에만
사용한다.

### R-03 — Generalization은 선형 사다리가 아님

미래 generalization study는 sparse multidimensional scope를 사용한다.

```text
Target x Relation x Context x Domain x Time x FunctionalSurface
```

모든 Cartesian cell을 구현하라는 뜻은 아니다. 관측자가 반복 패턴을 trait로 요약한
것과 runtime 내부에 일반 규칙이 저장된 것을 분리한다.

## Hold

| 항목 | 재개 조건 |
|---|---|
| `FirstLatentTransition` / failure order | source-specific latent measurement model 또는 identified runtime trace |
| recovery order / recovery time / hysteresis | perturbation ramp-down, repeated probe, censoring contract와 longitudinal sessions |
| durable residual / TargetForm retention | D2b retention/decay와 temporal flow |
| persona-specific grammar | role/state/history/elicitation/mask 통제와 held-out domain/session prediction |
| M4–M7 persona challengers | PERS preregistration과 longitudinal dataset |
| generalization lattice | source-specific repeated observations across scope axes |
| ACCESS-001 runtime | evidence existence, eligibility, access, attention, appraisal, use, report competing decomposition |
| PROMPT-REACT-001 result | stable instrument version과 no/free/structured schedule freeze |
| `NO_SELF_CERTIFICATION` defect case | external archive source freeze 또는 defect-source schema extension |
| new claim registry entry/support | formal scope, counterexample test와 implementation path |

## P1 authority

P1은 다음만 수행할 수 있다.

```text
frozen instrument-v0 exact scripted replay
coverage-bound adversarial corpus
mechanical candidate generation
author/language inspection
explicit analyst adjudication
revision proposal issuance
```

P1은 다음을 수행할 수 없다.

```text
actual human/LLM acquisition
instrument-v0 mutation
v1 adoption or execution
response-to-oracle mapping freeze
OUT_OF_MODEL classification by runner
persona / trait / latent mechanism claim
D2a recursion
claim support/status change
DEFECT_FIXED assertion
```

세부 실행 계약은
[P1 development-pilot preregistration](../scenarios/interp-dialogue-001/elicitation/p1-development-pilot-preregistration.md)에 둔다.

## Roadmap connection

```text
P0-v0                    MERGED / FROZEN / UNEXECUTED
P1 preregistration       DOCUMENTED / UNEXECUTED
P1 scripted pilot        PLANNED
P0-v1 decision           CONDITIONAL
ACQ0                      OPEN
PROMPT-REACT-001         OPEN
source-specific mappings OPEN
PERS longitudinal study  FUTURE HYPOTHESIS PROGRAM
```

이 adoption record는 P1 실행 결과, 수정안 채택, ACQ0, prompt-reactivity result 또는
persona program의 성공을 대신하지 않는다.
