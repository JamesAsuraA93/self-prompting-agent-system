from datetime import date

from shop.orders import Order


def export_orders_csv(
    orders: list[Order],
    status: str | list[str] | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> bytes:
    """Export orders as CSV for the accounting team. See reqs.md."""
    raise NotImplementedError
