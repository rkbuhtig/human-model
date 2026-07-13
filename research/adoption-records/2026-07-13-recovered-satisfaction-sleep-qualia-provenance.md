# Source-Recovery Record — `만족수면퀄리아통합`

| 항목 | 값 |
|---|---|
| Date | 2026-07-13 |
| Source bundles | `pluss.zip`; comparison corpus `연구(1).zip` |
| Decision | `REVISE — PROVENANCE ONLY`; recovered content lineage / authoring time unresolved |
| Authority | `SOURCE-CRITICAL PROVENANCE ONLY` |
| Adoption / implementation | `UNCHANGED / DOCUMENTATION CORRECTION ONLY` |
| Human-empirical status | `OPEN — NO HUMAN DATA; NO SUPPORT ADDED` |

이 기록은 이전 Chapter 10–11이 독립 파일 부재 때문에 보류했던
`만족수면퀄리아통합`의 **내용 계보**를 복구한다. 복구본은 대규모 byte-identical 원문
재사용과 downstream의 명시적 입력 문서 열거를 함께 가진다. 그러나 제공 ZIP의 entry
시각만으로 이 파일이 1월 당시 보존된 독립 원본인지, 같은 자료를 이용한 후대 재구성본인지
식별할 수 없다.

```text
recovered content lineage
≠ contemporaneous original identity
≠ active theory adoption
≠ implementation or empirical support
```

## Artifact identity

| Artifact | SHA-256 |
|---|---|
| `pluss.zip` | `4e2c88d92fbae5cef97d159f52bb13ecf27e02772b7af5abfff8914c3c7943bc` |
| `연구(1).zip` | `95442d5a1fb12b99f7bc39e02fe84e3bd05f80489361f3b9d6fe3f224de84258` |
| `pluss/만족수면퀄리아통합.txt` | `15fb834c87eda1ae3240a59fb3f73a3354a204f52b222a9e03039b02995c6115` |

복구 파일은 56,617 bytes, 물리적 1,180행이다. 마지막 substantive 문장은 1,175행이고,
1,177행에는 종결 구분선 `---`이 있다. 1,176행과 1,178–1,180행은 빈 행이다.
ZIP central-directory entry 시각은
`2026-07-13 21:19:14`지만 timezone 없는 DOS metadata이며 실제 작성시각의 근거로
사용하지 않는다.

## Composition audit

| 복구본 범위 | 비교 자료 | 판정 |
|---|---|---|
| `L1–206` | `fucstrees/0121 만족.txt:L1–206` | byte-for-byte exact |
| `L209–615` | `fucstrees/0121 수면.txt:L1–407` | 전체 407행 byte-for-byte exact |
| `L620–873` | `fucstrees/0122 newqual.txt:L1–245` | exact copy 아님; `ΞM` 표기·추가 봉인을 사용한 강한 textual derivative |
| `L879–1175` | downstream `0127 maybe통합1` | CallCapability·OpsLog·KnobRegistry·Jurisdiction·Viability·MeaningTriangulation의 입력 계보와 일치 |

`0121 만족`의 원본 마지막 빈 행은 복구본의 삽입 구분선 뒤 `L208`에 보존된다.
`L1–206` slice SHA-256은
`53823cd05d4baf9c6438279958fd84a64db3eee29dfd3e91ea8c452ecfc9928a`이고,
`0121 수면` 전체와 같은 `L209–615`의 SHA-256은
`55b972049efc3160995dc56c832ba785f277cb75465eb1ef37fd43206a4ac8c4`다.

`L620–873`은 `0122 newqual`과 byte-identical하지 않다. 따라서 이 구간에 등호를 쓰거나
exact inclusion으로 부르지 않는다. 체계적인 기호 치환과 확장을 포함한 파생 재작성으로만
판정한다.

## Downstream lineage evidence

`Overqorld/0127 maybe통합1:L1`은 자신이 다시 쓰는 세 입력 중 하나로
`만족수면퀄리아통합`을 직접 열거한다. `Overqorld/minipatch.txt:L142, L241`도 같은 이름을
통합·삽입 대상으로 지목한다. `0127 maybe통합1`에는 복구본 후반의 다음 구조가 실제로
이어진다.

- `Call ≠ entitlement`
- `OpsLog ≠ authority`
- `KnobRegistry / Epoch`
- jurisdiction non-substitution
- viability margin
- meaning triangulation

대규모 exact reuse, 강한 파생 재작성, 명시적인 downstream 동명 입력 열거가 함께 있으므로
복구 파일은 **내용 계보에 부합하는 복구본**으로 판정한다. 다만 `SYNTH27`이 실제로 읽은
역사적 동명 입력과 현재 복구 artifact의 동일성이나 직접적인 방향성 edge는 판정하지 않는다.

## Allowed use

- Chapter 10–11의 “독립 파일 부재로 내용이 알려지지 않음” 판정을 수정한다.
- 누락됐던 만족–수면–퀄리아 합성과 CVJU block의 실제 내용을 후기 계보 복원에 사용한다.
- Volume I.5의 source-critical 입력으로 등록한다.
- 현재 claim과 defect의 `historical_cases` 후보를 찾는 데 사용한다.

## Prohibited promotion

- 복구 파일 자체를 1월의 동시대 독립 정본으로 단정하지 않는다.
- ZIP entry 시각을 작성일로 사용하지 않는다.
- 복구 사실만으로 persistent qualia substrate, plastic update operator, memory archive 또는
  Ghost handoff가 완성됐다고 판정하지 않는다.
- historical link를 active adoption, implementation, structural support 또는 human-empirical
  evidence로 자동 승격하지 않는다.
- 물리·우주 은유를 측정된 인간·물리 법칙으로 승격하지 않는다.

## Repository consequence

이번 교정은 Chapter 10–11의 provenance 문장과 병렬 Volume I.5 문서 계획만 바꾼다.
Dynamics, `HumanState`, Evidence/Certification 계약, claim status와 support 배열은 변경하지
않는다. Volume I.5의 실제 장 구성과 claim별 lineage 연결은 별도 source-critical PR에서
검토한다.
