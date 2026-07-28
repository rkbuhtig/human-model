# Chapter 06 Terminology Intake — Basic Term List

이 문서는 Chapter 06의 역사적 명칭과 기호에서 `extraction-map.md`의 후보 항목으로 들어가는 색인이다. 후보의 정의나 설명을 복제하지 않는다.

| 역사적 명칭 | 관찰된 역할 | 추출 항목 | concept ID | 다음 확인 |
|---|---|---|---|---|
| Pressure | 예상 수리 요구와 현재 여유의 충돌 | X-CH06-001 | 미할당 | burden readout·repair demand와 구분 |
| Repair | 이미 생긴 불일치를 복구하는 실제 작동 | X-CH06-001 / X-CH06-019 | 보류 | C0007 후보군에서 generic·partitive 관계 확인 |
| Relief | 현재 느끼고 대응하는 부담 감소 | X-CH06-001 / X-CH06-008 | 미할당 | actual repair와 구분 |
| RiskCarry | 현재 전망 완화의 차액을 동일 tick에 계상 | X-CH06-002 | 미할당 | persistent σ와 자동 동일시 금지 |
| Witness / Control / Storage / Bill | 판정·조절·지속·청구의 네 층 | X-CH06-003 | 미할당 | 전역 schema로 승격 금지 |
| GateRaw | 외부 접촉을 판정 후보 입력으로 허용 | X-CH06-004 / X-CH06-024 | 미할당 | evidence certification과 구분 |
| RawIn | policy 비개입 판정 후보 입력 | X-CH06-004 | 미할당 | organismal raw·Witness와 구분 |
| RawSlice | gate·schema를 통과한 판정 조각 | X-CH06-004 / X-CH06-022 | 미할당 | ontological raw와 구분 |
| TR / TR_perc | RawIn을 policy-shaped PercIn으로 변환 | X-CH06-004 / X-CH06-024 | 미할당 | observation·experience construction과 구분 |
| PercIn | 체험·대응용 policy-shaped input | X-CH06-004 / X-CH06-024 | 미할당 | C0005·external occurrence와 구분 |
| Witness | 초기 반박 불가능한 흔적 또는 후기 trace bundle | X-CH06-005 | 미할당 | Truth·EvidenceLink·Warrant와 구분 |
| `Π_wit` | Witness 쪽 state projection | X-CH06-005 / X-CH06-021 | 미할당 | schema-relative admissibility 확인 |
| `ΔQ⊥_raw` | Witness/coverage 기반 판정 residual | X-CH06-006 / X-CH06-022 | 미할당 | complete world residual로 해석 금지 |
| `ΔQ⊥_eff` | policy·표현·주의를 통과한 체감 residual | X-CH06-006 | 미할당 | phenomenal burden·actual repair 경계 |
| Coverage_wit | 판정용 관측 도달 범위 | X-CH06-007 | 미할당 | observation coverage와 구분 |
| Coverage_view | 현재 체험·대응의 처리 범위 | X-CH06-007 | 미할당 | persistent CovState와 구분 |
| CosmeticRelief | raw를 줄이지 않은 현재 체감 완화 | X-CH06-008 / X-CH06-040 | 미할당 | fake change라는 규범 판정 금지 |
| TrueRelief | raw·σ·lock·margin 감소로 불린 완화 | X-CH06-008 / X-CH06-019 | 미할당 | 서로 다른 감소 경로 재분해 |
| ForecastBase | policy 표현 전 전망 기준 | X-CH06-009 | 미할당 | world truth와 구분 |
| ForecastCosmetic | 표현·주의를 거친 현재 전망 | X-CH06-009 | 미할당 | current regulation과 구분 |
| cosmetic delta | base와 cosmetic forecast 차액 | X-CH06-009 / X-CH06-012 | 미할당 | burden transfer evidence 여부 확인 |
| pledge | 미래 이월 자기서약 또는 controller strategy 명세 | X-CH06-010 / X-CH06-012 | HISTORICAL-ONLY | 인간 약속·의도 concept로 자동 승격 금지 |
| obs_gain | 즉시 완화와 초기 σ 법칙에 관여한 knob | X-CH06-011 | 미할당 | Bill rule 조작 누수 확인 |
| policy-free Bill | 현재 policy가 청구 법칙을 바꾸지 못함 | X-CH06-011 | 미할당 | obligation law·runtime coefficient 구분 |
| Receipt | strategy knob configuration 자동 기록 | X-CH06-012 / X-CH06-013 / X-CH06-034 | ENGINE-ONLY | performed action receipt와 구분 |
| `Receipt(=pledge payload)` | pledge의 실행판 별칭 | X-CH06-012 | ENGINE-ONLY | 실제 수행·결과를 보증하지 않음 |
| PledgeFn | 허용 knob에서 Receipt를 자동 산출 | X-CH06-012 | ENGINE-ONLY | controller configuration operation |
| AttachMeta | pledge/Receipt를 단일 원천으로 mint | X-CH06-012 | ENGINE-ONLY | action outcome 전 발행 문제 |
| Receipt-only | Receipt payload의 Store 전용 사용 | X-CH06-013 | ENGINE-ONLY | evidence·Bill direct read 금지 |
| PayloadFirewall | core별 payload read-cap 제한 | X-CH06-013 / X-CH06-025 | ENGINE-ONLY | record existence와 authority 구분 |
| `pledge_t` | STG1의 stored pledge 표기 | X-CH06-014 | ENGINE-ONLY | production tick 규약 확인 |
| `pledge_{t-1}` | STG2의 이전 tick stored pledge 표기 | X-CH06-014 | ENGINE-ONLY | double-delay 가능성 확인 |
| `pledge_next` | 현재 knob에서 mint된 다음 payload | X-CH06-014 / X-CH06-034 | ENGINE-ONLY | ActionOut보다 먼저 생성됨 |
| `σ` | 미해결 응력·수리 요구의 지속 vector | X-CH06-015 / X-CH06-017 | 미할당 | obligation·backlog와 구분 |
| `σ_age` | 미해결 상태의 경로 의존 경과 요약 | X-CH06-016 | 미할당 | 단순 이자·elapsed time과 구분 |
| Store / StoreFn | Receipt를 σ 상태에 적재 | X-CH06-017 | 미할당 | record store·obligation creation 경계 |
| SigmaCore | σ update를 수행하는 runtime core | X-CH06-017 / X-CH06-025 | 미할당 | 인간 concept로 자동 승격 금지 |
| Bill | 미래 청구·실현 후과·원장 line item | X-CH06-018 | 미할당 | 세 역할 분리 필요 |
| BillIssued | 청구가 발행된 상태 | X-CH06-018 | 미할당 | consequence·settlement와 구분 |
| bill_posted | 이전 Bill의 게시·참조 상태 | X-CH06-018 / X-CH06-030 | 미할당 | influence feature와 구분 |
| raw repair | 현재 판정 residual을 실제로 줄임 | X-CH06-019 | 미할당 | σ settlement와 자동 상쇄 금지 |
| σ settlement | 이월 부담을 등록 경로로 감소 | X-CH06-019 | 미할당 | current repair와 구분 |
| PaidRepair | 후기 EXPL18의 raw/σ 재결합 표현 | X-CH06-019 | 미할당 | late regression 기록 |
| default / forgiveness / loss | σ–Bill에 압축된 서로 다른 종료 상태 | X-CH06-020 | 미할당 | typed obligation cluster로 이관 |
| WitnessSchema / WIT_SCHEMA | 판정 입력의 versioned allowlist | X-CH06-021 | 미할당 | sufficiency·truth와 구분 |
| ProjectBySchema | allowlist 기반 Witness projection | X-CH06-021 | 미할당 | subtract 방식과 교정 관계 |
| HardExclude | schema allowlist와 함께 쓰는 명시 금지 | X-CH06-021 | 미할당 | default deny와 관계 확인 |
| policy-independent raw | schema 아래 policy 비개입 입력 | X-CH06-022 | 미할당 | complete·infallible과 구분 |
| schema gap | 등록되지 않은 현상·입력 공백 | X-CH06-023 / X-CH06-028 | 미할당 | false·disproved와 구분 |
| unregistered / undefined | schema에서 정의되지 않은 상태 | X-CH06-023 | 미할당 | observation proposal 필요 |
| EvidenceCore | Witness 기반 판정 runtime core | X-CH06-025 | 미할당 | EvidenceLink 발행과 구분 |
| LedgerCore | 비용·state·raw 판정을 함께 산출한 core | X-CH06-025 / X-CH06-026 | 미할당 | operational/evidentiary 혼합 확인 |
| evidence gap | negative closure 뒤 positive issuance 부재 | X-CH06-027 | 미할당 | Chapter 05 gap과 연결 |
| positive evidence path | observation→artifact→claim support 경로 요구 | X-CH06-027 | 미할당 | 현행 타입 소급 금지 |
| schema version event | WitnessSchema 변경 사건 | X-CH06-028 | 미할당 | lawful issuance·certification 공백 |
| calibration debt | schema 변경 뒤 calibration 부담 | X-CH06-028 / X-CH06-041 | 미할당 | obligation으로 자동 cast 금지 |
| slow doping | View가 policy를 거쳐 판정을 오염시키는 의심 | X-CH06-029 | 미할당 | causal influence와 hidden grounds 구분 |
| CtrlCtx | bounded control influence context | X-CH06-030 | 미할당 | C0006·policy operation 경계 |
| CTX_SCHEMA | Control에 전달 가능한 feature 규격 | X-CH06-030 | 미할당 | meaning compression loss 확인 |
| CtrlObsHandle | Raw/Witness digest 기반 control handle | X-CH06-031 | 미할당 | hidden evidence path로 교정됨 |
| `Raw→View` summary | Grounds에서 View로의 등록된 단방향 요약 | X-CH06-032 | 미할당 | control feature·evidence summary 경계 |
| Grounds | 판정이 사실을 확정할 때 참조하는 입력 역할 | X-CH06-033 / X-CH06-037 | 미할당 | claim-specific relation·Warrant 미완성 |
| Influence | 다음 변화에 반영되도록 전달되는 입력 역할 | X-CH06-033 / X-CH06-037 | C0006 부분 대조 | control lane 전체와 자동 동일시 금지 |
| M1 | irreversible SSOT update의 Commit-only 봉인 | X-CH06-037 / X-CH06-039 | 미할당 | write capability와 normative authority 구분 |
| M2 | 등록된 Raw/Witness만 Grounds에 참여 | X-CH06-021 / X-CH06-037 | 미할당 | positive evidence issuance 미완성 |
| M3 | Receipt→σ→Bill과 settlement 경로 봉인 | X-CH06-037 / X-CH06-040 | 미할당 | accounting imprint·obligation 구분 |
| M4 | 지연·저대역 control Influence | X-CH06-030 / X-CH06-037 / X-CH06-038 | 미할당 | Receipt bus와 scope conflict |
| same-commit prohibition | 현재 surface가 같은 commit의 grounds를 역주입하지 못함 | X-CH06-038 | 미할당 | 즉시 보호 반응 전체 금지 아님 |
| Authority | 특정 Commit의 irreversible write capability | X-CH06-039 | 미할당 | phys role·normative authority와 구분 |
| universal Receipt→σ→Bill | 모든 표면 완화를 debt로 확장한 후기 규칙 | X-CH06-040 | 미할당 | ordinary regulation 제외 필요 |
| Conn | 접촉·연결 일반 | X-CH06-041 | 미할당 | causal contact·normative obligation 구분 |
| Imprint(C/R/S) | 연결이 남기는 여러 흔적 | X-CH06-041 | 미할당 | residue·cost·debt 자동 통합 금지 |
| flux × resistance | 연결 비용·담보 하한 가설 | X-CH06-041 | 미할당 | SIDE BRANCH / HOLD |
| Obligation | actor·bearer·beneficiary·scope를 가진 후속 relation 요구 | X-CH06-020 / X-CH06-042 | 미할당 | 0118 원문 완성 타입 아님 |
| ActionOut | 선택 뒤 산출되는 행동 출력 | X-CH06-034 / X-CH06-036 | ENGINE-ONLY | actual occurrence·world outcome을 보증하지 않음 |
| BodyAuthorization | 몸의 허가·veto 단계 요구 | X-CH06-035 / X-CH06-036 | 보류 | 독립 긍정 근거·형제 대비 필요 |
| dm_phys / Damage | 미충족 repair demand에 가까운 scalar | X-CH06-035 | 보류 | body·repair demand cluster에서 재명명 판단 |
| PerformedAction | 실제 수행된 행동 단계 요구 | X-CH06-034 / X-CH06-036 | 보류 | C0002 NARROWER 후보; 행위자성·완료 문턱 대비 필요 |
| ExternalOutcome | 행동 뒤 세계 결과 | X-CH06-036 | 보류 | C0003 RELATED/NARROWER 후보; realized·relational·settlement 분리 필요 |

## Chapter 05 연결 요약

| Chapter 05 후보 | Chapter 06에서 이어진 문제 |
|---|---|
| X-CH05-028 ExternalIn over-closure | X-CH06-004 Raw/Perc 이중 입구, X-CH06-021 WitnessSchema |
| X-CH05-029 policy-shaped PercIn | X-CH06-006 raw/eff residual, X-CH06-024 GateRaw/TR_perc 분리 |
| X-CH05-030 input admission ≠ evidence | X-CH06-005 Witness 교정, X-CH06-027 positive issuance gap |
| X-CH05-031 evidence port 부재 | X-CH06-021~028 admissibility contract와 남은 공백 |
| X-CH05-024/026 Decision·Record | X-CH06-012~014 configuration Receipt와 firewall |
| X-CH05-033 Decision·ActionOut·outcome 공백 | X-CH06-034~036 action execution chain 결손 |

## 사용 규칙

- 후보 설명을 바꾸려면 `extraction-map.md`만 수정한다.
- 이 표는 명칭이 어느 추출 항목을 가리켰는지만 연결한다.
- 같은 철자가 여러 행이나 여러 추출 ID에 나타나는 것은 역할 이동·과적재를 보존하기 위한 것이다.
- `Witness`, `Receipt`, `Bill`, `Grounds`, `Influence`, `Authority`는 현재 권장 명칭이나 정본 concept로 승인된 것이 아니다.
- `C0006` 연결은 Influence 역할의 부분 대조일 뿐 CON06의 전체 runtime relation을 기존 concept와 동일시하지 않는다.
- C-ID 연결과 synonymy는 다르다. generic·partitive·associative 관계 후보는 `보류`와 다음 확인을 기록한다.
- Chapter 07 이후의 용어를 이 표에 소급해 넣지 않는다.
