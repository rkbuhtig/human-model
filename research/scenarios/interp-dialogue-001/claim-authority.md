# INTERP-DIALOGUE-001A Claim Authority

이 문서는 시나리오의 문장이 가질 수 있는 권한을 제한한다.

| Lane | 의미 | 허용되는 쓰임 | 금지되는 승격 |
|---|---|---|---|
| `public_record` | vignette에서 실제로 발화·관측·제시된 내용 | 모든 cell이 공유하거나 명시적 factor가 바꾸는 공개 자극 | 진실한 의도, 외부 대상의 속성, 미래 사건의 인증 |
| `author_origin_possibility` | 저자 경험·내성·사례 구성에서 출발한 1인칭 가능성 | 질문과 대조쌍 생성 | 인간 일반 법칙, 인과 residence, 경험적 빈도 |
| `phenomenological_expectation` | 사람에게 가능할 수 있다고 보는 비배타적 범위 | 인간 파일럿이 물을 반응 공간 | 정답 출력, 정답 숨은 상태, 메커니즘 인증 |
| `normative_invariant` | 연구 프로그램이 이미 채택한 타입·권한·시간 경계 | 월권과 소급 오염 검출 | 인간 현상 빈도, 특정 기능 배치의 경험적 증명 |
| `open_discriminator` | 현재 사례로 판별해야 하는 선택지 | 후속 기능 배치 비교의 질문 | fixture에서 정답을 암시하거나 expected trace로 기록 |
| `candidate_projection` | 같은 즉시 표면을 비교하기 위한 비규범적 probe anchor | 후속 판별성 문제 구성 | 자연스러운 정답, 바람직한 행동, 심리 진실 |

## Factor source lane

factor level의 `descriptor`는 하나의 source lane을 반드시 선언한다.

| Source lane | 기록하는 것 | 기록하지 않는 것 |
|---|---|---|
| `FIRST_PERSON_CONDITION_REPORT` | 현재 mood·evaluation threat·pre-event arousal에 대한 보고 | 실제 body state, ReceptionState residence, 보고의 정확성 |
| `VIGNETTE_HISTORY_RECORD` | vignette가 제시한 과거 이력 | 현재 대상의 속성, durable TargetForm, 현재 사건에 대한 Evidence |
| `EXPERIMENTER_CUE` | 어떤 과거 소재를 다시 제시했는지 | 실제 접근, 사용, 재해석, Episode integration |
| `PUBLIC_STIMULUS_VARIANT` | 현재 피드백 addendum이나 경로 관측의 명시적 차이 | 발화자 의도, 미식별 소스 정체, 주관적 encounter |

`level_specific_public_record`는 해당 report·history·cue·stimulus variant가 vignette에
제공됐다는 기록이다. 그 내용이 외부 세계에서 참임이나 내부 기능 상태가
실제로 형성됐음을 자동 인증하지 않는다.

각 level의 `operational_source_kind`는 저자 기원 가상 vignette 안에서 조작 출처를
구별하기 위한 운영상 식별자다. 이름에 source가 들어가더라도 empirical source,
reality authority, 사실 인증 또는 기능 residence 권한을 갖지 않는다.

## Registered candidate probe domain의 권한

`factor_contrast_contract.registered_candidate_probe_domains`는 후속 측정 설계가 먼저
살펴볼 후보 관측 영역이다. 가능한 효과나 메커니즘의 완전한 목록 또는 허용 목록이
아니다.

```text
unregistered or unexpected effect
≠ fixture violation
≠ mechanism falsification
≠ automatic retirement reason

unregistered or unexpected effect
→ OUT_OF_MODEL open result
  or CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE
```

`INTERP-DIALOGUE-001B`는 pilot이나 결과 판정 전에 이 out-of-model lane의 기록 및
판정 권한을 명시적으로 고정했다. 목록 밖 효과를 사후에 기존 domain으로 강제
cast해서는 안 된다.

## 저자 기원 사례의 경계

저자가 직접 관찰했거나 경험했다고 보고한 현상은 사례 생성에 강한 재료가 된다.
그러나 그 보고에 사용된 어휘가 이미 이론적일 수 있다.

```text
“나중에 과거 단서가 다르게 느껴졌다”
= author-origin first-person attestation candidate

“ReceptionState가 access를 바꿨다”
= mechanistic hypothesis
```

첫 문장은 시나리오의 출발점이 될 수 있지만 둘째 문장을 자동으로 지지하지
않는다.

## Candidate anchor의 권한

`same_immediate_projection_claim.candidate_projection` 속 문장·행동은 설계자가
“같은 표면이 가능하다고 가정할 때 후속 구분이 필요한가”를 묻기 위한 anchor다.

```text
design-only candidate anchor
≠ participant-facing prompt
≠ observed participant response
≠ allowed/preferred/correct output
```

후속 instrument에 그 anchor를 노출하려면 순서·선택지·anchoring 통제를 별도로
사전등록해야 한다.

## 이 사전등록이 지지하지 않는 claim

```text
시나리오가 schema를 통과함
≠ 사람이 실제로 그렇게 느낌
≠ 특정 내부 경로가 존재함
≠ Reception / TargetForm / Ghost residence가 확정됨
≠ 퀄리아를 측정함
```

후속 인간 자료가 추가되더라도 first-person attestation, 행동 선택, 외부 사실과
기능 메커니즘을 별도 record로 보존해야 한다.

## `001B` trace oracle의 추가 권한 경계

`001B`는 세 vocabulary를 분리한다.

```text
hypothesis relation
≠ future observation status
≠ adjudication result
```

`MUST_DIFFER_IF_PLACEMENT`는 placement 정의에 따른 계산 약속이지 인간이 반드시 다르게
느껴야 한다는 예측이 아니다. `EQUAL`은 미래 source-specific mapping의 관측 상태이지 두
기능이 본질적으로 같다는 판정이 아니다. `OPERATIONALLY_ALIASED`는 같은
probe·projection·horizon·measurement mapping에서 전체 hypothesis signature가 같은 경우에만
허용한다.

자연 contrast의 earliest divergence도 direct causal edge를 인증하지 않는다. direct-edge
주장은 아직 실행되지 않은 D2a node-clamp challenge를 요구한다. 인간 판단이나 LLM
activation은 source-specific mapping이 별도로 동결되기 전에는 내부 trace field 값이나
causal residence 증거가 아니다.
