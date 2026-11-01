# Task
Implement `export_orders_csv` in `shop/export.py` so the accounting team can download orders as CSV and open the file straight in Excel, and add tests that cover every requirement below.

## Why this matters
Accounting reconciles payments every morning in Excel on Thai-locale Windows.
Today they copy rows by hand from the admin page, and Thai customer names come out garbled when they try a plain CSV.
The file has to open correctly in Excel with no manual fixing, and the numbers and dates have to be unambiguous for reconciliation.

## Context
Python 3.11+, standard library only.
Run tests with `pytest` from the repo root (pyproject.toml sets `pythonpath = ["."]` and `testpaths = ["tests"]`).
`shop/orders.py` defines:
- `Order`, a frozen dataclass: `id: int`, `customer: str`, `status: str`, `amount: Decimal`, `created_at: datetime` (timezone-aware, usually Bangkok time but not always, so never assume the input zone), `note: str | None`.
- `BANGKOK`, a fixed UTC+7 tzinfo. Use it for the date filter instead of defining your own.
- `STATUSES = ("pending", "paid", "shipped", "cancelled")`. Validate against it.
- `SAMPLE_ORDERS`, five orders used by the acceptance criteria.
`shop/export.py` holds the stub with the signature you must keep.
`tests/test_smoke.py` is the only existing test.

## What to deliver
The implementation in `shop/export.py`.
A test file `tests/test_export.py` with tests for each of R1 to R13.
No changes to `shop/orders.py`.

## Requirements
- R1: Columns, in this order: order_id, customer, status, amount, created_at, note.
- R2: Output is UTF-8 with a BOM, so Excel shows Thai text correctly.
- R3: Rows end with CRLF.
- R4: Fields that contain a comma, a double quote, or a line break are wrapped in double quotes, with inner double quotes doubled (RFC 4180).
- R5: amount has exactly two decimals, a dot as decimal separator, and no thousands separator (1234.5 becomes 1234.50).
- R6: created_at is converted to UTC and written as ISO 8601 with a Z suffix and whole seconds, for example 2026-03-01T02:05:09Z.
- R7: A missing note is an empty field.
- R8: `status` may be one status or a list of statuses, matched case-insensitively.
- R9: Cancelled orders are left out unless the status filter explicitly includes cancelled.
- R10: `date_from` and `date_to` are inclusive and compare against the order's date in Bangkok time (UTC+7), because that is the day accounting thinks in.
- R11: Rows are sorted by created_at ascending, then by order_id ascending.
- R12: When nothing matches, the output is the header row only.
- R13: A status that is not one of pending, paid, shipped, cancelled raises ValueError, and the message names the bad value.


## Constraints and out of scope
Standard library only.
Do not change the `Order` dataclass or the function signature.
No HTTP endpoints, streaming, pagination, or UI.

## Acceptance criteria
- AC1: `pytest` passes, and the repo contains tests covering R1 to R13.
- AC2: For `SAMPLE_ORDERS` with no filters, the output starts with the UTF-8 BOM, the first line is the exact header from R1, rows end with CRLF, and order 3 is absent.
- AC3: Order 2's note is written as `"ส่งด่วน ""พิเศษ"""` and order 4's note keeps its line break inside quotes.
- AC4: Order 1's amount is `1234.50` and its created_at is `2026-03-01T02:05:09Z`.
- AC5: `status=["PAID", "cancelled"]` returns orders 1, 5 and 3 and nothing else.
- AC6: `date_from=date(2026, 3, 2), date_to=date(2026, 3, 2)` returns order 4 only (order 3 is cancelled).
- AC7: Orders 1 and 5 share a timestamp and appear as 1 then 5.
- AC8: `status="refunded"` raises ValueError mentioning "refunded".

## When something is unclear
Make the reasonable choice and keep going.
List each assumption in your final report.

## Before you finish
Run `pytest` and make sure it passes.
Check your work against every acceptance criterion; for each one, report PASS or FAIL and how you checked it, running code where possible.
