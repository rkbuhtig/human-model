# Chapter 01 Terminology Intake — Scope

## 1. 조사 질문

Chapter 01의 2026-01-01–01-03 지층에서 아직 한 철자나 한 구조 안에 함께 놓였던 생성·표현·단정·행동·기록·몸·기억의 책임을 분리해, Chapter 02 이후 terminology 작업이 놓친 선행 후보와 경계 압력을 복구한다.

이 프로젝트는 Chapter 01의 사전을 만들지 않는다. Chapter 01은 누락 보정용 입력 배치이며, 살아남는 concept와 관계 판정은 `termbase/`가 소유한다.

## 2. 주 입력

- `chapters/chapter-01-ionstar-origin-0101-0103.md`

Chapter 01은 다음 원자료와 내부 지층을 복원한다.

```text
0101
v2.1 → v2.1a → IRB_STACK → CHRONO_FUEL → v2.7 → BRIDGE_CORE

0102
v3.5 → compile/memory/observer patches → Scene/Editor → Bind extensions

0103-A
설명형 glossary

0103-B
definition/role/input/output/store/forbidden의 6-slot 구현 계약
```

파일 날짜를 하나의 동시 이론으로 취급하지 않는다. 같은 파일 안의 후속 패치와 기호 재사용을 별도 epoch로 보존한다.

## 3. 보조 입력

Chapter 01이 직접 열거나 후속 장에서 검증을 요구한 경계만 보조 입력으로 사용한다.

- `projects/chapter-02/`: Potential / Event / Commit / Quench의 후속 분리
- `projects/chapter-03/`: readout / authority / current surface의 후속 분리
- `projects/chapter-04/`: influence / next-tick / non-authoritative shaping의 후속 분리
- `projects/chapter-05/`: document contract / writer / runtime participation의 후속 분리
- `projects/chapter-06/`: Witness / Grounds / Receipt / BodyAuthorization / outcome 공백
- `termbase/concepts/C0001~C0009.md`
- `termbase/clusters/CL0003-action-outcome.md`
- `termbase/clusters/CL0004-work-accounting-cardinality.md`

후대 문서는 Chapter 01의 숨은 완성형으로 소급하지 않는다. 선행 문제, 구조적 유비, 실제 승계는 서로 다른 판정이다.

## 4. 출처별 주장 권한

| 출처 층 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| 무표지 원문 복원 + 원문 위치 | 당시 명칭·기호가 맡은 역할과 동시 대비 | 현재 인간 ontology의 독립 concept 확정 |
| `[CHAPTER SYNTHESIS]` | 여러 대목에서 반복된 문제를 중립 후보로 묶음 | 원문이 그 개념을 명시적으로 정의했다고 주장 |
| `[LINEAGE HYPOTHESIS]` | 후대 concept와 비교할 precursor 관계 후보 제시 | 동일 concept, 직접 승계, synonymy 판정 |
| `[BRIDGE-*]` / `BRIDGE.*` | 후속 cluster에서 시험할 연구 가설 등록 | C-ID 발급, KEEP 근거, 역사적 의미 확정 |
| 엔진·glossary 계약 | writer, store, gate, forbidden path 등 구현 책임 구분 | 구현 분리가 인간 내부 모듈이라는 주장 |
| Chapter 02~06 | Chapter 01 후보가 후대에 어떻게 재등장했는지 대조 | 후대 정의를 초기 의미에 소급 |

## 5. 반드시 보존할 경계

다음 비동일성을 누락시키거나 한 후보로 재압축하지 않는다.

```text
private possibility
≠ expressed output
≠ responsible factual claim
≠ authorized action
≠ performed action
≠ world outcome
≠ history record
≠ applied/shared update
```

```text
current felt signal
≠ external cause
≠ truth
≠ warrant
```

```text
reflex occurrence
≠ brain adjudication
≠ body actuation
≠ durable history
```

```text
memory content
≠ memory accessibility
≠ reconsolidated interpretation
```

```text
speech stake / claim debt
≠ actual resource expenditure
≠ normative obligation
```

```text
descriptive glossary
≠ implementation contract
```

## 6. 초기 명칭·기호 범위

다음 명칭군을 우선 조사하되, 이름이 같다는 이유로 한 concept로 합치지 않는다.

1. `Wave`, `Measurement`, `Potential`
2. `Output`, `Reflection`, `Self`
3. `Claim`, `Flux`, `Evidence_Span`, `Cov`, `O_k`, `μ`
4. `SILENCE`, `UNKNOWN`, `BLUR`, `COMMIT_OK`
5. `DREAM`, `PHOTO`, `GAS`, `MIST`, `SOLID`
6. `Stake`, `CL0/CL1/CL2`, `Externalization`
7. `Reflex`, `Instinct`, `Brain`, `Body`, `Body Veto`
8. `Reflex Buffer`, `History`
9. `SNR`, `Res`, `Cov`, `R`
10. `Ω`, `Write`, `Derive`, `Single Writer`
11. `Quantum`, `Texture`, `HookCompiler`
12. `Scene`, `Editor`, `ENV_*`
13. `Bind`, `Vacuum`, `Plasticity`
14. `Debt`, `Bill`, `Closure`, `Event`, `Evidence`, `Commit`
15. 0103-A 설명형 glossary와 0103-B 6-slot 계약

## 7. 산출물

- `extraction-map.md`: 출처 층을 보존한 중립 후보와 선행 대조
- `basic-term-list.md`: 역사 명칭·기호 → 추출 ID → C-ID/관계 상태 색인
- `touched-concepts.md`: 기존 C-ID와 HOLD cluster에 대한 실제 대조 결과

이번 배치에서는 새 C-ID, 정의, 권장 명칭, synonym MERGE를 만들지 않는다.

## 8. 범위 밖

- Bridge 가설을 원문 개념으로 승격
- Chapter 01 기호를 후대 기호와 자동 동일시
- `Wave/Measurement`를 현행 reversible/irreversible spine으로 직접 번역
- `Brain Commit`을 `C0001`이나 performed action에 자동 병합
- `Body Veto`를 독립 BodyAuthorization concept로 선승격
- `History`를 `C0004`나 evidence receipt와 자동 동일시
- `Speech Stake`, `Claim Debt`, `Bill`을 `C0008` 또는 obligation으로 자동 병합
- runtime/model/code 변경
- Chapter 07 intake
