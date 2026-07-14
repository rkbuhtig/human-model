# Adoption Record — D2a0 mainline priority before further elicitation

- Date: 2026-07-14
- Decision class: research program ordering and contract freeze
- Adopted slice: `INTERP-001D2a0`
- Contract status: `FROZEN / UNEXECUTED`
- Claim-support change: none

## Decision

The immediate mainline moves from a P1-v1 scripted re-pilot to the detached
minimal recursive interpretation spine.

```text
INTERP-DIALOGUE-001P0-v1 artifact lifecycle
FROZEN / UNEXECUTED

P0-v1 scheduling
HOLD / AVAILABLE_AS_DEVELOPMENT_INFRASTRUCTURE

P1-v1 scheduling
PLANNED / NON-MAINLINE HOLD

immediate mainline
INTERP-001D2a0 contract freeze
→ INTERP-001D2a1 detached runner and evaluator
→ OBS-MAP-000 observation requirement classification
```

This record supersedes only the statement that P1-v1 preregistration is the
immediate next PR. It does not mutate, revoke or reinterpret the frozen P0-v1
instrument, decision receipts, schemas, rendered surfaces or digests. P1-v1
remains necessary before a confirmed P1-v0 defect can be reported as no longer
reproduced.

`OBS-MAP-000` may classify the existing participant-facing surface as `KEEP`,
`REVISE`, `ADD`, `UNOBSERVABLE` or `SOURCE_SPECIFIC_ONLY`. P0-v2 and P1-v2 are
not pre-authorized; they are opened only if that classification supports the
same elicitation approach.

## Adopted contract boundaries

| Decision | Adopted boundary |
|---|---|
| AR-D2A0-01 | D2a0 is a minimal recursive interpretation spine, not a minimal human runtime. |
| AR-D2A0-02 | The common spine may express a revision decision but does not require a revision occurrence. |
| AR-D2A0-03 | Temporal/state, surface projection and declared heterogeneity are independent strategy axes. |
| AR-D2A0-04 | Heterogeneity uses exact declared profiles; PRNG, seed and persona inference are forbidden. |
| AR-D2A0-05 | Future eligibility requires matching runtime, target scope, interpretation scope and a strictly later access lineage. |
| AR-D2A0-06 | Emission, adjudication, eligibility, read, access-local application and retention observation are distinct records. |
| AR-D2A0-07 | Role-only and evidence-isolation assertions apply only under their frozen no-feedback and no-new-information clamps. |
| AR-D2A0-08 | Retirement language is limited to registered fixtures and horizons; global stage necessity is not decided here. |
| AR-D2A0-09 | Runner inputs contain no expected signature or retirement decision; evaluation remains a separate process role. |
| AR-D2A0-10 | D2a0 adds no runner, evaluator, synthetic result, canonical HumanState writer or claim support. |

## Frozen synthetic witnesses

The contract registers six fixture families:

1. equal immediate surface with different supplied paths and a common later event;
2. role-conditioned surface projection with action, self-observation and world feedback absent;
3. different subjective paths with external Evidence links and assessment policy clamped;
4. an illegal same-access revision read;
5. distinct emitted/adjudicated/eligible/read/applied/retained lifecycle states;
6. undeclared free-candidate and unbounded `OUT_OF_MODEL` escapes.

Expected relations are not stored in those fixtures. They are frozen only in
the evaluation manifest, which a future runner process may not read.

## Non-authorities

Passing the D2a0 validator means only that the unexecuted contract is closed and
internally consistent. It is not:

```text
a D2a result
a human or LLM observation
a human-mechanism result
a durable TargetForm or memory implementation
an Intent, action or world loop
an Evidence assessment
a placement winner
a defect-resolution result
claim support
```

The next implementation slice may add a detached D2a1 runner, serialized trace
and independent evaluator. It must not mutate canonical `HumanState` or read
the evaluator-only manifest during execution.
