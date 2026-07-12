# Adoption Record — Research Program Plan Assessment

| 항목 | 값 |
|---|---|
| Date | 2026-07-13 |
| Source | [External non-peer assessment](../../assessments/2026-07-13-research-program-plan-assessment.md) |
| Decision | `ADOPTED WITH REVISIONS` |
| Implementation | 문서·baseline `IMPLEMENTED`; 코드 분리 `PLANNED` |
| Human-empirical status | `OPEN` |

`ADOPTED`는 연구 방향의 채택이지 구현 완료나 경험적 참을 뜻하지 않는다.

## Adopt

| 결정 | 채택 내용 | 구현 지위 |
|---|---|---|
| A-01 | Assessment / Adoption / Implementation / Run / Empirical Evidence 분리 | 문서 `IMPLEMENTED` |
| A-02 | Contract / Descriptive Dynamics / Experimental Protocol 분리 | v0.1.1 `PLANNED` |
| A-03 | `EpistemicState → EvidenceAssessmentState`; `WarrantState` 유보 | v0.1.1 `PLANNED` |
| A-04 | claim 근거를 history/tests/datasets 독립 축으로 기록; scope/exclusions 필수 | schema + 첫 claim `IMPLEMENTED` |
| A-05 | Contract mutation / Structural ablation / Temporal comparison 분리 | 설계 문서 `IMPLEMENTED`; 실행 `PLANNED` |
| A-06 | 하나의 canonical `sim_time`과 여러 event timestamp | v0.2 `PLANNED` |
| A-07 | `occurrence_id ≠ delivery_id`; 과거 사건과 현재 재노출 분리 | v0.2 `PLANNED` |
| A-08 | v0.3은 `affect → SubjectiveBelief` 하나만 다룸 | v0.3 `PLANNED` |
| A-09 | 결함의 당시 기록과 현재 소급 해석 분리 | schema + 첫 case `IMPLEMENTED` |
| A-10 | 구조 변경 전에 v0.1 baseline 동결 | `FROZEN` |

## Revise

### R-01 — Certification은 Contract Layer의 일부

인증이 핵심이지만 출처 무결성, 전이 계보, 입력 회계도 계약이다.

```text
Contract Layer
├─ Certification
├─ Provenance / Integrity
├─ Transition Lineage
└─ Accounting
```

### R-02 — 관할별 typed record 유지

하나의 보편적 `CertificationRecord`로 합치지 않는다.

```text
BeliefUpdateRecord ≠ EvidenceAssessmentRecord
PerformanceReceipt ≠ ActionOccurrenceRecord ≠ WorldOutcomeRecord
```

### R-03 — Flow 법칙은 조건부

`Flow(Flow(x, dt1), dt2) ≈ Flow(x, dt1 + dt2)`는 무입력·동일 환경·시간
동질적인 경우에 검사한다. 그 밖에는 step-size convergence를 본다.

### R-04 — exact belief 값은 가설이 아님

v0.3은 `0.30 → 0.75` 같은 예시값이 아니라 affect–belief 방향성,
EvidenceAssessment 독립성, 인증 경계를 검증한다.

## Hold

| 항목 | 재개 조건 |
|---|---|
| `WarrantState` | reliability, defeater, validity, revalidation 규칙 정의 |
| 주관적/생물학적 시계 | canonical time과 구분되는 예측 제시 |
| 반복 서사→확신 | source-memory 구조 정의와 v0.3 종료 |
| 의도→수행 기억 오귀속 | action trace와 memory reconstruction 정의 |
| 위협→모호 증거 과채택 | ambiguous evidence와 criterion 모델 정의 |
| 물리 은유의 측정량 승격 | 단위, 관측 절차, 판별 예측 정의 |
| 인간 경험적 정확도 주장 | dataset, measurement model, competing baseline 평가 |

## 실행 연결

- [RFC 0001 — 층 분리](../rfcs/0001-certification-descriptive-split.md)
- [RFC 0002 — 시간 kernel](../rfcs/0002-temporal-kernel.md)
- [Roadmap](../roadmap.md)

이 기록은 RFC 승인이나 구현 완료를 대신하지 않는다.
