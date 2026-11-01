import csv
import io
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytest

from shop.export import export_orders_csv
from shop.orders import BANGKOK, Order

BOM = b"\xef\xbb\xbf"
HEADER = "order_id,customer,status,amount,created_at,note"
UTC = timezone.utc
NY = timezone(timedelta(hours=-5))


def rows(data: bytes):
    text = data[len(BOM):].decode("utf-8")
    return list(csv.reader(io.StringIO(text, newline="")))


def ids(data: bytes):
    return [int(r[0]) for r in rows(data)[1:]]


def o(i, status="paid", amount="1", at=None, customer="c", note=None):
    at = at or datetime(2026, 5, 1, 12, 0, 0, tzinfo=BANGKOK)
    return Order(i, customer, status, Decimal(amount), at, note)


def test_r1_header_exact():
    assert rows(export_orders_csv([o(1)]))[0] == HEADER.split(",")


def test_r2_bom_and_utf8_thai():
    data = export_orders_csv([o(1, customer="สมหญิง")])
    assert data.startswith(BOM) and not data.startswith(BOM + BOM)
    assert rows(data)[1][1] == "สมหญิง"


def test_r3_crlf_every_row():
    data = export_orders_csv([o(1), o(2)])
    body = data[len(BOM):]
    assert body.endswith(b"\r\n")
    assert body.count(b"\r\n") == 3 and b"\n" not in body.replace(b"\r\n", b"")


def test_r4_quoting_comma_quote_newline():
    data = export_orders_csv([o(1, customer='A, "B"', note="x\ny")])
    assert '"A, ""B"""' in data.decode("utf-8")
    r = rows(data)[1]
    assert r[1] == 'A, "B"' and r[5] == "x\ny"


@pytest.mark.parametrize("raw,expected", [("1234.5", "1234.50"), ("1000000", "1000000.00"), ("0", "0.00"), ("7.10", "7.10")])
def test_r5_amount_format(raw, expected):
    assert rows(export_orders_csv([o(1, amount=raw)]))[1][3] == expected


def test_r6_utc_iso_z_from_other_zones():
    a = o(1, at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=NY))
    b = o(2, at=datetime(2026, 1, 1, 7, 0, 0, 123456, tzinfo=BANGKOK))
    got = {int(r[0]): r[4] for r in rows(export_orders_csv([a, b]))[1:]}
    assert got[1] == "2026-01-01T05:00:00Z"
    assert got[2] == "2026-01-01T00:00:00Z"


def test_r7_missing_note_empty():
    assert rows(export_orders_csv([o(1, note=None)]))[1][5] == ""


def test_r8_status_single_case_insensitive():
    data = export_orders_csv([o(1, "paid"), o(2, "pending")], status="Paid")
    assert ids(data) == [1]


def test_r8_status_list():
    data = export_orders_csv([o(1, "paid"), o(2, "pending"), o(3, "shipped")], status=["PENDING", "shipped"])
    assert sorted(ids(data)) == [2, 3]


def test_r9_cancelled_excluded_by_default_and_on_other_filters():
    orders = [o(1, "paid"), o(2, "cancelled")]
    assert ids(export_orders_csv(orders)) == [1]
    assert ids(export_orders_csv(orders, status="paid")) == [1]


def test_r9_cancelled_included_when_requested():
    orders = [o(1, "paid"), o(2, "cancelled")]
    assert ids(export_orders_csv(orders, status="CANCELLED")) == [2]


def test_r10_date_filter_uses_bangkok_day():
    late = o(1, at=datetime(2026, 3, 1, 23, 30, tzinfo=BANGKOK))  # 16:30Z on Mar 1
    early = o(2, at=datetime(2026, 3, 2, 1, 0, tzinfo=BANGKOK))   # 18:00Z on Mar 1
    utc_given = o(3, at=datetime(2026, 3, 1, 20, 0, tzinfo=UTC))   # 03:00 Mar 2 in Bangkok
    orders = [late, early, utc_given]
    assert ids(export_orders_csv(orders, date_from=date(2026, 3, 1), date_to=date(2026, 3, 1))) == [1]
    assert sorted(ids(export_orders_csv(orders, date_from=date(2026, 3, 2)))) == [2, 3]
    assert ids(export_orders_csv(orders, date_to=date(2026, 3, 1))) == [1]


def test_r11_sort_by_instant_then_id():
    t = datetime(2026, 4, 1, 10, 0, tzinfo=BANGKOK)
    same_instant_utc = t.astimezone(UTC)
    orders = [o(9, at=t), o(3, at=t + timedelta(hours=1)), o(4, at=same_instant_utc), o(1, at=t - timedelta(minutes=1))]
    assert ids(export_orders_csv(orders)) == [1, 4, 9, 3]


def test_r12_empty_is_header_only():
    assert export_orders_csv([]) == BOM + (HEADER + "\r\n").encode()
    assert export_orders_csv([o(1, "paid")], status="pending") == BOM + (HEADER + "\r\n").encode()


@pytest.mark.parametrize("bad", ["refunded", ["paid", "lost"]])
def test_r13_invalid_status_raises(bad):
    name = bad if isinstance(bad, str) else "lost"
    with pytest.raises(ValueError, match=name):
        export_orders_csv([o(1)], status=bad)
