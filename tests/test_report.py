import pytest
from report import BriLoReport


@pytest.fixture
def sample_data() -> list[dict[str, str]]:
    """Testler için örnek veri fikstürü."""
    return [
        {"order_id": "1", "category": "Electronics", "amount": "100.0", "customer": "A"},
        {"order_id": "2", "category": "Electronics", "amount": "200.0", "customer": "B"},
        {"order_id": "3", "category": "Books", "amount": "50.0", "customer": "A"},
        {"order_id": "4", "category": "Books", "amount": "150.0", "customer": "C"},
        {"order_id": "5", "category": "Clothing", "amount": "300.0", "customer": "D"},
        {"order_id": "6", "category": "Clothing", "amount": "400.0", "customer": "E"},
    ]


def test_top_5_calculation(sample_data: list[dict[str, str]]) -> None:
    """Top-5-berekening testi."""
    reporter = BriLoReport(sample_data)
    top_5 = reporter.get_top_5_orders()
    assert len(top_5) == 5
    assert float(top_5[0]["amount"]) == 400.0


def test_revenue_per_category(sample_data: list[dict[str, str]]) -> None:
    """Omzet-per-categorie testi."""
    reporter = BriLoReport(sample_data)
    revenue = reporter.get_revenue_per_category()
    assert revenue["Electronics"] == 300.0
    assert revenue["Books"] == 200.0


def test_total_revenue(sample_data: list[dict[str, str]]) -> None:
    """Toplam ciro hesabı testi."""
    reporter = BriLoReport(sample_data)
    assert reporter.get_total_revenue() == 1200.0


def test_empty_report_data() -> None:
    """Boş veri seti ile rapor üretme testi."""
    reporter = BriLoReport([])
    assert reporter.get_total_revenue() == 0.0