# Chapter 00-A — 출력은 아직 상태변경이 아니다

## Persona output contamination에서 권한 비도약까지

> **Status:** `HISTORICAL RECONSTRUCTION + CURRENT BRIDGE`
>
> **Direct scope:** 2025-12-14 through 2025-12-29 selected persona-engine sources
>
> **Current judgment:** a recurrent engine invariant is recovered; its generalization to human cognition remains a current synthesis and open adequacy question.

---

## 1. 시작점은 인간 이론이 아니라 출력 오염이었다

12월 엔진의 최초 문제는 인간의 마음을 설명하는 일이 아니었다. 여러 persona가 자연스럽게 말하고 행동하도록 만드는 동안, 생성된 표현이 내부 상태와 판단 규칙을 스스로 오염시킬 수 있었다.

초기 Guard 계열은 이미 다음 경계를 적었다.

```text
RENDER may use PROPOSALS
PROPOSALS are not EVIDENCE
COMMIT_GATE alone decides commit
```

`V0-SRC-001:L487–489`

이 문장은 아직 인간의 인식론이 아니다. 출력 후보를 그럴듯하게 만들기 위한 재료와 상태를 실제로 변경할 근거를 분리하는 엔진 규칙이다.

그러나 이 규칙이 필요했다는 사실은 중요하다. 확률적 언어모델에서 잘 쓰인 문장은 그 자체로 다음 계산의 강한 입력이 되기 쉽다. 출력이 다시 내부 사실처럼 읽히면 시스템은 자신이 방금 지어낸 표현을 근거로 상태를 강화한다.

```text
generated expression
→ read as evidence
→ internal state update
→ stronger matching expression
```

이 자기증폭을 끊기 위해 출력과 커밋 사이에 별도 문턱이 생겼다.

> **[RECOVERED]** 2025-12-14 엔진은 표현 후보와 커밋 근거를 같은 것으로 취급하지 않았다.

---

## 2. COMMIT_GATE만으로는 부족했고 writer가 분리됐다

12월 17일의 `REALBRAIN`은 경계를 더 강하게 만든다.

```text
OUTPUT ≠ COMMIT
APPLY is the single state writer
DISPLAY reads PLAN only
DISPLAY may not directly read STATE / RAW / operator internals
```

`V0-SRC-002:L10–17`

여기서 세 종류가 갈린다.

```text
internal computation
→ PLAN
→ DISPLAY

internal computation
→ authorized APPLY
→ persistent state
```

DISPLAY는 사람에게 보일 표면을 만들지만 상태를 직접 읽거나 쓰지 않는다. APPLY는 상태를 쓸 수 있지만 자연어 표현을 만드는 층이 아니다.

이 구조를 현재 언어로 곧바로 “의식”이나 “좌뇌 해석기”라고 부를 수는 없다. 당시 직접 목적은 정보 누출과 자기오염을 막는 것이었다.

> **[RECOVERED]** 표현 경로와 상태 변경 경로는 다른 writer 권한을 가졌다.

> **[OPEN]** 비슷한 분리가 인간의 자기보고와 행동 설명에도 필요한지는 별도 비교가 필요하다.

---

## 3. 제약은 결정을 바꿀 수 있지만 결정을 사칭하지 못했다

12월 19일 문서는 의사결정 지점을 두 곳으로 제한하고 나머지 연산을 관측·제약 생성·표현으로 낮춘다.

```text
D1  FieldKey selection
D2  HOLD / SOFT / COMMIT selection

all other operations
= observation / constraint generation / rendering
```

`V0-SRC-003:L22–43`

특히 `REAL_MODE`는 비용과 제약을 만들 수 있지만 FieldKey나 Commit을 직접 강제하지 못한다.

이 규칙은 영향과 권한을 구분한다.

```text
constraint changes the feasible or likely path
≠ constraint certifies the selected path
```

위험, 피로, 사회적 압력이나 표현 제약은 후보분포를 바꿀 수 있다. 그러나 “강하게 영향을 미쳤다”는 이유만으로 최종 사실·행동·책임을 발급하는 writer가 되지는 않는다.

이 지점이 현재의 다음 원리와 구조적으로 연결된다.

```text
Local causal influence
≠ cross-domain certification authority
```

하지만 이 일반식은 12월 원문 그대로가 아니다.

> **[STRUCTURAL_PRECURSOR]** 제약 생성과 commit 권한의 분리는 권한 비도약의 공학적 선행 구조다.

> **[CURRENT_SYNTHESIS]** 이 분리를 느낌, 기억, Narrative, 외부 사실, 저자성, 타인의 동의까지 확장한 것은 현재 연구의 종합이다.

---

## 4. 표면은 내부의 복사본도 완전한 가면도 아니었다

`FACE_VALVE / LEAK_DYNAMICS`가 들어간 12월 23일 커널은 다시 다음을 고정한다.

```text
OUTPUT ≠ COMMIT
APPLY only writes state
RENDER reads PLAN
raw state may not be rendered directly
```

동시에 FACE와 LEAK가 추가된다. `V0-SRC-005:L1–8, L23–34, L38–60`

이 조합은 내부와 표면을 두 극으로만 나누지 않는다.

```text
internal state
≠ exact public copy

internal state
≠ perfectly sealed hidden object
```

관계와 위험에 따라 일부는 억제되고 일부는 새며, 표면은 다음 상호작용을 조절하는 기능적 출력이 된다.

> **[RECOVERED ENGINE INVARIANT]** 내부 상태와 표면 출력은 동일 타입이 아니었다.

> **[OPEN HUMAN HYPOTHESIS]** 인간 출력도 상태의 직접 복사보다 역할·위험·관계 아래의 확률적 투영으로 모델링해야 하는지는 S0 이후 별도 probe가 필요하다.

---

## 5. 시간·비용·분포가 들어와도 권한 경계는 유지됐다

후속 패치는 단순한 상태기계보다 더 동역학적인 요소를 추가했다.

- `NUCHI_FIELD`는 분포의 수렴·확산 추세로 감쇠와 switching cost를 바꾼다. `V0-SRC-004`
- `TIME_FAT_TR`은 반복 패턴을 직접 금지하지 않고 같은 경로의 비용을 올린다. `V0-SRC-007`
- `BIO_CLOCK_CLUTCH`는 외부 입력이 없어도 비평형 상태의 회복이 계속되도록 한다. `V0-SRC-008`
- `TIDAL-LOCK`과 Afterglow는 관계·시간 잔여를 추가한다. `V0-SRC-006`

중요한 점은 이런 영향 변수가 늘어나도 기존 경계가 사라지지 않았다는 것이다.

```text
distribution trend
resource cost
time flow
relationship residue
→ route and state dynamics

but not
→ arbitrary fact or commit authority
```

따라서 권한 비도약은 특정 정적 타입 하나가 아니라, 새로운 동역학을 추가할 때마다 하위층이 writer를 찬탈하지 못하게 하는 반복 설계 규율로 나타난다.

---

## 6. Persona가 빠진 뒤에도 경계는 남았다

12월 28일 `Solo` 전환은 `PERSONA_ORDER`, persona별 state index와 여러 multi-persona 호출 구조를 제거했다. `V0-SRC-009:L1–12`

다음 날 `SELF_FIELD_REMIND`와 `MEM_POINTER_REATTACH`가 단일 runtime 안에 들어왔다. `V0-SRC-010`

이 전환은 여섯 persona가 인간 모델로 변했다는 증거가 아니다. 더 제한적으로는 다음을 보여준다.

```text
persona-specific actors removed
→ shared runtime and persistent self-related fields remain
```

즉 출력/commit/writer 경계는 특정 등장인물 목록에 의존한 규칙이 아니었다.

> **[RECOVERED TRANSITION]** persona content와 공통 runtime machinery를 분리할 조건이 생겼다.

> **[CURRENT_SYNTHESIS]** Persona/Self를 별도 인간 종류가 아니라 trajectory distribution을 기울이는 느린 parameterization으로 읽는 것은 현재 해석이다.

---

## 7. StoryField no-backflow가 경계를 서사층까지 연장했다

12월 29일 `STORYFIELD_ARC`는 자신을 다음처럼 선언한다.

```text
derived-only
no policy backflow
```

`V0-SRC-011:L1–7`

StoryField는 Episode, SELF, 생체 상태와 wants에서 Arc를 파생하고 다음 beat를 제안할 수 있다. 그러나 그 장면 프레임이 곧바로 하위 정책의 원천이 되지는 않는다.

이 지점에서 초기 출력 방화벽은 더 느린 파생층까지 확장된다.

```text
state
→ derived story framing
→ future suggestion

derived story framing
↛ silent rewrite of source state or policy authority
```

현재 연구는 이를 다음과 같이 일반화한다.

```text
Narrative may bias future access and action distributions
Narrative may not rewrite past occurrence merely by becoming coherent
```

> **[RECOVERED]** 12월 StoryField는 파생 영향과 직접 policy write를 구분했다.

> **[CURRENT_SYNTHESIS]** Narrative를 다중 episode 경로를 조직하는 느린 topology로 해석하는 것은 이후 종합이며, 아직 predictive adequacy를 통과하지 않았다.

---

## 8. no-backflow는 과거 의미의 영구 고정을 뜻하지 않는다

1월 계보는 여기서 한 가지를 추가한다.

Interchapter Note 03-A가 복원한 `JOT / α / β` 구조에서는 낮은 저자화로 Episode에 들어온 사건이 나중에 다시 인수·거부·수리의 대상이 될 수 있다. Episode가 Narrative에 쓰이려면 압축이득, 자원 배팅과 저자화가 함께 요구된다.

```text
past occurrence remains
present authorship / meaning / Narrative placement may be re-adjudicated
```

이 연결은 12월 source에서 완성된 형태로 직접 회수되지 않는다. 1월 원문 계보와 현재 synthesis를 통해 들어온다.

그러므로:

```text
no-backflow
≠ no reinterpretation

occurrence immutability
+ retrospective authorship adjudication
```

은 서로 모순이 아니라 다른 원장을 다루는 쌍이다.

> **[CURRENT_SYNTHESIS]** 발생 원장과 저자성·Narrative 정산 원장을 분리한다.

---

## 9. 현행 판정: 권한 비도약은 회수되었지만 인간 법칙은 아직 아니다

이 장에서 직접 회수되는 것은 다음 공학적 반복이다.

```text
proposal
≠ evidence

output
≠ commit

display
≠ state writer

constraint
≠ decision authority

derived story
≠ source policy
```

이 반복을 현재는 더 넓은 typed authority topology 후보로 묶는다.

```text
Authority
= actor
× operation
× target
× scope
× grounds
× effective time
```

예를 들면:

```text
Feeling
- may bias attention and action candidates
- may not certify an external occurrence

Narrative
- may bias future sampling and interpretation
- may not rewrite a past occurrence

Authorship settlement
- may alter future self-commitment
- may not create another person's consent
```

이 표는 아직 구현된 인간 ontology가 아니다. 현재 synthesis를 판별 가능한 질문으로 바꾸기 위한 작업 가설이다.

---

## 10. S0에 넘기는 최소 판별 질문

이 계보 감사가 S0에 직접 요구하는 것은 거대한 권한 ledger 구현이 아니다. 첫 slice에서는 다음만 보존하면 된다.

### Probe A — surface-only intervention

역할 또는 공개 제약만 바꾼다.

```text
expected:
surface action distribution may shift

must remain equal:
past occurrence
held history
slow relationship state unless the changed surface causes a new consequence
```

### Probe B — narrative-frame intervention

같은 occurrence history에 서로 다른 frame을 제공한다.

```text
expected:
attention / interpretation / next-action distribution may shift

forbidden:
past occurrence or external evidence changes solely because the frame is coherent
```

### Probe C — direct-history baseline

명시적 state/settlement 표현 없이 전체 history에서 미래를 직접 예측하는 모델과 비교한다.

```text
If typed intermediate state adds no held-out benefit,
the representation is revised or retired.
```

권한 비도약은 그럴듯한 말이 아니라, 어떤 개입에서 무엇은 변하고 무엇은 변하면 안 되는지를 지정할 때만 설명력을 갖는다.

---

## 결론

12월 persona engine에서 가장 안정적으로 반복된 것은 인간의 감정 목록이나 특정 물리 은유가 아니었다.

> **출력·후보·제약·파생 서사가 실제로 미래를 바꿀 수 있으면서도, 그 영향만으로 증거·커밋·상태 writer의 권한을 획득하지 못하게 하는 구조였다.**

이 구조는 엔진 결함을 막는 공학 규율로 직접 회수된다. 그것이 인간의 실제 동역학을 설명하는 최상위 불변량인지 여부는 아직 열려 있다.

다음 단계는 문장을 더 확장하는 일이 아니라 `HUMAN-DYN-ADEQ-S0`에서 이 분리가 단순 모델보다 더 선택적인 미래 예측을 만드는지 실행하는 것이다.
