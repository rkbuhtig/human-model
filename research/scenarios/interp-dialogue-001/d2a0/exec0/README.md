# INTERP-001D2a0-EXEC0 — Executable Contract Closure

> **Status:** `FROZEN / UNEXECUTED`

This bundle closes the executable semantics that the merged D2a0-v0
discrimination contract intentionally left open. It binds the exact predecessor
manifest SHA-256
`8ee62993fbf302d8037f8cf898a0edca4fe7bbff7b01f73f6a71e8b6c04c3efd`
without changing any predecessor byte.

EXEC0 freezes:

- exact, axis-owned T/P/H operator semantics and contract-test-only golden vectors;
- a separate revision lifecycle processor and corrected dependency order;
- completed-versus-rejected trace carriers with typed terminal rejection;
- three additional T1/T2/H1 discrimination fixtures;
- 46 explicit execution units rather than an inferred Cartesian product;
- typed evaluator selectors, predicate arity/cardinality and result vocabularies;
- runner-visible, contract-test-only and evaluator-only artifact lanes.

It contains no runner, evaluator, run, evaluation receipt or synthetic result.
It grants no canonical `HumanState`, Evidence, durable `TargetForm`, Episode,
Narrative, Intent or action writer. Passing its verifier is contract conformance,
not support for a human mechanism.

```bash
python -m dynamics.labs.interp_d2a0_exec0_cli --verify
python -m unittest dynamics.tests.test_interp_d2a0_exec0_contract -v
```

The next slice, `INTERP-001D2a1`, may implement these frozen operators in a
runner that receives only the runner-visible lane. Golden expected outputs and
evaluation assertions are not runtime inputs. A separate post-run evaluator may
read the serialized run only after the runner process exits.
