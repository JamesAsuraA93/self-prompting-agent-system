---
name: temper
description: Turn a project's requirements file (reqs.md, need.md, requirements.md) into an engineered prompt, run that prompt with a fresh agent, grade the result against the acceptance criteria with a separate judge, and recursively rewrite the prompt until the result passes. Keeps versioned prompts and a learnings log so every run in the project starts sharper than the last. Use this whenever the user wants Claude to "prompt itself", generate the prompt from their needs first and then execute it, do meta-prompting, auto-iterate or self-correct a prompt, re-engineer a prompt from reqs.md or need.md, or says things like "here is what I need, work out the best prompt and do it", even if they never say "temper". Also use it when the user wants to write, clean up, or lint a reqs.md / need.md for a project, or wants to "dream", consolidate, or clean up the lessons an agent has learned across runs.
---

# Temper

Named after tempering steel: heat it, hammer it, test it, repeat until it holds.

A loop that turns what the user needs into a prompt, runs it, checks the result against the need, and fixes the prompt when the result falls short.

The requirements file is the source of truth.
Prompts are build artifacts compiled from it.
Lessons are memory that carries from one run to the next.

## Why the work is split into three roles

The context that writes a prompt is bad at noticing what the prompt left out, because it silently fills the gaps from its own head.
So the loop uses three roles that each see something different.

The compiler is you, in the main thread.
You read reqs.md, the repo, and learnings.md, and you write the prompt.

The executor is a fresh subagent that sees only the compiled prompt.
If the prompt is missing context, the executor fails in a visible way, and that failure is the signal the loop feeds on.

The judge is another fresh subagent that sees reqs.md and the output, never the prompt.
It grades against what the user needs, not against how the prompt interpreted the need.

Keep these roles separate even when it feels slower.
Merging them is how a loop ends up grading its own homework and reporting success on work that misses the point.

## Files

```
<project root>/
  reqs.md                     human-owned spec (need.md, needs.md, requirements.md also accepted)
  rules.md                    human-owned house rules that apply to every output and every Temper file
  .temper/
    config.json               max iterations and other settings (written by the script)
    learnings.md              lessons that carry across runs
    log.jsonl                 one line per graded iteration (written by the script)
    runs/<run-id>/
      prompt.v1.md            compiled prompt, one file per version
      output.v1/              what the executor produced (or output.v1.md)
      judge.v1.md             the judge's verdict per criterion
      diagnosis.v1.md         why each failure happened and what changes in v2
    dreams/<dream-id>/
      manifest.json           runs reviewed and the learnings.md hash (written by the script)
      proposal.md             proposed changes with evidence
      applied.md              which changes the user accepted
    learnings.history/        a copy of learnings.md from before each dream edit
```

The helper script lives at `scripts/temper.py` inside this skill's directory.
It handles the bookkeeping that should not depend on judgment: run ids, the iteration log, and the continue or stop decision.

## Pick the mode

Read what the user asked for and pick one.

Intake: there is no reqs file, or the user wants to write or clean one up.
Do step 1 only.

Compile: the user wants the prompt but not the execution.
Do steps 1 and 2, show the prompt, and stop.

Run: the default.
Do the whole loop.

Learn: the user is giving feedback on an earlier result.
Fold it into learnings.md, or propose a change to reqs.md if the feedback is really a requirement, and stop.

Dream: the user asks to dream, consolidate or clean up learnings, or asks why the same failure keeps coming back.
Do the dream pass in "Dreaming" below and stop.

## Step 1: Intake and lint the requirements

Look for `reqs.md`, `need.md`, `needs.md`, or `requirements.md` in the project root, in that order.
If the user named a different file, use that one.

If no file exists, interview the user and then write `reqs.md` from `references/reqs-template.md`.
Read the repo first so you only ask what you cannot find out yourself.
Use AskUserQuestion for choices with clear options, and plain conversation for open questions.

If a file exists, lint it.
These checks are the ones that decide whether the loop can work at all:

Every acceptance criterion can be checked by someone who did not write it.
"Fast" fails this check, "p95 under 200 ms on the seed dataset" passes.
"Looks good" fails, "renders without horizontal scroll at 375 px width" passes.

No two requirements contradict each other.

Scope is bounded: there is an out-of-scope section, even a short one.

Each criterion has an id (AC1, AC2, ...) so the judge and the log can refer to it.

When a check fails, propose concrete rewrites and get the user's yes before running.
Do not edit reqs.md quietly.
It is the user's statement of intent and the grading depends on it, so a silent edit would let the loop move the goalposts until it passes.

Some criteria are subjective by nature, like tone of voice.
Keep them, but tag them `[judgment]`.
The judge still grades them with a short rationale.
They never outweigh a hard criterion, but a failed one is not ignored either: see `pass_with_advisory` under Stop rules.

### Rules file

Every project with a reqs file also has a `rules.md` beside it.
If it is missing, create it from `references/rules-template.md`, show it to the user, and ask what to add before the first run.
Rules hold for every task in the project: forbidden characters, voice, language, naming, comment style.
They are separate from reqs.md because they do not change from task to task, and mixing them in would make every reqs file repeat them.

Rules bind Temper itself as much as the executor.
Every file Temper writes (prompts, verdicts, diagnoses, lessons, dream proposals, reports) follows them, and text quoted from a verdict into a prompt is cleaned to follow them too.

## Step 2: Compile the prompt

Set up the run:

```bash
python3 <skill-dir>/scripts/temper.py init
python3 <skill-dir>/scripts/temper.py new-run
```

`init` is safe to repeat.
`new-run` prints the run directory to write into.
Pass `--max N` to `init` if the user asked for a different iteration limit (default 3).

Read `references/compiler.md` and write `prompt.v1.md` in the run directory.
Copy `rules.md` into the prompt verbatim under a `## House rules` heading.
Before writing, gather the concrete facts the executor will need: stack, file paths, commands for tests and lint, conventions.
Spending time here is the cheapest way to save an iteration later.

In compile mode, show the prompt to the user and stop here.

## Step 3: Execute

Spawn a general-purpose subagent.
Its prompt is the full text of `prompt.vN.md`, verbatim, followed by one line saying where to save the output (`<run-dir>/output.vN/` or `output.vN.md`).

Add nothing else.
Any hint you slip in by hand is a hint the next run will not have, and it hides the gap the loop is supposed to expose.
If you notice the prompt is missing something, fix the prompt file first and then run it.

When the task changes code in a git repo, launch the executor with `isolation: "worktree"` so each attempt starts from a clean tree and failed attempts do not pile up in the user's branch.
Note the worktree path or branch name in the run directory so you can report it.

## Step 4: Judge

Spawn a second, fresh subagent.
Give it the text of `references/judge.md`, the path to the reqs file, and the path to the output (or the worktree).
Do not give it the prompt, and tell it not to read anything in `.temper/` except the verdict file it writes, since the prompts live there.

The judge writes `judge.vN.md` with a verdict for every criterion: PASS, FAIL, or UNCLEAR, each with evidence.
For any criterion that a command can check, such as tests, lint, a build, or a file existing, the judge has to run the command and quote the result instead of reasoning about it.
UNCLEAR counts as a failure for the decision, because an unproven criterion is not a met one.

The judge also checks the output against `rules.md`, and it runs the mechanical part itself:

```bash
python3 <skill-dir>/scripts/temper.py rules-check <output paths>
```

Any rule violation is a hard failure, recorded with the id `RULES` and counted in `--total` as one extra criterion.
After the judge finishes, run `rules-check` on the run directory as well, so Temper's own files are held to the same rules.

Then record the result:

```bash
python3 <skill-dir>/scripts/temper.py record <run-id> --version N --total <hard criteria count> --failed AC2,AC5 \
  --advisory-total <[judgment] criteria count> --advisory-failed AC15
```

Count `[judgment]` criteria only in the two `--advisory-` options, never in `--total` or `--failed`.
Pass `--failed ""` when every hard criterion passed, and leave out the advisory options when the reqs file has no `[judgment]` criteria.
The script prints a `DECISION=` line.
Follow it.

## Step 5: Diagnose and rewrite

Only when the decision is `continue`.

Classify each failed criterion into one of these causes:

Prompt gap: reqs.md states the thing, but the prompt left it out, buried it, or garbled it.
Fix the prompt.

Requirements gap: reqs.md is ambiguous, contradicts itself, or does not say what the judge needed to know.
Stop the loop, show the user the gap, and propose wording for reqs.md.
Do not guess on their behalf, because a guess baked into the prompt becomes an invisible requirement.

Execution slip: the prompt was clear and the executor still missed it.
Make the instruction more prominent or add it to the self-check list.
Suspect a prompt gap first, though, since "the model just missed it" is usually a prompt that buried the point.

Environment limit: missing access, a tool, a credential, or network.
Stop and report what is blocked.

Write `diagnosis.vN.md` with one short entry per failure: criterion id, cause, evidence, and the change you will make.
Then write `prompt.v(N+1).md` as a targeted edit of the previous version, not a fresh rewrite.
Small edits keep what already passed and make it clear which change fixed what.

Go back to step 3.

## Stop rules

The script applies these from the log, so the decision does not drift with mood:

`stop_pass`: every hard criterion and every `[judgment]` criterion passed.

`pass_with_advisory`: every hard criterion passed, but a `[judgment]` criterion did not.
Ask the user whether to run another version aimed at it, and continue without asking only when the user has already said this kind of quality matters to them (for example a standing instruction to be picky about UI).
Diagnose and rewrite exactly as for a hard failure.

`stop_max`: the iteration limit was reached.

`stop_plateau`: the score did not beat the best earlier version.
The score compares hard criteria first and uses `[judgment]` criteria only to break a tie, so a version that fixes a judgment issue by breaking a hard criterion counts as worse.
This usually means the problem is not the prompt any more, so another rewrite would just burn tokens.
Go back to the best version, which the script names, and look at the diagnosis for a requirements gap or an environment limit.

`continue`: the result improved but is not done yet.
If the script also lists regressed criteria (passed before, failing now), make sure the next version restores them.

Steps 1 and 5 can also stop the loop when they find a requirements gap or an environment limit.

## Step 6: Learn

Run this after every loop, passed or not, because failed loops usually teach more.

A lesson qualifies only when it would help a different future task in the same project.
"The executor does not know this repo uses pnpm, state the package manager in every prompt" qualifies.
"v2 fixed AC3" does not, it is history, and the run directory already holds it.

Append qualifying lessons to `.temper/learnings.md` under a dated heading, each with the run id that taught it.
If a similar lesson already exists, sharpen that one instead of adding a near-duplicate.
Keep the file short, around 40 lines, by merging and pruning, because the compiler reads all of it every time and a bloated file turns into noise.

If a lesson is really a requirement, for example "all API responses must be paginated", propose adding it to reqs.md instead.

This step is quick and sees one run.
Patterns that only show up across runs, and lessons that have gone stale, are the job of the dream pass.

## Dreaming

Dreaming is a separate pass that reviews many finished runs at once, finds failures that keep coming back, checks existing lessons against the current repo, and proposes changes to learnings.md for the user to accept.
It never edits learnings.md or reqs.md without the user's yes.

Start it with:

```bash
python3 <skill-dir>/scripts/temper.py dream-prep
```

It prints the dream directory, the runs to review, and the learnings.md hash to quote back when applying.
Then read `references/dreamer.md` and follow it.
It covers the analyst subagents, the merge rules, the staleness check, the proposal format, and how to apply accepted changes safely.

Suggest a dream to the user when `status` shows five or more runs since the last one, or when a diagnosis names a failure that learnings.md already claims to prevent.
Do not start one in the middle of a run.

## Step 7: Report

Tell the user, briefly:

the final decision and the pass count for each version,
where the result is (path, worktree, or branch),
the final prompt path,
one line per version on what changed and why,
lessons added to learnings.md,
and anything that needs their decision, such as a requirements gap.

If the result lives in a worktree, tell them how to merge or check out the branch.
