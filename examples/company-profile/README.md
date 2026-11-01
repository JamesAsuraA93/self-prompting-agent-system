# Example: static company profile, with and without Temper

The same brief built two ways: a one-page Thai company profile site for Doi Phrao Hill Roasters, a fictional coffee roaster in Chiang Mai.
The company, people, address and phone number are invented, and the site says so in its footer.

- [`reqs.md`](reqs.md): the shared requirements, with company facts and 15 acceptance criteria
- [`without-temper/`](without-temper/): built by one agent given only "Build what reqs.md in this folder asks for."
- [`with-temper/`](with-temper/): built by the Temper loop over three runs, with every prompt, verdict and diagnosis kept in [`with-temper/.temper/`](with-temper/.temper/)
- [`checker/`](checker/): the hidden acceptance checker used to grade both, which neither builder saw

## Final result

Live, once GitHub Pages has built:
[without Temper](https://jamesasuraa93.github.io/self-prompting-agent-system/examples/company-profile/without-temper/)
and
[with Temper](https://jamesasuraa93.github.io/self-prompting-agent-system/examples/company-profile/with-temper/).
You can also open `index.html` in either folder directly.

| Without Temper | With Temper |
|---|---|
| ![Without Temper, hero](screenshots/final-without-temper-hero.png) | ![With Temper, hero](screenshots/final-with-temper-hero.png) |
| ![Without Temper, hero in dark mode](screenshots/final-without-temper-hero-dark.png) | ![With Temper, hero in dark mode](screenshots/final-with-temper-hero-dark.png) |

Full page, desktop at 1280 px (scaled to half size) and mobile at 375 px:

| Without Temper | With Temper |
|---|---|
| ![Without Temper, full page desktop](screenshots/final-without-temper-desktop.png) | ![With Temper, full page desktop](screenshots/final-with-temper-desktop.png) |

| Without Temper, mobile | With Temper, mobile |
|---|---|
| ![Without Temper, mobile](screenshots/final-without-temper-mobile.png) | ![With Temper, mobile](screenshots/final-with-temper-mobile.png) |

Both pass all 35 automated checks.
The Temper site went through three runs and one extra requirement from the owner, so read the history below before comparing them like for like.

## How each side was built

The plain side got one sentence and the folder, and finished in one pass.

The Temper side went through the loop in [`SKILL.md`](../../plugins/temper/skills/temper/SKILL.md) three times.

### Run 001: build

1. The compiler wrote [`prompt.v1.md`](with-temper/.temper/runs/001/prompt.v1.md) from `reqs.md`, adding one environment fact: Playwright with Chromium is installed and can be used to check the page.
2. A fresh executor built the site from that prompt alone.
3. A separate judge graded it against `reqs.md` without seeing the prompt: [`judge.v1.md`](with-temper/.temper/runs/001/judge.v1.md). All 14 hard criteria passed; the `[judgment]` criterion AC15 failed because Thai text in the four-column cards broke mid-word at 1024 to 1280 px.
4. The script returned `pass_with_advisory`, and the run continued because the owner's standing rule is to fix anything that looks off.
5. [`diagnosis.v1.md`](with-temper/.temper/runs/001/diagnosis.v1.md) traced the cause and [`prompt.v2.md`](with-temper/.temper/runs/001/prompt.v2.md) is a targeted edit of v1.
6. The v2 executor found a second cause on its own (Chromium's Thai dictionary splits loanwords such as ทุกล็อต and บาริสต้า), fixed both, and the v2 judge passed everything: [`judge.v2.md`](with-temper/.temper/runs/001/judge.v2.md).

| Plain request | Temper v1 | Temper v2 |
|---|---|---|
| ![Plain request, service cards](screenshots/without-temper-cards-1280.png) | ![Temper v1, service cards](screenshots/with-temper-v1-cards-1280.png) | ![Temper v2, service cards](screenshots/with-temper-v2-cards-1280.png) |

### Run 002: polish

The v2 judge had passed the site but listed small nits: a footer box much wider than its text, unequal hero buttons at 360 px, a short first line in one card, the company name repeated in the hero, a `#top` link with no target, and a 1 px overlap under the sticky header.
The owner asked for them to be fixed.
A new run started from [`prompt.v1.md`](with-temper/.temper/runs/002-polish/prompt.v1.md), with the run 001 lessons from `learnings.md` copied into it, and the judge passed it: [`judge.v1.md`](with-temper/.temper/runs/002-polish/judge.v1.md).

### Run 003: design

Looking at the result, the owner said the site lacked taste: tidy, but it could be any company's template.
That is a requirements gap, since `reqs.md` only asked for "finished and intentional", so it was written into [`with-temper/reqs.md`](with-temper/reqs.md) as R16 plus two `[judgment]` criteria, AC16 (a memorable identity drawn from the subject) and AC17 (crafted details in both themes).
The fonts constraint stayed: no web fonts and nothing over 100 KB, so identity had to come from composition, color and inline SVG.
The executor was pointed at the `frontend-design` skill: [`prompt.v1.md`](with-temper/.temper/runs/003-design/prompt.v1.md).

The redesign added a contour map of the hill behind the hero, a kraft lot tag carrying the key numbers, the process drawn as a roast curve, team initials in espresso cups seen from above, and a different layout for every section.
The judge passed all 14 hard criteria and AC15 to AC17: [`judge.v1.md`](with-temper/.temper/runs/003-design/judge.v1.md).

Lessons from all three runs are in [`learnings.md`](with-temper/.temper/learnings.md).

## Results

| | Plain request | Temper |
|---|---|---|
| Hidden checker (35 checks, AC1 to AC14) | 35/35 | 35/35 after every run |
| AC15, looks finished | graded only by the builder itself | failed in run 001 v1, passed from v2 on |
| Design identity (AC16, AC17, added in run 003) | not asked for | passed |
| Runs and versions | 1 | 3 runs, 4 versions |
| Tokens | 156k | 1.31M |
| Wall time | 12 min | 73 min |

On the first two runs, which shared the plain side's requirements, Temper cost about 3.6 times the tokens and produced the same automated score.
What it added was a reviewer with fresh eyes, which caught a visual bug the builder had introduced and missed in its own review.
The bigger difference in the final screenshots comes from run 003, where the owner raised the bar and the loop had a way to absorb that: a new requirement, a judge that grades against it, and lessons carried forward.

## Still open

The run 003 judge passed the site and listed nits it did not count as failures.
The ones worth fixing next:

- In dark mode the red accent turns candy pink, and the focus color is close to the error color.
- In dark mode the footer's hill outline and the form card edge almost vanish (1.02:1 and 1.03:1 against the background).
- After a failed submit, the first field's label sits partly under the sticky header.
- On desktop the contact column has an empty gap of about 150 px above the details.
- The hero, about heading, about text and facts list repeat the same lines.
- The team section is sparse on desktop, and the hero markup has an unused hidden circle.

## Fairness notes

The checker was written and validated against a throwaway reference site before either side ran, and it was kept outside both project folders.
The transcripts of both builders were searched afterwards; neither opened the checker or the reference site.
Two checker bugs were found while grading and fixed for both sides alike: a word list that missed "สาธิต" (demo) in the footer notice, and a dark-mode contrast check that ran while color transitions were still animating.
The plain side's `reqs.md` is the original; the Temper side's carries the reworded AC13 and the run 003 design criteria.
One build per side, so there is no variance estimate.

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

It prints one JSON object per check and, with a second argument, saves screenshots at 375 px and 1280 px in light and dark mode.
