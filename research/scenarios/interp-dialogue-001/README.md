# INTERP-DIALOGUE-001A — Functional Jurisdiction Scenario Contract

| 항목 | 값 |
|---|---|
| Status | `INTERNAL_PREREGISTRATION_UNEXECUTED_NO_HUMAN_DATA` |
| Unit | 3개 author-origin operational factor의 2×2×2 vignette family |
| Families | `REL-BOUNDARY-001`, `WORK-FEEDBACK-001`, `RISK-FOOTSTEPS-001` |
| Cells | family당 8개, 총 24개 |
| Human data | 없음 |
| Runtime execution | 없음 |
| Correct mechanism / output | 지정하지 않음 |

## 목적

이 사전등록은 더 복잡한 모델이 더 많은 경우를 표현하는지 채점하지 않는다.
대신 현실 영역을 본뜬 저자 기원 vignette의 한 operational factor만 바꾸었을 때
어떤 기능적 위치에서 차이가 날 수 있는지를 물을 수 있도록 factor-label
Hamming-one contrast와 후속 probe를
먼저 고정한다.

```text
현상적 가능성이 있다
≠ 특정 메커니즘이 확인됐다
≠ 지금의 타입과 residence가 올바르다
```

각 family는 내부 모델 이름이 아니라 vignette에서 직접 제시할 수 있는
author-origin operational descriptor 세 개를 조작한다. 각 level은 또한
`FIRST_PERSON_CONDITION_REPORT`, `VIGNETTE_HISTORY_RECORD`, `EXPERIMENTER_CUE`,
`PUBLIC_STIMULUS_VARIANT` 중 하나의
`source_lane`을 선언한다. 이는 관찰 권한과 제공 방식을 나누는 것이지 기능
residence를 확정하는 태그가 아니다.

각 level의 `operational_source_kind`는 저자 기원 가상 vignette 안에서 그 조작을
구별하기 위한 운영상 출처 이름이다. 경험 자료의 출처, 현실성, 사실성 또는
메커니즘 권위를 부여하지 않는다.

| Family | Factor 1 | Factor 2 | Factor 3 |
|---|---|---|---|
| `REL` | 보고된 현재 mood | 대상과의 과거 이력 | 외부에서 cue한 과거 소재 |
| `WORK` | 보고된 평가 위협감 | 평가자의 criterion 일관성 이력 | 공개 피드백 addendum |
| `RISK` | 보고된 사전 arousal | 최근 위험 이력 | 경로 일치 관측 |

`ReceptionState`, `TargetForm`, access, encounter formation, Ghost 같은 용어는 가능한 기능
배치의 이름이다. 그 이름을 vignette의 사실이나 정답으로 넣지 않는다.
특히 외부 cue는 소재가 제시됐음만 기록하며, 그 소재가 실제로 접근·채택·사용됐는지는
열린 판별 문제로 남긴다.

각 factor에 하나의 `factor_contrast_contract` 또한 붙인다. 이 계약은 바꾸는 record,
고정할 나머지 factor, 후속 측정을 설계할 때 먼저 검토할
`registered_candidate_probe_domains`와 반드시 같아야 할 관할을 명시한다.
이 domain 목록은 가능한 메커니즘이나 효과의 허용 목록도, 완전한 열거도 아니다.
그러므로 목록 밖 효과는 fixture 위반이나 해당 기능의 retirement 사유가 아니라,
현재 기능 분해가 아직 포착하지 못한 `OUT_OF_MODEL` 결과 또는
`CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE`로 보존한다. 그러나 어떤 trace가
나와야 하는지는
`OPEN_NO_EXPECTED_TRACE`로 남긴다.

`INTERP-DIALOGUE-001B`는 pilot이나 결과 판정 전에 이 out-of-model lane을
명시적인 trace-oracle 계약으로 고정했다.

RISK family의 미식별 source는 stable resolved-entity TargetForm을 인스턴스화하지 않는다.
다만 provisional/category-level subjective target representation이 생길 수 있는지는
`OPEN_DISCRIMINATOR`로 남긴다.

## 출력을 정답으로 두지 않는 이유

같은 즉시 반응은 서로 다른 미해결 경로에서 나올 수 있고, 같은 체감에서도 다른
행동이 가능하다. 그러므로 각 family는 하나의 `same_immediate_projection_claim`을
`OPEN`으로 두고 다음 사건을 후속 probe로 붙인다.

```text
same immediate projection
+ claimed distinct internal path
→ at least one preregistered future probe must distinguish the later trace
```

후속 probe도 답을 미리 기록하지 않는다. 구분을 주장하려면 무엇이 달라져야
하는지만 고정한다.

`candidate_projection` 속 대사·행동은 설계자용 anchor이며 participant-facing
prompt가 아니다. 후속 인간 protocol이 이 anchor를 노출하거나 선택지로 쓰려면
anchoring과 순서 효과를 별도로 통제해야 한다.

## 용어 예약

`Episode`와 `Narrative`는 RFC 0004의 큰 시간·승격 단위로 계속 예약한다.
시나리오의 작은 과거 힌트, 회상, 임시 조립에 이 이름을 붙이지 않는다.

```text
prior material in a vignette
≠ Episode
≠ Narrative
≠ Evidence certification
```

## 범위 제외

- 인간 참가자 모집·질문·결과 기록
- LLM activation, probe readout, verbal report
- 시나리오 runner와 evaluator
- HumanState, reducer, routing, Evidence, action 변경
- durable `TargetForm`, Episode integration, Narrative writer
- 정답 대사·정답 메커니즘·성능 총점

JSON Schema와 현재 구현된 구조 validator는 envelope, authority lane, 8-cell cube의
완전성과 factor-label 수준의 Hamming-one 쌍을 검사한다. 이 검사는 자연어
descriptor가 실제로 단일 인과 조작인지나 현실의 기능 residence가 맞는지를
인증하지 않는다.

## `INTERP-DIALOGUE-001B` follow-up

[`trace-oracle.md`](trace-oracle.md)와
[`trace-oracle-v1.json`](trace-oracle-v1.json)은 `001A`의 source contract를 digest로
묶고 다음을 `FROZEN / UNEXECUTED` 상태로 고정한다.

- 11개 ordinal observation point와 prefix/initial/one-future horizon
- 23개 authority-scoped trace field
- 9개 factor별 38개 competing placement hypothesis
- 세 family의 same-future-option oracle
- REL initial reported mood × later reported mood 2×2 trajectory
- Ghost/adjudicator/action gate를 위한 3개 D2a-only challenge
- strict operational-alias, identifiability-limit와 out-of-model 규칙

이 oracle은 사람의 숨은 상태나 올바른 기능 residence를 기록하지 않는다. 각 placement를
계산적으로 구현했다고 주장할 때의 conditional conformance contract만 정의한다. 아직
human/LLM/D2a observation, runner, evaluator, placement winner 또는 claim support는 없다.

## `INTERP-DIALOGUE-001P0-v0` follow-up

[`elicitation/README.md`](elicitation/README.md)와
[`elicitation/instrument-v0.json`](elicitation/instrument-v0.json)은 세 family의 24개 cell과
`001B` oracle을 content digest로 결박한 development elicitation instrument를 동결한다.

```text
O0–O10 oracle coordinate
≠ E0–E3 delivery occurrence
≠ R1/R2 response event
```

P0는 vignette, generic immediate/later prompt, matched future option과 optional post-trace
diagnostic의 순서를 고정한다. 현재 runner는 `SCRIPTED_ADVERSARIAL_RESPONSE` input만 받아
그 schedule의 replay record와 exact scripted payload provenance를 materialize한다. 이
record는 실제 prompt delivery나 participant/model response occurrence를 인증하지 않는다.
R1/R2를 O5/O10 surface에 연결하려면 별도 future mapping freeze가 필요하고, materializer는
mapping, observation status, `OUT_OF_MODEL`, defect 또는 placement result를 발행하지 않는다.
author walkthrough와 language/comprehension inspection은 evaluator-side defect source이며
replay response source가 아니다.

P0의 상태는 `FROZEN / UNEXECUTED — DEVELOPMENT ELICITATION ONLY`다. P1은 exact v0에
결박된 immutable scripted replay를 실행해 analyst defect receipt와 revision proposal을
발행했다. proposal은 P1 안에서는 `PROPOSED_NOT_ADOPTED / UNEXECUTED`이며, P1은 revised
instrument를 채택하거나 실행하지 않았다. 별도 P0-v1은 exact candidate/decision receipt와
participant surface, rendered catalog, mapping lineage를 새 instrument로 동결했지만 실행하지
않았다. 실제 human, LLM 또는 다른 source acquisition은 각 source의 delivery, consent,
identity, mapping과 missingness를 별도 pre-run freeze한 뒤에만 가능하다. 이 follow-up도
human/LLM/D2a data, internal mechanism observation, claim support, durable TargetForm,
Episode 또는 Narrative writer를 만들지 않는다.

## `INTERP-001D2a0` mainline transition

[`d2a0/README.md`](d2a0/README.md)는 P0-v1을
`HOLD / AVAILABLE_AS_DEVELOPMENT_INFRASTRUCTURE`, P1-v1을 `NON-MAINLINE HOLD`로
두고 최소 재귀 해석 spine을 먼저 동결한다. 공통 spine은 future revision을 표현할 수
있지만 발생을 전제하지 않으며, temporal `D2A-T*`, surface `D2A-P*`, declared-profile
`D2A-H*` 축을 분리한다. six synthetic fixture, same-access prohibition, Evidence/role
clamp, lifecycle separation과 evaluator-only signature가 등록돼 있다.

D2a0는 `FROZEN / UNEXECUTED`다. runner, evaluator, synthetic result, canonical
`HumanState` writer, participant/model observation 또는 claim support는 없다. 후속
[`EXEC0`](d2a0/exec0/README.md)는 operator/unit/evaluator-selector를, 이어지는
[`MAT0`](d2a0/mat0/README.md)는 normalization, record/lifecycle/rejection과 byte publication ABI를
각각 `FROZEN / UNEXECUTED`로 닫는다. 그 뒤 D2a1 실행과 `OBS-MAP-000`이 이어진다.
