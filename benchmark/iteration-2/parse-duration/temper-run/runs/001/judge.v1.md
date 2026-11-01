# Verdict

Hard criteria: 6 of 6 passed
Failed or unclear: none
Must-have requirements not met: none

## AC1: `npm test` passes, and the test suite covers R1 to R12.
Verdict: PASS
Evidence: `npm test` from the repo root (Node v22.23.4):
```
# tests 39
# suites 14
# pass 39
# fail 0
# cancelled 0
# skipped 0
```
Coverage: `test/duration.test.js` has one `describe` block per requirement, named "R1: units d, h, m, s, case-insensitive" through "R12: parseDuration(formatDuration(n)) === n". Each block asserts the behaviour it names. For example, R5 checks `"0"`, `"90"`, `"1h30"`, `"2h 30"`; R7 checks `"30d"`, `"30d1s"`, `"0h0m"`; R8 checks `err.message === 'Invalid duration: "1h30"'`; R9 checks 11 non-string values, including `new String("1h")` and `5400n`; R12 round-trips every n from 1 to 2592000. There is also a separate "Acceptance examples" block for AC2 and AC3, and the original `test/smoke.test.js` is still there and passing.

## AC2: `parseDuration("1h30m")` is 5400, `parseDuration(" 2D 5s ")` is 172805, and `parseDuration("05m")` is 300.
Verdict: PASS
Evidence: probe script (/tmp/judge-probe/probe.mjs):
```
parse("1h30m") => 5400
parse(" 2D 5s ") => 172805
parse("05m") => 300
```

## AC3: `"1h30"`, `"90"`, `"1m1h"`, `"1 h"`, `"1.5h"`, `"-5m"`, `""` and `"30d1s"` each throw DurationError.
Verdict: PASS
Evidence:
```
parse("1h30") => throws DurationError "Invalid duration: \"1h30\""
parse("90") => throws DurationError "Invalid duration: \"90\""
parse("1m1h") => throws DurationError "Invalid duration: \"1m1h\""
parse("1 h") => throws DurationError "Invalid duration: \"1 h\""
parse("1.5h") => throws DurationError "Invalid duration: \"1.5h\""
parse("-5m") => throws DurationError "Invalid duration: \"-5m\""
parse("") => throws DurationError "Invalid duration: \"\""
parse("30d1s") => throws DurationError "Invalid duration: \"30d1s\""
```

## AC4: The DurationError for `1h30` has a message containing `"1h30"` with the double quotes.
Verdict: PASS
Evidence: the message is `Invalid duration: "1h30"`, built in src/duration.js as `` new DurationError(`Invalid duration: ${JSON.stringify(input)}`) ``. Other inputs are quoted the JSON way too: the probe checked `'a"b'`, `"\n"` and a string containing U+2028, and each message includes `JSON.stringify(input)` (true for all three).

## AC5: `parseDuration(5400)` throws TypeError.
Verdict: PASS
Evidence: `parse(5400) => throws TypeError "parseDuration expects a string, got number"`. The suite also asserts that this error is not a DurationError.

## AC6: `formatDuration(90061)` is `1d1h1m1s`, and `formatDuration(0)`, `formatDuration(1.5)` and `formatDuration(2592001)` throw RangeError.
Verdict: PASS
Evidence:
```
format(90061) => "1d1h1m1s"
format(0) => throws RangeError
format(1.5) => throws RangeError
format(2592001) => throws RangeError
```

## Must-have requirements, tested with my own inputs
- R1: PASS. `"2H30M"` => 9000, `"30D"` => 2592000. Look-alike letters are rejected: `"1ſ"` (long s), `"1K"`, fullwidth `"1ｈ"`. Repeats that differ only in case are rejected: `"1Hh"`, `"1hH"`.
- R2: PASS. `"0001d"` => 86400, `"00000000000000000000000000000000001s"` => 1, `"0m1s"` => 1. A number with no unit is rejected (`"h1"`, `"1hh"`), and so are fullwidth digits (`"１h"`).
- R3: PASS. `"1s1h"`, `"1m30s1m"` and `"1d1d"` are rejected.
- R4: PASS. `"1h\t\t30m"`, `"1h\r\n30m"` and `"1h 30m 15s"` (=> 5415) are accepted. `"Infinity s"` and `"1h30m 15"` are rejected.
- R5: PASS. `"0"`, `"00"` and `"1h30m 15"` are rejected.
- R6: PASS. `"+1h"`, `"1h-"`, `"1_000s"`, `"1e2s"`, `"NaNs"`, `"1h30m;"` and `"1h30m\u0000"` are rejected.
- R7: PASS. These equal exactly 2592000 and are accepted: `"720h"`, `"43200m"`, `"2592000s"`, `"29d24h"`. `"2592001s"`, `"0s0s"` and `"  0s  "` are rejected. A huge value, `"10000000000000000000000000000000000d"`, is rejected rather than overflowing.
- R8: PASS. `Object.getPrototypeOf(DurationError.prototype) === Error.prototype` is true. Every rejection above carried the JSON-quoted input in its message.
- R9: PASS. These all throw TypeError: null, undefined, `1n`, `{}`, `[]`, `new String("1h")`, `Symbol()`.
- R10: PASS. 59 => `59s`, 61 => `1m1s`, 86399 => `23h59m59s`, 2592000 => `30d`. I checked every n from 1 to 2592000 against the canonical pattern (descending, lowercase, no zero components, h<=23, m<=59, s<=59): 0 outputs broke it.
- R11: PASS. These all throw RangeError: `-5`, `NaN`, `Infinity`, `1e100`, `"60"` (string), `null`. `2.0` is accepted, since it is the integer 2.
- R12: PASS. I round-tripped every n from 1 to 2592000 myself: 0 failures.

## Advisory
No `[judgment]` criteria in the requirements.

## Other observations
- Exports are `DurationError`, `formatDuration` and `parseDuration`. No dependencies were added (`package.json` has no dependencies field).
- Requirements ambiguity (R4): "whitespace" is not defined. The implementation accepts only ASCII whitespace (space, \t, \n, \r, \f, \v). It rejects non-ASCII whitespace even around the whole string: `" 1h"` (NBSP) and `"1h　30m"` (ideographic space) both throw DurationError. This fits the strict intent, but if YAML values could carry NBSP, the requirements should say which whitespace counts.
- Non-canonical spellings that land within the limit are accepted, for example `"29d24h"` and `"720h"`. R2 and R7 allow this, so it is not a defect. Note it only in case the user expected per-unit bounds such as h<=23.
- The R12 test loops over 2.59M values and takes about 3 seconds. That is acceptable, but it is the slowest part of the suite.
