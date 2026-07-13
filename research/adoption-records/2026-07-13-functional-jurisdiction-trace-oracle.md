# Adoption Record — Conditional Functional-Placement Trace Oracle

| 항목 | 값 |
|---|---|
| Date | 2026-07-13 |
| Source | `INTERP-DIALOGUE-001A` functional-jurisdiction scenarios와 후속 식별 가능성 감사 |
| Decision | `ADOPTED WITH IDENTIFIABILITY LIMITS` |
| Implementation | `INTERP-DIALOGUE-001B` trace-definition contract `FROZEN / UNEXECUTED` |
| Empirical status | `NO HUMAN, LLM, OR D2A TRACE DATA` |

이 기록은 사람의 숨은 상태를 맞히는 정답 oracle을 채택하지 않는다. 각 경쟁 기능 배치를
계산적으로 구현했다고 주장할 때 어떤 trace 관계를 약속해야 하는지, 현재 probe와 horizon이
어디까지 그 배치들을 구분할 수 있는지를 결과 전에 고정한다.

현재 catalog는 9개 factor oracle의 38개 conditional hypothesis를 닫는다. condition 계열은
access/encounter/candidate 한 위치뿐 아니라 multiple-registered-locations 후보도 보존한다.

```text
hypothesis-conditional signature
≠ observed human result
≠ causal residence proof
≠ correct internal path
```

## Adopt

| 결정 | 채택 내용 | 현재 지위 |
|---|---|---|
| FJ-B-01 | `trace oracle`은 mental ground truth가 아니라 가설 정의에 대한 conformance predicate다. | contract `FROZEN` |
| FJ-B-02 | 가설 관계, 실제 관측 상태, 후속 판정 상태를 서로 다른 vocabulary로 저장한다. | schema `FROZEN` |
| FJ-B-03 | horizon은 initial access 한 번과, 동일한 등록 future option을 양 path에 적용한 strictly later access 한 번으로 제한한다. 같은 arm의 O0–O5 emitted prefix는 future-extension replay에서도 불변이다. | ordinal horizon `FROZEN` |
| FJ-B-04 | 자연 contrast의 earliest divergence는 association/location signature일 뿐 direct edge 인증이 아니다. direct-edge 주장은 별도 D2a node-clamp challenge를 요구한다. | authority boundary `ADOPTED` |
| FJ-B-05 | REL delayed-reorganization probe는 initial reported mood × later reported mood의 2×2 trajectory로 등록하며 cue와 external target record를 고정한다. | future trajectory `FROZEN` |
| FJ-B-06 | `OPERATIONALLY_ALIASED`는 동일 probe·projection·horizon·measurement mapping 아래 가설 signature 전체가 같을 때만 허용한다. 관측 무차이는 `EMPIRICALLY_UNRESOLVED_UNDER_SCOPE`다. | alias rule `FROZEN` |
| FJ-B-07 | 등록 밖 효과는 raw observation과 provenance를 보존한 `OUT_OF_MODEL` lane으로 보내며 가장 가까운 기존 placement에 강제 cast하지 않는다. | result boundary `FROZEN` |
| FJ-B-08 | 한 번의 later access로 durable TargetForm과 slow cache를 판정하지 않는다. | `NOT_IDENTIFIABLE_UNDER_HORIZON` |
| FJ-B-09 | Ghost/adjudicator/action-gate 분리는 `001A`의 자연 factor 결과로 주장하지 않고 D2a-only selective challenge로 남긴다. | `NO_001A_NATURAL_INTERVENTION` |

## 세 vocabulary의 권한

```text
hypothesis relation
→ placement를 구현했다고 주장할 때의 조건부 계산 약속

observation status
→ 미래 protocol이 실제로 기록한 equality/difference/missing/mapping 상태

adjudication status
→ frozen scope 아래 signature conformance와 식별 한계 판정
```

`MUST_DIFFER_IF_PLACEMENT`는 “실제 인간이 반드시 달라야 한다”는 예측이 아니다.
`MUST_REMAIN_EQUAL`도 frozen projection에서 placement가 약속하는 equality일 뿐
“인간에게 효과가 없다”는 뜻이 아니다.

23개 trace field는 external `EvidenceLink` set과 claim-scoped `EvidenceAssessment`를
분리한다. first-person condition은 둘을 바꾸지 못한다. same-target history와 현재 public
stimulus는 공개 입력 때문에 둘을 바꿀 수 있지만 current identity·intention 인증 권한은
얻지 않는다. separate prior risk incident는 현재 미식별 source의 Evidence를 바꾸지
못한다. cue의 link-set equality도 EvidenceLink membership을 주장하지 않으며, 별도
reassessment policy 없이는 assessment relation을 판정하지 않는다.

## 자연 contrast와 node clamp

자연 시나리오에서 access projection과 encounter projection이 모두 달라졌더라도 access가
encounter의 직접 원인이라고 판정할 수 없다. upstream 차이의 매개 효과, 공통 원인 또는
measurement mapping이 같은 표면을 만들 수 있기 때문이다.

```text
natural factor contrast
→ association / first-registered-divergence 후보

D2a-only node clamp
→ 대안 node projection을 고정한 direct-edge challenge 설계
```

node clamp는 이번 작업에서 실행되지 않는다. operator, fixture, measurement mapping과
결과 evaluator는 D2a protocol에서 별도로 동결해야 한다.

## Future discriminability

같은 즉시 표면 아래 서로 다른 내부 path를 주장하려면, 두 path에 **같은** future option을
적용한 뒤 적어도 하나의 등록 later projection에서 차이를 관측할 수 있어야 한다.

```text
path A + future option X
vs
path B + future option X
```

`path A + X`와 `path B + Y`를 비교해 생긴 차이는 path 차이가 아니라 새 사건 confound다.
candidate surface anchor는 계속 설계자용이며 participant-facing 응답이나 관측값이 아니다.
O5 표면이 실제 frozen mapping에서 같거나 D2a가 no-feedback equal-surface clamp를 미리
동결하지 않았다면 distinct-path future 판정은 `NOT_EVALUABLE`이다.

## 식별 한계

- `H_REGISTERED_FUTURE_ACCESS_K_PLUS_1`은 strictly later access 한 번만 포함한다.
- durable state와 slow cache의 persistence 차이는 이 horizon으로 판정할 수 없다.
- human pairwise judgment와 verbal report는 encounter 가능성을 제약할 수 있지만 내부 node를
  직접 측정하거나 causal residence를 인증하지 않는다.
- LLM activation과 readout도 source-specific mapping이 동결되기 전에는 trace field 값이 아니다.
- Ghost, adjudicator와 action gate는 `001A`의 아홉 factor가 선택적으로 조작하지 않는다.

## Out-of-model과 boundary challenge

예상 밖 효과는 raw payload/digest, source, provenance, observation point, horizon과 mapping
status를 보존한다. 같은 confirmatory run의 결과를 본 뒤 schema를 넓혀 사전등록 결과로
다시 채점하지 않는다.

```text
unexpected effect
→ OUT_OF_MODEL_EFFECT_RECORDED

normative invariant violation
→ BOUNDARY_OR_PROTOCOL_CHALLENGE
```

둘은 다르다. Evidence 승격, source identity 발명, 과거 prefix rewrite와 같은 월권은 단순한
새 심리 효과로 흡수하지 않는다.

## Authority and support boundary

이번 freeze가 검증하는 것은 contract의 참조 완전성, signature 폐쇄성, ordinal horizon과
금지 cast뿐이다.

```text
contract/schema validation
≠ placement execution
≠ human or latent measurement
≠ D2a direct-edge result
≠ functional placement winner
≠ HM-INV-013 or HM-DYN-004 support
```

따라서 claim registry의 historical, structural, empirical support 배열을 추가하지 않는다.
특히 `HM-INV-013`과 `HM-DYN-004`는 계속 `UNIMPLEMENTED`다.

## Hold

| 항목 | 재개 조건 |
|---|---|
| human trace mapping | development 자료와 분리된 문항·mapping·missingness protocol |
| LLM latent mapping | paraphrase 안정성, 교차 모델 복제와 projection mapping freeze |
| D2a node-clamp execution | exact operator, fixture, seed/determinism과 evaluator freeze |
| durable TargetForm vs cache | one-future-access보다 긴 retention/reaccess horizon |
| placement adjudication | source-specific measurement mapping과 sealed result protocol |
| Dynamics/Narrative integration | `INTERP-DIALOGUE-001C` 이후 별도 adoption gate |

## 연결

- [Functional-jurisdiction scenario adoption](2026-07-13-functional-jurisdiction-scenarios.md)
- [`INTERP-DIALOGUE-001A` scenarios](../scenarios/interp-dialogue-001/README.md)
- [`INTERP-DIALOGUE-001B` trace oracle](../scenarios/interp-dialogue-001/trace-oracle.md)
- [RFC 0004](../rfcs/0004-subjective-encounter-interpretive-reorganization.md)
- [Roadmap](../roadmap.md)
