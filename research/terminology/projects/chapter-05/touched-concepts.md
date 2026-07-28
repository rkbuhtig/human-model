# Chapter 05 — Touched Concepts

이 문서는 Chapter 05 배치가 concept 분석에서 갱신한 C-ID와, C-ID를 열지 않은 인접 후보의 관계·목적지를 기록한다. 정의는 `termbase/concepts/`, 후보 설명은 `extraction-map.md`, 형제 비교는 `termbase/clusters/`가 소유한다.

## 갱신한 concept

### C0001 — 행동 경로 선택

- 사용한 후보: `X-CH05-033`의 Decision·ActionOut 분리
- 판정:
  - `Decision_t`가 여러 행동 경로 중 하나를 수행 대상으로 채택하는 역할일 때 C0001을 사용한다.
  - 이 연결은 `Decision` 철자 전체의 synonymy를 승인하지 않는다.
  - `ActionOut_t`, `Gate_Action`은 ENGINE-ONLY 출력 경로다.
- 관계 교정: `../../termbase/harmonization/H0003.md`

### C0002 — 외부 occurrence

- 사용한 후보: `X-CH05-033`의 actual occurrence
- 판정:
  - actual occurrence와 C0002의 경계는 유지한다.
  - `PerformedAction`을 C0002에 MERGE하지 않는다.
  - 관계: `PerformedAction NARROWER-CANDIDATE-OF C0002`, 상태 `HOLD`.
  - ActionOut의 존재만으로 occurrence를 승인하지 않는다.
- cluster: `../../termbase/clusters/CL0003-action-outcome.md`

### C0003 — 결과 상태 후보군

- 사용한 후보: `X-CH05-033`의 world outcome·outcome receipt 공백
- 판정 변화: `KEEP → HOLD`
- 이유:
  - realized world outcome, relational outcome, settlement status, outcome의 epistemic status가 아직 분리되지 않았다.
  - `ExternalOutcome MERGE → C0003` 판정을 철회한다.
- 목적지: `../../termbase/clusters/CL0003-action-outcome.md`

### C0004 — occurrence record

- 사용한 후보: `X-CH05-033`의 action receipt 요구
- 판정:
  - C0004 KEEP 유지.
  - performed-action record를 C0004에 MERGE하지 않는다.
  - 관계: `performed-action record NARROWER-CANDIDATE-OF C0004`, 상태 `HOLD`.
  - generic CommitRecord, configuration Receipt, outcome receipt는 자동 연결하지 않는다.
- 관계 교정: `../../termbase/harmonization/H0003.md`

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH05-028` — 외부 입력 전체를 VIEW로 잠근 over-closure
  - `X-CH05-029` — policy-shaped PercIn이 phys·commit 경로에 들어가는 구조
- 유지한 경계:
  - runtime VIEW label은 현재 체험 표면 자체가 아니다.
  - PercIn은 구현 입력이며 1인칭 체험이나 자기보고와 자동 동일시하지 않는다.

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH05-018~019` — active/next policy·candidate 분리
  - `X-CH05-021` — 미래 후보 공간 변경
  - `X-CH05-023` — same-tick Propose→Select 재개방
- 유지한 경계:
  - next-tick은 역사적 안전장치이지 concept의 필수 지연이 아니다.
  - 후보 공간에 대한 영향과 current Select·Commit 권한은 별도다.
- 조화: `../../termbase/harmonization/H0001.md`

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보:
  - `X-CH05-017`, `X-CH05-022`, `X-CH05-024~027`, `X-CH05-033`
- 판정 변화: `ENGINE-ONLY → HOLD / SUBJECT-FIELD SPLIT`
- 이유:
  - work-performance record, expenditure record, dependency trace, attribution record는 표상 대상과 정확성 조건이 다르다.
  - action occurrence record는 C0004이며 generic audit record도 C0009와 동일하지 않다.
- 목적지: `../../termbase/clusters/CL0004-work-accounting-cardinality.md`

## 기술·역사 역할

### ENGINE-ONLY

- `X-CH05-033`의 `ActionOut_t`, `Gate_Action`

### HOLD

- `X-CH05-033`의 performed-action record
  - C0004 NARROWER 후보
- `X-CH05-033`의 world outcome
  - C0003 RELATED/NARROWER 후보
- `X-CH05-033`의 outcome receipt
  - outcome observation·record·claim support cluster

## 아직 남은 인접 후보

- `X-CH05-002`, `X-CH05-015` — textual preservation·PackRef와 record 관계
- `X-CH05-030~031` — input admission과 positive evidence path 공백
- registry·socket·integrity·Narrative binding 책임 — ENGINE-ONLY·HISTORICAL-ONLY·HOLD 후속 판정

`X-CH05-035`는 Narrative binding, `X-CH05-036`은 PackRef verifier stage다. action/outcome 사슬은 `X-CH05-033`이다.

## 판정 요약

```text
C0001: KEEP, Decision 역할 연결만 유지
C0002: KEEP, PerformedAction NARROWER 후보 / HOLD
C0003: KEEP 철회 → HOLD
C0004: KEEP, performed-action record NARROWER 후보 / HOLD
C0005: KEEP
C0006: KEEP
C0009: ENGINE-ONLY 철회 → HOLD / SUBJECT-FIELD SPLIT
MERGE: 없음
ENGINE-ONLY: ActionOut, Gate_Action
새 C-ID: 없음
```
