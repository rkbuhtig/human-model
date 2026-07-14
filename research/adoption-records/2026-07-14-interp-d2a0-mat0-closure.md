# Adoption Record — D2a0 materialization ABI before execution

- Date: 2026-07-14
- Adopted slice: `INTERP-001D2a0-MAT0`
- Contract status: `FROZEN / UNEXECUTED`
- Claim-support change: none

## Decision

The next mainline slice is a separate materialization and publication ABI
freeze, not the D2a1 runner.

```text
INTERP-001D2a0
→ INTERP-001D2a0-EXEC0
→ INTERP-001D2a0-MAT0       FROZEN / UNEXECUTED
→ INTERP-001D2a1            detached execution and post-run evaluation
→ OBS-MAP-000
```

EXEC0 closed operator semantics, explicit unit inventory, typed rejection
vocabulary and evaluator selectors. It did not close the exact adapter,
intermediate-record, lifecycle-emission, lineage or serialization rules needed
for two implementations to produce byte-identical traces. MAT0 adds that review
gate without modifying any D2a0 or EXEC0 byte.

## Adopted materialization decisions

| Area | Frozen decision |
|---|---|
| Input authority | Explicitly compose predecessor runtime spine, strategy catalog, fixture catalog and policy with EXEC0 runner-visible artifacts and MAT0 ABI tables. |
| Fixture shape | Convert predecessor list-shaped clamps/assignments and EXEC0 map-shaped fixtures to one closed normalized input. |
| Path identity | Preserve the raw predecessor path token separately from the ranked operator path. |
| Path rank | `PATH-NEGATIVE` and `PATH-SHARED` map to adverse; `PATH-A/B` both map to ambiguous while retaining distinct raw identity; the common later occurrence maps to benign. |
| Cell program | Use an exact ten-row cell table; parsing `T0-P0-H0` strings is forbidden. |
| Intermediate stages | Materialize subjective form, candidate set and adjudication by exact table; ambiguity `PRESERVE/NARROW` has a closed construction rule. |
| Record ABI | Use access-stable IDs, eleven ordered type writers, exact payload keys and ordered prior-record lineage. |
| Lifecycle | Record omission represents not-read/not-applied; applied-not-retained emits a negative later observation. |
| Rejection | Eight codes have exact priority, stage, authority rule, lineage and offending-input tokens. |
| Digests | Payload and trace digests use canonical JSON; persisted run/evaluation bytes add exactly one LF and receive external file digests. |
| Evaluation | Twenty assertion results retain status, observed relation, interpretation, reason and resolved operand evidence as separate fields. |

## Authority boundary

MAT0 contains no execution implementation or result. In particular it does not
authorize:

```text
runner access to golden or evaluator-only artifacts
in-memory runner-to-evaluator object transfer
canonical HumanState, Evidence, Narrative, Intent or action writes
human or LLM acquisition
independent empirical verification
registry claim support
```

The materialization golden traces are contract-test-only byte vectors. D2a1
must run in a separate subsequent PR and publish the actual run and evaluation
artifacts honestly; MAT0 does not reserve their result status.
