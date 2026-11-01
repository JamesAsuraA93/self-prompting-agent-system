# Compiling a prompt from requirements

The executor is a capable engineer who has never seen this project, this conversation, or the user.
Everything it needs has to be in the prompt or reachable from paths the prompt names.
Write for that reader.

## Inputs to read before writing

reqs.md, in full.

rules.md, in full.
It goes into the prompt verbatim, and the prompt itself has to obey it.

`.temper/learnings.md`, in full.
Carry over only the lessons that apply to this task.

The repo, enough to state concrete facts: language and framework, package manager, where the relevant code lives, how to run tests, lint and build, and the conventions in use.
If the project has a CLAUDE.md or contributing guide, pull the parts that matter for this task.

For prompt v2 and later: the previous prompt and its diagnosis file.

## What the prompt has to do

Carry the why.
A short paragraph on the goal and the reason behind it lets the executor make sensible choices about things the requirements never mention.

State facts instead of asking the executor to discover them.
"Tests run with `pnpm test`, the handler is in `src/api/export.ts`" saves the executor ten tool calls and removes a way to go wrong.

Copy the acceptance criteria verbatim, with their ids.
Paraphrasing them is where meaning drifts.

Tell the executor to check its own work against each criterion before finishing, and to report a line per criterion with how it checked.

Say what to do when something is unclear: make the reasonable choice, keep going, and list every assumption in the final report.
This keeps the run moving and surfaces the requirements gaps for the next diagnosis.
Keep this instruction neutral.
Do not add a tie-break rule of your own such as "pick the stricter reading", because the executor will apply it to words the requirements already define and narrow them.
In a benchmark run, "pick the stricter reading" made the executor decide that "whitespace" excluded newlines, which broke a requirement the plain request got right.

Never narrow or widen a requirement while copying it.
If you think a requirement is ambiguous, that is a requirements gap: raise it with the user before the run, do not resolve it inside the prompt.

Name the deliverable exactly: which files, which format, where to save.

## What to leave out

Persona fluff such as "you are a world-class expert".
It adds nothing a clear task does not.

Capital-letter commands and stacked MUSTs.
Explain the reason instead, the executor follows reasons better than volume.

Restating the same rule in three places.

Anything from the conversation that is not in reqs.md.
If it matters, it belongs in reqs.md, so propose adding it there.

## Template

Adapt freely.
Skip a section when there is nothing true to put in it.

```markdown
# Task
<One paragraph: what to produce, for whom, and where it goes.>

## Why this matters
<The goal and the reason, from reqs.md.>

## Context
<Stack, relevant paths, commands, conventions, existing behavior to keep.>

## What to deliver
<Exact files or artifacts, format, save location.>

## Requirements
<Must-haves from reqs.md with ids. Nice-to-haves, labelled as optional.>

## Constraints and out of scope
<Hard limits. What not to touch or build.>

## Acceptance criteria
<Verbatim from reqs.md, with ids.>

## House rules
<rules.md, verbatim. Every file you produce must follow these.>

## Lessons from earlier runs
<Only the learnings that apply to this task.>

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Check your work against every acceptance criterion.
For each one, report PASS or FAIL and how you checked it, running the command where one exists.
```

## Rewriting for the next version

Start from the previous prompt and change only what the diagnosis calls for.
When you quote a verdict or review note into the prompt, clean any text that breaks `rules.md`, for example replacing a forbidden dash with a plain hyphen, so the prompt never models what the rules forbid.
Keep the sections that produced passing criteria as they were.
When a fix adds an instruction, put it where the executor will read it at the moment it matters, usually in Context or next to the related requirement, and also in the "Before you finish" list if it was missed last time.
