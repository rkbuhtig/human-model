# Dynamics v0.1 — Scenario and Stress Report

> **지위:** simulation contract test  
> **실행일:** 2026-07-12  
> **환경:** Python 3.12.13, Linux 6.12.47 x86_64  
> **seed:** `20260712`  
> **경험적 인간 정리:** 아님

## 1. 검사 대상

이 실행은 실제 인간의 감정이나 행동을 예측하는 정확도 시험이 아니다. 다음 구조적 질문만 검사했다.

1. 숨은 세계 정답이 인간 런타임으로 새는가.
2. 느낌·Stake·반복이 EvidenceLink로 세탁되는가.
3. Candidate·Intent·Attempt·Performance·ActionOccurrence가 분리되는가.
4. declared independence 반복, exact duplicate, payload collision이 구분되는가.
5. 부하 아래에서 입력 손실과 권한 위반이 명시적으로 기록되는가.
6. 회복 입력이 도달하고도 상태가 완전 리셋되거나 경계값에 고착되는가.

## 2. 자동 테스트

```text
25 tests
25 passed
0 failed
```

포함된 주요 대조는 다음과 같다.

- `busy / avoiding` 세계가 같은 관측을 내는 구간에서는 동일 궤적, 다른 관측이 도착한 뒤에는 다른 궤적을 만드는지 검사
- 관계 Stake와 rejection history가 routing만 바꾸고 evidence digest는 보존하는지 검사
- action capacity만 차단했을 때 prior route는 같고 PerformanceReceipt와 downstream ActionOccurrence가 함께 사라지는지 검사
- 같은 declared independence group의 소문 30회가 support mass 30배로 세탁되지 않는지 검사
- 내부 거절 시뮬레이션 40회가 EvidenceLink를 만들지 않는지 검사
- arbitrary observation→claim grounding 위조와 forged EvidenceLink를 producer·validator 양쪽에서 거부하는지 검사
- 서로 다른 scope의 근거가 합쳐지지 않는지 검사
- 한 사건과 같은 tick의 support·contradiction이 순서로 히스테리시스를 세탁하지 않는지 검사
- exact duplicate는 멱등 처리하고 같은 ID의 다른 payload는 HARD collision으로 격리하는지 검사
- imagination이 action window를 위조하지 못하는지 검사
- JSON 문자열 `"false"`를 boolean으로 오인하지 않는지 검사
- 무사건 실행도 초기 상태 invariant를 검사하는지 확인
- 큐 overflow가 `processed + dropped + unresolved`로 회계되는지 검사

## 3. `delayed_reply` 기준 실행

10개 사건을 모두 처리했고 HARD invariant 위반은 없었다.

### 결정 시점

| 후보 | call probability |
|---|---:|
| wait | 0.276646 |
| ask | 0.282993 |
| accuse | 0.130661 |
| withdraw | 0.106963 |
| recheck | 0.129649 |
| ruminate | 0.073089 |

현재 임의 계수에서는 `ask`가 선택됐고 BodyAuthorization을 통과해 실제 수행으로 기록됐다. 이것은 인간 행동에 대한 정답이 아니라 `EXPLORATORY` 출력이다.

### claim 경로

```text
C3 counterpart intentionally avoids
support mass       = 0.20
contradiction mass = 0.80
final confidence   = 0.166667
stance             = held

C7 schedule conflict existed
final confidence   = 0.818182
stance             = adopted

C8 busy was actual cause
final confidence   = 0.733333
stance             = held
```

친구의 해석은 `C3`에 약한 testimony link만 만들었다. 내부 거절 시뮬레이션은 `C4` evidence를 만들지 않았다. 상대의 설명은 “바빴다고 말했다”와 “바쁨이 실제 원인이었다”를 분리한다. 독립 일정 기록은 `C7`의 일정 충돌만 확정하며, 실제 원인인 `C8`은 testimony만으로 문턱 아래에 남았다.

```text
authority leaks = 0
invariant errors = 0
peak distress = 0.400583
final residual distress = 0.193617
```

반증·설명 입력 이후에도 정서 잔여가 즉시 0이 되지 않았다.

## 4. 다축 부하 sweep

기본 정책은 evidence strength와 무관한 `priority ingress`다.

| preset | generated | processed | dropped | unresolved | recovery drop | post-recovery stress | recovery status | HARD |
|---|---:|---:|---:|---:|---:|---:|---|---|
| baseline | 120 | 120 | 0 | 0 | 0.176271 | 0 | passed_nonreset | PASS |
| ambiguity_stake | 469 | 340 | 0 | 129 | 0.582468 | 61 | passed_nonreset | PASS |
| fatigue_pressure | 498 | 255 | 68 | 175 | 0.586209 | 61 | passed_nonreset | PASS |
| conflict_interference | 781 | 335 | 273 | 173 | 0.558811 | 61 | passed_nonreset | PASS |
| combined | 2,656 | 615 | 1,866 | 175 | 0.663412 | 61 | passed_nonreset | PASS |
| soak | 31,331 | 5,304 | 25,990 | 37 | 0.711005 | 161 | passed_nonreset | PASS |

모든 행에서:

```text
AuthorityLeakCount = 0
PhantomActionCount = 0
ProvenanceLossCount = 0
InvariantErrorCount = 0
InputAccounting = exact
```

`HARD PASS`는 인간적으로 바람직한 행동이나 회복을 뜻하지 않는다. 타입 안전성과 입력 회계가 보존됐다는 뜻이다.

또한 현재 `AuthorityLeakCount`는 구현된 내부 인식 권한 경계의 위반을 센다. EvidenceLink 없는 factual stance 채택뿐 아니라 등록되지 않은 grounding rule, 잘못된 ground 집합·강도·scope도 포함한다. 외부 `Warrant / AuthorityGrant / AppliedRecord` 전이는 v0.1에 아직 없으므로 전체 권한 체계를 통과했다는 뜻이 아니다.

## 5. 첫 실패 — FIFO recovery starvation

초기 FIFO 큐에서는 복합 부하 뒤의 직접 확인·휴식·관계 수리 사건이 오래된 모호 입력 뒤에 갇혔다.

| policy | processed | dropped | unresolved | recovery delivery | recovery drop | status | HARD |
|---|---:|---:|---:|---:|---:|---|---|
| FIFO | 564 | 1,866 | 226 | 0.00 | 0.000000 | not_reached_due_to_backlog | PASS |
| priority | 615 | 1,866 | 175 | 1.00 | 0.663412 | passed_nonreset | PASS |

이 결과는 회복 연산의 실패가 아니었다. 회복 입력이 실행 경로에 도달하지 못한 access-policy failure였다.

이를 고치기 위해 `ingress_priority`를 별도 타입 필드로 추가했다. 이 값은 시나리오 작성자가 주는 access-policy 입력이며, 어떤 입력을 먼저 처리할지만 바꾼다. `EvidenceLink.strength`나 claim confidence 계산에는 들어가지 않는다. 런타임이 중요도를 스스로 추론한 결과는 아니다.

## 6. 두 번째 발견 — 회복과 backlog 재노출

초기 구현은 `AssociativeState`를 사건 한 건마다 빠른 계수로 갱신했다. 입력률을 올리자 느린 상태가 사건 밀도에 비례해 즉시 `1.0`으로 포화됐다. associative·habit·narrative 계수를 느린 규모로 낮췄지만, 실제 tick/episode 단위 update cadence는 아직 미구현이다.

첫 보고 계산은 회복 뒤의 최종 상태만 보아 `combined / soak`를 plastic lock으로 오판했다. phase-aware trace를 추가해 첫 회복 입력 직전과 마지막 회복 입력 직후의 같은 상태량을 비교하자 실제 경로는 달랐다.

```text
combined
  residual distress  0.806259 → 0.142848
  rejection access   1.000000 → 0.978775

soak
  residual distress  0.778132 → 0.067127
  rejection access   1.000000 → 0.929713
```

두 실행 모두 회복 구간에서는 경계에서 이완됐다. 그 뒤 drain이 오래된 stress backlog를 각각 61건·161건 다시 처리하며 최종 상태가 재상승했다. 따라서 현재 판정은 plastic recovery failure가 아니라 **회복 뒤 미처리 과거 입력에 대한 재노출**이다.

다음 버전에서는 다음을 비교해야 한다.

- tick별 plastic update budget
- episode-boundary update
- saturation 근처의 비선형 학습률 감소
- 안전 경험의 별도 extinction/reconsolidation 경로
- backlog 사건과 현재 사건의 plastic eligibility 분리
- stale decision·soothing·testimony의 expiry/decay/revalidation
- 회복 phase barrier와 실제 backlog 처리의 분리

아직 어느 구현도 인간의 실제 생물학적 법칙으로 채택하지 않는다.

## 7. 계산 soak

`soak`은 31,331개 입력 사건을 생성했다.

```text
processed                   = 5,304
dropped                     = 25,990
unresolved                  = 37
engine-only elapsed                     = 7.117432 s
engine-only processed events / second   = 745.213
engine-only peak traced memory          = 44.589 MiB
```

높은 손실률은 처리량 성공이 아니다. 의도적으로 제한한 attention·queue 정책이 입력을 명시적으로 포기한 결과다. 이 단일 실행의 성능 수치는 사건 생성 비용을 제외한 engine-only 측정이며, 실행 환경과 Python 구현에 종속된다. 인간 인지 용량으로 해석할 수 없다.

## 8. 현재 판정

### 통과

- hidden-world oracle isolation
- routing/evidence type firewall
- claim-specific provenance
- declared-independence repetition discount
- grounding rule producer/validator 이중 검사
- `(claim_id, scope)` 격리와 atomic adjudication
- Candidate/Intent/Attempt/Performance/ActionOccurrence 분리
- blocked action의 phantom-world-effect 차단
- append-only correction
- duplicate-event idempotence와 payload-collision 격리
- explicit overload accounting
- deterministic replay

### 실패 또는 미구현

- episode 단위의 느린 update cadence
- 오래된 backlog 사건의 expiry·decay·revalidation
- recovery 이후 backlog 재노출 정책
- partial performance
- 외부 outcome과 후속 observation의 완전한 world simulator
- memory archive·rehydration·source confusion 모델
- source reliability와 독립성 추론
- 외부 Warrant·AuthorityGrant·AppliedRecord 전이
- 다중 인간 runtime의 상호작용
- 실제 관측 자료에 대한 calibration·falsification

## 9. 결론

첫 부하 테스트에서 가장 중요한 결과는 “모델이 인간답게 행동했다”가 아니다.

> 느낌·관계 Stake·내부 반복·피로가 커져도 외부 사실 권한으로 직접 새지 않았고, 수행되지 않은 행동이 세계 사건으로 기록되지 않았다.

동시에 부하는 세 개의 구조 문제를 드러냈다.

```text
FIFO access starvation
event-density-dependent plastic update
recovery와 backlog 재노출을 섞은 test oracle
```

첫 결함은 evidence와 분리된 ingress priority로 완화했다. 두 번째는 느린 계수로 급한 포화만 낮췄지만 실제 slow clock은 남았다. 세 번째는 phase-aware snapshot과 `post_recovery_stress_processed`로 분리했다. 따라서 v0.1을 완성된 인간 동역학으로 승격하지 않는다.
