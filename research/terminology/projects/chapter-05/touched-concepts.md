# Chapter 05 — Touched Concepts

이 문서는 Chapter 05 배치가 실제 concept 분석에서 갱신한 C-ID와, 아직 C-ID를 열지 않은 인접 후보의 목적지를 기록한다. 정의와 후보 설명은 각각 `termbase/concepts/`와 `extraction-map.md`가 소유한다.

## 갱신한 concept

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
- 반영한 경계:
  - 실행 trace와 audit record는 외부 명제의 truth·warrant가 아니다.
  - decision input, pointer rotation parameter, candidate provenance, 수행·지출 회계 기록은 같은 record concept가 아니다.
  - Chapter 05의 여러 record 후보는 C0009에 자동 병합하지 않고 기술 인접 후보로 남긴다.
- 상세 판정: `../../termbase/concepts/C0009.md`

## 기존 concept를 비춘 인접 후보

다음 후보는 이번 PR에서 기존 C-ID의 정의로 흡수하지 않는다.

- `X-CH05-002`, `X-CH05-015` — textual preservation·PackRef와 occurrence record의 관계: `C0004` 및 record cluster에서 후속 판정
- `X-CH05-030~031` — input admission과 positive evidence path 공백: evidence / claim-support cluster로 보류
- `X-CH05-035~036` — Decision·ActionOut·actual occurrence·world outcome·record 분리: performed-action / outcome cluster로 보류
- `X-CH05-003~017`, `X-CH05-032~034`의 순수 registry·socket·integrity 책임: 인간 concept로 자동 승격하지 않고 ENGINE-ONLY 또는 HISTORICAL-ONLY 판정 대상으로 보류

## 이번 배치의 판정 요약

```text
기존 C-ID 갱신: C0005, C0006, C0009
새 C-ID: 없음
MERGE: 없음
HISTORICAL-ONLY: 다음 cluster에서 판정
ENGINE-ONLY: 다음 cluster에서 판정
보류: evidence, performed action/outcome, registry/socket/integrity cluster
```
