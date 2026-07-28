# CL0003 — 선택·수행·결과·기록

## cluster 질문

Chapter 05·06의 실행 사슬에 나열된 역할은 서로 같은 concept인가, generic 관계인가, partitive 관계인가, associative 관계인가?

이 파일은 PR #44에서 결과만 기록했던 세 번째 cluster를 사후 복구하고, 당시 `MERGE`가 synonymy가 아니라 상·하위 또는 연관 관계에 사용된 오류를 교정한다.

## 입력 후보

- `X-CH05-033` — Decision·ActionOut·actual occurrence·world outcome·receipt 공백
- `X-CH06-010~014` — pledge·strategy configuration Receipt
- `X-CH06-034` — configuration Receipt가 ActionOut보다 먼저 생성됨
- `X-CH06-035` — body authorization·veto·execution state 부재
- `X-CH06-036` — Choice·StrategyAdoption·ActionOut·PerformedAction·ExternalOutcome·관측 결과 분리 요구
- `C0001` — 행동 경로 선택
- `C0002` — 외부 occurrence
- `C0003` — 결과 상태 후보
- `C0004` — occurrence record

## 형제 후보

```text
행동 경로 선택
장기 전략 채택
strategy configuration record
ActionOut
body authorization
performed action
external outcome
outcome observation
performed-action record
outcome record
```

## 관계 분석

### 행동 경로 선택 / StrategyAdoption

- 공통점: 이후 수행과 관련된 경로 또는 전략을 채택한다.
- 미확정 차이: 선택 대상의 크기, 지속 시간, 철회 조건, 하위 행동과의 관계.
- 현재 관계: `StrategyAdoption NARROWER-OR-RELATED-CANDIDATE-OF C0001`.
- 판정: `HOLD`.
- 이전 `MERGE → C0001`은 synonymy 근거가 없으므로 철회한다.

### 외부 occurrence / PerformedAction

- `C0002`는 행동·자극·상호작용 등 외부에서 실제 성립한 occurrence의 유개념 후보다.
- `PerformedAction`은 행위자가 수행한 행동 occurrence라는 추가 차별 특성을 가질 가능성이 있다.
- 현재 관계: `PerformedAction NARROWER-CANDIDATE-OF C0002`.
- 판정: `HOLD`.
- 실제 외부 행동이 occurrence이기도 하다는 사실은 동일 concept를 뜻하지 않는다.

### occurrence record / performed-action record

- `C0004`는 특정 occurrence의 성립을 보존한 표상이다.
- performed-action record는 기록 대상이 performed action으로 제한된 종개념 후보다.
- 현재 관계: `performed-action record NARROWER-CANDIDATE-OF C0004`.
- 판정: `HOLD`.
- C0004 정의 안의 “포함할 수 있다” 외연 절은 제거하고 관계 절로 이동한다.

### 결과 상태 / ExternalOutcome

- Chapter 06은 performed action 뒤의 external outcome을 요구한다.
- 현재 C0003은 일반 세계 상태, 관계 상태, 후속 가능성, 미결·정산 상태를 함께 열거한다.
- `ExternalOutcome`이 C0003과 synonym인지, 특정 종개념인지, 별도 realized outcome인지 확인되지 않았다.
- 현재 관계: `ExternalOutcome RELATED-OR-NARROWER-CANDIDATE-OF C0003`.
- 판정: C0003과 ExternalOutcome 모두 `HOLD`.

### ActionOut / configuration Receipt

- 실제 인간 occurrence나 결과가 아니라 runtime 명령·설정 기록이다.
- 판정: `ENGINE-ONLY` 유지.
- ActionOut과 Receipt는 서로도 동일하지 않다.

### body authorization / outcome observation

- 긍정 정의와 형제 대비가 부족하다.
- 판정: `HOLD` 유지.

## generic / partitive / associative 질문

| 후보 쌍 | generic 질문 | partitive 질문 | associative 질문 | 현재 상태 |
|---|---|---|---|---|
| C0001 / StrategyAdoption | 전략 채택이 행동 경로 선택의 종인가 | 장기 전략이 선택 과정의 한 단계인가 | 전략 채택이 개별 선택을 제약하는가 | HOLD |
| C0002 / PerformedAction | 수행 행동이 외부 occurrence의 종인가 | 수행이 occurrence 성립 과정의 부분인가 | 내부 motor execution이 외부 occurrence를 산출하는가 | HOLD |
| C0004 / performed-action record | action record가 occurrence record의 종인가 | action record가 더 큰 audit record의 부분인가 | performed action이 record 발행을 촉발하는가 | HOLD |
| C0003 / ExternalOutcome | external outcome이 결과 상태의 종인가 | 결과 상태가 outcome lifecycle의 부분인가 | occurrence가 outcome을 발생시키는가 | HOLD |

## definition gate

- C0002의 `포함할 수 있다`와 `본질·범위`: 외연을 특성표에 넣은 오류.
- C0003의 `세계·관계·후속 가능성` 및 `미결 상태`: 복수 축 접속 의심.
- C0004의 `action receipt는 이 범위에 포함할 수 있다`: 외연 확장절.

C0002·C0004는 상위 concept로 유지 가능하므로 외연 절만 관계로 이동한다. C0003은 단일 genus + differentia로 재작성되지 않아 HOLD한다.

## 코퍼스 대비

현재 코퍼스는 다음 경계를 지지한다.

```text
선택됨
≠ 명령이 출력됨
≠ 실제 행동이 수행됨
≠ 세계 결과가 생김
≠ 결과가 관측됨
≠ 기록이 발행됨
```

그러나 이 대비만으로 `PerformedAction`, `ExternalOutcome`, `performed-action record`가 각각 상위 concept와 synonym인지 종개념인지 확정할 수 없다.

## 판정 요약

| 후보 | 판정 | 관계·목적지 |
|---|---|---|
| Decision 역할 | C0001 연결 유지 | 실제 동일성은 후보별 확인 |
| StrategyAdoption | HOLD | C0001 NARROWER/RELATED 후보 |
| ActionOut | ENGINE-ONLY | runtime output |
| configuration Receipt | ENGINE-ONLY | runtime configuration record |
| PerformedAction | HOLD | C0002 NARROWER 후보 |
| ExternalOutcome | HOLD | C0003 RELATED/NARROWER 후보 |
| performed-action record | HOLD | C0004 NARROWER 후보 |
| BodyAuthorization | HOLD | body cluster |
| outcome observation / record | HOLD | evidence·observation cluster |
| pledge | HISTORICAL-ONLY | 역할 이동 명칭 |

## 재개 조건

- StrategyAdoption과 단일 행동 경로 선택의 시간 범위·철회 조건 대비
- generic occurrence와 performed action을 가르는 긍정 사례
- performed-action record만의 추가 차별 특성
- realized outcome, relational outcome, settlement status, epistemic outcome status의 분리 사례

## 역참조

- `../harmonization/H0002.md`
- `../harmonization/H0003.md`
- `../concepts/C0001.md`
- `../concepts/C0002.md`
- `../concepts/C0003.md`
- `../concepts/C0004.md`
- `../../projects/chapter-05/touched-concepts.md`
- `../../projects/chapter-06/touched-concepts.md`
