# INTERP-001D2a0 — Minimal Recursive Interpretation Spine

> **Status:** `FROZEN / UNEXECUTED`

This directory freezes a detached, synthetic contract for the smallest
interpretation path that can distinguish a current-access surface from a
future-effective interpretive revision. It is not a minimal human runtime and
does not execute a participant, an LLM, or canonical `HumanState`.

```text
ExternalOccurrence / CurrentAccessOccurrence_k
+ DeclaredRuntimeViewReceipt_k
  -> ReceptionCandidate_k
  -> SubjectiveEncounterFormCandidate_k
  -> InterpretationCandidateSet_k
  -> ScopedAdjudicationReceipt_k
  -> ImmediateSurfaceProjectionCandidate_k
  -> RevisionEligibilityDecisionReceipt_k
       eligible no earlier than a later access in the same lineage
```

The common spine can express a future revision but does not require one.
`NOT_EMITTED`, `NOT_ELIGIBLE`, `REJECTED_BY_POLICY`, and
`NOT_APPLICABLE_TO_MODEL` are first-class decisions alongside
`ELIGIBLE_FROM_FUTURE_ACCESS`.

## Frozen boundary

The contract freezes:

- occurrence, candidate, view and receipt identities;
- declared runtime-view fields and stage-level read/write authority;
- access-lineage and future-effect ordering;
- independent temporal (`D2A-T*`), projection (`D2A-P*`) and heterogeneity
  (`D2A-H*`) strategy axes;
- exact synthetic fixture inputs and evaluator-only witnesses;
- scoped non-identifiability, authority-failure and hard-failure vocabulary;
- runner/evaluator artifact separation.

It does not provide:

- a D2a runner, evaluator or synthetic result;
- `Intent`, `Attempt`, `Performance`, `ActionOccurrence` or `WorldOutcome`;
- durable `TargetForm`, memory, Episode or Narrative writes;
- Evidence mutation or claim-support changes;
- participant/model acquisition or a human-mechanism result.

The contract-only verifier is:

```bash
python -m dynamics.labs.interp_d2a0_cli --verify
python -m unittest dynamics.tests.test_interp_d2a0_contract -v
```

The runner in the next slice may read only the execution manifest and its
declared contract inputs. Expected signatures and retirement predicates remain
evaluator-only. A completed run must later be bound to both manifests by a
separate evaluation receipt.

## Program order

`INTERP-DIALOGUE-001P0-v1` remains `FROZEN / UNEXECUTED`; its scheduling state
is `HOLD / AVAILABLE_AS_DEVELOPMENT_INFRASTRUCTURE`. P1-v1 remains required
before any defect-resolution claim, but is no longer the immediate mainline.
After D2a1, `OBS-MAP-000` decides whether the existing elicitation surface is
kept, revised or replaced. This contract does not pre-authorize P0-v2.
