# Benchmark: Temper vs a plain request

Each task has its own `reqs.md` and is built twice: once with Temper, once with the plain request "Do what reqs.md in this repo asks for."
Grading uses hidden tests that neither side saw, written before any run and validated first against reference implementations.

The three code and docs tasks live in `plugins/temper/skills/temper/evals/<case>/files/`, their hidden tests in [`hidden/`](hidden/), and [`grade.py`](grade.py) applies them to an iteration folder laid out as `<case>/<with_skill|without_skill>/outputs/repo`.
The fourth task is the [company profile example](../examples/company-profile/), graded by its own Playwright and axe-core checker.

## Current results (Temper 0.1.0)

| Task | Plain request | Temper | Tokens, plain / Temper | Wall time, plain / Temper |
|---|---|---|---|---|
| csv-export-thai (Python) | 21/21 | 21/21 | 71k / 149k | 101 s / 164 s |
| parse-duration (Node) | 51/51 | 51/51 | 65k / 147k | 65 s / 156 s |
| runbook-from-cli (Thai docs) | 17/17 | 17/17 | 65k / 144k | 61 s / 149 s |
| company profile site (HTML, CSS, JS) | 35/35 | 35/35 | 156k / 557k | 12 min / 27 min |
| Total | 124/124 | 124/124 | 356k / 997k | |

Temper's figures cover its executor and judge subagents, not the compile step in the main thread, so its real overhead is somewhat higher.
For the company profile site the Temper figure is run 001 (two versions), the one built from the same requirements as the plain side; the later polish and design runs are described in that example.

Per-case artifacts for the three code and docs tasks are in [`iteration-2/`](iteration-2/): the compiled prompt, the judge's verdict, the diagnosis where there was one, and the hidden-test grading for both sides.

## What it shows

On these tasks Temper does not score higher than a plain request.
Every `reqs.md` here already has specific, testable acceptance criteria, which is the part Temper's intake step normally adds, so a strong model gets full marks either way.
Temper costs about 2.2 times the tokens on the small tasks and about 3.6 times on the site, where it ran a second version.

What it adds shows up outside the hidden tests:

- On the site, the judge caught Thai text breaking mid-word in the cards, which the builder had introduced and missed in its own review, and the loop fixed it in a second version.
- On the runbook, the judge failed AC3 and R3 on a strict reading: an uncaught crash exits with code 1, which the exit code table leaves out, and argparse's built-in `--help` is never mentioned. It called both requirements gaps, and the loop stopped to ask the owner instead of guessing ([diagnosis](iteration-2/runbook-from-cli/temper-run/runs/001/diagnosis.v1.md)).
- The judges also listed choices the requirements leave open, such as how amounts round and what an empty status list means in the CSV task, which an owner would want to settle before shipping.

## History

Iteration 1 used an earlier version of the skill.
Temper scored 88/89 then: its compiler had added "pick the stricter reading" to the duration prompt, and the executor read "whitespace" as excluding newlines.
`references/compiler.md` now forbids tie-break rules that the requirements do not state, and the iteration 2 prompt for that task differs from iteration 1 only by removing that rule and one similar line.
The judge brief also changed between iterations: it now probes every must-have requirement with its own inputs, which is why the runbook verdict is stricter in iteration 2.

| Task | Temper, iteration 1 | Temper, iteration 2 |
|---|---|---|
| csv-export-thai | 21/21 | 21/21 |
| parse-duration | 50/51 | 51/51 |
| runbook-from-cli | 17/17 | 17/17 |

## Caveats

One run per configuration, so there is no variance estimate.
The plain side was run once, in iteration 1, and reused, since a plain request does not depend on the skill.
The skill's author also compiled the prompts; test-informed hints were removed before execution, and grading used only the hidden tests.
