# Current Research Terminology Intake — Scope

## 1. 조사 질문

현재 연구 문서가 실제로 어떤 구분을 필요로 하며, Chapter 02에서 복원된 역사적 명칭군이 현재 설명에서 어떤 역할로 남아 있는지 조사한다.

이 배치는 Chapter 계보를 다시 해석하지 않는다. 현재 연구의 설명 책임을 별도로 추출해, 첫 concept ID가 엔진 시대 어휘만으로 결정되는 것을 막는다.

## 2. 주 입력

현재 연구의 직접 설명과 accepted/proposed RFC를 우선한다.

- `README.md`
- `research/README.md`
- `research/rfcs/0001-certification-descriptive-split.md`
- `research/rfcs/0002-temporal-kernel.md`
- `research/rfcs/0003-transition-density-morphic-load.md`
- `research/rfcs/0004-subjective-encounter-interpretive-reorganization.md`

## 3. 보조 입력

현재 synthesis와 경계 문제를 확인할 때만 사용한다.

- `notes/interchapter-note-03a-self-boundary-ghost-editor-episode.md`
- `notes/interchapter-note-04a-flow-boundary-decision-checkpoint.md`
- `notes/interchapter-note-08a-qualia-morphic-medium.md`
- `checkpoints/checkpoint-05a-current-tad-analysis.md`
- `models/README.md`

`models/README.md`는 현재 연구가 모델 수행에서 어떤 구분을 관찰하는지 확인하는 자료다. 개별 `models/<model>/prompt.md`와 평가는 정확한 모델 artifact이므로 이 입력 배치에서 개명하거나 현재 용어의 정본 근거로 사용하지 않는다.

## 4. 제외하는 입력

- `chapters/`: 각 Chapter 프로젝트에서 별도로 조사한다.
- 과거 원문 엔진 파일: Chapter가 제공하는 계보 확인 밖에서 직접 인간 근거로 사용하지 않는다.
- 폐기된 thread/crossing/map 구조: 현재 `main`에 존재하지 않으며 조사 단위로 복구하지 않는다.
- PR #33의 pilot harness: 현재 용어 조사 방법의 입력으로 사용하지 않는다.

## 5. 출처별 주장 권한

| 출처 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| 루트·research README | 현재 연구가 중요하게 보는 현상과 설명 요구 | 독립 인간 메커니즘의 경험적 확정 |
| RFC 0001 | Candidate/Intent/Attempt/Performance, occurrence/outcome, belief/evidence의 현재 계약 경계 | 인간에게 그대로 대응하는 내부 단계가 존재함 |
| RFC 0002 | 발생·가용·처리 시간, occurrence/delivery/reexposure의 현재 구현·연구 경계 | 인간 주관 시간 모델의 검증 |
| RFC 0003 | 처리 occurrence, qualified transition, deformation demand/load를 분리할 필요 | 인간 부하 차원과 계수의 확정 |
| RFC 0004 | access, encounter proxy, material, assembly candidate, adjudication, integration, Narrative write의 현재 제안 경계 | 제안 타입이 canonical human object라는 주장 |
| notes/checkpoints | 현재 synthesis 후보와 미해결 충돌 | accepted definition 또는 glossary 항목 |
| models README | 실제 모델 평가에서 구분해야 할 수행 표면 | 기존 모델 artifact 개명 권한 |

## 6. 초기 조사 명칭

Chapter 02 배치와 직접 대조하기 위해 다음 명칭의 현재 사용을 우선 조사한다.

- `Commit`
- `Event`
- `JOT`
- `Quench`

그러나 현재 연구의 구분 요구가 이 네 철자에 한정되는 것은 아니다. 현재 문서가 이미 명시한 다음 경계도 함께 추출한다.

- Candidate / Intent / Attempt / Performance
- Performance / ActionOccurrence / WorldOutcome
- occurrence / delivery / reexposure / access
- processed occurrence / qualified transition
- subjective encounter / evidence / world occurrence
- candidate / adjudication / integration / persistent write
- record / persistent state / write authority
- current readout / durable trace / writable state

## 7. 조사 원칙

1. `Commit`·`Event`가 등장했다는 사실만으로 그 문장을 같은 개념으로 묶지 않는다.
2. 구현 타입과 인간 설명 요구를 분리한다.
3. 현재 문서가 명시적으로 `A ≠ B`를 요구하면 독립 concept 후보로 자동 승인하지 않고, 왜 그 구분이 필요한지 extraction map에 기록한다.
4. 현재 직접 사용이 없는 `Quench`는 임의의 현재 개념으로 번역하지 않는다.
5. 현재 `JOT` 사용이 Chapter 계보를 언급하는 것인지 새 개념 use인지 구분한다.
6. `Event`라는 일반 자연어와 타입·단계·기록을 가리키는 기술어를 구분한다.
7. 모델 artifact는 잔여 검색 대상이지만 이 배치의 개명 대상이 아니다.

## 8. 이 배치가 만드는 산출물

- `extraction-map.md`: 현재 연구에서 요구되는 후보 책임과 관계
- `basic-term-list.md`: 조사 명칭에서 추출 항목으로 들어가는 색인

이 배치에서는 concept ID, 정의, 권장 명칭, glossary를 만들지 않는다.

## 9. 완료 조건

- 첫 concept 분석 전에 Chapter 02와 현재 연구를 나란히 비교할 수 있다.
- 현재 연구가 요구하는 구분과 엔진 구현 구분이 같은 근거 칸에 섞이지 않는다.
- `Commit`, `Event`, `JOT`, `Quench`의 현재 use/mention/absence가 구분된다.
- 현재 연구에서 확인되지 않은 후보를 곧바로 ENGINE-ONLY로 판정하지 않는다.
- 후보 내용은 extraction map만 소유하고 basic term list는 색인으로 남는다.
