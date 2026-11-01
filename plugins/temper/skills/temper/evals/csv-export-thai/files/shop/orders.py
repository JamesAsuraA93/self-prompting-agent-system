from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal

BANGKOK = timezone(timedelta(hours=7), "Asia/Bangkok")

STATUSES = ("pending", "paid", "shipped", "cancelled")


@dataclass(frozen=True)
class Order:
    id: int
    customer: str
    status: str
    amount: Decimal
    created_at: datetime  # timezone-aware, usually Bangkok time
    note: str | None = None


SAMPLE_ORDERS = [
    Order(1, "สมชาย ใจดี", "paid", Decimal("1234.5"), datetime(2026, 3, 1, 9, 5, 9, tzinfo=BANGKOK)),
    Order(2, "Acme, Inc.", "shipped", Decimal("99"), datetime(2026, 3, 1, 6, 30, 0, tzinfo=BANGKOK), 'ส่งด่วน "พิเศษ"'),
    Order(3, "มานี มีนา", "cancelled", Decimal("500.00"), datetime(2026, 3, 2, 23, 59, 59, tzinfo=BANGKOK), "ลูกค้ายกเลิก"),
    Order(4, "Bob", "pending", Decimal("10000"), datetime(2026, 3, 2, 0, 15, 0, tzinfo=BANGKOK), "line one\nline two"),
    Order(5, "Ann", "paid", Decimal("0.5"), datetime(2026, 3, 1, 9, 5, 9, tzinfo=BANGKOK)),
]
