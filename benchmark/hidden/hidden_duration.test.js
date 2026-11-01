import { test } from "node:test";
import assert from "node:assert/strict";
import { parseDuration, formatDuration, DurationError } from "../src/duration.js";

const ok = (s, n) => test(`valid ${JSON.stringify(s)}`, () => assert.equal(parseDuration(s), n));
const bad = (s) => test(`invalid ${JSON.stringify(s)}`, () => assert.throws(() => parseDuration(s), DurationError));

ok("1h30m", 5400);
ok("1H30M", 5400);
ok(" 2D 5s ", 172805);
ok("05m", 300);
ok("1d1h1m1s", 90061);
ok("30d", 2592000);
ok("0h1s", 1);
ok("\t1h\t30m\n", 5400);

for (const s of ["1h30", "90", "0", "1m1h", "1h1h", "1s1d", "1 h", "1.5h", "-5m", "+5m", "", "   ", "30d1s", "31d", "0s", "0h0m", "5x", "h", "1hh", "1h,30m", "5m 5", "1h_30m"]) bad(s);

test("error is a DurationError subclass of Error with quoted input", () => {
  try {
    parseDuration("1h30");
    assert.fail("should throw");
  } catch (e) {
    assert.ok(e instanceof DurationError && e instanceof Error);
    assert.ok(e.message.includes('"1h30"'), e.message);
  }
});

test("error message JSON-quotes inputs with special characters", () => {
  try {
    parseDuration('1"h');
    assert.fail("should throw");
  } catch (e) {
    assert.ok(e.message.includes(JSON.stringify('1"h')), e.message);
  }
});

for (const v of [5400, null, undefined, {}, ["1h"]]) {
  test(`non-string ${JSON.stringify(v)} throws TypeError`, () => assert.throws(() => parseDuration(v), TypeError));
}

const fmt = (n, s) => test(`format ${n}`, () => assert.equal(formatDuration(n), s));
fmt(5400, "1h30m");
fmt(86400, "1d");
fmt(90061, "1d1h1m1s");
fmt(1, "1s");
fmt(2592000, "30d");
fmt(3601, "1h1s");

for (const v of [0, -1, 1.5, 2592001, NaN, "60"]) {
  test(`format ${String(v)} throws RangeError`, () => assert.throws(() => formatDuration(v), RangeError));
}

test("round trip on a spread of values", () => {
  for (const n of [1, 59, 60, 61, 3599, 3600, 86399, 86401, 1234567, 2592000]) {
    assert.equal(parseDuration(formatDuration(n)), n);
  }
});
