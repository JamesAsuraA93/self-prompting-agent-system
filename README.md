# Temper

A Claude Code skill that turns a requirements file into a prompt, runs it, grades the result against the requirements, and rewrites the prompt until the result passes.
It keeps versioned prompts and a lessons file per project, and a separate "dream" pass reviews past runs to clean up what was learned.

Named after tempering steel: heat it, hammer it, test it, repeat until it holds.

## Benchmark

Four tasks, each built from the same `reqs.md` with a plain request and with Temper, graded by hidden tests that neither side saw.

| Task | Plain request | Temper | Tokens, plain / Temper |
|---|---|---|---|
| csv-export-thai (Python) | 21/21 | 21/21 | 71k / 149k |
| parse-duration (Node) | 51/51 | 51/51 | 65k / 147k |
| runbook-from-cli (Thai docs) | 17/17 | 17/17 | 65k / 144k |
| company profile site (HTML, CSS, JS) | 35/35 | 35/35 | 156k / 557k |

Honest reading: when the requirements are already sharp, Temper does not score higher, and it costs about 2 to 3.6 times the tokens.
What it adds is outside the tests.
On the site, its judge caught Thai text breaking mid-word that the builder had introduced and missed, and the loop fixed it.
On the runbook, the judge found two places where the requirements were ambiguous and stopped to ask instead of guessing.
Details, per-case prompts and verdicts, and the history of earlier runs are in [benchmark/](benchmark/).

Final result of the company profile example, after the owner asked Temper for more taste (see [the example](examples/company-profile/) for how it got there):

| Without Temper | With Temper |
|---|---|
| ![Without Temper](examples/company-profile/screenshots/final-without-temper-hero.png) | ![With Temper](examples/company-profile/screenshots/final-with-temper-hero.png) |

The loop is most useful where a single attempt tends to miss: vague requirements, larger tasks, work that tests cannot fully check, and projects where the same mistakes repeat across runs.

## How it works

You write what you need in `reqs.md` (or `need.md`), with acceptance criteria that someone else could check.
Beside it sits `rules.md`, the house rules that hold for every task in the project, such as forbidden characters (the em dash, for one) or voice and naming conventions. Temper creates it from a template when it is missing, copies it into every prompt, has the judge check every output against it, and follows it in its own files. `temper.py rules-check` does the mechanical part and fails on any forbidden text.
Temper then runs a loop with three roles that deliberately see different things:

```
reqs.md + rules.md + repo + learnings.md
        |
        v
  compiler (main thread): writes prompt.vN.md
        |
        v
  executor (fresh subagent): sees only the prompt, does the work
        |
        v
  judge (fresh subagent): sees reqs.md and the output, never the prompt
        |
        v
  temper.py record: decides to stop, continue, or ask
        |
        v
  diagnose -> prompt gap? fix the prompt and go again
              requirements gap? stop and ask you
```

The split is the point.
The context that writes a prompt cannot see what it left out, so a fresh executor exposes missing context by failing, and a judge that never saw the prompt grades against what you asked for rather than how the prompt interpreted it.

A small script makes the stop decision from the log instead of the model's mood: stop when everything passes, stop when a new version does not beat the best one so far, stop at the iteration limit, and ask you when only subjective `[judgment]` criteria are left.

### Dreaming

The in-band lessons file has blind spots: the agent writing a lesson is busy finishing its run, it sees one run only, and lessons go stale as the code changes.
`dream` mode is a separate pass: subagents read every past run, find failures that keep coming back, check existing lessons against the current code, and propose edits with evidence and counts.
You accept or reject each one, and the script snapshots the old file and refuses to write if it changed in the meantime.

The dreaming idea comes from a talk by Anthropic's Applied AI team at AI DevCon on agent memory.

## Install

As a plugin, from inside Claude Code:

```
/plugin marketplace add JamesAsuraA93/self-prompting-agent-system
/plugin install temper@asuraa93
```

Or from your shell:

```bash
claude plugin marketplace add JamesAsuraA93/self-prompting-agent-system
```

```bash
claude plugin install temper@asuraa93
```

Or copy the skill folder into your personal skills:

```bash
git clone https://github.com/JamesAsuraA93/self-prompting-agent-system /tmp/temper && cp -r /tmp/temper/plugins/temper/skills/temper ~/.claude/skills/temper
```

## Use

In a project that has a `reqs.md`:

- "use temper on reqs.md" runs the full loop
- "write a reqs.md for this" interviews you and writes one, with testable criteria
- "just compile the prompt from need.md" stops after writing the prompt
- "dream over the last runs" consolidates the lessons file

Everything Temper writes lives in `.temper/` in your project: prompts, verdicts, diagnoses, the iteration log, `learnings.md`, and dream proposals.

## Layout

```
.claude-plugin/marketplace.json
plugins/temper/
  .claude-plugin/plugin.json
  skills/temper/
    SKILL.md
    references/      compiler, judge, dreamer briefs and the reqs template
    scripts/temper.py
    evals/           benchmark task repos
benchmark/           results, hidden tests, grading script
examples/            sample projects built with and without Temper
```

## License

MIT
