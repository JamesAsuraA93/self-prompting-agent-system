# Dreaming: consolidating learnings out of band

Dreaming is a separate pass over many finished runs.
It exists because the in-band Learn step (Step 6) has three blind spots.

The orchestrator that writes a lesson at the end of a run is also busy finishing that run, so curation gets whatever attention is left over.

It sees one run only, so it cannot notice that the same failure keeps coming back across runs.

Lessons go stale.
The repo changes, a lesson stops being true, and the compiler keeps copying it into prompts with full confidence.

A dream pass gives curation its own budget and a view across every run.
Its output is a proposal the user accepts or rejects line by line.
It never edits learnings.md or reqs.md on its own.

## Roles

The orchestrator is you, in the main thread.
You prepare the manifest, hand batches of runs to analysts, merge what they find, check existing lessons against the repo, and write the proposal.

Analysts are fresh subagents, one per batch of runs.
They read raw evidence (prompts, verdicts, diagnoses, the log) and report patterns with quotes.
They do not propose wording for learnings.md; that is the orchestrator's job, because only the orchestrator sees every batch.

## Analyst brief

Give each analyst this brief, followed by the list of run directories in its batch and the paths to learnings.md, reqs.md and log.jsonl.

```markdown
You are reviewing finished runs of a prompt-improvement loop to find patterns worth remembering.
Each run directory holds prompt.vN.md (what the executor was told), judge.vN.md (how the result was graded against reqs.md), and diagnosis.vN.md (why it failed and what changed next).
log.jsonl has one line per graded version with pass counts, failed criteria ids, and the stop decision.

Read every file in the run directories you were given.
Report patterns, not run summaries.
A pattern is something that went wrong, or a fix that worked, in a way that would recur in a different future task in this project.

For each pattern, give:
- a one-line statement of the pattern
- every run id where it appears, with a short quote from the file that shows it
- the kind: missing context in the prompt, a prompt instruction that backfired, a requirements gap, an environment or tooling problem, or a fix that reliably worked
- whether the current learnings.md already covers it (quote the lesson if so), and whether that lesson helped, failed to help, or is contradicted by the evidence

Also report any lesson in learnings.md that the evidence shows to be wrong or outdated, with the quote that shows it.

Do not propose new wording for learnings.md.
Do not report something you only infer without a quote.
If you find nothing that meets this bar, say so; an empty report is a valid result.
```

Batch size is about five runs per analyst.
With five runs or fewer, use one analyst.
Run analysts in parallel in a single turn.

## Merging

A pattern seen in two or more runs becomes a proposed change.

A pattern seen once goes on a watch list in the proposal and is not applied, with two exceptions:
a requirements gap, which is proposed as a reqs.md change because it will bite every future run until fixed,
and a prompt instruction that backfired, meaning the evidence shows it caused a regression or broke a requirement, because one occurrence is already proof the instruction is harmful.
A broken requirement counts even when every acceptance criterion passed: the judge's must-have probing is where these usually show up.

Merge duplicates across batches before counting.
Count runs, not versions: three failing versions inside one run are one occurrence.

## Checking existing lessons against the repo

For every lesson in learnings.md, check whether it is still true against the current repo, for example that the package manager, test command, path or convention it names still exists.
Read the files; do not assume.
Propose removing a lesson only when the repo contradicts it or a newer lesson supersedes it.
A lesson that no run cited is not stale on that basis alone: a lesson that prevents a failure leaves no trace in later runs.

## Proposal format

Write `proposal.md` in the dream directory:

```markdown
# Dream <dream-id>

Runs reviewed: <n> (<first run id> to <last run id>)
learnings.md sha256 at start: <hash>

## Proposed changes

### D1: add | sharpen | merge | remove | move to reqs.md
Before: <current lesson text, or "none">
After: <new lesson text, or "removed">
Evidence: <run ids with one quote each>
Seen in: <k> of <n> runs
Why: <one or two sentences>

## Watch list
<patterns seen once, with run id and quote, not applied>

## Checked and kept
<existing lessons that were verified against the repo, one line each>
```

Keep each lesson to one or two lines and keep the whole learnings.md around 40 lines after changes; propose merges when it would grow past that.

## Applying

Show the user the proposed changes and let them pick which to accept (AskUserQuestion with multiSelect works well, one option per change, at most four per question).
Then:

1. Run `temper.py snapshot --expect <hash from dream-prep>`.
   It refuses if learnings.md changed since the dream started, because another run or a person edited it in the meantime and the proposal may be based on old text.
   If it refuses, run the dream again rather than forcing the edit.
2. Edit learnings.md with the accepted changes only.
   Each lesson keeps its run ids so its origin stays traceable.
3. For accepted reqs.md changes, show the exact diff and edit reqs.md only after the user confirms that diff.
4. Write `applied.md` in the dream directory listing which changes were accepted and rejected.
5. Run `temper.py dream-done <dream-id>` so `status` can count runs since the last dream.
