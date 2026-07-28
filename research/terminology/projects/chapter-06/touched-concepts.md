# Chapter 06 — Touched Concepts

이 문서는 Chapter 06 배치가 concept 분석에서 갱신한 C-ID와, C-ID를 열지 않은 인접 후보의 관계·목적지를 기록한다. 정의는 `termbase/concepts/`, 후보 설명은 `extraction-map.md`, 형제 비교는 `termbase/clusters/`가 소유한다.

## 갱신한 concept

### C0001 — 행동 경로 선택

- 사용한 후보: `X-CH06-010~014`, `X-CH06-034`, `X-CH06-036`
- 판정:
  - C0001 KEEP 유지.
  - `StrategyAdoption MERGE → C0001`은 철회한다.
  - 관계: `StrategyAdoption NARROWER-OR-RELATED-CANDIDATE-OF C0001`, 상태 `HOLD`.
  - configuration Receipt는 ENGINE-ONLY 설정 기록이다.
- 조화: `../../termbase/harmonization/H0003.md`

### C0002 — 외부 occurrence

- 사용한 후보: `X-CH06-034`, `X-CH06-036`
- 판정:
  - C0002 KEEP 유지.
  - `PerformedAction MERGE → C0002`는 철회한다.
  - 관계: `PerformedAction NARROWER-CANDIDATE-OF C0002`, 상태 `HOLD`.
  - ActionOut·body permission·configuration Receipt는 occurrence가 아니다.
- cluster: `../../termbase/clusters/CL0003-action-outcome.md`

### C0003 — 결과 상태 후보군

- 사용한 후보: `X-CH06-036`
- 판정 변화: `KEEP → HOLD`
- 이유:
  - ExternalOutcome, relational outcome, settlement status, observed outcome의 경계가 닫히지 않았다.
  - `ExternalOutcome MERGE → C0003`은 철회한다.
- cluster: `../../termbase/clusters/CL0003-action-outcome.md`

### C0004 — occurrence record

- 사용한 후보: `X-CH06-012~014`, `X-CH06-034`, `X-CH06-036`
- 판정:
  - C0004 KEEP 유지.
  - `performed-action record MERGE → C0004`는 철회한다.
  - 관계: `performed-action record NARROWER-CANDIDATE-OF C0004`, 상태 `HOLD`.
  - configuration Receipt는 occurrence record가 아니다.
- 조화: `../../termbase/harmonization/H0003.md`

### C0005 — 현재 체험 표면

- 사용한 후보: `X-CH06-004~006`, `X-CH06-008`
- 코퍼스 확인 대비:
  - 통증을 느꼈다 ≠ 조직 손상이 있었다 ≠ 통증이 있다고 말했다
  - 체감이 줄었다 ≠ 실제 수리·잔여·lock·margin이 개선됐다
- 판정: KEEP 유지.

### C0006 — 비권위적 인과 영향

- 사용한 후보: `X-CH06-029~033`, `X-CH06-037~038`
- 유지한 경계:
  - 체험·서사의 인과 영향과 Grounds·writer authority를 분리한다.
  - next-tick은 역사적 안전장치이지 concept의 필수 지연이 아니다.
- 조화: `../../termbase/harmonization/H0001.md`

### C0007 — 수행 활동 후보군

- 사용한 후보: `X-CH06-001`, `X-CH06-019`, `X-CH06-034~036`
- 판정 변화: `KEEP → HOLD`
- 확인된 경계:
  - 수리가 요구됨 ≠ 수리 활동이 수행됨
  - 전략 설정·Receipt 발행 ≠ 활동 수행
  - 활동 수행 ≠ 결과 성공 ≠ 자원 지출
- 보류 이유:
  - 탐색·비교·재표현·수리가 generic relation인지 과정의 partitive relation인지 미확정이다.
- cluster: `../../termbase/clusters/CL0004-work-accounting-cardinality.md`

### C0008 — 실제 자원 지출

- 사용한 후보: `X-CH06-001`, `X-CH06-002`, `X-CH06-008`, `X-CH06-026`
- 코퍼스 확인 대비:
  - 체감 부담 감소 ≠ 실제 자원 소비 감소
  - 수리 활동 수행 ≠ 그 활동에 든 자원 지출
  - 운영 비용 ≠ schema-relative raw 판정량
- 판정: KEEP 유지.

### C0009 — 수행·지출·provenance 기록 후보군

- 사용한 후보: `X-CH06-012~014`, `X-CH06-018`, `X-CH06-025~026`, `X-CH06-031`, `X-CH06-034`, `X-CH06-036`
- 판정 변화: `ENGINE-ONLY → HOLD / SUBJECT-FIELD SPLIT`
- 이유:
  - work-performance record, work-quantity record, expenditure record, dependency trace, attribution record의 표상 대상이 다르다.
  - configuration Receipt, performed-action record, Bill obligation, realized consequence와도 동일하지 않다.
- cluster: `../../termbase/clusters/CL0004-work-accounting-cardinality.md`

## 기술·역사 역할

### ENGINE-ONLY

- configuration Receipt 계열
  - `Receipt`, `PledgeFn`, `AttachMeta`, `Receipt-only`, `PayloadFirewall`, `pledge_t`, `pledge_{t-1}`, `pledge_next`
- `ActionOut`

### HISTORICAL-ONLY

- `pledge`

### HOLD

- `StrategyAdoption` — C0001 NARROWER/RELATED 후보
- `PerformedAction` — C0002 NARROWER 후보
- `ExternalOutcome` — C0003 RELATED/NARROWER 후보
- performed-action record — C0004 NARROWER 후보
- `BodyAuthorization`, `dm_phys / Damage`
- outcome observation / outcome receipt

## 후속 cluster

### Evidence / observation / claim support

- `X-CH06-004~007`, `X-CH06-021~028`
- outcome observation / outcome receipt

### Unresolved state / repair / obligation / settlement

- `X-CH06-015~020`, `X-CH06-040~042`
- full typed Obligation relation: HOLD
- universal Receipt→σ→Bill: HISTORICAL-ONLY 후보

### Body authorization / execution / recovery

- `X-CH06-035~036`
- permission·veto·motor execution·pain·recovery 관계: HOLD

## 판정 요약

```text
C0001: KEEP; StrategyAdoption HOLD relation candidate
C0002: KEEP; PerformedAction HOLD narrower candidate
C0003: KEEP 철회 → HOLD
C0004: KEEP; performed-action record HOLD narrower candidate
C0005: KEEP
C0006: KEEP
C0007: KEEP 철회 → HOLD
C0008: KEEP
C0009: ENGINE-ONLY 철회 → HOLD / SUBJECT-FIELD SPLIT
MERGE: 없음
ENGINE-ONLY: configuration Receipt 계열, ActionOut
HISTORICAL-ONLY: pledge
새 C-ID: 없음
```
