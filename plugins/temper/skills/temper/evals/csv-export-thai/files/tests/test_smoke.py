from shop.export import export_orders_csv
from shop.orders import SAMPLE_ORDERS


def test_returns_bytes():
    assert isinstance(export_orders_csv(SAMPLE_ORDERS), bytes)
