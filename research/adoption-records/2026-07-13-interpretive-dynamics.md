# Adoption Record — Subjective Encounter and Interpretive Dynamics

| 항목 | 값 |
|---|---|
| Date | 2026-07-13 |
| Source | 사용자 주도 이론 보정과 Chapter 02 / Interchapter Note 03-A / Checkpoint 05-A 기능 경계 대조 |
| Decision | `ADOPTED WITH REVISIONS` |
| Implementation | `INTERP-001A` boundary `DOCUMENTED`; `INTERP-001A2` reception M1 manifest `FROZEN / UNEXECUTED`; broader manifest, detached lab과 runtime integration `UNIMPLEMENTED` |
| Human-empirical status | `OPEN` |

`ADOPTED`는 연구 방향과 금지 등식을 채택한다는 뜻이다. 실제 인간의 퀄리아,
기억 구조, 기분 효과 또는 점화 법칙을 구현·측정·입증했다는 뜻이 아니다.

## Adopt

| 결정 | 채택 내용 | 지위 |
|---|---|---|
| I-A-01 | 외부 occurrence, 관측·증거, 현재 access, 주관적 encounter proxy와 Episode material 역할을 분리한다. | 방향 `ADOPTED`; 신규 타입 `PROPOSED` |
| I-A-02 | 현재의 수용 상태는 material access와 interpretive-candidate fit을 서로 다른 operator로 기울일 수 있다. | `DYNAMICAL_HYPOTHESIS` |
| I-A-03 | 당시 조립되지 못한 단서는 삭제나 반대 극성 확정 없이 이후 access/assembly의 source ref로 남을 수 있다. | `DYNAMICAL_HYPOTHESIS` |
| I-A-04 | 과거 material의 현재 재접근은 별도 access occurrence이며 과거 occurrence, 최초 encounter receipt와 EvidenceLink를 다시 쓰지 않는다. | provenance 방향 `ADOPTED` |
| I-A-05 | Ghost는 interpretation candidate를 생성·탐색하지만 scoped adjudication, Episode integration, Narrative write 또는 external truth를 인증하지 않는다. | 방향 `ADOPTED` |
| I-A-06 | 대상 형태는 전역 긍정·부정 lens가 아니라 actor, interpreted-target, relation/context scope에 한정된 readout 후보로 시작한다. | `HOLD / TYPE CANDIDATE` |
| I-A-07 | 같은 event/material 수·크기에서 access, assembly topology, reception profile과 탐색 경로가 단순 합·threshold와 다른 구조 구분을 만드는지 비교한다. | hypothesis `PROPOSED`; reception access/coherence M1 manifest `FROZEN / UNEXECUTED`; broader manifest `OPEN` |

## Revise

### I-R-01 — `EpisodeNarrative` 용어 폐기

작은 임시 해석 묶음을 `EpisodeNarrative`라고 부른 것은 기존 연구의 큰
`Episode → Narrative` 승격 의미와 충돌한다. 역사에서 반복되는 것은 다음 기능
경계다.

```text
Ghost candidate
≠ Editor / JOT.court 계열의 후보 판정
≠ Episode buffer / write
≠ Narrative Field write
```

새 detached-lab 합성은 과거 정본이 아니라 다음 `PROPOSED` 객체열이다.

```text
EpisodeMaterialReference
→ EpisodeAssemblyCandidate + AssemblyMaterialMembershipCandidate[]
→ InterpretiveBindingCandidate
→ BindingAdjudicationReceipt
→ optional adopted-only EpisodeIntegrationReceipt
```

### I-R-02 — 역사적 ontology를 현행 정본으로 소급하지 않음

Ghost/Editor/Episode는 시대에 따라 독립 역할과 하나의 field mode 사이를 오갔고,
`JOT`도 court-cycle, sketch stream, store를 뜻한 적이 있다.
`EpisodeMaterial / EpisodeAssembly / NarrativeBinding`은 Checkpoint 05-A의 현행
synthesis candidate이지 이미 구현된 canonical 타입이 아니다.

새 RFC는 `JOT.court`처럼 지층을 한정해 참조하고, 새 adjudicator나 curator를
역사적 Editor/JOT와 동일시하지 않는다.

### I-R-03 — 점화는 단일 사건 속성이 아님

`ignition_power(event)` 또는 `cue_sum >= threshold` 하나로 정의하지 않는다.
첫 실험에서 점화는 material access, assembly bridge, current reception, prior
target-form readout과 Ghost exploration의 관계적 결과 후보로만 다룬다.

### I-R-04 — 기분은 외부 사실이나 단일 threshold가 아님

`ReceptionStateSnapshot`은 multi-component simulation fixture로 시작한다.
외부 occurrence의 진실, Evidence strength, 실제 인간의 기분 측정값 또는 보편적인
긍정/부정 scalar가 아니다. 긍정·부정 방향 성분은 상쇄하지 않으며 access 효과와
candidate-coherence 효과를 별도 경쟁 모델로 분리한다.

### I-R-05 — 컨디션 변화만으로 과거를 자동 재작성하지 않음

현재 상태가 달라져도 재접근·연상·회상과 같은 `CurrentAccessOccurrence`가 없으면
과거 material, assembly 또는 binding을 바꾸지 않는다. 자발적 회상도 source가
known/claimed/unknown일 수 있는 현재 access occurrence로 남기며 Ghost가 원인이었다고
자동 인증하지 않는다.

### I-R-06 — candidate, 판정, integration은 append-only로 분리

```text
InterpretiveBindingCandidate
≠ BindingAdjudicationReceipt
≠ EpisodeIntegrationReceipt
≠ authored Narrative write
```

rejected/deferred candidate를 persistent binding으로 취급하지 않는다. adjudication
outcome은 candidate를 mutate하지 않는 append-only receipt다.

### I-R-07 — `TargetForm`은 먼저 readout 후보

새 durable writer를 추가하지 않는다. `TargetFormReadout`이 Narrative Field,
object-scoped integration/binding, implicit/plastic trace 중 무엇을 읽어야 하는지와
writer·retention·revalidation을 아직 식별하지 못했으므로 현재 지위는
`HOLD / READOUT CANDIDATE`다.

## Hold

| 항목 | 재개 조건 |
|---|---|
| 실제 `EncounterQualia` 측정 주장 | 독립 관측 절차와 인간 자료 |
| 인간 일반의 mood-congruent ignition 법칙 | preregistered human measurement와 competing baseline |
| authored `Narrative Field` write | 기존 ΔC / α / β 계열 gate와 writer 계약 대조 |
| implicit formation 통합 | endorsement 없는 slow writer의 scope와 lineage 정의 |
| `TargetForm` readout 구현 또는 durable state 승격 | source-definition ablation, writer, retention과 revalidation 규칙 확인 |
| `MORPH-001B` proxy와 interpretive reorganization 접합 | INTERP detached lab 구조 구분 성공과 독립 measurement mapping |
| 정신 시간·퀄리아·사랑의 정량 출력 | 각각의 독립 claim, measurement model, falsifier |

## 실행 연결

- [RFC 0004 — Subjective Encounter and Interpretive Reorganization](../rfcs/0004-subjective-encounter-interpretive-reorganization.md)
- [INTERP-001 preregistration](../benchmarks/interp-001-subjective-encounter-binding.md)
- [Roadmap](../roadmap.md)

이 기록은 RFC 승인, 코드 구현, synthetic 결과, predictive support 또는 인간 경험적
지지를 대신하지 않는다.
