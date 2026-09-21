import json

import pytest

from writer import BriLoWriter
from dataclasses import dataclass

@dataclass
class ReportData :
    """Een speciaal type (Data Class) dat de berekende rapportgegevens bevat."""

    totaal_aantal_orders: int
    totale_omzet: float
    top_5_klanten: list[tuple[str, float]]
    omzet_per_categorie: dict[str, float]
    top_5_producten: list[tuple[str, float]]

def test_json_output_format(tmp_path: pytest.TempPathFactory) -> None:
    """JSON uitvoerformaat test."""
    aantal_orders = 20
    var_totale_omzet = 2500.00
    var_top_5_klanten = [("Klant 1", 790.00),
                         ("Klant 2", 600.00),
                         ("Klant 3", 550.00),
                         ("Klant 4", 500.00),
                         ("Klant 5", 450.00),
                         ]
    var_categorie_omzet = {
                        "categorie 1": 450.00,
                        "categorie 2": 400.00,
                        "categorie 3": 350.00,
                        "categorie 4": 300.00,
                        "categorie 5": 250.00,

    }
    var_top_5_producten = [
        ('product 1', 7800.0),
        ('product 2', 2452.5),
        ('product 3', 2380.0),
        ('product 4', 1820.0),
        ('product 5', 1820.0),
    ]

    report_data = ReportData(
        totaal_aantal_orders = aantal_orders,
        totale_omzet= var_totale_omzet,
        top_5_klanten= var_top_5_klanten,
        omzet_per_categorie= var_categorie_omzet,
        top_5_producten= var_top_5_producten,
    )
    output_file = tmp_path / "output.json"
    #data = {"total_revenue": 1000.0}
    writer = BriLoWriter(report_data)
    writer.write(output_path="output\\rapport.json", output_format="json")

    assert output_file.exists()
    content = json.loads(output_file.read_text())
    assert content["total_revenue"] == 1000.0


def test_markdown_output_format(tmp_path: pytest.TempPathFactory) -> None:
    """Markdown uitvoerformaat test."""
    aantal_orders = 20
    var_totale_omzet = 2500.00
    var_top_5_klanten = [("Klant 1", 790.00),
                         ("Klant 2", 600.00),
                         ("Klant 3", 550.00),
                         ("Klant 4", 500.00),
                         ("Klant 5", 450.00),
                         ]
    var_categorie_omzet = {
        "categorie 1": 450.00,
        "categorie 2": 400.00,
        "categorie 3": 350.00,
        "categorie 4": 300.00,
        "categorie 5": 250.00,

    }
    var_top_5_producten = [
        ('product 1', 7800.0),
        ('product 2', 2452.5),
        ('product 3', 2380.0),
        ('product 4', 1820.0),
        ('product 5', 1820.0),
    ]

    report_data = ReportData(
        totaal_aantal_orders=aantal_orders,
        totale_omzet=var_totale_omzet,
        top_5_klanten=var_top_5_klanten,
        omzet_per_categorie=var_categorie_omzet,
        top_5_producten=var_top_5_producten,
    )
    output_file = tmp_path / "output.csv"
    #data = "category,amount\nElectronics,300.0"
    writer = BriLoWriter(report_data)
    writer.write(output_path="output\\rapport.md", output_format="md")

    assert output_file.exists()
    assert "Electronics" in output_file.read_text()