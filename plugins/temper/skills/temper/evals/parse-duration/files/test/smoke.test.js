import { test } from "node:test";
import assert from "node:assert/strict";
import { parseDuration } from "../src/duration.js";

test("parses minutes", () => {
  assert.equal(parseDuration("5m"), 300);
});
