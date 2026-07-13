# INTERP-DIALOGUE-001B — Hypothesis-Conditional Trace Oracle

| 항목 | 값 |
|---|---|
| Status | `INTERNAL_PREREGISTRATION_UNEXECUTED_NO_HUMAN_LLM_OR_D2A_TRACE_DATA` |
| Bound input | `INTERP-DIALOGUE-001A` family 3개를 content SHA-256으로 결박 |
| Factor oracles | 9개 |
| Conditional hypotheses | 38개 |
| Trace fields | 23개 |
| Observation points / horizons | 11개 / 3개 |
| Matched-future oracles | 3개 |
| Human·LLM·D2a result | 없음 |
| Correct output / winning placement | 없음 |

## 목적

[`trace-oracle-v1.json`](trace-oracle-v1.json)은 현실의 인간 반응을 정답으로 적는
oracle이 아니다. `001A`의 열린 기능 배치 중 하나를 채택했다고 가정할 때 그 배치가
계산적으로 어떤 equality/difference signature를 약속하는지를 결과 전에 고정한다.

```text
MUST_DIFFER_IF_PLACEMENT
= 해당 placement 정의의 조건부 약속
≠ 실제 인간이 반드시 다르게 반응한다는 예측
```

자연 vignette contrast에서 나타난 최초 차이는 association/location signature일 뿐이다.
상류 차이의 매개 효과일 수 있으므로 직접 인과 간선을 인증하지 않는다. `DIRECT_EDGE`
주장은 별도의 미실행 D2a node-clamp challenge를 참조해야 하며 이 버전에는 그러한 결과가
없다.

## 001A snapshot 결박

세 family 파일의 정확한 byte digest를 `bound_family_files`에 기록한다. 각 factor oracle은
원래 `factor_contrast_contract`의 다음 필드를 그대로 복사한다.

```text
source_lane
held_constant_factor_ids
public_record_effect
registered_candidate_probe_domains
must_remain_equal
open_discriminator_refs
status
```

따라서 `001A`를 바꾸고 이전 oracle을 그대로 재사용할 수 없다. digest나 snapshot이
달라지면 새 oracle version이 필요하다.

## 시간과 관측 위치

세 horizon은 duration이나 객관 시간의 양이 아니라 access-relative 연구 범위다.

```text
H_PREFIX_BEFORE_K
  O0  완성된 vignette input 수락 및 prior prefix snapshot

H_INITIAL_ACCESS_K
  O1  initial admission/access window close
  O2  initial encounter window close
  O3  initial candidate/source-use/affordance window close
  O4  initial adjudication window close
  O5  실제로 elicitation한 경우에만 immediate surface 기록

H_REGISTERED_FUTURE_ACCESS_K_PLUS_1
  O6  동일 future option을 양 prior path에 적용하고 prefix snapshot
  O7  later admission/access opportunity close
  O8  later encounter window close
  O9  later candidate/adjudication/non-durable reorganization close
  O10 실제로 elicitation한 경우에만 later surface 기록
```

window가 닫혔다는 것은 해당 내부 객체가 실제로 존재하거나 사람에게서 관측됐다는 뜻이
아니다. access가 없거나 측정 mapping이 없으면 `NOT_OBSERVED`로 남긴다. `0`이나 equality로
대체하지 않는다.

같은 access ordinal에서 새 readout을 소급 적용하지 않는다. `prior_occurrence_prefix`는
서로 다른 factor arm끼리 같다고 가정하지 않는다. 특히 history arm은 과거 입력 자체가
다르다. prefix guard는 같은 arm의 truncated base run과 future-extension run에서 이미
발행된 동일 O0 prefix artifact와 O0–O5 initial trace prefix 전체가 보존되는지를 비교한다.
missing/`NOT_OBSERVED` status도 frozen digest의 일부이며 future extension은 O5 뒤에만
append할 수 있다. O0 prefix와 current occurrence가 추가된 O6 pre-future prefix 자체를
같다고 비교하지 않는다. 이 replay guard는 D2a/runtime용이고 사람에게 동일 경험을 다시
겪으라고 요구하는 관측 계약이 아니다. 이 계약은
`H_REGISTERED_FUTURE_ACCESS_K_PLUS_1` 뒤의 장기 retention을 관측하지 않으므로 durable
target-scoped state와 slow cache를 판별할 권한도 없다.

## 세 개의 서로 다른 어휘

### 1. 가설 정의 relation

```text
MUST_REMAIN_EQUAL
MUST_DIFFER_IF_PLACEMENT
MAY_DIFFER_DOWNSTREAM
MUST_DIFFER_BY_DESIGN
MAY_DIFFER_WITH_DECLARED_PUBLIC_INPUT
MUST_REMAIN_ABSENT
NOT_EVALUABLE_WITHOUT_FROZEN_REASSESSMENT_POLICY
RELATION_NOT_APPLICABLE
```

`MAY_DIFFER_DOWNSTREAM`은 차이가 없어도 placement 위반이 아니며, 차이가 있어도 직접
residence를 뜻하지 않는다. 앞의 세 항목과 `RELATION_NOT_APPLICABLE`은 competing placement
projection에 쓰고, 나머지는 공개 입력·Evidence·금지 writer의 unconditional guard를
기계적으로 닫는 데 쓴다.

### 2. source-specific observation

```text
EQUAL
DIFFERENT
NOT_OBSERVED
OBSERVATION_NOT_APPLICABLE
```

인간 attestation, LLM latent, D2a trace는 서로 다른 source다. 각 source가 어떤
`trace_field_id`를 어떻게 측정하는지는 해당 실행 전에 별도 mapping으로 동결해야 한다.
사람의 “거절처럼 느껴졌다”는 보고를 `subjective_encounter_form` 내부 residence로 직접
cast하지 않는다.

### 3. 판정

```text
SIGNATURE_CONFORMS
SIGNATURE_DOES_NOT_CONFORM_UNDER_SCOPE
NOT_EVALUABLE
EMPIRICALLY_UNRESOLVED_UNDER_SCOPE
NOT_IDENTIFIABLE_UNDER_HORIZON
OPERATIONALLY_ALIASED
OUT_OF_MODEL
CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE
```

정의·관측·판정을 한 enum에 섞지 않는다. 특히 관측 equality는 operational alias가 아니다.

## Factor placement 계약

각 factor oracle은 하나의 `projection_set`을 가지며 모든 hypothesis가 그 set 전체에 대해
relation을 명시한다. 생략된 field를 암묵적으로 equal 또는 irrelevant로 취급하지 않는다.

| 001A factor | 주요 경쟁 위치 |
|---|---|
| REL reported mood | registered-null / access-first / encounter-first / third projection (`candidate_set`)-first / multiple registered locations |
| REL target history | active-material readout / target-scoped readout / slow cache |
| REL external cue | delivery-only / admission-access / encounter / candidate source-use |
| WORK reported threat | registered-null / access-first / encounter-first / third projection (`candidate_set`)-first / multiple registered locations |
| WORK evaluator history | active-material readout / target-scoped readout / slow cache |
| WORK public addendum | public-record-only / information uptake / encounter / revision affordance |
| RISK reported arousal | registered-null / access-first / encounter-first / third projection (`action_affordance`)-first / multiple registered locations |
| RISK recent history | no current trace / prior-material access / provisional category representation |
| RISK route match | public-observation-only / encounter / provisional representation / action affordance |

`C0_REGISTERED_TRACE_NULL`은 인간에게 아무 현상도 없다는 보편 null이 아니다. 등록된
projection과 horizon에서 해당 factor가 internal difference를 만들지 않는다는 조건부
정의뿐이다.

RISK route match와 WORK addendum은 공개 입력 자체가 달라지는 contrast다. 전체 public
record나 Evidence lane을 같게 강제하지 않는다. 특히 route-match 관측은 별도로 동결된
EvidenceAssessment를 바꿀 수 있지만, 그것만으로 source identity·hostile intention·resolved
entity status를 인증할 수는 없다.

## Source-sensitive guard policy

23개 field는 `external_target_evidence_link_set`과
`evidence_assessment_by_claim_scope`를 분리한다. 모든 factor oracle은 내부 placement
signature와 별도로 8-coordinate guard policy 하나를 참조한다.

```text
FIRST_PERSON_CONDITION_REPORT
→ external EvidenceLink와 claim-scoped assessment 동일

same-target history / current public stimulus
→ declared public input 때문에 EvidenceLink·assessment가 달라질 수 있음
→ current identity·intention 인증은 계속 금지

EXPERIMENTER_CUE
→ underlying link set 동일; equality는 membership을 주장하지 않음
→ 별도 reassessment policy 전에는 assessment relation을 판정하지 않음

separate prior risk incident
→ 현재 미식별 발소리 source의 link set·assessment는 동일
→ 일반 환경 위험 평가는 이 current-source guard의 범위 밖
```

`world_unknowns`는 각 001A base stimulus가 보호한 unknown set에만 묶이며 factor-level
사실을 포함하지 않는다. identity/intention certification, durable TargetForm write와
Narrative write는 양 arm에서 모두 absent여야 한다. cue link equality도 두 material이
EvidenceLink membership을 가진다고 인증하지 않는다.

## 같은 즉시 표면과 matched-future 규칙

`001A`의 immediate utterance/action illustration은 설계용 anchor다.

```text
candidate anchor
≠ participant-facing prompt
≠ observed immediate surface
≠ correct or preferred output
```

각 family의 full future-probe snapshot과 compared prior cell을 다시 결박한다. prior path를
구분하려면 반드시 동일한 `future option`을 두 path에 적용한 뒤 later trace를 비교한다.
서로 다른 option을 각각 주어 생긴 차이는 path 차이가 아니라 새 사건 차이다.

이 비교는 O5 immediate surface가 frozen mapping에서 실제로 양 arm `EQUAL`이거나, D2a
protocol이 no-feedback equal-surface clamp를 결과 전에 동결한 경우에만 evaluable하다.
`001A` candidate anchor만 같다는 이유로는 실행할 수 없다. 각 future option은 left/right
prior cell에 동일한 option index를 주는 arm pair로 명시한다. 같은 option 아래서 주관 trace는
갈릴 수 있지만 future public record, external EvidenceLink와 claim-scoped assessment는
같아야 하며 identity/intention 인증과 durable/Narrative writer는 계속 absent다.

## REL delayed-reorganization 2×2

REL은 다음 네 trajectory cell을 등록한다.

```text
initial reported mood: ordinary / low
×
later reported mood: ordinary / low
```

target history, cue identity와 외부 target record는 고정한다. 두 edge class를 따로 본다.

```text
initial-mood edge at matched later mood
later-mood edge at matched initial mood
```

후보 pattern은 `D0`, `DC`, `DI`, `DX`이며 각각 no registered difference, later-current-only,
initial-residue-only, interaction을 뜻한다. 이는 결과가 아니며 회복량·점화력 같은 scalar도
만들지 않는다. `later_reported_ordinary_mood`와 `later_reported_low_mood`는 bound future
probe의 option index 0과 1에 각각 machine-readable하게 결박되어 runner가 두 option을
바꾸어 연결할 수 없다.

## D2a-only challenges

`001A`의 자연 factor는 Ghost, adjudicator, action gate를 직접 조작하지 않는다. 따라서
이 셋의 선택적 기능 분리는 자연 vignette의 인간 반응으로 인증할 수 없다.

```text
GHOST
  access + encounter + adjudicator policy clamp
  exploration program만 변경
  → candidate-set conditional signature

ADJUDICATOR
  source view + encounter + candidate originals clamp
  scoped policy만 변경
  → adjudication conditional signature

ACTION_GATE
  encounter + candidate + adjudication + affordance clamp
  feasibility/opportunity만 변경
  → ActionOccurrence conditional signature
```

세 challenge의 status는 모두 `NO_001A_NATURAL_INTERVENTION`이며 아직 실행되지 않았다.

## Durable readout과 slow cache

`TS_TARGET_SCOPED_READOUT`과 `TC_SLOW_CACHE_READOUT`은 현재 horizon에서 같은 signature를
가질 수 있다.

```text
NOT_IDENTIFIABLE_UNDER_HORIZON
≠ durable state confirmed
≠ globally identical
≠ placement winner
```

장기 retention·decay·revalidation horizon 없이 둘 중 하나를 선택하거나 factor를 폐기하지
않는다.

## Scoped operational alias

`OPERATIONALLY_ALIASED`는 다음 scope key가 모두 고정되고, 모든 evaluable contrast와
matched-future branch에서 두 placement의 **조건부 정의 signature 자체가 동일할 때만** 쓴다.

```text
ProbeSet
ProjectionSet
Horizon
source kind
measurement mapping version
```

실제 자료에서 차이를 찾지 못한 경우는 `EMPIRICALLY_UNRESOLVED_UNDER_SCOPE`다. 검출력 부족,
미관측과 equality를 alias로 승격하지 않는다.

단, durable target-scoped-state candidate와 slow-cache candidate의 horizon limitation은
일반 alias rule보다 우선한다. 현재 one-future horizon에서 두 signature가 같아도
`OPERATIONALLY_ALIASED`나 placement winner로 판정하지 않는다.

## Out-of-model 보존

등록되지 않은 효과는 가장 가까운 기존 field에 강제로 넣지 않는다.

```text
raw observation ID
source kind / provenance
observation point / horizon
measurement-mapping status
immutable payload 또는 digest
→ OUT_OF_MODEL
```

결과를 본 같은 run에서 schema를 넓혀 재채점하지 않는다. 새 domain은 다음 protocol
version에서만 추가한다. 반복성, 모든 placement의 표현 실패, forbidden cast 필요성과
instrument failure 배제를 모두 확인한 뒤에만
`CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE` 후보로 올릴 수 있다.

normative invariant 위반은 out-of-model 효과가 아니라 별도 boundary/protocol challenge다.

## 이 계약이 구현하지 않는 것

- 인간 participant instrument, attestation 또는 결과
- LLM activation, probe, verbal report 또는 cross-model 결과
- D2a runner, node clamp 또는 synthetic trace
- correct output, placement winner, 총점 또는 factor retirement
- 실제 퀄리아·기분·위협·점화 측정
- durable `TargetForm` writer
- Episode integration 또는 Narrative writer
- Dynamics runtime feedback

이 계약의 성공은 001A 질문에 답한 것이 아니라, **어떤 답을 무엇과 비교해야 하며 현재
probe가 무엇을 답할 수 없는지까지 결과 전에 고정했다는 것**이다.
