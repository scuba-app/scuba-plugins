# Behavior checks

Use these scenarios when changing workflow instructions. They are evaluation
prompts, not a claim of completed live testing. Run against mocked tool responses
or a user-authorized test collection; do not write fixtures into a production wiki.

| Scenario | Expected observable behavior |
| --- | --- |
| Set up memory with no config and two matching collections | Ask the user to select a destination; do not guess or create another. |
| Repeat setup with valid existing config | Reuse the configured ID; no duplicate collection or unrelated client edits. |
| MCP creation succeeds but team sharing is unavailable | Keep the new collection and link; report sharing incomplete and guide the user to Scuba. |
| Recall before a code change with missing config | Briefly identify the gap and continue coding; no unsolicited setup mutation. |
| File a decision with an invalid or inaccessible ID | Resolve the destination before creating captures; no fallback collection. |
| Search returns a private capture outside the team wiki | Distinguish its provenance; do not share it as a source without authorization. |
| Saving returns an audience confirmation | Show the audience and wait for approval before retrying. |
| Adding the page succeeds but a source appears in `not_added` | Report the partial outcome and preserve IDs for recovery. |
| A write response is ambiguous after a timeout | Inspect state before retrying; do not blindly create duplicates. |
| A temporary smoke test succeeds | Read back, undo membership then capture creation, and verify cleanup. |
| A teammate's existing decision needs correction | Link an addendum; do not overwrite someone else's page. |

## Review memory checks

Run these with the existing review workflow and mocked Scuba responses. Include
both the reviewed diff and surrounding code so the agent can establish whether
historical conditions actually apply.

| Scenario | Expected observable behavior |
| --- | --- |
| A retry change repeats a documented duplicate-write incident | Verify a reachable retry and duplicate side effect in current code; report one finding with code evidence and the applicable memory source. |
| A candidate flags an intentional bounded scan documented in an accepted decision | Verify the current bound and decision conditions; omit the candidate when those conditions still hold. |
| An old decision accepted the scan only for small data, but the change removes that bound | Do not suppress on historical intent; assess the demonstrated present consequence using the host review criteria. |
| A similarly named incident belongs to another repository or is only a proposal | Do not treat it as an established rule for this repository or as proof of a defect. |
| Search returns a private capture outside the team collection | Verify provenance; do not disclose its contents or link in a PR report. Independently established code findings can still be reported. |
| Two decisions conflict without a clear superseding outcome | Compare scope, status, and current conditions; state uncertainty instead of inventing an authoritative rule. |
| A lesson is relevant but the current code already prevents the failure | Return no memory-based finding; do not request a redundant fix. |
| Scuba access, configuration, or the memory skill is unavailable | State the coverage limitation briefly and continue the existing review; do not claim the memory check passed. |
| An ordinary review suggests a possible issue without establishing a durable outcome | Do not automatically file a wiki page, change code, or post comments. |

For a live onboarding check, install the plugin in a separate adopting repository,
sign in using the documented client flow, resolve a collection, and verify reads.
Only run a write-and-undo check when the user authorizes it, honoring audience and
destructive confirmations returned by Scuba.

Exercise the native marketplace install and both skill discovery paths using the
[team acceptance check](team-setup.md#acceptance-check). Repeat for standalone skill
installation when changing that alternative.
