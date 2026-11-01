# Verdict

Hard criteria: 8 of 8 passed
Failed or unclear: none
Must-have requirements not met: none

## AC1: `pytest` passes, and the repo contains tests covering R1 to R13.
Verdict: PASS
Evidence: `PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q` from the repo root:
```
...................................                                      [100%]
35 passed in 0.10s
```
`tests/test_export.py` has tests labelled for every requirement, for example `# R1 / AC2 test_header_columns_in_order`, `# R2 ... test_output_is_utf8_with_bom_and_thai_survives`, `# R3 ... test_rows_end_with_crlf`, `# R4 ... test_rfc4180_quoting`, `# R5 ... test_amount_two_decimals_no_thousands_separator`, `# R6 ... test_created_at_is_utc_iso_with_z`, `# R7 test_missing_note_is_empty_field`, `# R8 ... test_status_list_case_insensitive`, `# R9 ... test_cancelled_excluded_by_default`, `# R10 ... test_date_compares_in_bangkok_time_not_utc`, `# R11 ... test_sorted_by_created_at_then_order_id`, `# R12 test_no_matches_gives_header_only`, `# R13 ... test_unknown_status_raises_value_error_naming_it`.

## AC2: For `SAMPLE_ORDERS` with no filters, the output starts with the UTF-8 BOM, the first line is the exact header from R1, rows end with CRLF, and order 3 is absent.
Verdict: PASS
Evidence: raw output from `export_orders_csv(SAMPLE_ORDERS)`:
```
b'\xef\xbb\xbforder_id,customer,status,amount,created_at,note\r\n2,"Acme, Inc.",...\r\n1,...\r\n5,Ann,paid,0.50,2026-03-01T02:05:09Z,\r\n4,Bob,pending,10000.00,2026-03-01T17:15:00Z,"line one\nline two"\r\n'
AC2 bom: True first line: 'order_id,customer,status,amount,created_at,note'
AC2 ids: ['2', '1', '5', '4']
```
Every record ends with `\r\n`; the only bare `\n` is inside the quoted note of order 4. Order 3 is absent.

## AC3: Order 2's note is written as `"ส่งด่วน ""พิเศษ"""` and order 4's note keeps its line break inside quotes.
Verdict: PASS
Evidence: substring check on the decoded output: `AC3 order2: True order4: True`. Order 4's row in the raw bytes is `4,Bob,pending,10000.00,2026-03-01T17:15:00Z,"line one\nline two"\r\n`.

## AC4: Order 1's amount is `1234.50` and its created_at is `2026-03-01T02:05:09Z`.
Verdict: PASS
Evidence: `AC4 line1: ['1,สมชาย ใจดี,paid,1234.50,2026-03-01T02:05:09Z,']`

## AC5: `status=["PAID", "cancelled"]` returns orders 1, 5 and 3 and nothing else.
Verdict: PASS
Evidence: `AC5: ['1', '5', '3']`

## AC6: `date_from=date(2026, 3, 2), date_to=date(2026, 3, 2)` returns order 4 only (order 3 is cancelled).
Verdict: PASS
Evidence: `AC6: ['4']`

## AC7: Orders 1 and 5 share a timestamp and appear as 1 then 5.
Verdict: PASS
Evidence: the unfiltered order is `['2', '1', '5', '4']`, so 1 comes right before 5. The test `test_sorted_by_created_at_then_order_id` also checks this with the input reversed and passes.

## AC8: `status="refunded"` raises ValueError mentioning "refunded".
Verdict: PASS
Evidence: `AC8: ValueError("Unknown order status 'refunded'; expected one of pending, paid, shipped, cancelled")`

## Must-have requirements checked with my own inputs
I wrote a probe script in /tmp and ran it against `shop/export.py`. Every must-have held:
- R4: `customer='a,b'`, `note='x"y'`, `note='cr\ronly'` came out as `"a,b"`, `"x""y"` and `"cr\ronly"`. An empty-string note came out as an empty field.
- R5: `1234567` -> `1234567.00`, `-3.1` -> `-3.10`, `0` -> `0.00`, `1.234E+5` -> `123400.00`. No thousands separator and no exponent notation.
- R6: `2026-12-31 23:59:59.999999` at UTC-10 -> `2027-01-01T09:59:59Z`. It converts to UTC, rolls over the year, and drops the microseconds.
- R8: a tuple `("Shipped","PENDING")` -> `['2', '4']`. A stored status of `"Cancelled"` is matched case-insensitively.
- R9: a stored `"Cancelled"` order is hidden by default and returned with `status="cancelled"`.
- R10: at the Bangkok midnight boundary, `2026-03-01 16:59:59Z` falls on 3/1 and `17:00:00Z` falls on 3/2 when filtering on a single day.
- R11: when timestamps tie, ids 10 and 2 sort numerically as `['2', '10', ...]`.
- R12: `status="shipped", date_from=2026-03-02` -> `b'\xef\xbb\xbforder_id,customer,status,amount,created_at,note\r\n'`
- R13: `"Refunded"`, `["paid","refunded"]`, `""` and `"paid "` each raise ValueError, and each message names the bad value.

## Advisory
There are no `[judgment]` criteria in the requirements.

## Other observations
- The implementation imports only the standard library (`csv`, `io`, `datetime`, `decimal`).
- Some behaviour goes beyond what the requirements ask for, but none of it conflicts with them:
  - A naive `created_at` raises ValueError.
  - Amounts with more than two decimals are rounded half-up (`2.005` -> `2.01`).
  - An empty status list counts as "no filter", so cancelled orders are still hidden.
  - `date_from > date_to` returns the header only.
  - The requirements do not specify these cases. If accounting cares about the empty-list or rounding behaviour, the requirements should say so.
- The status column is written exactly as stored, not lower-cased. R1 and R8 do not settle this.
- There is no git history, so I could not diff the `Order` dataclass or the function signature against an original. Both look consistent with the requirements (`export_orders_csv(orders, status=None, date_from=None, date_to=None) -> bytes`).
- `__pycache__` folders in `shop/` and `tests/`, and a `.pytest_cache`, were already in the repo before my checks ran. My runs used `PYTHONDONTWRITEBYTECODE=1 -p no:cacheprovider` and created none, so I left the existing ones alone.
