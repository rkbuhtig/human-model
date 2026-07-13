# Adoption Record — Development Elicitation Instrument Contract

| 항목 | 값 |
|---|---|
| Date | 2026-07-13 |
| Source | `INTERP-DIALOGUE-001A` 3개 family/24개 cell, `INTERP-DIALOGUE-001B-TRACE-ORACLE-V1`, prompt-induced event와 response provenance에 대한 방법론 교정 |
| Decision | `ADOPTED WITH SOURCE-AND-AUTHORITY LIMITS` |
| Implementation | `INTERP-DIALOGUE-001P0-v0` contract/schema `FROZEN`; scripted replay materializer/scanner `IMPLEMENTED`; actual acquisition과 P1 pilot `UNEXECUTED` |
| Empirical status | `NO PARTICIPANT DATA; NO HUMAN, LLM, OR D2A TRACE; NO MECHANISM SUPPORT` |

이 기록은 내부 상태를 측정하는 도구나 실제 acquisition recorder를 채택하지 않는다. P0가
고정하는 것은 미래 source-specific protocol이 어떤 vignette와 future option을 보여 주고,
어떤 prompt를 전달하며, 어떤 response record와 원문 payload를 어떤 순서로 보존해야
하는지다. 현재 runner는 이 schedule을 scripted input으로만 재현한다.

```text
what the instrument schedules and scripted replay materializes
≠ evidence that anything was actually shown / asked / returned
≠ encounter or candidate-set measurement
≠ TargetForm or Ghost observation
≠ external fact certification
≠ general human-mechanism support
```

## Adopt

| 결정 | 채택 내용 | 현재 지위 |
|---|---|---|
| FJ-P0-01 | 이름을 development **elicitation** instrument로 제한한다. frozen response-to-trace mapping과 calibration이 없으므로 measurement instrument라고 부르지 않는다. | terminology `FROZEN` |
| FJ-P0-02 | 세 `001A` family와 `001B` trace oracle을 content SHA-256으로 결박한다. 어느 source가 바뀌면 같은 instrument version을 재사용할 수 없다. | source binding `FROZEN` |
| FJ-P0-03 | `001B`의 O0–O10 observation coordinate와 P0의 delivery/response schedule을 분리한다. future acquisition에서는 prompt delivery도 독립 event와 provenance를 가져야 하지만 현재 replay record는 실제 occurrence가 아니다. | event grammar `FROZEN` |
| FJ-P0-04 | current materializer는 `SCRIPTED_ADVERSARIAL_RESPONSE`만 받아 `RESPONDED`, `REFUSED`, `NO_RESPONSE`, `TECHNICAL_FAILURE` record와 exact scripted UTF-8 payload를 정규화 없이 보존한다. | scripted provenance `FROZEN` |
| FJ-P0-05 | R1/R2 record는 별도 mapping이 미래에 동결된 경우에만 O5/O10 surface의 입력 후보가 될 수 있다. materializer는 actual occurrence, observation status, internal trace 또는 `OUT_OF_MODEL`을 발행하지 않는다. | mapping boundary `FROZEN` |
| FJ-P0-06 | `ScriptedReplayMaterializer`, `MechanicalDefectScanner`, analyst adjudication을 분리한다. scanner는 candidate만 발행하고 `InstrumentDefectReceipt`는 분석자의 명시적 판정을 요구한다. | role boundary `FROZEN` |
| FJ-P0-07 | structured choice와 retrospective diagnostic은 R2 뒤에만 허용한다. D0/RD0는 당시 ordinal의 직접 관측이 아니라 사후 진단이다. | prompt-order boundary `FROZEN` |
| FJ-P0-08 | scenario의 candidate anchor와 내부 identifier를 presentation에 노출하지 않는다. base surface 번역은 author-rendered text이며 certified semantic equivalence가 아니다. | presentation boundary `FROZEN` |
| FJ-P0-09 | P1은 exact v0의 immutable scripted replay, evaluator-side walkthrough/inspection, defect receipt와 revision proposal만 발행할 수 있다. actual acquisition과 수정 instrument 실행은 금지되고, 수정안 채택 권한은 다음 P0 version에만 있다. | revision authority `FROZEN` |

## Elicitation event와 observation coordinate

P0는 `001B`의 내부 observation slot을 질문 개수로 채우지 않는다. future acquisition
schedule에 별도 namespace를 쓰고, current runner는 그 schedule의 scripted record만
materialize한다.

```text
E0  initial vignette delivery
E1  generic immediate-response prompt delivery
R1  immediate response event

E2  registered matched future-option delivery
E3  generic later-response prompt delivery
R2  later response event

D0 / RD0  optional retrospective diagnostic pair, after R2 only
```

```text
R1
→ future DevelopmentMappingCandidate for O5/immediate_surface 가능

R2
→ future DevelopmentMappingCandidate for O10/later_surface 가능

D0 / RD0
→ retrospective diagnostic only
↛ O1–O10 direct observation
```

질문이 중립적인 창이라는 가정은 두지 않는다. future acquisition에서 E1과 E3도 뒤의
응답에 영향을 줄 수 있는 delivery occurrence로 기록해야 한다. current replay의 E/R
record는 실제 delivery나 response가 있었다는 receipt가 아니다. O1–O4와 O7–O9는 별도
mapping이 없으면 `NOT_OBSERVED`로 남으며, 질문을 추가해 억지로 채우지 않는다.

## Response provenance의 제한된 권한

```text
scripted response record + ResponseProvenanceLink
⊢ replay 안에서 declared presentation·prompt와 response record가 연결됐음
⊢ scripted payload의 exact bytes, length와 digest가 보존됐음

scripted response record + ResponseProvenanceLink
⊬ 실제 participant 또는 model delivery/response occurrence
⊬ 실제 encounter 또는 candidate set
⊬ TargetForm, Ghost 또는 adjudicator의 residence
⊬ 외부 대상의 정체·의도·사실
⊬ 인간 일반 메커니즘
```

P0의 replay record는 first-person attestation이나 human scenario judgment receipt가 아니다.
vignette 속 사람에 대한 scenario judgment와 참가자 자신의 경험 보고는 서로 다른
protocol이므로, source-specific acquisition을 별도로 동결하지 않는 한 어느 쪽으로도
승격하지 않는다.

```text
NOT_OBSERVED
≠ NO_RESPONSE
≠ REFUSED
≠ TECHNICAL_FAILURE
```

## Raw response와 mapping-relative out-of-model

scripted raw payload 자체는 모델 밖 판정이 아니다. materializer는 payload를 현재
vocabulary에 맞추거나 가장 가까운 내부 위치로 cast하지 않는다.

```text
scripted raw payload
→ exact replay provenance

future frozen MappingAttempt
→ mapping candidate
→ analyst adjudication
→ OUT_OF_MODEL 가능
```

따라서:

```text
scripted raw payload ≠ OUT_OF_MODEL response

OUT_OF_MODEL
= frozen mapping이 해당 응답을 수용하지 못했다는 scope-relative adjudication
```

이 구분은 응답자를 오류 source로 취급하지 않고 현재 기능 분해나 mapping의 협소함을 열린
결과로 보존한다.

## Runner, scanner와 analyst authority

```text
ScriptedReplayMaterializer
→ immutable scripted replay / provenance artifact
↛ actual acquisition occurrence
↛ mapping, defect, observation status, placement result

MechanicalDefectScanner
→ MechanicalDefectCandidate
↛ InstrumentDefectReceipt
↛ pass/fail 또는 revision adoption

Analyst adjudication
→ explicit InstrumentDefectReceipt
↛ mechanism truth
↛ instrument revision adoption
```

digest mismatch, prompt-order violation, missingness collapse와 literal leak처럼 기계적으로
검출 가능한 항목도 scanner 단계에서는 candidate다. ambiguity, participant burden,
multi-factor wording, semantic drift와 perspective ambiguity는 analyst-only 판단으로 남긴다.
author walkthrough와 language/comprehension inspection은 이 analyst/evaluator lane의 source이며
runner의 response source나 actual occurrence가 아니다.

## P1과 다음 P0 version

P1은 v0를 덮어쓰지 않는다.

```text
P0-v0 frozen instrument
→ P1-v0 immutable scripted adversarial replay
→ evaluator-side walkthrough / language inspection
→ InstrumentDefectReceipt
→ InstrumentRevisionProposal(PROPOSED_NOT_ADOPTED / UNEXECUTED)

P1-v0
↛ actual human / LLM / author acquisition
↛ v1 adoption
↛ revised instrument execution
↛ DEFECT_FIXED 판정
```

후속 P0 version만 proposal을 `ACCEPTED / REJECTED / DEFERRED`로 판정하고 새 immutable
instrument를 동결할 수 있다. 수정본이 결함을 해결했는지는 별도 P1 replay를 다시 실행하기
전에는 알 수 없다. 실제 human, LLM 또는 다른 source acquisition은 source identity,
delivery, consent/privacy, response provenance, mapping과 missingness를 결과 전에 별도
동결해야 한다.

## Authority and support boundary

이번 freeze와 validator가 판정하는 것은 source digest, 24개 presentation의 구조,
delivery/response order, provenance envelope와 금지 cast다.

```text
contract/schema/validator conformance
≠ actual acquisition or development response result
≠ human trace mapping
≠ functional placement adjudication
≠ D2a k→k+1 recursion
≠ durable TargetForm, Episode or Narrative write
≠ HM-INV-013, HM-DYN-004 or HM-MEAS-005 support
```

따라서 claim registry의 adoption/implementation status, dependency와 historical/structural/
empirical support 배열을 변경하지 않는다. `HM-INV-013`과 `HM-DYN-004`는 계속
`UNIMPLEMENTED`이고, P0는 `HM-MEAS-005`의 human-comparable measurement receipt를
구현하지 않는다.

## Hold

| 항목 | 재개 조건 |
|---|---|
| P1-v0 development replay | exact P0-v0 digest에 결박된 scripted adversarial input; walkthrough/inspection은 evaluator-side source로 별도 보존 |
| P0-v1 adoption | P1-v0 defect receipt와 revision proposal에 대한 별도 decision receipt |
| actual human acquisition | source identity, delivery, consent/privacy, response provenance, mapping과 missingness의 pre-run freeze |
| LLM acquisition / representation mapping | model/version/prompt delivery, response provenance, paraphrase stability, cross-model replication과 projection mapping freeze |
| D2a recursion | future-effective revision candidate operator, k→k+1 fixture와 evaluator freeze |
| placement adjudication | source-specific mapping과 sealed result protocol |
| Dynamics/Narrative integration | `INTERP-DIALOGUE-001C` 이후 별도 adoption gate |

## 연결

- [`INTERP-DIALOGUE-001P0-v0` instrument](../scenarios/interp-dialogue-001/elicitation/README.md)
- [`INTERP-DIALOGUE-001A` scenario adoption](2026-07-13-functional-jurisdiction-scenarios.md)
- [`INTERP-DIALOGUE-001B` trace-oracle adoption](2026-07-13-functional-jurisdiction-trace-oracle.md)
- [Roadmap](../roadmap.md)
- [Claim registry](../claims/README.md)

이 기록은 presentation의 자연스러움, 인간 대표성, internal-state mapping의 타당성 또는
기능 배치의 참을 인증하지 않는다.
