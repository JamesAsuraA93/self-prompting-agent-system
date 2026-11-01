# Task
Implement `parseDuration` and `formatDuration` in `src/duration.js`, and write a test suite that covers every requirement below.
This module becomes the single strict duration parser that every service in the company imports for job timeouts and intervals written in YAML as strings like `1h30m`.

## Why this matters
Every service currently parses these strings its own way.
Last month a typo, `1h30` instead of `1h30m`, was read as 1 hour 30 seconds and a backup job was killed early.
So the parser's job is to reject anything ambiguous instead of guessing.

## Context
Node 22, ES modules (`"type": "module"` in package.json), no dependencies.
Tests run with `npm test`, which is `node --test` and picks up `test/*.test.js`.
`src/duration.js` already exports `DurationError` (a subclass of Error), `parseDuration` and `formatDuration` as stubs. Keep all three exports and their names.
`test/smoke.test.js` has one existing test.

## What to deliver
The implementation in `src/duration.js`.
A test file `test/duration.test.js` covering R1 to R12.

## Requirements
- R1: Units are d, h, m, s (days, hours, minutes, seconds), case-insensitive.
- R2: A duration is one or more components like `2h`, each a non-negative integer followed by a unit. Leading zeros are allowed (`05m`).
- R3: Components must appear in descending unit order (d, h, m, s) and each unit at most once, so `1m1h` and `1h1h` are invalid.
- R4: Whitespace is allowed around the whole string and between components (` 1h 30m `), but not between a number and its unit (`1 h` is invalid).
- R5: A bare integer with no unit is invalid, including `0` and `90`. This is the bug from the Why section.
- R6: Decimals, signs (`+`, `-`), and any other characters are invalid.
- R7: The total must be greater than 0 and at most 30 days (2592000 seconds). `0s` and `0h0m` are invalid, `30d` is valid, `30d1s` is invalid.
- R8: Invalid strings throw `DurationError` (already exported, a subclass of Error) whose message includes the original input in JSON-quoted form, for example `Invalid duration: "1h30"`.
- R9: Non-string input throws TypeError.
- R10: `formatDuration(seconds)` returns the canonical form: units in descending order, zero components left out, no spaces, lowercase. 5400 becomes `1h30m`, 86400 becomes `1d`, 90061 becomes `1d1h1m1s`.
- R11: `formatDuration` throws RangeError unless its input is an integer from 1 to 2592000.
- R12: For every valid input, `parseDuration(formatDuration(n)) === n`.


## Constraints and out of scope
No dependencies; keep the existing exports.
No months, weeks, milliseconds, or natural-language phrases.

## Acceptance criteria
- AC1: `npm test` passes, and the test suite covers R1 to R12.
- AC2: `parseDuration("1h30m")` is 5400, `parseDuration(" 2D 5s ")` is 172805, and `parseDuration("05m")` is 300.
- AC3: `"1h30"`, `"90"`, `"1m1h"`, `"1 h"`, `"1.5h"`, `"-5m"`, `""` and `"30d1s"` each throw DurationError.
- AC4: The DurationError for `1h30` has a message containing `"1h30"` with the double quotes.
- AC5: `parseDuration(5400)` throws TypeError.
- AC6: `formatDuration(90061)` is `1d1h1m1s`, and `formatDuration(0)`, `formatDuration(1.5)` and `formatDuration(2592001)` throw RangeError.

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Run `npm test` and make sure it passes.
Check your work against every acceptance criterion; for each one, report PASS or FAIL and how you checked it, running code where possible.
