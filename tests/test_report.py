import pytest

from report import BriLoReport


@pytest.fixture
def sample_data() -> list[dict[str, str]]:
    """voorbeeld data vor testen"""
    return [
        {"order_id": "1", "datum":"4-1-2026", "klant": "A", "product": "product 1", "categorie": "category 1", "aantal": "2",  "prijs": "100.0"},
        {"order_id": "2", "datum":"5-1-2026", "klant": "A", "product": "product 2", "categorie": "category 2", "aantal": "2",  "prijs": "100.0"},
        {"order_id": "3", "datum":"6-1-2026", "klant": "B", "product": "product 3", "categorie": "category 3", "aantal": "3",  "prijs": "200.0"},
        {"order_id": "4", "datum":"7-1-2026", "klant": "B", "product": "product 4", "categorie": "category 4", "aantal": "4",  "prijs": "300.0"},
        {"order_id": "5", "datum":"8-1-2026", "klant": "C", "product": "product 1", "categorie": "category 1", "aantal": "5",  "prijs": "400.0"},
        {"order_id": "6", "datum":"9-1-2026", "klant": "A", "product": "product 5", "categorie": "category 5", "aantal": "1",  "prijs": "500.0"},
    ]


def test_top_5_producten(sample_data: list[dict[str, str]]) -> None:
    """Top-5-berekening test."""
    reporter = BriLoReport(sample_data)
    top_5 = reporter.top_5_producten_op_omzet
    assert len(top_5) == 5
    assert float(top_5[0][1]) == 2200.0


def test_omzet_per_category(sample_data: list[dict[str, str]]) -> None:
    """Omzet-per-categorie test."""
    reporter = BriLoReport(sample_data)
    omzet = reporter.omzet_per_categorie
    assert omzet["category 2"] == 200.0
    assert omzet["category 5"] == 500.0


def test_total_omzet(sample_data: list[dict[str, str]]) -> None:
    """test voor de berekening van de totale omzet."""
    reporter = BriLoReport(sample_data)
    assert reporter.totale_omzet == 4700.0


def test_empty_report_data() -> None:
    """test voor de berekening van de totale omzet met lege data """
    reporter = BriLoReport([])
    assert reporter.totale_omzet == 0.0