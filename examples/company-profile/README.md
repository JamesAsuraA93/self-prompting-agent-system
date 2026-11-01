# Example: static company profile, with and without Temper

The same `reqs.md` built twice: a one-page Thai company profile site for Doi Phrao Hill Roasters, a fictional coffee roaster in Chiang Mai.
The company, people, address and phone number are invented, and the site says so in its footer.

- [`reqs.md`](reqs.md): the shared requirements, with company facts and 15 acceptance criteria (one of them `[judgment]`)
- [`without-temper/`](without-temper/): built by one agent given only "Build what reqs.md in this folder asks for."
- [`with-temper/`](with-temper/): built by the Temper loop, with every artifact kept in [`with-temper/.temper/`](with-temper/.temper/)
- [`checker/`](checker/): the hidden acceptance checker used to grade both, which neither side saw

Open `index.html` in either folder to see the site.

## How each side was built

The plain side got one sentence and the folder.

The Temper side went through the loop in [`SKILL.md`](../../plugins/temper/skills/temper/SKILL.md):

1. The compiler wrote [`prompt.v1.md`](with-temper/.temper/runs/001/prompt.v1.md) from `reqs.md`, adding one environment fact: Playwright with Chromium is installed and can be used to check the page.
2. A fresh executor built the site from that prompt alone.
3. A separate judge graded it against `reqs.md` without seeing the prompt: [`judge.v1.md`](with-temper/.temper/runs/001/judge.v1.md). All 14 hard criteria passed; the `[judgment]` criterion AC15 failed because Thai text in the four-column cards broke mid-word at 1024 to 1280 px.
4. The script returned `pass_with_advisory`. The run continued because the project owner's standing rule is to fix anything that looks off.
5. [`diagnosis.v1.md`](with-temper/.temper/runs/001/diagnosis.v1.md) traced the cause, and [`prompt.v2.md`](with-temper/.temper/runs/001/prompt.v2.md) is a targeted edit of v1.
6. The v2 executor found a second cause on its own (Chromium's Thai dictionary splits loanwords such as ทุกล็อต and บาริสต้า), fixed both, and the v2 judge passed everything: [`judge.v2.md`](with-temper/.temper/runs/001/judge.v2.md).
7. Two lessons went into [`learnings.md`](with-temper/.temper/learnings.md) for the next task in this project.

## Results

| | Plain request | Temper |
|---|---|---|
| Hidden checker (35 checks, AC1 to AC14) | 35/35 | 35/35 after v1 and after v2 |
| AC15, looks finished at 375 and 1280 px | not graded by anyone | v1 failed, v2 passed |
| Thai wrapping in the service cards at 1280 px | two awkward breaks (ลาเต้ / อาร์ต, เครื่อง / ชง) | v1 three broken breaks, v2 clean |
| Tokens | 156k | 557k (two executor and two judge runs) |
| Wall time | 12 min | 27 min |

Service cards at 1280 px, plain request:

![Plain request, service cards](screenshots/without-temper-cards-1280.png)

Temper v1, where the judge failed AC15:

![Temper v1, service cards](screenshots/with-temper-v1-cards-1280.png)

Temper v2:

![Temper v2, service cards](screenshots/with-temper-v2-cards-1280.png)

More screenshots are in [`screenshots/`](screenshots/), including both heroes in light and dark mode and both mobile layouts.

## What this shows

On the automated checks the two sides are identical.
Both agents read the same sharp `reqs.md`, both checked their own work with Playwright, and both passed everything a script can test.

The difference is in what nobody tests by script.
The plain side never had its "looks finished" criterion graded by anyone but itself.
Temper's judge looked at the page with fresh eyes, caught a visual problem the executor had introduced while fixing another one, and the loop fixed it.
That cost about 3.6 times the tokens.

The v2 judge still noted small things it did not count as failures: the footer notice box is much wider than its text on desktop, the two hero buttons stack at unequal widths at 360 px, and AC13's wording ("every script") technically includes the JSON-LD block, which should be reworded to "every executable script".

## Fairness notes

The checker was written and validated against a throwaway reference site before either side ran, and it was kept outside both project folders.
The transcripts of both builders were searched afterwards; neither opened the checker or the reference site.
Two checker bugs were found while grading and fixed for both sides alike: a word list that missed "สาธิต" (demo) in the footer notice, and a dark-mode contrast check that ran while color transitions were still animating.
One run per side, so there is no variance estimate.

## Run the checker

```bash
cd checker && npm install
```

```bash
node check.cjs ../without-temper
```

```bash
node check.cjs ../with-temper ./shots
```

It prints one JSON line per check and, with a second argument, saves screenshots at 375 px and 1280 px in light and dark mode.
