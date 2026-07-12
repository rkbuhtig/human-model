# Chapter 05 — 문서는 아직 런타임이 아니다

## 문장에서 소켓으로: 0117 통합 공장과 실행 의미론의 탄생

> **상태:** 역사 복원 + 연구 후기 v1.0  
> **범위:** 2026-01-17 `통합을 위한 공장`의 Spine·Skeleton·Manifest·Socket·Closure·Core부터 `공장2/0117 canon05 1`의 v0.5-STG까지  
> **직전 장:** Chapter 04 — 다음 박자에만 닿는 것들  
> **전방 경계:** 0118 Pressure/Witness/Receipt–σ–Bill 계열은 Chapter 06으로 보류

---

## 들어가며 — 남아 있는 문장과 작동하는 문장은 다르다

Chapter 04의 종점에는 하나의 좁은 통로가 남았다.

```text
readout_t
↛ current authority
→ next-tick search / comparison / work policy
```

하지만 이 규칙은 아직 문장이었다. “권한이 아니다”, “다음 tick에만 닿는다”, “same-tick 역류 금지”라고 선언할 수는 있었지만, 긴 문서의 어느 함수가 어느 값을 읽고 어떤 포인터를 돌리며 어떤 기록을 남기는지까지 닫히지는 않았다.

0117의 통합 공장은 이 문제를 철학 문장으로 더 설명하지 않는다. 대신 묻는다.

> 이 문장은 어느 모듈에 속하는가?  
> 어느 키를 읽을 수 있는가?  
> 어느 소켓으로 들어가는가?  
> 무엇을 절대 만져서는 안 되는가?  
> 표에 없는 경로를 실행기가 어떻게 거절하는가?

이때 통합의 뜻이 바뀐다.

```text
여러 설명을 한 문서에 모음
→ 충돌 시 적용권을 정함
→ 모듈의 빈 소켓을 먼저 만듦
→ 키·read scope·write scope를 등록함
→ allow/deny 표로 실제 연결을 닫음

후기 평행 STG branch
→ 같은 문제군을 단일 상태 전이 F로 재구성
```

이 장은 새로운 인간 현상을 발명한 장이 아니다. **어떤 인간 이론이 실제 상태 전이에 참여할 자격을 얻는지 결정하는 공장**이 생긴 장이다.

그리고 그 공장은 중요한 것을 얻는 동시에 중요한 것을 잃는다. v0.4b–Core branch는 readout의 권한 탈취를 어렵게 만드는 대신 ExternalIn을 VIEW로 제한해 별도 evidence port를 만들지 못한다. 시간상 마지막인 v0.5-STG branch에는 외부 input을 받는 policy-shaped TR/phys 경로가 있지만 authenticity·evidence type이 없다. 이 branch는 앞선 Core의 명시 승계를 선언하지 않으며 NextWire·Decision/Record에 대응하는 봉인 일부도 보이지 않는다.

그러므로 이 장의 질문은 단순히 “통합에 성공했는가?”가 아니다.

> **문장을 실행 계약으로 바꾸려면 무엇을 포기해야 했으며,  
> 누수를 막기 위해 만든 벽은 무엇까지 함께 막았는가?**

---

# 역사 본문 — 그 시점의 문제와 변형을 따라가기

## 0. 범위·판본·중복 규율

### 0.1 이번 장의 실제 시작과 종점

Chapter 04는 0117의 RATION v0.5와 기술 통합 branch를 하나의 aggregate로 모은 지점에서 끝났다. 이번 장은 그 뒤 별도 폴더에 형성된 `통합을 위한 공장`에서 시작한다.

시작점은 우선순위와 해석권을 세운 `0117 spine`이고, 내부 종점은 두 단계다.

1. `0117 core`의 v1.2a-SEAL: key/socket wiring의 봉인
2. `공장2/0117 canon05 1`의 v0.5-STG: 같은 문제군을 단일 전이 `F`로 다시 쓴 후기 실행 정본

두 번째 문서는 첫 번째의 모든 표를 문자 그대로 포함하는 합본도, 명시된 직접 후계도 아니다. Core와 STG를 기능별로 대조하면 대응 봉인이 있거나 보이지 않는 곳이 드러난다. 따라서 이 장은 `core → canon05`를 매끈한 직선 승계로 가정하지 않는다.

`STG17`은 `CORE17`을 자신의 명시 source set으로 선언하지 않는다. 같은 날짜·9U 규율·PackRef/Gate·current/next 문제를 공유하고 단일 실행 정본을 표방한다는 기능적·판본상 이유로 종점에 두되, 정확한 textual descendant라고 단정하지 않는다.

### 0.2 파일명보다 내부 버전과 포함 관계를 따른다

원본 ZIP에서 추출된 파일에는 서로 다른 분 단위 mtime이 보존되어 있고, 그 상대 순서가 내부 버전·명시 의존과 대체로 일치한다. 따라서 이번 장은 이를 판 계보의 보조 증거로 사용한다. 표의 시각은 **상대 순서 확인용**이며 파일시스템에 표시된 timezone을 저자의 작성 timezone으로 해석하지 않는다.

| 순서 | 보존 mtime | 별칭 | 내부 지위 | 이 장에서의 역할 |
|---:|---:|---|---|---|
| 1 | 17:33 | `SP17` | Spine v0.2.3 | 9U와 적용·해석 우선순위 |
| 2 | 17:38 | `SK17` | Skeleton v0.3b | timebase·snapshot·interface 조립틀 |
| 3 | 17:46 | `MIM17` | Module Interface Manifest v0.1 | 모듈별 read/output/no-touch/write 표 |
| 4 | 17:59 | `SS17` | Spine+Skeleton v0.3c | 두 문서의 재컴파일·경계 보강 |
| 5 | 18:25 | `C04B17` | Executable Canon v0.4b | 조립 가능한 런타임 템플릿·Gate A–D |
| 6 | 18:29 | `MF17` | Build Step v0.4c | Registry·SKR·직렬화·빈 소켓·Gate checklist |
| 7 | 19:06 | `FS17` | Full Spec v0.4d | spine/skeleton/manifest·interface 계열 통합 + Addendum A |
| 8 | 19:56 | `SOC17` | Core Socket Contract v1.0 | CANON/SELECT/COMMIT/POLICY와 최소 SKR |
| 9 | 19:58 | `CL17` | Closure Tables v1.1 | key-level deny와 active/next 교정 |
| 10 | 20:17 | `CORE17` | Core v1.2 + v1.2a-SEAL | CANDGEN·NextWire·Decision/Record·PackStore 봉인 |
| 11 | 22:33 | `STG17` | Executable Canon v0.5-STG | 같은 문제군을 단일 전이 `F`로 다시 쓴 후기 branch |

다음 두 합본은 독립 발명으로 중복 계산하지 않는다.

- 17:51의 `0117 fornext` 401행은 `SP17` 175행과 `SK17` 226행의 **byte-identical 연속 결합**이다.
- 20:21의 `0117 FUULL` 1–561행은 `FS17` 전체, 562–1163행은 `CORE17` 전체와 **byte-identical**하다.

즉 `fornext`와 `FUULL`은 중요한 보존 산물이지만 새 개념의 최초 출처는 아니다.

### 0.3 이 장의 판정 표지

| 표지 | 뜻 |
|---|---|
| `[DIRECT]` | 해당 판본이 직접 선언한 내용 |
| `[RECOMPILED]` | 앞선 규율을 새 형식·한 문서로 재조립 |
| `[FUNCTIONAL CORRECTION]` | 뒤 판본이 앞 판본의 실제 모호성을 좁힘 |
| `[REAL CONFLICT]` | 같은 역할·writer·clock 아래 동시에 유지하기 어려운 정의 |
| `[CROSS-BRANCH COMPARATIVE OMISSION]` | 시간상 후기 branch를 Core 기준과 비교할 때 대응 봉인이 보이지 않음. 직접 승계·기능 상실·공식 rollback을 뜻하지 않음 |
| `[NON-ADOPTION]` | 보존된 가지가 새 registry/runtime에 채택되지 않음 |
| `[FUNCTIONAL REDISCOVERY]` | source 승계 선언 없이 유사 기능이 다시 구현됨 |
| `[TYPE RESIDUE]` | 의미 봉인은 생겼지만 schema·field·type 배치가 따라오지 못함 |
| `[OVER-CLOSURE]` | 누수 차단 범위가 넓어 정당한 입력 port까지 함께 막을 위험 |
| `[EXACT REPACKAGING]` | 기존 파일의 byte-identical 결합이며 새 발명은 없음 |
| `[SCOPE LIMIT]` | 원문이 직접 봉인한 범위 밖으로 완성 판정을 확장하지 않음 |
| `[LINEAGE]` | 후대 현행 구조와 직접 또는 강하게 이어지는 계보 판정 |
| `[RESIDUE]` | 통합 과정에서 빠지거나 집이 정해지지 않은 것 |
| `[BRIDGE]` | 이번 독해에서 새로 연결한 가설 |
| `[OPEN]` | 다음 지층에서 확인할 질문 |

---

## 1. Spine — 최신 문서가 아니라 누수를 닫는 문서가 위에 선다

### 1.1 한 문장이 통합의 헌법이 되다

`SP17`은 통합본이 단일 이론인 이유를 하나의 문장으로 고정한다.

```text
Authority는 SSOT/원장/commit에만 존재한다.
Φ/Story/Marker/ε·J 같은 surface는 view/readout이다.
view는 next-tick policy에만 영향을 줄 수 있다.
same-tick의 원장·물리·commit을 변경할 수 없다.
```

`[SP17:L4–12]`

Chapter 04에서는 이 문장이 RATION과 technical branch를 묶는 종점이었다. 공장에서는 이 문장이 개념 요약을 넘어 **모든 하위 모듈의 적용 자격을 판정하는 최상위 규칙**이 된다.

### 1.2 append-only는 모든 문장의 동등한 실행을 뜻하지 않는다

공장은 과거 문서를 삭제하지 않는다. 하지만 보존되어 있다는 이유만으로 모든 문장을 동시에 실행하지도 않는다.

```text
9U → 9b → 7i → 9a → 7L → 6c → 7g/h
```

이 순서는 최신 날짜순이 아니다. 권한 위치, 입력 그래프 closure, timebase 위생, 축 잠금처럼 **누수를 닫는 역할을 먼저** 둔 해석·적용 우선순위다 `[SP17:L16–36]`.

충돌한 하위 문장은 삭제되지 않는다. 상위 규칙 아래 view/readout 의미로 격하되거나, 실행 의미론에서 authority만 무효가 된다 `[SP17:L38–52]`.

이때 공장 문법에서 선명해진 중요한 구분은 다음이다.

```text
textual persistence
≠ interpretive priority
≠ executable authority
```

위 세 줄은 원문의 단일 공식이 아니라 이 장의 압축이다. 그러나 `SP17`의 실제 편집 규율은 이미 그 방향으로 움직인다.

### 1.3 권한 위반을 내용이 아니라 경로로 판정한다

`SP17`은 잘못된 이론을 의미 내용으로 판정하지 않는다. 세 종류의 경로를 검사한다.

1. readout이 same-tick SSOT·Π_phys·계수·commit decision으로 재유입되는가
2. 비용함수·원장규칙·계수를 변경하거나 discount하는가
3. 9b/9a의 CanonFn allow/deny를 우회해 ΔQ·선택을 조작하는가

`[SP17:L43–52]`

권한이 값에 붙은 명예 라벨이 아니라 **어디까지 도달할 수 있는가라는 그래프 속성**으로 이동하기 시작한다.

### 1.4 첫 우선순위가 남긴 비채택

Spine의 module chain에는 7L, 6c, 7g/h가 들어 있지만 RATION은 독립 module로 등재되지 않는다. FrameGate·coverage·X/R/U/A Residence Law는 이 우선순위 체인의 직접 구성원이 아니다.

> **[NON-ADOPTION]** 공장이 Chapter 04의 RATION을 그대로 컴파일했다고 쓰면 과장이다. 공장은 같은 9U 문장을 공유하지만, 선언된 module lineage는 9U/9b/7i/9a/7L/6c/7g-h다.

---

## 2. Skeleton — 본문보다 경계를 먼저 쓴다

### 2.1 통합 순서가 뒤집히다

`SK17`의 첫 문장은 권한·시간축·결정론·closure를 먼저 고정하고 나머지 모듈을 그 뒤에 조립한다고 선언한다 `[SK17:L4–15]`.

이것은 단순한 문서 양식 변경이 아니다.

```text
이론 본문 작성 → 충돌을 나중에 수정

에서

경계·소켓·금지 경로 작성 → 통과하는 본문만 삽입

으로
```

통합의 방향이 바뀐다.

### 2.2 세 timebase와 snapshot

Skeleton은 `t_eng`, `t_bio`, `t_commit`을 서로 다른 갱신 축으로 두고 tick 시작의 `S_t`를 입력 경계로 고정한다. 같은 tick의 view가 직접·간접·cache를 경유해 현재 SSOT 계산으로 되돌아오는 길도 금지한다 `[SK17:L72–86]`.

```text
t_eng    : 탐색·비교·canonical 계산의 엔진 축
t_bio    : LPF·리듬·열의 내부 적분 축
t_commit : SSOT 확정 축
```

여기서 timebase와 current/future transition lane은 아직 완전히 같은 타입 언어로 분리되지는 않지만, “느린 상태는 별도 writer가 아니다”라는 규칙은 명시된다 `[SK17:L188–194]`.

### 2.3 함수도 자기 경계를 가져야 한다

`SliceFn`은 축 매핑만, `CanonFn`은 ΔQ/ΔQ⊥ 계산만 담당한다. 서로의 정의를 침범할 수 없고 view는 CanonFn 입력축이 아니다 `[SK17:L88–113]`.

인간의 역할을 Reporter·Editor·Actor로 나누었던 문제와 닮아 보이지만, 이 문서는 인간 은유를 말하지 않는다. 이 시점의 직접 성취는 **함수 책임을 read/input/output/no-touch로 제한하는 것**이다.

### 2.4 네 줄짜리 모듈 계약

각 모듈은 본문보다 먼저 다음을 선언해야 한다.

```text
read-set
output
no-touch
write-set
```

`[SK17:L160–170]`

특히 `no-touch`가 중요하다. 무엇을 읽고 쓰는지만이 아니라, 어떤 우회도 가져서는 안 되는지를 interface의 일부로 만든다.

### 2.5 Shadow SSOT와 cache

tick 사이에 남는 값은 SSOT에 기록되거나, `S_t`에서 순수함수로 재구성 가능해야 한다. cache hit/miss가 결과를 바꾸면 cache가 사실상 숨은 writer가 되므로 금지된다 `[SK17:L172–186]`.

```text
오래 남음
≠ SSOT일 자격

빠른 cache
≠ 선택을 바꿀 권한
```

Chapter 02의 `Persistence ≠ Authority`가 이 공장 안에서는 **Shadow SSOT 금지**라는 구현 규율로 다시 나타난다. 원문이 이 역사 계보를 선언한 것은 아니므로 강한 문제 계보로만 둔다.

### 2.6 v0.3c와 v0.4b — 조립 가능한 Canon

`SS17`은 자신을 Spine+Skeleton v0.3c 통합본으로 선언하고 두 문서를 선택적으로 재컴파일한다 `[SS17:L3–16]`. 그러나 policy 저장 위치·적용 tick·수치 정규화 같은 문제를 편집 메모로 남긴다 `[SS17:L305–313]`.

보존 시각상 더 이른 `MIM17`이 canonical ID와 pruning 제한을 먼저 표로 쓴다 `[MIM17:L128–131]`. `C04B17`은 ExternalIn, commit 최소 입력, 동일 취지의 pruning 제한, 고정 hash requirement, Gate A–D를 명시하며 자신을 “조립 가능한 런타임 의미론 템플릿”으로 규정한다 `[C04B17:L3–8, L21–61, L147–179, L186–228, L255–277]`. 두 문서 사이의 직접 승계 선언은 확인되지 않는다.

상세 `SerializeNorm_v1 / HashFn_v1` 요구는 `MF17`에서, concrete SHA-256 고정은 `FS17`에서 뒤이어 나타난다 `[MF17:L62–89; FS17:L228–235]`.

v0.4b의 tick pipeline은 다음과 같다.

```text
S_t snapshot
→ CanonFn / ΔQ
→ view/readout
→ Policy_{t+1}
→ commit
```

commit은 `S_t + 선택 결과 + canonical impulse + 정책 로그`만 받으며 원시 view를 write-set에 직접 반영하지 않는다고 선언한다 `[C04B17:L21–39]`.

하지만 이 단계는 여전히 문장형 템플릿이다. 어느 `K.*` 키가 실제로 이 집합에 들어오는지, 같은 이름의 포인터가 현재용인지 미래용인지, ref가 가리키는 payload가 바뀌지 않았는지는 아직 표로 닫히지 않았다.

---

## 3. Manifest — 문서의 존재와 실행 참여를 분리하다

### 3.1 Registry-First

`MF17`은 v0.4b의 “다음 제작 스텝”을 자처하며 본문 삽입보다 registry를 먼저 만든다 `[MF17:L3–11]`.

가장 중요한 문장은 이것이다.

> Registry에 없는 본문은 참고·주석으로는 존재할 수 있지만 Executable 의미론의 권한·입력·commit에는 관여할 수 없다 `[MF17:L13–29]`.

이 장의 제목인 “문서는 아직 런타임이 아니다”는 바로 이 규율을 압축한 것이다.

```text
written
≠ registered
≠ linked
≠ executable
```

### 3.2 SSOT Key Registry

Manifest는 SSOT 키를 LEDGER, STATE, META로 분류하고 각 키에 writer, update rate, read scope, write scope를 붙인다 `[MF17:L31–53]`.

```text
key_name
+ class
+ writer
+ update_rate
+ read_scope
+ write_scope
```

이것은 Chapter 04의 X/R/U/A보다 구체적이다. “어디에 사는가”뿐 아니라 누가 어느 stage에서 읽고 쓸 수 있는지를 묻기 때문이다.

그러나 이 시기 `META_KEYS`가 SSOT key 3분류 안에 놓이면서도 권한은 없다고 서술된다. persistence, SSOT residence, decision authority가 하나의 분류표 안에서 아직 완전히 직교화된 것은 아니다.

### 3.3 결정론은 재현 가능한 내용 식별 규약이 된다

`SerializeNorm_v1`은 문자열, map 순서, 배열, 숫자, type tag를 고정하고 runtime 기본 hash나 객체 표현을 금지한다. `MF17`의 `HashFn_v1`은 별도로 명시 고정할 알고리즘과 정규화 payload를 요구하지만 알고리즘을 아직 확정하지 않는다 `[MF17:L62–89]`. Concrete SHA-256과 domain tag는 `FS17`에서 뒤이어 고정된다 `[FS17:L228–235]`.

No-RNG와 정규화 hash는 세계가 확률적일 수 없다는 형이상학적 선언이라기보다, **같은 정규화 입력에서 같은 실행 결과와 tie-break를 재현하기 위한 build requirement**다. 이것만으로 실제 worldline이나 누가 후보·선택을 만들었는지의 source provenance가 생기지는 않는다.

### 3.4 빈 소켓을 먼저 만든다

Manifest는 실제 7L·6c·7g/h 본문을 가져오기 전에 모듈별 Interface Sheet를 만든다. read-set, output, no-touch, write-set이 없는 긴 설명은 실행 자격을 얻지 못한다 `[MF17:L91–160]`.

Gate도 네 묶음으로 고정된다.

- Authority / same-tick
- No-discount / heuristic revaluation
- Determinism
- Snapshot / Shadow SSOT

`[MF17:L162–186]`

그리고 실제 조립 순서도 registry → closure table → notation/timebase → SliceFn → 현상학 module 순으로 정한다 `[MF17:L189–200]`.

> **[DIRECT]** 인간적 설명은 먼저 쓰이는 본체가 아니라, 상위 봉인과 빈 소켓이 준비된 뒤 삽입되는 payload가 된다.

이 순간 통합 공장의 성격이 확정된다. 공장은 내용을 많이 아는 문서가 아니라, **어떤 내용이 어느 권한으로 작동할 수 있는지 링크하는 문서**다.

---

## 4. MIM과 Full Spec — 설명을 넣기 전에 읽기 능력부터 제한하다

MIM은 ZIP 보존 시각상 FS보다 먼저 기록되었다. 여기서는 그 module-level 계약이 후대 FS·Core에서 어떻게 재배열되는지 보기 위해 주제상 함께 읽는다. 보존 시각은 순서를 지지하지만 직접 의존 선언과 같지는 않다.

### 4.1 MIM은 모듈의 능력을 표 한 장으로 제한한다

`MIM17`은 9U·9b·7i·9a·7L·6c·7g/h 각각에 read-set, output, no-touch, write-set을 부여한다.

예를 들어:

- 7L은 Φ·Meta·Story와 policy hint를 만들지만 SSOT를 쓰지 못한다.
- 6c는 후보와 결정론적 비교 결과를 만들지만 원장 규칙을 바꾸지 못한다.
- 7g/h의 SLOW state도 commit에서만 쓸 수 있다.

`[MIM17:L12–126]`

이 표가 얻은 것은 모듈 이름과 권한의 분리다. `Ego`, `Love`, `Qualia`처럼 의미가 큰 이름도 interface에 없는 능력을 가질 수 없다.

그러나 MIM의 6c는 같은 tick의 view를 읽고 후보를 만들 수 있으면서, 그 후보가 언제 활성화되는지 아직 밝히지 않는다 `[MIM17:L78–108]`. 후보 생성이 선택을 우회 조작하는 문제는 뒤의 Candidate route seal과 NextWire가 맡게 된다.

### 4.2 v0.4d는 선택·commit·외부 입력을 addendum으로 잠근다

`FS17`은 Spine·Skeleton·Manifest 계열을 한 통합판으로 재배열한 뒤 Addendum A를 붙인다. Addendum은 다음 여섯 구멍을 겨냥한다.

- SelectIn의 정의
- CommitPayload의 최소 schema
- ExternalIn의 registry label
- FloatPolicy
- ViewGraph purity
- 강화된 Gate C+

`[FS17:L450–466]`

이 시점부터 선택과 commit은 자연어 동사가 아니라 입력 집합과 payload schema를 가진다. CommitPayload에 허용되는 것은 `chosen_candidate_id`, canonical impulse summary, spend delta, audit ref뿐이며 원시 view·meta 본문은 금지된다 `[FS17:L484–504]`.

Addendum은 단순 부록이 아니라 base v0.4d의 실제 공백을 수리한다. base의 commit 최소 정의는 `S_t + 선택 결과 + 정책 기록`을 말해 canonical impulse를 표면상 누락하지만, Addendum의 CommitPayload가 이를 `canonical_impulse_summary`로 다시 넣는다 `[FS17:L136–154, L484–502]`.

Registry 분류도 변한다. `MF17`은 LEDGER·STATE·META만 SSOT key class로 두고 VIEW는 등록 불가라고 했지만, `FS17`은 LEDGER·STATE·VIEW·META를 registry **label**로 함께 두며 label이 곧 type은 아니라고 제한한다 `[MF17:L31–41; FS17:L262–287]`.

> **[FUNCTIONAL CORRECTION]** registry가 “SSOT에 사는 것만의 목록”에서 “실행기가 추적해야 하는 모든 key label의 목록”으로 넓어진다. 다만 residence와 authority를 완전히 다른 type으로 푼 것은 아니다.

### 4.3 첫 SelectIn에는 미래 정책이 들어가 있었다

그러나 최초의 addendum은 다음과 같이 쓴다.

```text
SelectIn_t
= S_t + CanonFn outputs + Policy_{t+1} allowlist outputs
```

`[FS17:L470–482]`

이 정의를 문자 그대로 읽으면 같은 tick의 view가 만든 `Policy_{t+1}`가 현재 선택에 다시 들어올 수 있다. 바로 막으려던 same-tick feedback이 이름만 `next`인 정책을 통해 되살아난다.

> **[REAL CONFLICT]** “view는 다음 tick에만 영향한다”는 9U와, 현재 SelectIn에 `Policy_{t+1}`를 넣은 A-SEL01은 같은 clock convention 아래 동시에 유지되기 어렵다.

이 충돌은 뒤의 Closure Table v1.1이 `policy_act_ref`와 `policy_next_ref`를 갈라 교정한다. 공장은 완성된 설계가 한 번에 나온 것이 아니라, **자신이 만든 배선도를 실제로 읽다가 새 누수를 발견한 과정**이었다.

### 4.4 ExternalIn을 전부 VIEW로 잠그다

Addendum A는 외부 텍스트·센서·marker를 `VIEW_KEYS`로만 등록하고 CanonFn·Select·Commit 입력으로의 승격을 기본 deny한다 `[FS17:L506–519]`.

이 봉인은 외부 marker나 발화가 곧바로 진실이 되는 길을 강하게 막는다. 현행 감사 렌즈로 보면 센서 흔적·몸의 손상·actual world response처럼 후대에 evidence 후보가 될 수 있는 입력까지 같은 VIEW 범주에 넣는 over-closure 위험이 있다.

```text
External input ≠ truth

를 지키려다가

External input ↛ canonical grounds

까지 닫을 위험
```

이것은 아직 이 branch 내부에서 해결되지 않는다. 후대 0118이 `GateRaw / TR_perc`, `Π_wit / Π_view`로 이 공백과 유사한 문제를 다룬다고 연구 후기가 역조명할 수 있지만, 0117 원문이 그 인과를 선언하지는 않는다.

---

## 5. Socket Contract v1.0 — 이름 대신 키와 참조가 흐르기 시작하다

### 5.1 네 개의 코어 소켓

`SOC17`은 CANON, SELECT, COMMIT, POLICY 네 소켓을 정의한다 `[SOC17:L19–70]`.

| 소켓 | 하는 일 | 금지되는 것 |
|---|---|---|
| `IS-CANON` | `S_t`와 허용된 state/ledger key에서 canonical summary 산출 | VIEW·META·ExternalIn 승격 |
| `IS-SELECT` | 검증된 CandidateSet과 policy allowlist에서 ID 선택 | 원시 view, 즉석 candidate 생성 |
| `IS-COMMIT` | 정규화 CommitPayload를 SSOT에 기록 | commit 밖 write, 원시 VIEW/META |
| `IS-POLICY` | view·요약을 바탕으로 next policy ref 산출 | ledger 규칙·Canon 입력축 변경 |

이전 문서의 4줄 module header가 이제 tick 내부의 구체 배선이 된다.

### 5.2 payload 대신 ref를 보낸다

후보팩과 정책팩은 payload를 직접 흘리지 않고 digest 기반 `ref`로 전달한다. PackStore는 같은 digest가 같은 immutable payload를 가리키는지 다시 hash해 검증해야 한다 `[SOC17:L32–40, L58–69, L138–160]`.

```text
payload를 직접 신뢰
→ ref를 전달
→ schema/version 검증
→ normalized payload 재hash
→ digest 일치 때만 load
```

이것은 내용이 참이라는 증명은 아니다. **전송 중 바뀌지 않았고 같은 입력을 다시 불러올 수 있다는 동일성·재현성 계약**이다.

```text
integrity / reproducibility
≠ source authenticity
≠ truth
```

### 5.3 정책 포인터는 META가 아니라 STATE다

`policy_act_ref`, `policy_next_ref`, candidate manifest pointer처럼 시스템이 실제로 따라야 하는 지시자는 감사용 META가 아니라 STATE로 강제된다 `[SOC17:L156–160, L203–298]`.

이 교정은 `Persistence ≠ Authority`를 조금 더 정밀하게 만든다.

- META 원문은 기본 deny지만 `audit_ref`는 CommitPayload에 허용된다. v1.0만으로 decision과 record가 분리된 것은 아니다 `[SOC17:L87–107]`.
- STATE pointer는 내용 자체가 아니라 검증된 pack의 active/next ref를 가리키며 writer는 commit-only다.
- Select가 act만 읽는 교정은 `CL17`, 명시적 `act←next` rotation assignment는 `CORE17`에서 닫힌다.

### 5.4 SKR은 이름에 residence·clock·scope를 붙인다

각 key는 label, axis, rate, writer, read scope, write scope를 가진다 `[SOC17:L180–201]`.

초기 최소 registry에는 lens·attention·damping·Γ·vitality와 active/next policy pointer, candidate manifest, external view, audit ref가 들어간다 `[SOC17:L203–339]`.

이것은 X/R/U/A Residence Law보다 강한 진전이지만 완성된 typed architecture는 아니다.

- `label`은 type이라기보다 분류 라벨이다.
- AuthorityGrant 같은 별도 권한 object는 없다.
- outcome·evidence·episode receipt key는 없다.
- `ExternalIn`은 오직 VIEW로만 등록된다.

### 5.5 v1.0도 같은 clock 오류를 반복한다

`SOC17`의 SelectIn은 다시 `Policy_{t+1} allowlist outputs`를 현재 선택 입력에 넣는다 `[SOC17:L32–46, L73–84]`.

Spine의 지연 원칙을 socket으로 옮겼지만, 이름 `t+1`만으로 실제 latch timing이 보증되지는 않았다. 두 ref는 `SOC17`에 이미 있었지만 SelectIn 식이 current/next read rule로 사용하지 못했다. `CL17`이 act-only/next-deny를 고정하고 `CORE17`이 명시적 rotation assignment로 마감한다.

---

## 6. Closure Tables v1.1 — “현재 읽기”와 “next 금지”를 표로 정의하다

### 6.1 표에 없으면 deny

`CL17`은 모든 socket input에 다음 기본 규칙을 적용한다.

```text
표에 없으면 deny
SKR에 없으면 deny
VIEW / META / raw ExternalIn은 Canon·Select·Commit에서 deny
PackRef는 검증 load 뒤에만 입력으로 인정
```

`[CL17:L9–32]`

금지문을 해석하는 사람이 아니라 build/linker가 연결 가능성을 판정하도록 바뀐다.

### 6.2 `Policy_{t+1}`를 active policy로 교정하다

v1.1은 앞선 두 문서의 clock ambiguity를 명시적으로 닫는다.

```text
현재 Select가 읽는 것
= S_t.policy_act_ref에서 load한 active allowlist

현재 Select가 읽지 못하는 것
= 같은 tick에 생성된 policy_next_ref
```

`[CL17:L28–39]`

> **[FUNCTIONAL CORRECTION]** v1.1은 현재 Select가 `S_t.policy_act_ref`만 읽고 `policy_next_ref`를 읽지 못한다고 정의한다. 두 pointer의 명시적 assignment equation은 뒤의 `CORE17`에서 처음 닫힌다.

### 6.3 Decision과 Record를 가르다

Commit 입력도 둘로 분리된다.

```text
CommitDecisionIn
  chosen candidate
  canonical impulse summary
  spend delta
  audit_ref (reference only)

CommitRecordIn
  policy_next_ref
  candidate_manifest_ref_next
```

두 집합 모두 commit에 도달할 수 있지만 Record field는 현재 ledger decision에 쓰일 수 없다고 선언한다 `[CL17:L121–159]`.

```text
recorded at commit
≠ evidence for the decision
≠ input to the decision
```

그러나 v1.1의 실제 schema에는 `audit_ref`가 아직 DecisionIn에 남아 있다. “참조일 뿐”이라는 설명은 있어도 decision code가 이를 읽지 못하게 하는 별도 read-cap은 없다.

> **[TYPE RESIDUE]** 역할 분리의 원칙은 생겼지만 field 배치는 아직 원칙을 끝까지 따르지 않는다. Core v1.2가 audit를 Record로 옮겨 이 부분을 교정한다.

### 6.4 후보 공간도 권한 레버다

선택 함수만 봉인해도 후보 집합을 누가 만들었는지 열려 있으면 결과를 사실상 조종할 수 있다.

```text
원하는 후보만 생성
→ deterministic Select
→ 원하는 결과
```

그래서 CandidateGen 산출은 `candidate_manifest_ref_next`로만 기록되고, 현재 Select는 `S_t`에 이미 고정된 `candidate_manifest_ref`만 읽는다 `[CL17:L161–198]`.

> **[DIRECT]** 후보 생성은 commit authority는 아니지만 미래 선택 공간을 바꾸는 실질적 influence다. 이 influence도 activation route와 delay를 가져야 한다.

원문은 이를 Candidate provenance라고 부르지만, 보장되는 것은 주로 ref·next-wire·활성 tick 추적이다. producer identity, source snapshot, authorship까지 증명하는 완전한 causal provenance는 아니다.

이 발견은 Ghost와 직접 동일하지 않다. 원문은 인간의 자발적 상상·rehearsal을 복원하지 않고, executable CandidatePack의 우회 레버를 봉인한다.

Chapter 04에서 복원한 `FULL15` Story 9c의 add-only next-candidate 기능과는 구조가 매우 가깝다 `[FULL15:L2725–2824, L2924–3027]`. 그러나 factory는 Story 9c를 source로 선언하지 않고 generic view/ExternalIn→CANDGEN 경로로 재정의한다.

> **[FUNCTIONAL REDISCOVERY][NON-ADOPTION]** 기능은 다시 나타나지만 직접 승계 계보는 확인되지 않는다.

---

## 7. Core v1.2 — 배선의 단일 진실

### 7.1 key 이름조차 신뢰하지 않는다

`CORE17`은 allow/deny 판정을 `key_id` 문자열이 아니라 다음 전체 record의 digest로 수행한다.

```text
KeyRec
= key_id
+ label
+ axis
+ rate
+ read_scope
+ write_scope
```

`[CORE17:L40–61]`

같은 이름을 붙인 뒤 scope만 바꾸는 우회까지 막으려는 조치다.

### 7.2 CandidateGen과 분리된 Commit이 여섯 소켓을 만든다

v1.0의 네 소켓 사이에서 암묵적이던 CandidateGen이 독립 interface가 된다 `[CORE17:L137–229]`.

```text
CANON
CANDGEN
SELECT
POLICY
COMMIT-DECISION
COMMIT-RECORD
```

CandidateGen은 view와 ExternalIn canonical form을 읽을 수 있지만 `CandidateManifestPack_ref_next`만 출력한다. 현재 Select는 active candidate manifest만 읽는다 `[CORE17:L172–208, L370–409]`.

이것이 NextWire다.

### 7.3 현재와 미래는 commit에서만 교대한다

```text
policy_act_ref_{t+1}
  := policy_next_ref_t

candidate_manifest_ref_{t+1}
  := candidate_manifest_ref_next_t
```

Canon과 Select는 `act`만 읽고 `next`는 읽지 못한다 `[CORE17:L441–468]`.

Core branch에서 두 rotation assignment가 처음 명시된다. 이를 Chapter 04가 미폐쇄로 남긴 `U_t` 실행과 `U_{t+1}` 생성의 구체화로 읽는 것은 이 장의 역사적 합성이지 원문의 직접 승계 선언은 아니다.

### 7.4 audit 기록 경로가 결정 경로와 갈라진다

Core는 `IS-COMMIT-DECISION`과 `IS-COMMIT-RECORD`를 별도 socket으로 둔다. v1.1의 DecisionIn에 있던 `audit_ref`는 Record로 이동하고, Record는 ledger delta나 선택을 바꾸는 연산을 할 수 없다 `[CORE17:L230–267, L290–309]`.

다만 `policy_next_ref`와 candidate next ref는 state rotation을 이유로 아직 `CommitDecisionIn_v1` field에 들어간다. audit 분리는 구조화됐지만 결정 계산과 불투명 pointer 복사의 type은 아직 한 schema 안에 있다.

Chapter 02와의 구조적 유비로 읽으면 durable non-authoritative trace에 구현 자리가 생긴다. 두 문서 사이의 source 승계 선언은 없다.

```text
durable record
≠ decision input
≠ warrant
```

이 마지막 `warrant` 비동일식은 현행 역조명이다. 원문이 공적 증거 이론을 완성했다는 뜻은 아니다.

### 7.5 v1.2a-SEAL — 봉인 뒤에도 발견된 세 우회

Core는 자신을 v1.2로 닫은 직후 세 개의 patch를 append한다 `[CORE17:L516–529]`.

1. `policy_next_ref`와 candidate next ref가 CommitDecisionIn에 있더라도 delta 계산에는 쓰지 못하고 pointer rotation에만 사용한다.
2. CandidateManifestPack에 원시 text·view를 넣어 미래 선택을 간접 조작하는 경로를 막는다.
3. `t_bio` 중간 적분값이 Shadow SSOT처럼 현재 결정에 새는 경로를 막는다.

`[CORE17:L530–600]`

중요한 것은 `SEALED`라는 말의 범위다.

> **[SCOPE LIMIT]** 원문이 `SEALED`라고 직접 열거한 범위는 rotation-ref payload, CandidatePack raw view, `t_bio` shadow 경로다. 이를 인간 이론·외부 증거·world outcome·self-boundary의 완성으로 확장할 수 없다.

### 7.6 현행 감사 렌즈에서 scope 밖이거나 미등재인 것

다음 항목은 Core가 명시적으로 해결하겠다고 약속한 뒤 실패한 것이라기보다, 현행 인간·증거 이론의 렌즈로 볼 때 **이번 registry scope 밖이거나 미등재인 것**이다.

- external source authenticity
- claim-specific evidence와 warrant
- Action 뒤 실제 world outcome receipt
- Episode·Narrative write gate
- Ghost 후보 내용과 Editor 호출 trace의 분리
- Belonging·Stake·Responsibility와 정당한 Authority
- CovState와 MeaningFlux의 명시 residence

또 하나의 내부 긴장도 남는다. Canon socket은 active policy와 `PolicyConstraintsPack`을 읽을 수 있다 `[CORE17:L154–170, L321–349]`. Policy가 검색·노동 배치만 바꿔야 한다면, canonical impulse가 policy 내용에 얼마나 의존할 수 있는지 별도 algebra가 필요하다. 이 경계는 이 지층에서 닫히지 않는다.

### 7.7 `SEALED` 안에 남은 version·registry 충돌

v1.2a의 봉인 선언만 읽으면 공장 전체가 하나의 정합 schema로 닫힌 듯 보인다. 실제 append 지층에는 다음 잔차가 남는다.

| 잔차 | 실제 상태 |
|---|---|
| 같은 `SKR v0.2` | Socket판의 `V_caps=t_commit/FAST`가 Core판에서 `t_bio/SLOW`로 바뀌고 LEDGER·next manifest key가 추가되지만 version bump·migration 없음 `[SOC17:L247–285; CORE17:L492–512]` |
| `PolicyConstraintsPack` | Canon은 이를 입력으로 요구하지만 Core 최소 SKR에는 명시 source ref가 없음 `[CORE17:L154–164, L492–512]` |
| CANDGEN의 view input | interface는 `K.view.*`를 허용하지만 Core 최소 SKR에는 concrete VIEW key와 CANDGEN read scope가 없음 `[CORE17:L172–189, L492–512]` |
| Gate D | Full Spec에서는 cache equivalence, BIO-SEAL에서는 Shadow SSOT 실패를 같은 Gate D로 부름 `[FS17:L397–405; CORE17:L581–589]` |
| rotation ref | payload read는 금지됐지만 field는 여전히 `CommitDecisionIn_v1` 안에 있음 `[CORE17:L290–309, L544–560]` |

> **[REAL CONFLICT][TYPE RESIDUE]** 후기 patch는 유효 의미를 좁혔지만 낡은 식과 schema를 물리적으로 제거하지 않는다. append-only 보존과 executable effective manifest가 별도로 필요해진다.

또한 이 문서군에는 실제 linker program의 실행 결과나 test report가 없다. 따라서 말할 수 있는 것은 **검사 가능한 spec을 만들었다**는 것이지, 모든 구현이 그 검사를 통과했다는 사실이 아니다.

```text
spec closure
≠ verified implementation closure
```

---

## 8. v0.5-STG — 후기 branch가 같은 문제를 하나의 전이로 접다

### 8.1 단일 전이 `F`

`STG17`은 자신을 v0.5-STG 단일 전이 정본으로 제시하며, 유사한 규율과 인간 module을 하나의 함수로 독립 재정렬한다 `[STG17:L3–8]`. Core의 literal merge나 declared descendant는 아니지만 보존 시각상 마지막 unified runtime이므로 기능적 종점에서 비교한다.

```text
(S_{t+1}, ActionOut_t, ViewOut_t)
= F(S_t, X_t, Mark_x)
```

`F` 밖에서는 SSOT를 갱신할 수 없고, `policy_{t+1}`도 별도 writer가 아니라 `S_{t+1}`에 함께 기록되는 산출물이다 `[STG17:L378–389]`.

내부 전개는 Intake, dual projection, View, Propose, Select, Control, Commit, ActionOut을 한 tick에 배치한다 `[STG17:L390–447]`.

이것은 중요한 성취다.

- 모든 상태 변화에 단일 외부 경계를 준다.
- current `policy_t`와 next `policy_{t+1}`를 표면상 분리한다.
- View는 `CtrlSolveFn`을 통해서만 next policy에 닿는다.
- ActionOut도 상태 전이와 함께 명시적 output이 된다.

### 8.2 인간 현상이 실행 surface에 함께 놓인다

v0.5-STG branch는 배선형 규율만 쓰지 않는다. Chapter 04에서 보았던 것과 기능적으로 유사한 인간적 surface들도 runtime spec 안에 넣는다.

- Coverage와 CacheSpan을 처리 가능 범위와 내부 도달 범위로 둔다.
- Priority를 시간·거리·alignment·policy의 scheduling으로 둔다.
- 기자/바둑돌 은유를 선택의 placement 규칙으로 번역한다.
- Joy·Lucidity·ActReady를 원인이 아닌 계기판으로 둔다.
- 리듬과 alignment를 위상오차 제어로 둔다.

`[STG17:L184–236, L309–359]`

> **[FUNCTIONAL REDISCOVERY]** Chapter 04의 Coverage·Priority·기자·행복·정렬 기능이 실행 정본의 surface로 다시 나타난다. 그러나 `STG17`은 RATION을 declared source module로 적지 않으므로 직접 source 승계라고 확정하지 않는다.

이 인간적 개념들은 STG 안에서 모두 같은 방식으로 배치되지는 않는다.

```text
Coverage / CacheSpan : SSOT state 또는 state update 대상
Priority             : policy scheduling
Joy / Lucidity       : ViewOut
Alignment            : next-policy influence
Action               : F의 external output
```

STG branch는 인간 현상을 서로 다른 residence와 transition에 재배치하려 한다. evidence와 outcome은 없고, Narrative는 “서사 binding”이라는 이름으로 Memory/Cache의 phys-authority block에 들어갈 뿐 별도 residence·writer·write gate를 갖지 않는다 `[STG17:L94–103]`.

### 8.3 Core 대응 봉인이 STG 실행면에 보이지 않는 곳

그러나 v0.5-STG는 core/socket spec을 그대로 펼친 것이 아니다.

#### A. Candidate NextWire 대응 봉인이 없다

```text
Cand_t := ProposeFn(S_t, PercIn_t, policy_t)
Choice_t := SelectFn(Cand_t, SelectIn_t)
```

같은 tick에 생성한 후보를 같은 tick에 선택한다 `[STG17:L237–264, L406–420]`.

`CORE17`의 `candidate_manifest_ref_next → commit rotation → next tick active` 경로에 대응하는 봉인은 STG 실행면에서 보이지 않는다.

> **[CROSS-BRANCH COMPARATIVE OMISSION]** NextWire가 공식 폐기·승계되었다는 migration 문장은 없다. 다만 STG 실행 전개만 구현하면 Core 기준의 candidate delay에 대응하는 봉인이 없다.

#### B. Record가 Commit과 한 signature에 놓인다

v0.5는 `Record → Decision`은 금지하지만 `CommitFn`의 인자에는 `Record_t`가 들어간다. CommitFn이 Record에서 무엇을 읽을 수 없는지 read-cap이 없다 `[STG17:L265–305]`.

```text
Record cannot alter Decision
≠ Record cannot alter committed state
```

따라서 STG signature는 Core 비교 기준보다 Decision/Record read-cap을 덜 명시적으로 제한한다.

#### C. `policy_{t+1}`가 rotation parameter인지 state delta input인지 불명확하다

`CommitFn(..., policy_{t+1})`는 next policy를 `S_{t+1}.Policy`에 latch하려는 의도다. 하지만 v1.2a-SEAL처럼 payload가 ledger/state delta 계산에서 금지된다는 signature 규율은 없다 `[STG17:L279–305, L421–439]`.

#### D. policy-shaped perception이 phys 판정으로 들어간다

TR은 `policy_t`를 입력으로 `PercIn_t`를 만들고, `Π_phys`와 `ResidualFn`은 그 PercIn을 읽는다. `ΔQ⊥` 식에는 `policy_t`가 직접 들어간다 `[STG17:L119–183]`.

```text
policy_t
→ TR / PercIn_t
→ PhysSig_t / ΔQ⊥_t
→ Commit
```

문제는 policy가 “physical evidence”를 바꾼다고 단정할 수 있다는 것이 아니라, **evidence type 자체가 없다**는 데 있다. policy-shaped PercIn은 PhysSig·ΔQ⊥뿐 아니라 CommitFn의 직접 인자로도 들어가며, 어느 field가 state delta에 허용되는지 read-cap이 없다 `[STG17:L119–183, L279–305, L421–439]`.

#### E. Action은 생겼지만 outcome은 없다

`ActionOut_t`는 `F`의 output이지만 `S_{t+1}`은 실제 world response가 돌아오기 전에 같은 전이에서 만들어진다. Action receipt, outcome receipt, attester, 이후 authorized state update가 없다 `[STG17:L378–447]`.

```text
Decision / ActionOut
≠ action occurred in the world
≠ world outcome
≠ evidence for persistent update
```

Chapter 04-A가 요구한 outcome lane은 아직 열리지 않았다.

#### F. PackRef 검증의 책임 stage가 없다

v0.5의 Gate C1은 검증된 PackRef만 입력으로 인정한다고 선언한다. 그러나 단일 전이 `F`의 내부 전개에는 ref load, schema check, digest 재검증 단계나 그 책임 stage가 없다 `[STG17:L360–376, L390–447]`.

> **[CROSS-BRANCH COMPARATIVE OMISSION]** STG에는 verified-PackRef 요구만 있고, Core의 explicit PackStore/load/schema/digest-rehash 계약에 대응하는 실행 stage는 보이지 않는다.

#### G. Candidate가 닫힌 SelectIn 옆문으로 들어온다

v0.5는 SelectIn을 `S_t + CanonFn(S_t) + Allow(policy_t,S_t)`로 닫았다고 말한다. 하지만 실제 `SelectFn`은 별도 인자 `Cand_t`도 받는다.

```text
Cand_t := ProposeFn(S_t, PercIn_t, policy_t)
Choice_t := SelectFn(Cand_t, SelectIn_t)
```

`[STG17:L237–264]`

따라서 SelectIn allowlist만 검사해서는 후보 내용의 출처와 세탁 경로를 닫을 수 없다. Core의 manifest ref·NextWire가 보이지 않으면서 TR와 policy allowlist를 거친 `PercIn_t`가 후보 형성으로 들어오는 옆문이 생긴다.

#### H. 커밋된 Decision과 실제 ActionOut이 갈라질 수 있다

`Decision_t`는 Commit에 쓰이지만 `ActionOut_t`는 Decision이 아니라 `Choice_t`, `policy_t`, `Gate_Action`에서 별도로 만들어진다 `[STG17:L421–447]`.

```text
Decision_t := DecisionFn(Choice_t, S_t)
ActionOut_t := ActionFn(Choice_t, policy_t, Gate_Action(...))
```

더 직접적인 틈은 `Gate_Action`이 Commit 뒤의 ActionOut 계산에만 등장한다는 점이다. Gate가 행동을 막거나 바꾸어도 `Decision_t`를 사용한 상태 commit은 이미 일어날 수 있다. ledger에 인수된 결정과 실제 출력·실제 행동을 묶는 action receipt나 shared action id가 없다.

#### I. Narrative binding의 residence가 모호하다

v0.5의 `S_t.Memory/Cache`에는 cache·coverage와 함께 “서사 binding”이 들어가며 모두 phys authority 아래라고 적힌다. 동시에 Canon과 Select는 넓은 `S_t`를 입력으로 받는다 `[STG17:L92–103, L248–255]`.

```text
Narrative binding inside authoritative S_t
≠ separately typed Narrative view/readout
```

Narrative binding의 writer·schema·read scope가 별도로 갈리지 않으므로 어떤 서사 흔적이 단순 persistence인지 canonical decision input인지 모호하다. 이는 Narrative write gate가 아직 없다는 판정을 강화한다.

### 8.4 ExternalIn은 들어왔지만 evidence는 아니다

v0.5-STG는 `X_t`와 marker를 TR로 받아 `PercIn_t`를 만든다. 그러나 TR은 policy allowlist를 따르는 perc 경계이고, source authenticity·witness schema·attestation이 없다 `[STG17:L92–138]`.

외부가 내부 계산에 들어오는 길은 생겼지만, **무엇이 단순 자극이고 무엇이 판정 근거인가**는 분리되지 않는다.

### 8.5 실행 정본의 성취와 실패를 함께 보존한다

v0.5-STG는 실패한 문서가 아니다. 단일 writer와 current/next policy의 큰 골격을 인간 현상 module들과 한 함수 안에서 독립적으로 표현한다.

Core branch와 기능별로 비교하면 서로 다른 장단점이 선명하다.

```text
Core branch : 세밀한 key-level closure와 여러 명시 봉인
STG branch  : 읽기 쉬운 single-transition runtime과 인간 surface
비교 결과   : STG 실행면에는 몇몇 no-touch/read-cap/NextWire 대응 봉인이 보이지 않음
```

이 장의 종점은 완성된 런타임이 아니라, **이론을 실행 가능한 한 줄로 만들수록 그 한 줄 안의 증거·시간·기록 권한을 다시 타입으로 쪼개야 한다는 사실이 드러난 순간**이다.

---

## 9. 역사 본문의 결론 — 통합은 합치기가 아니라 링크 허가였다

0117 공장의 실제 변화는 다음과 같다.

```text
9U 한 문장
→ 해석·적용 우선순위 Spine
→ 본문보다 경계를 먼저 두는 Skeleton
→ Registry-First
→ SKR와 module interface
→ payload 대신 검증된 ref
→ key-level allow/deny
→ active / next pointer 분리
→ Candidate route seal과 NextWire
→ Decision / Record socket 분리
→ v1.2a-SEAL

후기 평행 STG branch
→ 같은 문제군의 single-transition F
```

가장 큰 발명은 특정 함수가 아니다.

> **문서가 존재한다는 사실과 그 문서가 실행에 참여할 권한을 분리한 것.**

Append-only는 모든 과거 문장을 같은 순간에 실행하라는 명령이 아니었다. 과거는 보존하되, 현재 runtime에 들어오는 경로는 registry와 interface와 closure가 결정한다.

그래서 Chapter 02의 문장이 이 장에서 한 번 더 변형된다.

```text
Persistence ≠ Authority

에서

Preservation ≠ Adoption ≠ Executable participation

으로
```

후자의 식은 이 장의 역사적 합성이다. 원문이 이 정확한 세 항을 한 줄로 선언하지는 않았다.

동시에 공장은 자기 한계도 드러냈다.

- input을 닫는 것과 evidence를 정의하는 것은 다르다.
- payload integrity와 truth는 다르다.
- deterministic choice와 legitimate choice는 다르다.
- Decision record와 world outcome은 다르다.
- 하나의 `F`와 완성된 인간·생명 이론은 다르다.

0118은 바로 이 남은 틈에서 시작한다. 그것은 더 좋은 linker를 만드는 데서 멈추지 않고, policy가 오염할 수 없는 Witness, raw/eff 분리, Receipt→σ→Bill이라는 새 상태 ontology를 요구한다.

---

# 연구 후기 — 현재 이론으로 역조명하되 0117에 소급하지 않기

## A1. 이번 장에서 실제로 수거된 것

### A1.1 통합은 의미의 합성이 아니라 실행 참여 자격의 배분이다

이번 장의 가장 큰 수확은 새로운 인간 변수가 아니다.

```text
과거 문장 보존
≠ 현재 정본 채택
≠ 실행 graph 연결
≠ state transition authority
```

Registry-First는 append-only 연구가 겪는 근본 문제를 푼다. 과거의 실패·충돌·다른 가지를 삭제하지 않으면서도, 현재 runtime이 무엇을 실제로 읽고 쓰는지는 제한할 수 있다.

이는 편집 규율이면서 존재론적 구분이다. **무언가가 기록 속에 존재한다는 것과 현재 변화의 원인으로 작동한다는 것은 다르다.**

### A1.2 Authority는 값의 속성보다 허용된 경로의 성질이다

이 시기 문서는 Authority를 SSOT/commit에 있다고 말한다. 그러나 실제 공장이 한 일은 “SSOT”라는 이름에 권위를 붙이는 것만이 아니다.

```text
Authority at transition τ
= registered key
+ allowed read scope
+ allowed writer
+ allowed clock
+ closed input graph
+ passing gate
```

이 식은 연구 후기의 합성이다. 원문은 하나의 type으로 쓰지 않았지만, key record와 closure table은 이미 이 방향을 향한다.

따라서 `Residence ≠ Authority`는 다음처럼 더 세분된다.

```text
값이 저장됨
≠ 어느 함수나 읽을 수 있음
≠ 결정에 사용할 수 있음
≠ 상태를 쓸 수 있음
≠ 그 결정이 정당한 근거를 가짐
```

### A1.3 후보 생성은 중립적 전처리가 아니다

선택 알고리즘이 완전히 결정론적이어도 후보 집합을 누가 만들었는지 열려 있으면 결과는 조작될 수 있다.

```text
Candidate space
→ feasible choice space
→ selected action
```

그래서 CandidateGen은 commit writer가 아니면서도 강한 influence를 가진다. Core는 이 influence를 없애지 않고 next-only로 지연시키며 route와 activation tick을 추적할 수 있는 manifest ref로 만든다.

다만 이 ref는 producer identity·source snapshot·authorship을 필수로 담지 않는다. 그러므로 여기서의 provenance는 **causal provenance 전체가 아니라 route/integrity provenance**로 한정한다.

이것은 현행 `Influence ≠ Warrant`에 중요한 보강이다.

> influence는 warrant가 아니지만, warrant가 아니라고 추적 대상이 아닌 것은 아니다.

### A1.4 기록과 결정은 같은 transaction 안에서도 다른 역할이다

Chapter 02가 `Event ≠ Commit`을 발견했다면, 이번 장은 commit 내부에서도 다음을 가른다.

```text
결정을 계산하는 입력
≠ 다음 tick pointer를 회전시키는 parameter
≠ 감사·재현을 위해 남기는 record
```

한 transaction 안에 함께 들어온다고 같은 권한을 갖는 것이 아니다. v1.2a-SEAL이 rotation ref를 DecisionIn에서 의미상 다시 격리한 이유가 여기에 있다.

### A1.5 결정론은 truth가 아니라 감사 가능성이다

No-RNG, perm-invariant, normalized serialization, fixed hash, immutable PackStore는 같은 입력으로 같은 결과를 재현하게 한다.

그러나 다음은 여전히 다르다.

```text
reproducible ≠ true
digest-matched ≠ authentic source
deterministic ≠ legitimate
internally closed ≠ externally adequate
```

공장은 integrity와 route reproducibility를 강화했지만 evidence와 truth를 아직 만들지 않았다.

### A1.6 강한 closure는 인식의 굶주림을 만들 수 있다

v0.4b–Core branch는 ExternalIn을 VIEW로 제한하되 POLICY/CANDGEN의 influence port는 남긴다. 후기 STG branch에는 `X_t→TR→PercIn→PhysSig/Commit` 경로가 있다. 두 branch 어디에도 **policy-independent·attestable grounds/evidence 전용 port**는 없다.

이 장이 새로 보여준 설계 원칙은 다음이다.

> 권한 없는 입력을 막는 것만으로는 충분하지 않다.  
> 세계가 실제로 남긴 흔적을 권한과 분리된 evidence로 받아들이는 port도 필요하다.

후대 0118이 바로 이 공백과 유사한 문제를 Witness 계열로 다룬다고 이 장의 연구 후기가 역조명한다. 0117 문서가 그 인과를 source로 선언한 것은 아니다.

---

## A2. 계보 등급 — 무엇이 현행 구조를 선행하고 무엇은 아직 유비인가

| 0117 요소 | 판정 | 이유 |
|---|---|---|
| 9U의 readout same-tick 역류 금지 | `강한 구조적 선행` | 현행 Influence/Warrant 분리와 typed transition wall을 선행. 직접 승계는 별도 확인 필요 |
| Registry-First | `강한 편집·실행 선행` | 보존된 문서와 adopted runtime semantics를 분리 |
| SKR read/write scope | `typed authority의 선행 구조` | key residence와 transition access를 함께 기록하지만 AuthorityGrant type은 아직 없음 |
| active/next pointer와 commit rotation | `강한 clock 선행 구조` | 현재 실행과 future candidate-set activation lane을 실제 state pointer로 분리 |
| Candidate route seal / NextWire | `강한 문제 선행 구조` | 후보 발견 influence를 same-tick decision에서 격리. source/authorship provenance는 아님 |
| Decision / Record | `EventRecord 분해의 선행 구조` | 결정 입력과 감사 기록을 분리하지만 outcome·attestation은 없음 |
| PackStore digest | `integrity 계보` | content identity와 재현성. evidence authenticity는 아님 |
| Single transition `F` | `typed transition의 강한 선행 구조` | state update의 외부 경계를 하나로 만들지만 내부 타입은 다시 뭉침 |
| CandidateGen | `Ghost와 기능적 유비` | 가능성 생성 역할은 닮지만 자발성·rehearsal·자기 서사 계약 없음 |
| Module Registry | `self-boundary와 구조적 유비` | 무엇이 내부 실행에 참여하는지 가르지만 정신적 자기 경계의 직접 계보는 아님 |

### 계보 봉인

```text
Registry ≠ self-boundary
CandidateGen ≠ Ghost
CommitRecord ≠ EventRecord
PackDigest ≠ Evidence
Determinism ≠ Warrant
Runtime Authority ≠ authority over another person
```

---

## A3. Interchapter Note 04-A 감사 카드 결과

| # | 04-A 질문 | 0117 판정 |
|---:|---|---|
| 1 | 지속값마다 writer·clock·scope가 있는가 | `부분 해결` — SKR에 들어간 key는 명시, 전체 인간 state는 미등재 |
| 2 | State/Readout/Policy/Receipt/AuthorityGrant가 갈리는가 | `미해결(선행 구조만)` — label/pointer는 갈리지만 label은 type이 아니며 Receipt·AuthorityGrant 없음 |
| 3 | 지속·강도·회계에서 truth/authority를 추론하는가 | `branch별 부분 봉인` — Core는 VIEW/META의 decision 승격을 막지만 STG는 PercIn·Record·policy_next의 Commit read-cap이 열려 있고 truth/evidence는 미정 |
| 4 | 현재 실행이 latched `Policy_t`를 쓰는가 | `branch별 부분 해결` — Core Canon/Select는 act-only. STG Select/Action은 policy_t지만 CommitFn은 policy_next를 받아 delta read-cap 미폐쇄 |
| 5 | 새 readout은 `Policy_{t+1}`에만 닿는가 | `미해결/분기` — Core는 view→policy_next뿐 아니라 candidate_next도 허용하고, STG는 PercIn→same-tick Cand·PhysSig·Commit 경로를 가짐 |
| 6 | timebase와 transition lane을 구별하는가 | `부분 해결` — 세 timebase와 active/next pointer 병존 |
| 7 | CommitCheckTick의 정확한 지위 | `미해결/비채택` |
| 8 | 후보·호출·전략·실행·결과가 분리되는가 | `후보·정책·선택·Action은 부분 분리`, 호출·outcome 없음 |
| 9 | Ghost content와 compute/call trace를 함께 표현하는가 | `미해결` |
| 10 | Editor proposal의 same-tick action 침투를 막는가 | `유비 수준 부분 해결` — CandidateGen/Propose를 Editor proposal에 비유할 때 Core는 next-only지만 Editor/Action type은 없고 STG는 same-tick Propose→Select |
| 11 | Action receipt와 world outcome receipt가 갈리는가 | `미해결` — 둘 다 없음 |
| 12 | 노출·행동·결과·저자성·미청산을 가르는가 | `미해결` |
| 13 | Episode→Narrative 별도 gate가 있는가 | `미해결/비채택` |
| 14 | formed/felt/endorsed/responsible/authorized가 갈리는가 | `미해결/비채택` |
| 15 | self-boundary가 타자 Authority로 승격되지 않는가 | `대상 자체가 없음`; runtime Authority를 인간 관할권으로 읽으면 안 됨 |
| 16 | Story 9c와 RATION shaping 중 무엇을 채택하는가 | `branch별 상이·채택 미확정` — Core branch에는 두 generic route가 각각 있으나 STG에서는 candidate delay가 보이지 않음. Story/RATION 채택 판정 불가 |
| 17 | UL·IE15 비채택을 공식 폐기로 오인하지 않는가 | `문서가 판정하지 않음`; registry 미등재만 확인 가능 |
| 18 | Story omission/capability가 복구되는가 | `interface 수준 부분·승계 미확정` — Core에 유사 generic 경로가 있으나 concrete VIEW/CANDGEN SKR closure가 없고 STG에서는 next delay도 보이지 않음 |
| 19 | CovState·MeaningFlux residence/writer가 정해지는가 | `미해결/비채택` |
| 20 | 물리 경계와 정신적 self-boundary 연결 조건 | `미해결` |
| 21 | life에 stake·body accounting·repair·reproduction 중 무엇이 필요한가 | `ledger/repair 일부만`, life 정의 없음 |
| 22 | Extended/Coupled/Collective Self를 가르는가 | `미해결` |
| 23 | 집단 패턴에서 희생 정당성을 도출하는가 | `대상 없음`; 어떤 규범적 결론도 회수 불가 |

이번 감사에서 가장 선명한 것은 공장이 04-A의 **A–C 영역 일부만** 닫았다는 점이다. residence·transition·candidate influence는 크게 진전했지만 Episode·Narrative·self-boundary·life는 해결한 것이 아니라 executable registry 밖에 남겨두었다.

---

## A4. 새 Bridge I — 자기 경계는 Narrative 등고선과 실행 capability map의 교차일 수 있다

Interchapter Note 04-A는 자기 경계를 누구의 미래·손상·연속성이 나의 유지에 들어오는가라는 Narrative readout으로 잡았다. 이번 공장은 다른 종류의 경계를 보여준다.

```text
Narrative self-boundary
  무엇을 나의 손실·미래·책임처럼 느끼고 인수하는가

Execution capability boundary
  어느 state·candidate·policy가 어느 transition을 읽고 쓸 수 있는가
```

> **[BRIDGE]** 실제 자기 모델에는 두 경계가 모두 필요할 수 있다.

- Narrative 경계만 있으면 “내 것처럼 느껴짐”이 곧 행동 권한으로 승격될 수 있다.
- capability 경계만 있으면 실제 경험이 무엇을 소중하게 만들고 어떤 미래를 인수하게 했는지 사라진다.

```text
felt inclusion
≠ executable adoption
≠ valid authority
```

가족이 자기 경계 안에 있어도 타자를 통제할 capability나 정당한 Authority가 자동 생기지 않는 이유도 이 두 경계를 분리하면 더 정확히 표현할 수 있다.

이것은 0117 원문의 직접 인간 이론이 아니다. 공장의 registry/closure 구조와 04-A의 자기 경계를 결합한 새 Bridge다.

---

## A5. 새 Bridge II — Ghost의 자유와 Editor의 채택 사이에 linker가 필요하다

Ghost-space에는 극단적이고 모순된 후보가 존재할 수 있다. 이번 장의 언어로 옮기면 다음 비동일식이 생긴다.

```text
candidate exists
≠ candidate registered for execution
≠ strategy latched
≠ action authorized
≠ outcome occurred
```

> **[BRIDGE]** Editor의 핵심 역할 중 하나는 내용을 “좋다/나쁘다”라고 판정하는 것만이 아니라, Ghost 후보를 어떤 scope의 실행 proposal로 링크할지 결정하는 것일 수 있다.

그러나 공장의 CandidateGen을 그대로 Ghost라 부를 수는 없다.

- CandidateGen에는 spontaneous/invoked 구분이 없다.
- rehearsal·주의 반복·call trace가 없다.
- 후보가 누구의 자기 서사에서 왔는지 없다.
- 선택 뒤 body veto와 world outcome이 없다.

공장이 제공한 것은 Ghost의 내용이 아니라 **후보가 존재하는 것과 실행 graph에 채택되는 것을 분리할 linker 문법**이다.

---

## A6. 새 Bridge III — 생명 경계는 default-deny만으로 유지되지 않는다

0117 공장은 “표에 없으면 deny”로 형태를 보호한다. 이는 생명을 선택적 투과 경계로 보는 가설과 닮는다.

하지만 살아 있는 경계는 모든 외부 flux를 VIEW로 격리할 수 없다.

```text
완전 개방
→ 내부 형태가 외부 변화에 즉시 덮어쓰임

완전 폐쇄
→ 새로운 증거·자원·손상·학습을 편입할 수 없음

선택적 투과
→ source를 검사하고, 서로 다른 port로 편입하며,
   결과와 비용을 거쳐 state를 갱신
```

> **[BRIDGE]** 생명 경계에는 최소 두 종류의 intake가 필요할 가능성이 크다.

1. 판단 grounds가 될 수 있는 policy-independent evidence intake
2. 의미·전략·주의를 바꾸는 policy-shaped influence intake

Core branch는 view-derived influence를 `policy_next`와 `candidate_next`로 지연시키려 했지만 STG branch는 policy-shaped PercIn을 same-tick Cand·PhysSig·Commit에 넣는다. 따라서 0117은 influence intake를 일관되게 next-only로 제한하지도, policy-independent evidence intake를 만들지도 못했다. 강한 closure는 형태 보존의 필요조건일 수 있어도 충분조건은 아니다.

---

## A7. 형식화하며 얻은 것과 잃은 것

| 얻은 것 | 약해지거나 빠진 것 |
|---|---|
| 적용 우선순위와 append-only 보존의 공존 | 개념이 왜 인간에게 필요했는지의 체험 맥락 |
| Registry-First | registry 밖에 남은 branch의 의미 있는 잔차 |
| key-level scope와 default deny | 외부 증거를 받아들이는 양의 계약 |
| active/next pointer | 생물학적·체험적 시간의 질감 |
| Candidate route/integrity | spontaneous thought·rehearsal·Editor authorship·source provenance |
| Decision/Record split | Action·world outcome·repair·settlement |
| deterministic PackStore | source authenticity와 truth |
| single transition F | 내부 단계 사이의 typed no-touch 세부 |

공장이 인간다움을 제거하려 했다고 읽을 필요는 없다. 오히려 인간적 module을 안전하게 다시 넣기 위해 빈 소켓을 먼저 만든다. 다만 실제로 이번 지층이 끝날 때까지는 **소켓이 인간 현상보다 훨씬 더 완성되어 있다.**

---

## A8. 이 장에서 확정된 충돌·교정·비채택 지도

| 쟁점 | 판정 |
|---|---|
| Addendum/Socket의 current SelectIn에 `Policy_{t+1}` | `[REAL CONFLICT]` — 9U delay 위반 가능 |
| Closure v1.1의 `policy_act_ref` 교정 | `[FUNCTIONAL CORRECTION]` |
| CandidateGen의 next-only manifest | `[DIRECT]` — 후보 influence의 route/delay 봉인 |
| Core DecisionIn 안의 next refs | `[TYPE RESIDUE]` — SEAL이 rotation-only로 의미 제한, 물리 type은 미분리 |
| v0.4b–Core branch의 ExternalIn=VIEW | `[OVER-CLOSURE]` — POLICY/CANDGEN influence는 허용하지만 grounds/evidence 전용 port 없음 |
| STG branch의 policy-shaped TR→PhysSig/Commit | `[OPEN]` — 외부 입구가 있으나 authenticity·evidence type·read-cap 없음 |
| active policy/PolicyConstraints의 Canon read | `[OPEN]` — search policy와 canonical grounds 경계 미폐쇄 |
| v0.5 같은-tick Propose→Select | `[CROSS-BRANCH COMPARATIVE OMISSION]` — Core의 NextWire에 대응하는 봉인 미표시, 직접 승계·rollback 선언 없음 |
| v0.5 CommitFn의 Record·PercIn·policy_next 입력 | `[CROSS-BRANCH COMPARATIVE OMISSION][OPEN]` — Core 기준의 read-cap 미표시 |
| RATION·Story 9c source attribution·Ghost·self-boundary | `[NON-ADOPTION]` — generic next-candidate 기능은 재등장하지만 직접 승계·폐기 선언 없음 |
| `FUULL`, `fornext` | `[EXACT REPACKAGING]` — 새 발명으로 중복 계상 금지 |

---

## A9. Recovered / Lineage / Residue / Bridge / Open

### Recovered — 원문에 직접 있었던 것

- 9U 한 문장을 최상위 실행 헌법으로 둔 것
- 최신성보다 closure 역할을 우선하는 Spine
- 삭제 없이 적용권을 제한하는 append-only merge 규율
- authority·timebase·determinism·closure를 본문보다 먼저 두는 Skeleton
- read/output/no-touch/write 네 줄 interface
- Shadow SSOT와 result-changing cache 금지
- Registry 미등재 본문의 executable 참여 금지
- fixed serialization/hash와 immutable PackStore
- active/next policy·candidate pointer와 commit-only rotation
- key-level allow/deny와 “표에 없으면 deny”
- Candidate route seal과 NextWire
- Commit Decision/Record 분리
- v1.2a의 rotation ref·candidate payload·t_bio intermediate seal
- 하나의 상태 전이 `F`

### Lineage — 현행과 구조적으로 이어지는 선행(직접 승계 미확정)

- `Influence ≠ Authority`
- `Persistence ≠ executable authority`
- transition별 read/write capability
- current state와 future proposal의 latch 분리
- 후보 생성 influence의 route·activation provenance
- 결정·기록·회전의 역할 분리
- single-writer와 typed transition boundary
- content-addressed integrity와 deterministic replay

### Residue — 다음 이론이 다시 받아야 할 것

- external evidence와 source authenticity
- actual Action과 world Outcome의 receipt
- claim-specific evidence와 warrant
- compute cost·Editor call trace·rehearsal
- Episode·Narrative·settlement
- CovState·MeaningFlux의 residence
- 자기 경계와 valid interpersonal Authority
- 사랑·리듬·행복·활력의 인간적 설명

### Bridge — 이번 독해에서 새로 얻은 가설

- 자기 경계는 Narrative 등고선과 execution capability map의 교차일 수 있다.
- Editor는 Ghost 후보를 execution proposal로 링크하는 제한된 linker일 수 있다.
- 생명 경계에는 evidence intake와 influence intake가 서로 다른 port로 필요할 수 있다.
- 보존된 과거가 현재 행동을 자동 지배하지 않는 구조는 개인 Narrative 편집에도 적용될 수 있다.

### Open — 다음 장에서 확인할 질문

1. 외부 input을 policy가 오염할 수 없는 Raw/Witness로 받는 port가 생기는가?
2. `Policy_t`는 대응만 바꾸고 evidence/ResidualRaw는 바꾸지 못하도록 algebra가 갈리는가?
3. Commit에서 Evidence, Ledger, future payload가 서로 다른 read-cap을 갖는가?
4. next policy와 candidate proposal은 pointer rotation 외 state delta 계산에서 완전히 사라지는가?
5. Decision/Action 뒤 world outcome과 attestation이 생기는가?
6. 즉시 완화의 비용을 미래에 청구하는 Receipt·debt·settlement가 생기는가?
7. registry 밖 현상학은 안전한 load slot으로 돌아오는가?
8. runtime Authority와 Grounds/Warrant, 타자에 대한 valid Authority가 더 분리되는가?

---

## A10. 다음 장 경계 — 0118은 더 좋은 공장이 아니라 새로운 헌법이다

0118을 이 장에 붙이지 않은 이유는 날짜가 바뀌어서가 아니다. 중심 문제가 달라지기 때문이다.

```text
Chapter 05
어떻게 문장을 안전한 실행 배선으로 조립할 것인가?

Chapter 06
무엇이 판정의 grounds이며,
표면 조작의 차익은 어떻게 미래에 청구되는가?
```

0118은 다음을 새로 도입한다.

- policy-independent Witness
- `Π_wit / Π_view`
- `ΔQ⊥_raw / ΔQ⊥_eff`
- Receipt 또는 pledge
- 미해결 응력 `σ`
- 미래 청구 `Bill`
- Grounds와 Influence의 독립 검사

이는 0117 공장의 단순 patch가 아니다. 공장이 닫지 못한 외부 evidence와 policy 오염 문제를 새 상태 ontology로 다시 푸는 다음 장이다.

따라서 이 장은 v0.5-STG의 `F`에서 멈춘다.

> **문서를 하나의 전이로 만드는 데는 성공했다.  
> 이제 그 전이가 무엇을 근거로 세계를 갱신하는지 물어야 한다.**

---

## 부록 A. 출처 별칭

| 별칭 | 경로 | 행수 | 핵심 역할 |
|---|---|---:|---|
| `SP17` | `연구/통합을 위한 공장/0117 spine` | 175 | 9U·우선순위 Spine |
| `SK17` | `연구/통합을 위한 공장/0117 skeleton` | 226 | Assembly Skeleton |
| `MIM17` | `연구/통합을 위한 공장/0117 모듈 인터페이스` | 134 | Module Interface Manifest |
| `SS17` | `연구/통합을 위한 공장/0117 spineskeleton+수정 합침 1` | 315 | v0.3c 통합 rewrite |
| `C04B17` | `연구/통합을 위한 공장/0117 canon` | 317 | Executable Canon v0.4b |
| `MF17` | `연구/통합을 위한 공장/0117 manifest` | 201 | Build Step v0.4c |
| `FS17` | `연구/통합을 위한 공장/0117 spineskeletonmanifest 1` | 561 | Full Spec v0.4d + Addendum A |
| `SOC17` | `연구/통합을 위한 공장/0117 socketcontract` | 345 | Socket v1.0 + SKR v0.2 |
| `CL17` | `연구/통합을 위한 공장/0117 table` | 210 | Closure Tables v1.1 |
| `CORE17` | `연구/통합을 위한 공장/0117 core` | 602 | Core v1.2 + v1.2a-SEAL |
| `STG17` | `연구/공장2/0117 canon05 1` | 466 | v0.5-STG single transition |
| `FULL15` | `연구/PARADIM/full` | 3468 | Chapter 04 Story 9c 비교 지층(본 장 판 계보 밖) |

## 부록 B. 정확 합본 감사

```text
0117 fornext
= SP17 175 lines
+ SK17 226 lines
= 401 lines, both segments byte-identical

0117 FUULL
= FS17 561 lines
+ CORE17 602 lines
= 1163 lines, both segments byte-identical
```

따라서 이 장의 최초 출처 판정은 합본 행이 아니라 원 개별 문서 행을 우선한다.

## 부록 C. 소급 금지

```text
R05 X/R/U/A ≠ SKR의 직접 선행 선언
FrameGate / coverage ≠ factory module
Story 9c ≠ restored CandidateGen contract
Ghost ≠ IS-CANDGEN
Editor ≠ linker
Episode ≠ CommitRecord
Narrative ≠ META log
Self-boundary ≠ Module Registry
Runtime write authority ≠ interpersonal jurisdiction
v1.2a SEALED ≠ completed human theory
```

구조적 유비와 후대 계보는 연구 후기에서만 사용한다. 0117 원문이 직접 선언하지 않은 인간·생명 이론을 역사 본문으로 소급하지 않는다.
