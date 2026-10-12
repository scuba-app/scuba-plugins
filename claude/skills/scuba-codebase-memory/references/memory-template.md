# Memory page template

Use only the sections needed to explain the decision or finding. A short useful
page is better than a filled-out form with no new information.

```markdown
# Decision: <specific choice>

> eng-memory · <date> · repo: <repository> · author: <author> · status: <status>

## Context
What required a choice, and the constraints that mattered.

## Decision
What was chosen and its scope.

## Reasoning and alternatives
Why it was chosen, what was rejected, and what was actually tried.

## Evidence
Observed results and important limits on the conclusion.

## Code anchors
- <path> @ <commit> — why this location matters

## Sources
- <PR, discussion, or source-capture link>
```

Use `Finding:` or `Incident:` when those better describe the content. Suggested
statuses are `active`, `in-review`, `landed`, `abandoned`, or `superseded`. Verify
the outcome before choosing a status. Include the actual author when known; do not
invent attribution. Code anchors describe a particular revision and must be checked
before being reused. Source links preserve provenance without implying everyone has
access to the underlying source.
