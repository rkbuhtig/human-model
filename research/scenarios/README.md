# Research Scenarios

이 디렉터리는 인간다운 대사를 채점하는 benchmark가 아니라, 현실 영역의 저자 생성
가상 사례에서 서로 다른 기능의 관할을 구분할 수 있는지 묻는 research scenario
contract를 보관한다.

```text
public record
≠ author-origin phenomenological possibility
≠ phenomenological expectation
≠ mechanistic placement
≠ correct output
```

시나리오는 세계의 사실과 Evidence 권한, 저자의 내성에서 출발한 가능성,
구조상 지켜야 할 불변식, 개연적인 현상 범위와 아직 열린 기능 배치를
서로 다른 lane으로 기록한다. 어떤 lane도 자동으로 인간 심리 메커니즘의
인증서가 되지 않는다.

현재 사전등록:

- [`INTERP-DIALOGUE-001A`](interp-dialogue-001/README.md): 관계·업무·위험 영역의 3개
  시나리오 family에서 factor-label Hamming-one contrast와 후속 probe를 고정한다.
  인간 자료, 정답 메커니즘, 정답 출력, runner와 runtime feedback은 없다.
- [`INTERP-DIALOGUE-001B`](interp-dialogue-001/trace-oracle.md): 001A를 content digest로
  결박하고 조건부 placement signature, ordinal horizon, same-future-option과 out-of-model
  규칙을 동결한다. human·LLM·D2a trace data나 placement winner는 없다.
