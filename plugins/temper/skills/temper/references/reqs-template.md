# Requirements template

Use this shape for a new reqs.md.
Drop a section only when it truly has nothing in it, and leave out-of-scope in even when it is one line.
Write in the user's language; keep technical terms as they are.

```markdown
# <Project or task name>

## Goal
What should exist when this is done, and who it is for.
Two to four sentences.

## Why
The problem this solves or the outcome it unlocks.
The executor uses this to make good calls on details nobody wrote down, so it is worth a few honest sentences.

## Users and context
Who uses the result and in what setting.
Relevant facts about the environment: stack, platform, existing systems, data sources.

## Must have
- R1: ...
- R2: ...

## Nice to have
- N1: ...

## Constraints
Hard limits: tech choices, budget, performance, security, style guides, deadlines.

## Out of scope
What this task deliberately does not do.

## Acceptance criteria
Each one checkable by someone who did not write it.
Prefer criteria a command can verify.
Tag subjective ones with [judgment].

- AC1: `pnpm test` passes with no skipped tests.
- AC2: The /export endpoint returns CSV with a header row for a request with no filters.
- AC3: [judgment] Error messages read as plain language a non-engineer can act on.

## Open questions
Things still undecided.
The loop stops and asks when it hits one of these, so resolve what you can before running.
```

## What a good criterion looks like

Weak: "The page is fast."
Strong: "AC4: Lighthouse performance score is 90 or higher on the /pricing page in mobile mode."

Weak: "Handles errors well."
Strong: "AC5: When the payment API returns 503, the user sees a retry message and no order row is written."

Weak: "Good summary."
Strong: "AC6: The summary is under 200 words and names every risk listed in section 3 of the source."
