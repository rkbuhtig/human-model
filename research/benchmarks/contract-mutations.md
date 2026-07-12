# Contract Mutation Suite

> **Status:** PLANNED

이 검증군은 인간을 설명하는 후보 모델을 비교하지 않는다. 일부러 certification·provenance·transition lineage를 위반하는 mutant를 만들고, Contract 테스트가 그 위반을 실제로 검출하는지 검사한다.

초기 mutant 후보:

```text
RoutedCandidate → EvidenceLink
Intent → ActionOccurrence
PerformanceReceipt → WorldOutcome
View → evidence deletion
IngressPriority → EvidenceStrength
```

각 mutant는 적어도 하나의 Contract 테스트에서 실패해야 한다. 살아남은 mutant는 인간적 설명력이 아니라 테스트 방어력의 결함을 뜻한다.

```text
mutation score
= detected contract mutants / total executable contract mutants
```

이 점수는 인간에 대한 경험적 타당성 점수가 아니다.
