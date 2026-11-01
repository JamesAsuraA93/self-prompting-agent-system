# Benchmark: Temper vs a plain request

Three tasks, each with its own `reqs.md`, run once with Temper and once with a plain "Do what reqs.md in this repo asks for."
The task repos live in `plugins/temper/skills/temper/evals/<case>/files/`.

Grading used hidden tests that neither side could see, written before any run and validated first against reference implementations.
They are in `hidden/`, and `grade.py` applies them to an iteration folder laid out as `<case>/<with_skill|without_skill>/outputs/repo`.

## Results

| Case | Temper | Plain request |
|---|---|---|
| csv-export-thai (Python) | 21/21 | 21/21 |
| parse-duration (Node) | 50/51 | 51/51 |
| runbook-from-cli (Thai docs) | 17/17 | 17/17 |
| Mean tokens | 156k | 67k |
| Mean wall time | 216 s | 76 s |

Temper's token and time figures cover the executor and judge subagents only, not the compile work in the main thread, so its real overhead is higher.

## What it shows

There is a ceiling effect.
Every `reqs.md` already had specific, testable acceptance criteria, which is the part Temper's intake step normally adds, so the plain request scored full marks.

Temper's one miss came from its own compiler: prompt v1 added "pick the stricter reading", and the executor decided "whitespace" excluded newlines.
`references/compiler.md` now forbids tie-break rules the requirements do not state.

Temper's judge flagged things the hidden tests do not measure:
an undefined "whitespace" in one spec, "6000 characters" meaning characters or bytes in another, and runbook actions written as fact without support in the code.
Under the skill's rules those stop the loop and go back to the user as requirements gaps.

## Caveats

One run per configuration, so there is no variance estimate.
The skill's author also compiled the prompts; test-informed hints were removed from the prompts before execution, and grading used only the hidden tests.
