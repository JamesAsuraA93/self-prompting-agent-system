# Rules template

`rules.md` sits next to `reqs.md` and holds the house rules that apply to everything in the project, whatever the task.
`reqs.md` says what to build this time; `rules.md` says how anything here must always be written.
Temper copies it into every prompt, the judge checks every output against it, and Temper's own files (prompts, verdicts, diagnoses, lessons, dream proposals) follow it too.

Start a new `rules.md` from the block below, then ask the user what to add or remove.
Keep the `## Forbidden text` section in this exact shape, because `temper.py rules-check` reads it: one bullet per item, either a Unicode code point written as `U+XXXX` or a literal sequence inside backticks, followed by a short reason.
Write code points rather than the characters themselves, so the rules file never contains what it forbids.

```markdown
# Rules

## Forbidden text
- U+2014 em dash: reads as machine-written; use a plain hyphen, a colon, or restructure the sentence
- U+2013 en dash: use a plain hyphen, or "to" in ranges
- U+2015 horizontal bar: same as the em dash
- ` -- ` spaced double hyphen used as a dash in prose: same as the em dash

## Writing
- Prose follows the voice and language rules of this project.

## Code
- Follow the conventions already used in the repo.
```

Common additions, offered to the user rather than added silently:

- U+201C, U+201D, U+2018, U+2019 curly quotes, when straight quotes are the house style
- U+2026 ellipsis character, when three dots are preferred
- U+2192 arrow, when "to" or "->" is preferred
- Rules for tone, language, naming, comment language, or commit messages
