# Human Model Research Program

## 정체성

Human Model은 불완전한 관측과 여러 시간척도 아래에서 인간의 경로 의존적
변화를 연구한다. 한 상태의 국소적 인과 영향이 다른 관할의 사실·의도·수행·
세계 사건을 성립시킬 권한으로 자동 승격되지 않도록 구분하고, 실제 인간에서
그 경계가 어떻게 무너지는지도 모델링하려는 typed hybrid dynamics 연구
프로그램이다.

```text
Local causal influence
≠ cross-domain certification authority
```

이 원리는 상태 간 영향을 금지하지 않는다. 느낌은 믿음을, 기억은 접근성을,
몸은 수행 가능성을 바꿀 수 있다. 그 영향만으로 타 관할을 인증하지 못한다는
뜻이다.

## 현재 상태

현재 Dynamics v0.1.1은 일부 구조적 구분과 동역학적 반례를 실행화한 최소
모델이다. 인간에 대한 경험적 예측 정확도는 아직 검증되지 않았다.

| 근거 층 | 지위 |
|---|---|
| Historical / engineering | `PARTIAL` |
| Executable / structural | `PARTIAL` |
| Human-empirical | `OPEN` |

구조 테스트 통과나 그럴듯한 출력은 인간에 대한 경험적 증거가 아니다.

## 문서 권위

```text
assessment
→ adoption record / RFC
→ implementation
→ versioned execution report
→ empirical evaluation
```

각 화살표는 자동 승격이 아니라 별도 판정 문턱이다.

- [`assessments/`](../assessments/): 외부 비동료평가·비정본 자료
- [`adoption-records/`](adoption-records/): `Adopt / Revise / Hold` 판정
- [`architecture.md`](architecture.md): 연구층과 의존 경계
- [`roadmap.md`](roadmap.md): 단계별 범위와 종료 조건
- [`rfcs/`](rfcs/): 구현 전 제안
- [`claims/`](claims/): claim의 종류·범위·근거·실패 조건
- [`defects/`](defects/): 당시 기록과 현재 해석을 분리한 결함 corpus
- [`benchmarks/`](benchmarks/): 계약 mutation, 구조 ablation, 시간 비교 계획

## 목표 아키텍처

```text
Contract Layer
├─ Certification Contract
├─ Provenance / Integrity Contract
├─ Transition Lineage Contract
└─ Accounting Contract

Descriptive Dynamics
Experimental Protocol
```

v0.1 baseline은 [원격 source revision과 semantic golden](../dynamics/reports/baseline-v0.1.md)으로 동결했다. v0.1.1 package 경계는 구현되었고, 기존 queue→Access
결합은 명명된 legacy bridge로 남아 있다. 가까운 순서는
v0.2 canonical-time kernel → read-only mental-transition ledger → `MORPH-001`
count–load 비교다. `affect → SubjectiveBelief`는 독립 v0.3 축이고,
`WarrantState`, 독립 주관 시계, 퀄리아–부하 대응식, 다른 기억 오귀속은 `HOLD`다.

상세 범위는 [roadmap](roadmap.md)과 세 RFC를 따른다.
