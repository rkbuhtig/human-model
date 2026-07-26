# Chapter 03 Terminology Intake — Scope

## 1. 조사 질문

Chapter 03에서 Chapter 02의 `Event ≠ Commit`, `Persistence ≠ Authority`, `PROCESS ≠ STORE` 문제가 어떤 새 명칭과 구조로 이동했는지 추출한다.

이 배치는 특히 다음 이동을 본다.

```text
사건 / 고정
→ readout / persistent state
→ proposal / selection
→ provenance / authority lane
→ application gate
```

목표는 Chapter 03의 역사적 어휘를 현재 concept로 승인하는 것이 아니다. 같은 이름이 어떤 거주지·writer·clock·권한을 오갔는지 보존하고, Chapter 02 및 current-research 배치와 대조할 입력을 만든다.

## 2. 선행 입력

이 프로젝트는 PR #34에서 만든 다음 배치를 전제한다.

- `projects/chapter-02/`
- `projects/current-research/`

Chapter 03 후보는 기존 추출 ID와 연결할 수 있지만, 기존 후보를 자동 통합하거나 C-ID로 승격하지 않는다.

## 3. 주 입력

- `chapters/chapter-03-readout-authority-0111-0115.md`

Chapter가 구분한 원문 지층과 재발행 관계를 그대로 따른다.

```text
P52 / P521 / P524 / P526 / P527
INT14 / PHI14 / TIME14 / FULL15
LS15 / UL15 / LAB15
```

같은 본문의 재발행을 독립 증거로 중복 계상하지 않는다.

## 4. 보조 입력

다음 문서는 Chapter 03의 현재 대응과 명칭 잔존을 확인할 때만 사용한다.

- `research/terminology/projects/chapter-02/extraction-map.md`
- `research/terminology/projects/current-research/extraction-map.md`
- `research/terminology/README.md`

Chapter 04 이후 문서는 이번 배치에서 선행 정답으로 사용하지 않는다. Chapter 03이 남긴 open question을 후대 개념으로 소급 해소하지 않는다.

## 5. 출처별 주장 권한

| 출처 | 이 배치에서 할 수 있는 주장 | 이 배치에서 할 수 없는 주장 |
|---|---|---|
| Chapter 03 역사 본문 | 당시 명칭이 어떤 역할·writer·clock·권한을 맡았는가 | 그 구조가 현재 인간 내부의 독립 메커니즘임 |
| Chapter 03 synthesis/afterword | 여러 지층 사이의 충돌과 현행 문제틀의 계보 | 최종 정의·권장 용어·경험적 확정 |
| Chapter 02 배치 | 선행 과적재 후보와의 연결 | Chapter 03 후보와의 concept 동일성 확정 |
| current-research 배치 | 현재 사용과 계약 경계 | 인간 현상 근거 또는 KEEP 승인 |

Chapter 03에는 인간적 장면과 뉘앙스가 포함돼 있지만, 이 저장소 내부의 역사 복원·이론 synthesis다. 독립 인간 현상 근거로 사용하지 않는다.

## 6. 초기 조사 명칭과 기호

### Chapter 02에서 이어진 명칭

- `Event`, `EventFire`
- `Commit`, `CommitEvent`
- `Quench`
- `JOT`, `View`, `Ψ`
- `SSOT`
- `Φ`
- `e`

### Chapter 03에서 새로 중심이 된 명칭

- `Π_phys`, `Π_perc`
- `Z`
- `𝒢⁺`
- `Γ`
- `StoryField`, `MeaningFlux`
- `AttachTag`
- `Budget`
- `Why-token`, collapse signature
- `READOUT_ONLY`, `AuthorityLane`
- `SourceEvent`, `TraceRoot`, `ImpactDeps`, `Trace/Facts`
- `WorkEvent`, Billing
- `ULGATE`, `CommitAnchor`
- `LAB`, `RATIONALE`, `CORE`

### 별도 충돌 확인 대상

- `P`, `A`, `W`
- `C`
- `g_i`, `g_t`
- `h`
- `F_out`, `F_use`, `Spend`
- `q_conf`, `q_lock`, `q_rate`
- `VOID`, `Γ_void`

이 목록은 최종 concept 목록이 아니라 용어 색인의 초기 진입점이다.

## 7. 우선 대조할 선행 추출 항목

- X-CH02-003 외부 발생
- X-CH02-005 단계·위상
- X-CH02-006 검사점·시점
- X-CH02-007 기록
- X-CH02-008 비가역 잠금
- X-CH02-009 Event 뒤 Quench
- X-CH02-010 Quench 포함 Event
- X-CH02-012 JOT 판정 cycle
- X-CH02-013 JOT store
- X-CH02-015 persistent/SSOT state
- X-CH02-019 의미 확정
- X-CH02-021 phenomenal surface
- X-CH02-022 routing field
- X-CH02-025 readout과 write authority 분리
- X-CURR-015 믿음과 증거 평가
- X-CURR-016 record/provenance와 state
- X-CURR-017 readout과 writable state

## 8. 조사 원칙

1. Chapter 03의 새 이름을 Chapter 02 후보의 정답으로 소급하지 않는다.
2. `Event`, `Commit`, `Quench`의 철자가 같아도 occurrence, phase, application, gate를 같은 후보로 묶지 않는다.
3. `JOT`의 가역 후보장과 append-only log를 별도 추출한다.
4. `Φ`, `Z`, Story, Why-token의 강도·지속성·설명력을 authority로 해석하지 않는다.
5. proposal influence와 selection/application authority를 별도 후보로 둔다.
6. SourceEvent·TraceRoot·ULGATE는 provenance와 실행 감사를 제공하지만 epistemic evidence로 자동 번역하지 않는다.
7. 인간적 사례 문장은 경계 설명에 사용할 수 있지만 인간 연구 concept의 KEEP 근거로 사용하지 않는다.
8. A2 symbol collision은 해당 철자가 실제로 다른 writer·clock·거주지를 가질 때 색인에 남긴다.
9. 후보 설명의 단일 권위는 `extraction-map.md`다. `basic-term-list.md`는 색인만 제공한다.

## 9. 산출물

- `extraction-map.md`: Chapter 03에서 추출한 중립 후보와 관계
- `basic-term-list.md`: 역사적 명칭·기호에서 추출 ID로 들어가는 색인

이 배치에서는 다음을 만들지 않는다.

- C-ID
- concept 정의
- KEEP / MERGE / ENGINE-ONLY 판정
- harmonization 기록
- glossary
- 현재 문서 rename

## 10. 완료 조건

- Chapter 02의 핵심 분리가 Chapter 03에서 어떻게 일반화됐는지 추적 가능하다.
- Event/Commit/Quench, JOT/View/SSOT, Φ/readout/authority의 이동이 별도 후보로 보존된다.
- JOT의 process/store 충돌이 다시 한 항목으로 접히지 않는다.
- Story의 proposal 권한과 selector/application 권한이 분리된다.
- provenance·trace·gate와 epistemic evidence가 구분된다.
- Chapter 03의 주요 symbol collision이 basic term index에서 누락되지 않는다.
- 이 배치의 인간적 장면이 독립 인간 현상 근거로 오인되지 않는다.
