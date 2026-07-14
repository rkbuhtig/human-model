# INTERP-001D2a0-MAT0 — Materialization and Publication ABI Closure

> **Status:** `FROZEN / UNEXECUTED`

MAT0 closes the byte-level execution meaning that D2a0 and EXEC0 intentionally
did not implement. It binds the exact predecessor manifests:

```text
INTERP-001D2a0 frozen manifest
8ee62993fbf302d8037f8cf898a0edca4fe7bbff7b01f73f6a71e8b6c04c3efd

INTERP-001D2a0-EXEC0 frozen manifest
1a7203d93a341c3b4570d4070d95457441da190e4c8ff167f86d89d0135c40f3
```

MAT0 freezes:

- the exact composed predecessor, EXEC0 and MAT0 runner-visible input bundle;
- predecessor-to-EXEC0 field and path-value normalization with raw subjective
  identity preserved;
- exact cell-to-operator programs without parsing cell IDs;
- the pre-interpretation lifecycle phase: a prior eligible revision is selected,
  read and applied before the same access forms candidates or runs T3;
- record IDs, writer order, payload shape, source lineage and digest targets,
  including the application-to-candidate provenance edge;
- lifecycle-arm emission and typed-rejection truth tables;
- disjoint TRACE and RECORD evaluator operands and exact run-status precedence;
- manifest-rooted runner bootstrap and transitively closed source bundles;
- completed, rejected and multi-access canonical trace vectors in a
  contract-test-only lane, with their normalized-input derivation checked.

It contains no runner, evaluator implementation, run, evaluation result or
publication manifest. The golden traces are conformance vectors and are not
runner input. Passing this verifier is ABI closure, not a D2a result or evidence
for a human mechanism.

```bash
python -m dynamics.labs.interp_d2a0_mat0_cli --verify
python -m unittest dynamics.tests.test_interp_d2a0_mat0_contract -v
```

After MAT0 is reviewed and merged, `INTERP-001D2a1` may implement the frozen
runner and separate post-run evaluator. That execution must reproduce the
frozen materialization bytes rather than inventing adapters, record lineage or
diagnostic labels. The runner source must bind the merged MAT0 manifest's exact
raw-file SHA-256; the manifest then resolves every runner-visible MAT0 document
by its frozen kind, path and SHA-256 row without a circular self-digest.
