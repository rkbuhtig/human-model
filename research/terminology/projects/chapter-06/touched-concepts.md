# Chapter 06 — Touched Concepts

이 문서는 Chapter 06 배치가 실제 concept 분석에서 갱신한 C-ID와, 아직 C-ID를 열지 않은 인접 후보의 목적지를 기록한다. 정의와 후보 설명은 각각 `termbase/concepts/`와 `extraction-map.md`가 소유한다.

## 갱신한 concept

### C0001 — 행동 경로 선택

- 사용한 후보:
  - `X-CH06-010~014` — pledge와 strategy configuration Receipt 역할 이동
  - `X-CH06-034` — configuration Receipt가 ActionOut보다 먼저 생성됨
  - `X-CH06-036` — Choice·StrategyAdoption·ActionOut·PerformedAction 분리 요구
- 판정:
  - 경로·전략이 수행 대상으로 채택되는 `StrategyAdoption` 역할은 `MERGE → C0001`이다.
  - configuration Receipt는 선택된 설정의 기술 기록이며 C0001이 아니다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0001.md`

### C0002 — 외부 발생

- 사용한 후보:
  - `X-CH06-034` — Receipt·ActionOut이 실제 수행을 보증하지 못함
  - `X-CH06-036` — PerformedAction이 별도 실제 occurrence 단계로 요구됨
- 판정:
  - 외부에서 실제 수행된 행동 occurrence는 `MERGE → C0002`다.
  - `ActionOut`, body permission, strategy Receipt는 occurrence 자체가 아니다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0002.md`

### C0003 — 세계 결과 상태

- 사용한 후보:
  - `X-CH06-036` — ExternalOutcome과 observed outcome 분리 요구
- 판정:
  - 선행 performed action 뒤 세계·관계가 이른 `ExternalOutcome`은 `MERGE → C0003`이다.
  - outcome observation·outcome receipt는 결과 상태와 별도로 보류한다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0003.md`

### C0004 — occurrence record

- 사용한 후보:
  - `X-CH06-012~014` — configuration Receipt와 저장 경로
  - `X-CH06-034` — Receipt가 실제 수행보다 먼저 발행됨
  - `X-CH06-036` — performed-action record와 outcome observation 분리 요구
- 판정:
  - 실제 performed action occurrence의 성립을 표상하는 기록은 `MERGE → C0004`다.
  - Chapter 06의 configuration Receipt는 수행 전 payload이므로 C0004가 아니다.
- 경계 조화: `../../termbase/harmonization/H0002.md`
- 상세 판정: `../../termbase/concepts/C0004.md`

### C0005 — 현재 체험 표면

- 사용한 후보:
  - `X-CH06-004` — 판정용 입구와 체험·대응용 입구 분리
  - `X-CH06-005` — Witness를 truth가 아닌 schema-relative trace bundle로 낮춘 교정
  - `X-CH06-006` — raw residual과 experienced residual 분리
  - `X-CH06-008` — 현재 체감 완화와 실제 잔여 개선 분리
- 제공한 코퍼스 확인 대비:
  - “나는 통증을 느꼈다” ≠ “조직 손상이 있었다” ≠ “나는 통증이 있다고 말했다”
  - 체감이 줄었다 ≠ 실제 수리·잔여·lock·margin이 개선됐다
- 상세 판정: `../../termbase/concepts/C0005.md`

### C0006 — 비권위적 인과 영향

- 사용한 후보:
  - `X-CH06-029` — View가 policy를 통해 Grounds를 오염시키는 slow-doping 문제
  - `X-CH06-030` — bounded `CtrlCtx`
  - `X-CH06-031` — Grounds digest를 Control handle로 포장한 hidden path
  - `X-CH06-032` — 등록된 `Raw→View` 단방향 요약 교정
  - `X-CH06-033` — Grounds와 Influence의 명시 분리
  - `X-CH06-037` — Grounds·Control Influence·Accounting Imprint scope 충돌
  - `X-CH06-038` — same-commit 금지의 정확한 범위
- 제공한 코퍼스 확인 대비:
  - 체험·서사·감정이 주의·휴식·거리두기·도움 요청을 바꿀 수 있음 ≠ 외부 사실의 Grounds가 됨
  - 즉시 가역 반응 ≠ 같은 irreversible commit의 Grounds·writer 역류
- 판정 변화:
  - `next-tick`을 필수 특성에서 역사적 구현 조건으로 낮춘다.
  - concept의 중심을 `비권위적 미래 편성 영향`에서 `비권위적 인과 영향`으로 넓힌다.
- 경계 교정 기록: `../../termbase/harmonization/H0001.md`
- 상세 판정: `../../termbase/concepts/C0006.md`

### C0007 — 실제 탐색·비교 노동

- 사용한 후보:
  - `X-CH06-001` — 감당 요구·실제 수리·체감 완화 분리
  - `X-CH06-019` — 현재 raw repair와 과거 부담 settlement 분리
  - `X-CH06-034` — strategy Receipt가 ActionOut보다 먼저 생성됨
  - `X-CH06-035` — body authorization·veto·execution state 부재
  - `X-CH06-036` — Choice·StrategyAdoption·PerformedAction·Outcome 분리 요구
- 제공한 코퍼스 확인 대비:
  - 수리가 요구됨 ≠ 수리 노동이 수행됨
  - 전략이 설정됨·Receipt가 발행됨 ≠ 행동이 수행됨
  - 노동이 수행됨 ≠ 의도한 결과가 발생함
- 추가 판정:
  - 외부 performed action의 사건 성립 역할은 C0002에 병합한다.
  - C0007은 탐색·비교·수리라는 수행 내용과 노동 여부를 별도 축으로 유지한다.
- 상세 판정: `../../termbase/concepts/C0007.md`

### C0008 — 실제 자원 지출

- 사용한 후보:
  - `X-CH06-001` — 감당 요구·실제 수리·체감 완화 분리
  - `X-CH06-002` — 현재 전망 완화 차액의 별도 계상 시도
  - `X-CH06-008` — CosmeticRelief와 TrueRelief
  - `X-CH06-026` — 운영 비용과 raw 판정량의 LedgerCore 재혼합
- 제공한 코퍼스 확인 대비:
  - 현재 체감 부담 감소 ≠ 실제 자원 소비 감소
  - 실제 수리 수행 ≠ 그 수행에 든 자원 지출
  - 운영 비용 ≠ schema-relative raw 판정량
- 상세 판정: `../../termbase/concepts/C0008.md`

### C0009 — 수행·지출 회계 기록

- 사용한 후보:
  - `X-CH06-012` — strategy knob configuration 기반 Receipt auto-mint
  - `X-CH06-013` — Receipt-only payload firewall
  - `X-CH06-018` — Bill의 청구·후과·line-item 과적재
  - `X-CH06-025~026` — core별 read-cap과 LedgerCore 역할 혼합
  - `X-CH06-031` — Grounds digest를 Control handle로 포장한 경로
  - `X-CH06-034` — Receipt가 실제 수행보다 먼저 발행됨
  - `X-CH06-036` — performed action·external outcome·관측 결과 분리
- 반영한 경계:
  - configuration Receipt는 수행·지출 회계 기록이나 performed-action record가 아니다.
  - action occurrence record는 C0004다.
  - Bill line item, obligation, realized consequence, evidence는 C0009와 자동 병합하지 않는다.
- 상세 판정: `../../termbase/concepts/C0009.md`

## 판정된 기술·역사 역할

### ENGINE-ONLY

- `X-CH06-012~014`의 configuration Receipt 계열
  - `Receipt`, `PledgeFn`, `AttachMeta`, `Receipt-only`, `PayloadFirewall`, `pledge_t`, `pledge_{t-1}`, `pledge_next`
  - strategy knob 설정과 저장·접근을 다루는 기술 계약이다.
  - actual performance·resource expenditure·external outcome·obligation을 보증하지 않는다.
- `X-CH06-034~036`의 `ActionOut`
  - 선택된 결정을 외부 실행기로 전달하는 출력이며 actual occurrence가 아니다.

### HISTORICAL-ONLY

- `pledge`
  - 미래 자기서약과 controller strategy payload를 한 철자로 가리킨 역할 이동을 보존한다.
  - 현재 인간 concept 명칭으로 채택하지 않는다.

### 보류

- `X-CH06-035~036`의 `BodyAuthorization`
  - permission·veto·motor execution의 독립 긍정 근거가 부족하다.
- `X-CH06-035`의 `dm_phys / Damage`
  - body·repair demand cluster에서 `UnmetRepairDemand` 재명명과 독립 concept 여부를 판단한다.
- `X-CH06-036`의 outcome observation / outcome receipt
  - outcome state, observation artifact, record, claim support의 경계가 닫히지 않았다.

## 후속 cluster로 남긴 후보

### Evidence / observation / claim support

- `X-CH06-004~007`
- `X-CH06-021~028`
- outcome observation / outcome receipt
- 목적지: Witness trace, admissibility, observation artifact, claim-specific support, certification, warrant 비교

### Unresolved state / repair / obligation / settlement

- `X-CH06-015~020`
- `X-CH06-040~042`
- 현재 판정:
  - `X-CH06-041` Conn→Imprint: `SIDE BRANCH / HOLD`
  - universal Receipt→σ→Bill: HISTORICAL-ONLY 후보
  - full typed Obligation relation: 원문 완성 타입이 아니므로 `보류`

### Body authorization / execution / recovery

- `X-CH06-035~036`
- 목적지: body permission, veto, motor execution, pain, recovery, unmet repair demand cluster
- 현재 판정: 긍정 근거 부족으로 `보류`

## 이번 배치의 판정 요약

```text
기존 C-ID 갱신: C0001~C0009
새 C-ID: 없음
경계 교정: C0006 → H0001
역할 조화: action/outcome chain → H0002
MERGE: StrategyAdoption→C0001, PerformedAction→C0002, ExternalOutcome→C0003, performed-action record→C0004
ENGINE-ONLY: configuration Receipt 계열, ActionOut
HISTORICAL-ONLY: pledge
보류: BodyAuthorization, dm_phys/Damage, outcome observation/receipt, evidence, obligation
```
