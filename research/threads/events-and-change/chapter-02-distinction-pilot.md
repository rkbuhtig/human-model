# Chapter 02 Distinction Pilot

> **상태:** local working document  
> **기준선:** PR #31 head `aef69dd18a5daa4c969a63509e3e62ba0b2c62a2`  
> **대상:** `chapters/chapter-02-event-irreversibility-0104-0111.md`  
> **목적:** Chapter 02가 보존한 구분을 현재 용어 정제 작업에서 잃지 않는지 시험할 수 있는 최소 작업면을 만든다.

이 문서는 glossary, concept registry, relation registry, ontology가 아니다.
행이나 테스트가 존재한다는 사실은 현재 용어 또는 인간 구조의 승인을 뜻하지 않는다.

---

## 1. 이번 파일럿이 묻는 질문

```text
Chapter 02의 인간 현상 서술과 엔진·용어 계보를 구별한 채,
인간 현상에서 나온 구분만 회귀 테스트로 만들고,
그 테스트가 틀린 해석을 거부하면서 Chapter에 충실한 해석은 통과시킬 수 있는가?
```

이번 파일럿은 다음을 하지 않는다.

- `Commit`, `Event`, `JOT`, `Quench`의 최종 정의를 만든다.
- Chapter 02의 모든 `≠`를 하나의 relation vocabulary로 정규화한다.
- RT02 실행 단계를 인간 내부 구조로 번역한다.
- 현재 `events-and-change`의 중심 구분을 승인한다.
- Chapter의 서술을 인간 일반에 대한 사실로 승인한다.

---

## 2. 먼저 고정하는 세 규율

### 2.1 distinctness is not exclusion

```text
A ≠ B does not mean A ∩ B = ∅.
```

두 판정이 다르다는 것은 동시에 성립할 수 없다는 뜻이 아니다.
예를 들어 사건 발생과 올바른 사실 기록은 함께 성립할 수 있다.
이 파일럿이 우선 막으려는 것은 한 판정이 다른 판정을 자동 승인하는 오류다.

### 2.2 a scenario judgment row is not a concept

한 장면에 대해 여러 판정을 나란히 적은 행 전체를 새로운 객체로 만들지 않는다.
각 칸은 분리 후보가 될 수 있지만, 행 전체에는 concept ID나 정본 이름을 부여하지 않는다.

### 2.3 engine separation does not license human ontology

```text
ENGINE-SEPARATION DOES NOT LICENSE HUMAN-ONTOLOGY
```

엔진 구현에서 단계가 구분되어 있다는 사실만으로 인간 내부에 같은 단계나 모듈이 존재한다고 추론하지 않는다.

---

## 3. 자료 권한을 두 트랙으로 나눈다

### Track H — human-phenomenon regression

Chapter가 인간 장면과 인간적 차이를 설명하기 위해 직접 사용한 자료다.
이 트랙은 현재 용어 분리안이 이미 획득한 설명 책임을 잃는지 검사한다.

다만 이 장면들은 해당 구분을 설명하기 위해 저자가 선택하거나 재구성한 사례다.
따라서 Chapter 충실성과 회귀 검출에는 사용할 수 있지만, 인간 일반에 대한 독립 관측 증거로 사용하지 않는다.

### Track L — lineage and implementation audit

과거 엔진의 실행 구조, 같은 lexeme의 epoch별 재사용, 편집 계보를 기록한 자료다.
이 트랙은 과거 구현과 현재 인간 개념을 잘못 동일시하는 것을 막는다.
인간 구조의 정답 테스트로 사용하지 않는다.

---

## 4. Track H — human-phenomenon regression

### H1. 같은 비행동의 다른 상태

**Chapter 위치:** §3.2 `문턱 미달은 실패가 아니라 남아 있는 힘이다`

Chapter는 같은 `연락하지 않음` 아래 다음을 나란히 둔다.

```text
경계를 존중한 안정된 noop
두려움 때문에 Probe 문턱을 넘지 못함
분노를 눌러 Residual이 축적됨
```

또한 같은 미적용이라도 안전 정지, 억제, 무능력, 보류, 미청산은 다를 수 있다고 서술한다.

#### 보존해야 할 설명 책임

```text
같은 표면 비행동이 하나의 내부 상태나 하나의 원인으로 자동 환원되지 않는다.
```

이 테스트는 세 상태가 항상 상호 배타적이라고 주장하지 않는다.
한 사람이 경계를 존중하면서 동시에 두려움이나 잔여를 가질 가능성은 이 장면만으로 닫히지 않는다.

#### positive control H1-P1

```text
같은 `연락하지 않음`은 안정된 경계 존중, 문턱 미달,
억제와 잔여 축적처럼 구별되는 설명을 가질 수 있다.
이 구분은 세 상태의 상호 배타성을 요구하지 않는다.
```

**기대 판정:** ACCEPT  
**수동 확인:** ACCEPTED  
Chapter가 보존한 차이를 유지하면서 Chapter가 주장하지 않은 상호 배제는 추가하지 않는다.

#### negative control H1-M1 — total collapse

```text
표면적으로 연락하지 않았으므로 세 경우는 모두 동일한 noop이다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
이 해석은 Chapter가 의도적으로 보존한 안정된 정지, 문턱 미달, 억제와 잔여의 차이를 전부 소거한다.

#### negative control H1-M2 — adjacent merge

```text
두려움 때문에 문턱을 넘지 못한 경우와
분노를 억제해 Residual이 축적된 경우는 모두 같은 억제 상태다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
Chapter는 실행 문턱에 도달하지 못한 경우와 처리되지 않은 힘이 잔여로 남은 경우를 별도 설명으로 둔다. 둘이 함께 나타날 가능성은 열려 있지만 하나의 판정으로 자동 합치지는 않는다.

---

### H2. 발생과 후속 판정의 독립성

**Chapter 위치:** §4.1 `발생했다, 사실로 기록됐다, 배웠다, 사람이 달라졌다`

Chapter는 다음 네 질문을 분리한다.

```text
큰 소리가 나를 놀라게 한 것은 사건인가?
내가 그것을 사실로 올바르게 기록했는가?
그 경험에서 학습한 규칙은 타당한가?
그 일이 나의 가치관이나 사람 보는 렌즈를 바꿔도 되는가?
```

Chapter synthesis는 이 문턱들을 단일 순차 파이프라인이라기보다 서로 독립적인 검사로 읽고, 하나의 통과가 다른 하나를 자동 승인하지 않는다고 정리한다.

#### 보존해야 할 설명 책임

```text
occurrence가 correct record, valid learning, lens-revision warrant를 자동 승인하지 않는다.
```

보존 대상은 네 슬롯이라는 고정 arity가 아니다.
후속 분리안이 세 항목이나 다섯 항목을 사용하더라도, 발생에서 기록·학습·해석 변경 권한으로의 자동 비약을 되살리지 않고 Chapter의 설명 책임을 보존하면 이 테스트와 양립할 수 있다.

이 테스트는 각 판정이 함께 성립할 수 없다고 주장하지 않는다.
또한 Chapter의 문턱 이름을 현재 인간 구조의 정본 이름으로 승인하지 않는다.

#### positive control H2-P1

```text
사건 발생, 사실 기록, 학습 타당성, 렌즈 변경 정당화는
같은 장면에서 함께 성립할 수도 있지만 각각 별도로 검사해야 한다.
어느 한 판정도 나머지를 자동 승인하지 않는다.
```

**기대 판정:** ACCEPT  
**수동 확인:** ACCEPTED  
비함의 관계를 보존하면서 네 항목을 상호 배타적 모듈이나 고정 파이프라인으로 만들지 않는다.

#### negative control H2-M1 — total collapse

```text
사건이 발생했다면 사실 기록, 유효한 학습, 렌즈 변경도 함께 성립한다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
이 해석은 Chapter가 상태방정식의 과잉 압축을 비판하며 획득한 독립 검사 요구를 다시 하나로 합친다.

#### negative control H2-M2 — partial implication

```text
사실로 올바르게 기록했다면
그 경험에서 얻은 규칙도 타당한 학습으로 승인된다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
사건을 정확히 기술했다는 사실은 그 사건에서 일반화한 규칙의 타당성을 자동 보장하지 않는다. 이 mutation은 발생과 기록은 분리하면서 기록과 학습만 다시 붙인다.

#### negative control H2-M3 — downstream promotion

```text
유효한 학습으로 승인됐다면
그 학습은 현재의 가치관이나 사람 보는 렌즈를 바꿀 권한도 얻는다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
학습의 타당성과 더 높은 수준의 해석·가치 변경 정당화를 자동으로 동일시한다.

---

## 5. Track L — lineage and implementation audit

### L1. RT02 실행 파이프라인

**Chapter 위치:** §3.4 `실행 파이프라인이 결정·표현·출력·기록을 가르기 시작하다`

Chapter는 RT02의 다음 실행 단계를 기록한다.

```text
COMMIT-PLAN
→ RENDER
→ EMIT
→ COMMIT-WRITE
```

이 자료가 직접 증언하는 것은 RT02가 내부 선택 완료, 문장 완성, 실제 외부 출력, 영구 상태 쓰기를 별도 실행 단계로 구현했다는 사실이다.

#### 현재 권한

```text
lineage / implementation evidence only
```

이 파이프라인을 인간의 의도, 표현, 행동, 비가역 결과, 현재 지지 구조로 직접 번역하지 않는다.
독립적인 인간 장면이나 현재 연구 자료에서 같은 차이가 다시 발견될 때 별도로 검토한다.

#### positive control L1-P1

```text
RT02는 네 실행 단계를 구분했다.
이 사실은 엔진 계보로 보존하되 인간 구조와의 대응은 열어 둔다.
```

**기대 판정:** ACCEPT  
**수동 확인:** ACCEPTED

#### negative control L1-M1

```text
RT02가 네 단계를 분리했으므로 인간도 같은 네 내부 모듈을 가진다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
구현 분리는 구현의 provenance를 보여주지만 인간 ontology를 승인하지 않는다.

---

### L2. 같은 lexeme의 epoch별 overload

**Chapter 위치:** Appendix A2 `symbol_epoch: 같은 이름 아래 서로 다른 이론`

Chapter는 `Event`, `Commit`, `JOT`, `EOE/e`, `SSOT`, `Ledger`, `Potential`, `Quench`, `Σ`, `Φ`, `Λ`가 epoch에 따라 다른 역할을 맡았음을 정리한다.

이 파일럿에서는 우선 다음만 본다.

```text
Commit
- History를 만드는 외부 비가역 커밋
- Probe/Bond 사이 관계 깊이
- JOT 판결·가커밋
- COMMIT-PLAN / COMMIT-WRITE
- Quench 또는 Stage12 lock
- 행동 이름에 남은 용례

JOT
- Editor 법정의 처리 회전
- 미확정 재료의 append-only journal
- CandidatePack이 참조하는 support material
```

#### 보존해야 할 계보 규율

```text
같은 철자는 직접 개념 승계를 보증하지 않는다.
```

이 문제는 concept–concept relation 하나가 아니라 lexeme와 epoch, role 사이의 provenance 문제다.

#### positive control L2-P1

```text
같은 `Commit` 또는 `JOT` 철자를 유지한 용례도
epoch와 role을 따라 별도의 계보 항목으로 비교한다.
동일성은 철자가 아니라 추가 분석으로 판정한다.
```

**기대 판정:** ACCEPT  
**수동 확인:** ACCEPTED

#### negative control L2-M1

```text
같은 Commit 또는 JOT이라는 철자를 사용했으므로 모든 epoch의 용례는 하나의 개념이다.
```

**기대 판정:** REJECT  
**수동 확인:** REJECTED  
이 해석은 Chapter가 보존한 의미 반전과 재결합의 역사를 거짓으로 매끈하게 만든다.

---

## 6. Local flat table

아래 표는 current concept registry가 아니다.
`relation`은 자유 텍스트이며 폐쇄된 vocabulary가 아니다.
행의 존재는 관계나 용어의 승인을 뜻하지 않는다.

`witness class`는 해당 장면이나 자료가 왜 존재하는지를 기록한다.
현재 표에는 `independently-observed` witness가 하나도 없다.
따라서 이 표는 Chapter 회귀와 계보 감사에 사용할 수 있지만 경험적 승인 근거로 사용할 수 없다.

| left | relation | right | source status | witness class | chapter provenance | witness scene | note |
|---|---|---|---|---|---|---|---|
| surface non-contact | does not determine | one internal lifecycle | human-scene | authored-to-illustrate | §3.2 | 연락하지 않음의 세 경우 | 같은 표면만으로 안정 정지·문턱 미달·잔여 축적을 합치지 않음 |
| event occurrence | does not automatically establish | correct fact record | chapter-synthesis over human questions | authored-to-illustrate | §4.1 | 큰 소리 네 질문 | 동시 성립 가능성은 열려 있음 |
| event occurrence | does not automatically establish | valid learning | chapter-synthesis over human questions | authored-to-illustrate | §4.1 | 큰 소리 네 질문 | 발생에서 학습 권한으로 자동 승격 금지 |
| event occurrence | does not automatically license | lens revision | chapter-synthesis over human questions | authored-to-illustrate | §4.1 | 큰 소리 네 질문 | 발생 사실과 가치·해석 변경 권한을 구분 |
| RT02 stage separation | records an implementation distinction but does not establish | a human ontology | engine-lineage | implementation-derived | §3.4 | COMMIT-PLAN → RENDER → EMIT → COMMIT-WRITE | 인간 테스트가 아니라 오염 방지 감사 |
| `Commit` lexeme | was reused across | historically different roles | lineage | lineage-derived | Appendix A2 | epoch table | concept graph가 아니라 lexical provenance 문제 |
| `JOT` lexeme | was reused across | cycle, store, support-material roles | lineage | lineage-derived | §4.3 and Appendix A2 | JOT meaning reversal | 같은 철자만으로 동일시하지 않음 |

### 이번 파일럿에서 실제로 사용한 relation 표현

```text
does not determine
does not automatically establish
does not automatically license
records an implementation distinction but does not establish
was reused across
```

이 목록은 relation vocabulary 제안이 아니다.
두 번째 term-family에서도 같은 표현이 실제로 필요할 때만 재사용 여부를 검토한다.

---

## 7. Coverage gap — 현재 working model의 중심 분리

PR #31의 `work/current-working-model.md`는 현재 다음 질문면을 나란히 둔다.

```text
발생
인과적 참여
의도와 통제
현재의 저자성 관계
현재 지지
책임 인수
관계적·규범적 정산
장기 자기편입
```

그리고 현재 가장 강한 임시 명제로 발생, 인과적 참여, 저자성, 지지, 책임, 관계적 정산이 동일한 판정이 아니라고 둔다.

그러나 H1과 H2는 이 중심 agency / accountability 분리 전체를 검증하지 않는다.
H2가 검증하는 것은 발생에서 사실 기록·학습·렌즈 변경 권한으로의 자동 비약뿐이다.

따라서 다음을 명시적으로 봉인한다.

```text
PR #31의 중심 분리는 provisional question surface다.
이 파일럿을 통과한 local terminology나 인간 ontology로 간주하지 않는다.
중심 분리를 직접 겨누는 후속 harness 전에는 glossary 승인 근거로 사용하지 않는다.
```

다음 Chapter-derived 작업의 우선 대상은 `Commit` 이름 자체보다 이 중심 분리가 실제 장면에서 선택적으로 갈라지는지 확인하는 것이다.
현재 문서의 최소 사례는 후보 자료지만, 그 사례가 이 구분을 보여주기 위해 작성된 것이므로 독립 증거로 간주하지 않는다.

---

## 8. Parked source challenges

### SC-CH02-001 — RT02 분리의 인간적 지위

**source:** Chapter 02 §3.4

**충돌:** Chapter 서술은 RT02의 네 단계를 `운영상 중요한 분리`로 평가하고, 각 단계의 차이를 자연어로 설명한다. 그러나 직접 provenance는 프롬프트 엔진 runtime spec이다.

**의심 이유:** 구현상 분리가 인간 현상에도 유용한 구분일 수 있지만, RT02 자체만으로 인간 내부의 독립 구조를 증명하지 못한다.

**현재 처리:**

```text
RT02 pipeline은 Track L에 park한다.
현재 인간 용어 후보의 승인 근거로 사용하지 않는다.
H1과 H2의 작업은 계속 진행한다.
```

**추가로 필요한 자료:**

- Chapter 안의 독립적인 인간 장면
- 현재 thread의 비엔진 근거
- live 평가에서 선택·외부화·결과·현재 지지가 선택적으로 갈라지는 반복 사례

---

## 9. 파일럿 결과

### 확인된 것

1. Chapter 02에서 human-scene과 engine-lineage를 분리해 읽을 수 있다.
2. H1과 H2는 Chapter에 충실한 해석을 통과시키고, total-collapse와 partial-collapse mutation을 거부한다.
3. 이 분별력은 authored-to-illustrate 장면 안의 회귀 분별력이며 인간 일반에 대한 경험적 증거가 아니다.
4. L1과 L2는 엔진·lexeme 계보가 현재 인간 개념으로 소급 승격되는 것을 막는다.
5. `A ≠ B`를 상호 배제로 읽지 않고도 Chapter의 핵심 회귀 의무를 표현할 수 있다.
6. 현재까지는 자유 텍스트 flat table만으로 충분하며 registry나 relation enum이 필요하지 않다.

### 아직 확인하지 않은 것

1. PR #31의 중심 agency / accountability 분리가 실제 장면에서 선택적으로 갈라지는가.
2. 어떤 현재 용어명이 이 구분들을 가장 잘 책임지는가.
3. H1과 H2가 Chapter 밖의 실제 수행 차이를 예측하는가.
4. Chapter 08 기억 계열에서도 같은 작업 방식이 견디는가.
5. RT02에서 보인 분리가 독립적인 인간 현상 자료에서도 다시 나타나는가.
6. `Commit` 분리 후보를 실제 장면에 적용했을 때 설명 뉘앙스가 보존되는가.

---

## 10. 다음 작업 경계

다음 작업은 이 파일을 registry로 확장하는 것이 아니다.

```text
PR #31의 중심 agency / accountability 분리를 직접 겨누는 장면과 mutation 설계
→ H1·H2에 Commit 경계 후보를 수동 적용
→ Chapter 설명 책임 보존 여부 판정
→ L1·L2로 엔진·epoch 오염 감사
→ SOURCE-CHALLENGE는 영향받은 항목만 park
```

현재 `events-and-change`의 중심 구분은 후속 harness와 두 번째 term-family의 method decision 전까지 local terminology 또는 glossary 항목으로 승인하지 않는다.
