# Chapter 05 — Touched Concepts

이 문서는 Chapter 05 배치가 실제 concept 분석에서 갱신한 C-ID와, 아직 C-ID를 열지 않은 인접 후보의 목적지를 기록한다. 정의와 후보 설명은 각각 `termbase/concepts/`와 `extraction-map.md`가 소유한다.

## 갱신한 concept

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH05-033` — Decision·ActionOut·actual occurrence·world outcome이 갈림
- 판정:
  - `Decision_t`의 경로 채택 역할을 `MERGE → C0001`로 판정한다.
  - `ActionOut_t`와 `Gate_Action`은 선택 상태가 아니라 ENGINE-ONLY 출력 경로다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0001.md`

### C0002 — 외부 발생

- 사용한 후보:
  - `X-CH05-033` — actual occurrence가 Decision·ActionOut과 분리됨
- 판정:
  - 외부에서 실제 수행된 행동 occurrence는 `MERGE → C0002`다.
  - `ActionOut`이 존재하는 것만으로 occurrence를 승인하지 않는다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0002.md`

### C0003 — 세계 결과 상태

- 사용한 후보:
  - `X-CH05-033` — world outcome이 actual occurrence와 분리됨
- 판정:
  - 선행 occurrence 뒤 생긴 세계 결과 상태는 `MERGE → C0003`다.
  - outcome receipt·관측 결과는 결과 상태 자체가 아니며 보류한다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0003.md`

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH05-033` — 실제 행동 occurrence를 결박할 action receipt 요구
- 판정:
  - 실제 performed action의 성립을 표상하는 action receipt는 `MERGE → C0004`다.
  - generic CommitRecord, configuration Receipt, outcome receipt는 자동 병합하지 않는다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0004.md`

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH05-028` — 외부 입력 전체를 `VIEW`로 잠근 over-closure
  - `X-CH05-029` — policy-shaped `PercIn`이 phys·commit 경로에 들어가는 구조
- 반영한 경계:
  - runtime의 `VIEW` label은 현재 체험 표면 자체가 아니다.
  - `PercIn`은 체험 구성에 관여하는 구현 입력일 수 있지만, 실제 1인칭 체험이나 그 보고와 자동 동일시하지 않는다.
- 상세 판정: `../../termbase/concepts/C0005.md`

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH05-018` — active policy와 next policy 분리
  - `X-CH05-019` — active candidate manifest와 next manifest 분리
  - `X-CH05-021` — CandidateGen이 미래 후보 공간을 바꾸는 경로
  - `X-CH05-023` — STG branch에서 same-tick Propose→Select가 재개방된 비교 누락
- 반영한 경계:
  - next-tick 경로는 비권위적 영향을 구현한 역사적 안전장치이지 concept의 필수 시간 지연이 아니다.
  - 후보 공간을 바꾸는 영향과 current Select·Commit 권한은 별도다.
  - same-tick이라는 이유만으로 영향이 곧 권한이 되는 것도, 모든 즉시 영향이 금지되는 것도 아니다.
- 경계 교정 기록: `../../termbase/harmonization/H0001.md`
- 상세 판정: `../../termbase/concepts/C0006.md`

### C0009 — 수행·지출 회계 기록

- 사용한 후보:
  - `X-CH05-017` — integrity·reproducibility와 truth·legitimacy 분리
  - `X-CH05-022` — candidate route provenance
  - `X-CH05-024` — Commit decision input과 record input 분리
  - `X-CH05-025` — next pointer가 substantive decision이 아니라 rotation parameter인 경우
  - `X-CH05-026` — record-only CommitRecord
  - `X-CH05-027` — 의미 교정 뒤 낡은 field가 남은 type residue
  - `X-CH05-033` — action receipt·outcome receipt 공백
- 반영한 경계:
  - 실행 trace와 audit record는 외부 명제의 truth·warrant가 아니다.
  - decision input, pointer rotation parameter, candidate provenance, 수행·지출 회계 기록은 같은 record concept가 아니다.
  - action occurrence record는 C0004이며 work/spend를 표상하지 않는 한 C0009가 아니다.
- 상세 판정: `../../termbase/concepts/C0009.md`

## 판정된 기술·역사 역할

### ENGINE-ONLY

- `X-CH05-033`의 `ActionOut_t`, `Gate_Action`
  - 선택된 결정을 외부 실행기로 전달하는 출력·gate 역할이다.
  - actual occurrence와 world outcome을 보증하지 않는다.

### 보류

- `X-CH05-033`의 outcome receipt
  - outcome state, outcome observation, observation artifact, claim support의 경계가 아직 닫히지 않았다.

## 아직 남은 인접 후보

- `X-CH05-002`, `X-CH05-015` — textual preservation·PackRef와 occurrence record의 관계: record cluster에서 후속 판정
- `X-CH05-030~031` — input admission과 positive evidence path 공백: evidence / claim-support cluster로 보류
- `X-CH05-003~017`, `X-CH05-032`, `X-CH05-034~036`의 registry·socket·integrity·Narrative binding 책임: 인간 concept로 자동 승격하지 않고 후속 cluster에서 ENGINE-ONLY·HISTORICAL-ONLY·보류 판정

`X-CH05-035`는 Narrative binding, `X-CH05-036`은 PackRef verifier stage 문제다. action/outcome 사슬의 추출 항목은 `X-CH05-033`이다.

## 이번 배치의 판정 요약

```text
기존 C-ID 갱신: C0001, C0002, C0003, C0004, C0005, C0006, C0009
새 C-ID: 없음
MERGE: Decision→C0001, performed action→C0002, world outcome→C0003, action receipt→C0004
ENGINE-ONLY: ActionOut, Gate_Action
HISTORICAL-ONLY: 없음
보류: outcome receipt, evidence, registry/socket/integrity/Narrative cluster
```
