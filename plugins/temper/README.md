# Temper

Temper turns a project's requirements file (`reqs.md` or `need.md`) into an engineered prompt, runs it with a fresh agent, grades the result against the acceptance criteria with a separate judge that never sees the prompt, and rewrites the prompt until the result passes.
Every run keeps its prompts, verdicts and diagnoses in `.temper/` in your project, and a lessons file carries what was learned into the next run.
A `dream` mode reviews many past runs at once, finds failures that keep coming back, checks old lessons against the current code, and proposes edits for you to accept.

## Install

In Claude Code:

```
/plugin install temper --marketplace JamesAsuraA93/self-prompting-agent-system
```

## Use

In a project with a `reqs.md`, ask Claude to "use temper on reqs.md".
Ask it to "write a reqs.md for this" to be interviewed and get requirements with testable criteria, "just compile the prompt" to stop before running, or "dream over the last runs" to consolidate lessons.

## Setup

None beyond Python 3 for the bookkeeping script.
The loop uses subagents, so it works best in Claude Code.

Source, benchmark and a worked example: https://github.com/JamesAsuraA93/self-prompting-agent-system
