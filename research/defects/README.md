# Defect–Principle Abduction Corpus

이 디렉터리는 과거와 현재 구현에서 발견된 결함을 현행 원리의 성공담으로 다시 쓰지 않고, 재검사 가능한 반례로 보존한다.

```text
Defect
→ candidate principles
→ competing repairs
→ legal control cases
→ minimal counterexample
→ current regression
```

`schema.json`은 당시 기록과 현재의 소급 해석을 의도적으로 분리한다.

- `contemporaneous_record`: 당시 자료가 실제로 관찰하고 진단한 내용
- `retrospective_interpretation`: 현재 연구가 제안하는 결함 분류와 후보 원리

`artifact_status`는 실행에서 관찰한 실패, 정적 설계 위험, 저자 주장도 구분한다. 역사적 패치는 정답 라벨이 아니며 `candidate_principles`는 복수일 수 있다.

원리의 가치는 결함 제거 수만으로 평가하지 않는다. 새롭게 구분하는 예측, 정상 통제 사례를 막는 비용, 추가 자유도도 함께 기록한다.

repository tests는 보존 artifact의 SHA-256과 행 범위, 원격 baseline commit의
원본 path·git blob SHA·원본 행 범위, 당시 기록/소급 해석 분리, 후보 원리·경쟁
수리·정상 통제 사례의 존재를 검사한다. git blob SHA는 원본 동일성을 외부에서
재검증할 포인터이며 local excerpt의 SHA-256을 대신하지 않는다. 전체 Draft
2020-12 schema는 다음 release check로 검증한다.

```bash
npx --yes ajv-cli validate --spec=draft2020 \
  -s research/defects/schema.json \
  -d research/defects/cases/event-count-slow-update-v01.json
```
