# INTERP-DIALOGUE-001A Jurisdiction Matrix

이 표의 용어는 fixture의 정답이 아니라 `INTERP-DIALOGUE-001B`가 조건부 signature로
동결한 기능 배치 후보다.

| 후보 기능 | 후보 입력 | 허용될 수 있는 영향 | 바뀌어서는 안 되는 것 | 사례에서 열린 질문 |
|---|---|---|---|---|
| `ReceptionState` | 현재 body·condition descriptor | material access, encounter formation, 또는 둘의 별도 간선 | 외부 사실, Evidence, 과거 occurrence | access만 바꾸는가, formation만 바꾸는가, 둘 다인가 |
| `TargetFormReadout` | 대상 범위의 과거 소스 | 해당 대상 encounter의 경사 또는 candidate fit | 전역 mood, 다른 대상, 외부 대상의 실제 속성 | durable state인가, active memory readout인가, 느린 cache인가; unresolved source에 provisional/category 표상이 가능한가 |
| `CurrentAccess` | 현재 접근된 과거 material | 이번 처리에서 사용 가능한 source view | material의 원본, 과거 체험 receipt | 상태가 access를 바꾸는가, access가 현재 형성의 결과인가 |
| `SubjectiveEncounterFormProxy` | 현재 자극·scope·pre-access snapshot | 관계적 형태와 후속 candidate affordance | Evidence strength, 외부 의도, 실제 qualia claim | 어떤 조건이 formation 단계에 직접 작용하는가 |
| `Ghost` | 현재 encounter와 access view | 탐색 순서, 비교, 반사실, 해석 candidate | 이미 형성된 encounter의 소급 수정, Evidence, 행동 occurrence | candidate만 생성하는가, coherence도 평가하는가 |
| scoped adjudicator | candidate·제약·유예 정책 | adopted / contested / rejected / deferred receipt | candidate 원본, 과거 사실, 외부 결과 | Ghost와 분리되는가, 생성 과정의 stop condition인가 |
| action gate | intent candidate·opportunity·feasibility | 수행 여부 | encounter, belief, intent의 자동 수정 | 같은 체감에서 다른 행동을 어떤 조건이 가르는가 |

## Family가 잡는 관할 경계

| Family | 선택적으로 바꾸는 operational source | 유지되어야 할 공개 기록 | 특별 negative control |
|---|---|---|---|
| `REL-BOUNDARY-001` | 보고 mood / 대상 이력 / 외부 cue 소재 | 경계 요청과 내일 연락 발화 | cue를 실제 access·use로, 같은 즉시 응답을 동일 내부 경로로 cast하지 않음 |
| `WORK-FEEDBACK-001` | 보고 evaluation threat / criterion 일관성 이력 / 공개 addendum | 실제로 주어진 평가 문구와 addendum | 공개 addendum의 존재를 평가자 의도·작업 진실·주관적 encounter로 cast하지 않음 |
| `RISK-FOOTSTEPS-001` | 보고 pre-event arousal / 최근 위험 이력 / 경로 일치 관측 | 들린 발소리와 명시된 경로 관측 | provisional/category 표상을 resolved entity·공격자·의도·Evidence로 cast하지 않음 |

각 factor의 `registered_candidate_probe_domains`는 이 표에서 먼저 계측할 후보 영역을
가리킬 뿐, 가능한 효과나 메커니즘의 완전한 관할 목록이 아니다. 등록되지 않았거나
예상 밖인 효과는 fixture 실패 또는 자동 retirement로 처리하지 않는다.
`INTERP-DIALOGUE-001B`는 그런 효과를 raw provenance와 함께 `OUT_OF_MODEL` 또는
`CURRENT_FUNCTIONAL_DECOMPOSITION_SCOPE_FAILURE`로 보존하는 명시적 판정 lane을
pilot과 결과 판정 전에 고정했다.

## `001B`에서 동결한 판정 기준

```text
Selective effect
Non-target invariance
Scope preservation
Temporal non-retroactivity
Path multiplicity
Future discriminability
Non-redundancy
Forbidden-cast preservation
Out-of-model effect preservation
```

[`trace-oracle-v1.json`](trace-oracle-v1.json)은 위 기준을 hypothesis-conditional
projection으로 구체화하지만 아직 어떤 기능 배치도 실행하거나 통과·실패로 판정하지
않는다. natural contrast의 최초 차이는 association signature일 뿐 direct causal
residence가 아니며, direct edge는 별도 D2a-only challenge로 남는다.
