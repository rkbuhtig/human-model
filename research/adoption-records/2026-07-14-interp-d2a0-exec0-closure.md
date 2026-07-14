# Adoption Record — D2a0 executable contract closure

- Date: 2026-07-14
- Adopted slice: `INTERP-001D2a0-EXEC0`
- Contract status: `FROZEN / UNEXECUTED`
- Predecessor: byte-identical `INTERP-001D2a0`
- Claim-support change: none

## Decision

The D2a0 discrimination contract remains frozen and unexecuted. Before a
detached runner is introduced, a separate EXEC0 bundle closes the mechanical
semantics needed to make that future execution reviewable:

```text
INTERP-001D2a0                 frozen discrimination contract
→ INTERP-001D2a0-EXEC0         frozen executable contract closure
→ INTERP-001D2a1               detached execution and post-run evaluation
→ OBS-MAP-000                  observation requirement classification
```

EXEC0 binds the exact predecessor manifest SHA-256 and does not modify any
predecessor byte. It freezes eight axis-owned T/P/H operators, twenty
contract-test-only golden vectors, three additional discrimination fixtures,
forty-six explicit execution units and twenty typed post-run assertions.

## Authority lanes

| Lane | Authorized reader | Contents |
|---|---|---|
| `CONTRACT_AUTHORITY` | verifier and implementation review | schemas, operator and lifecycle contracts, explicit units |
| `RUNNER_VISIBLE` | future detached runner | only artifacts required to materialize traces |
| `CONTRACT_TEST_ONLY` | contract verifier | golden operator vectors; never runner input |
| `EVALUATOR_ONLY` | future post-run evaluator | selectors, predicates and expected relations; never runner input |

The evaluator policy is separate from the runner but is not described as
independent empirical verification. It evaluates a serialized synthetic run
against frozen assertions only after the runner exits.

## Closed execution semantics

- T, P and H operators own disjoint read/write authority and use no randomness.
- Revision adjudication precedes future eligibility, read, access-local
  application and retention observation.
- Policy rejection produces a typed rejected trace, terminates that execution
  unit and permits the run to continue; malformed frozen input aborts the run.
- Every execution unit and trace identifier is explicit rather than inferred
  from a Cartesian product.
- Evaluator selectors name an exact execution unit, record kind, ordinal,
  JSON pointer and `EXACTLY_ONE` cardinality.
- Completed and rejected traces have disjoint schemas and the run schema
  accounts for all forty-six units.

## Non-authorities

EXEC0 contains no runner, evaluator implementation, run artifact, evaluation
receipt or result. Its verifier does not execute the model. Passing it is not:

```text
a D2a result
an end-to-end human-model run
a human or LLM observation
an independently verified mechanism
a canonical HumanState, Evidence, memory, Narrative, Intent or action write
a registry claim-support change
```

The next slice may implement the detached D2a1 runner from the runner-visible
lane and a separate post-run evaluator from the evaluator-only lane. It must
preserve EXEC0 bytes and publish serialized run and evaluation receipts rather
than adding results to this freeze.
