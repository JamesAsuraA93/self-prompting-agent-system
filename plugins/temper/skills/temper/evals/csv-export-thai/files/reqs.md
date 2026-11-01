# Order CSV export

## Goal
Implement `export_orders_csv` in `shop/export.py` so the accounting team can download orders and open them straight in Excel.

## Why
Accounting reconciles payments every morning in Excel on Thai-locale Windows.
Today they copy rows by hand from the admin page, which is slow and error prone, and Thai customer names come out garbled when they try a plain CSV.

## Users and context
Accounting staff in Bangkok, working in Thai local time.
Python 3.11+, standard library only, tests run with `pytest` from the repo root.
Order data lives in `shop/orders.py`.

## Must have
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

## Constraints
Standard library only.
Do not change the `Order` dataclass or the function signature.

## Out of scope
HTTP endpoints, streaming, pagination, and any UI.

## Acceptance criteria
- AC1: `pytest` passes, and the repo contains tests covering R1 to R13.
- AC2: For `SAMPLE_ORDERS` with no filters, the output starts with the UTF-8 BOM, the first line is the exact header from R1, rows end with CRLF, and order 3 is absent.
- AC3: Order 2's note is written as `"ส่งด่วน ""พิเศษ"""` and order 4's note keeps its line break inside quotes.
- AC4: Order 1's amount is `1234.50` and its created_at is `2026-03-01T02:05:09Z`.
- AC5: `status=["PAID", "cancelled"]` returns orders 1, 5 and 3 and nothing else.
- AC6: `date_from=date(2026, 3, 2), date_to=date(2026, 3, 2)` returns order 4 only (order 3 is cancelled).
- AC7: Orders 1 and 5 share a timestamp and appear as 1 then 5.
- AC8: `status="refunded"` raises ValueError mentioning "refunded".
