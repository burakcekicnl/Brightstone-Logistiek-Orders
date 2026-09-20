import logging
from collections import defaultdict
from dataclasses import dataclass

loggerReport = logging.getLogger(__name__)

@dataclass(frozen=True)
class ReportData:
    """Een speciaal type (Data Class) dat de berekende rapportgegevens bevat."""

    totaal_aantal_orders: int
    totale_omzet: float
    top_5_klanten: list[tuple[str, float]]
    omzet_per_categorie: dict[str, float]
    top_5_producten: list[tuple[str, float]]


class BriLoReport:
    """ Het is de klasse die de gegevens verwerkt.

        Attiributes:
            VERPLICHTE_COLUMNS (set[str]): Vereiste kolommen die in een CSV-bestand moeten worden opgenomen.
            file_path (str): Het pad naar het te verwerken CSV-bestand.
    """
    def __init__(self, orders: list[dict[str, str]]) -> None:
        """ Start de BriLoReader-klasse.
        Args:
            orders: Het pad naar het te lezen CSV-bestand.
        """
        self.orders_data: list[dict[str,str]] = orders

    @property
    def totaal_aantal_orders(self) -> int:
        loggerReport.info("Het totale aantal orders is berekend.")

        return len(self.orders_data)

    @property
    def totale_omzet(self) -> float:

        orderkosten: float = 0.0
        totale_omzet: float = 0.0

        for order in self.orders_data: #bereken totale omzet
            orderkosten = int(order["aantal"]) * float(order["prijs"])
            totale_omzet += orderkosten
        loggerReport.info("Het totale omzet uit orders werd berekend.")
        return totale_omzet


    @property
    def top_5_producten_op_omzet(self) -> list[tuple[str, float]]:
        # 1 klant dictionary met omzet
        product_omzet: dict[str, float] = defaultdict(float)

        # 2 for lus om gegevenst te groepen
        for order in self.orders_data:
            product = order["product"]

            aantal = int(order["aantal"])
            prijs = float(order["prijs"])

            product_omzet[product] += aantal * prijs

        sorted_producten: list[tuple[str, float]] = sorted(
            product_omzet.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]

        loggerReport.info("Top 5 producten op omzet werd berekend.")
        return [(product, round(omzet, 2)) for product, omzet in sorted_producten]

    @property
    def top_5_klanten_op_besteed_bedrag(self) -> list[tuple[str, float]]:
        # 1 klant dictionary met omzet
        klant_omzet: dict[str, float] = defaultdict(float)

        # 2 for lus om gegevenst te groepen
        for order in self.orders_data:
            klant = order["klant"]

            aantal = int(order["aantal"])
            prijs = float(order["prijs"])

            klant_omzet[klant] += aantal * prijs

        sorted_klanten: list[tuple[str, float]] = sorted(
            klant_omzet.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]

        loggerReport.info("Top 5 klanten op besteed bedrag werd berekend.")
        return [(klant, round(omzet, 2)) for klant, omzet in sorted_klanten]

    @property
    def omzet_per_categorie(self) -> dict[str, float]:
        # 1 klant dictionary met omzet
        categorie_omzet: dict[str, float] = defaultdict(float)

        # 2 for lus om gegevenst te groepen
        for order in self.orders_data:
            categorie = order["categorie"]

            aantal = int(order["aantal"])
            prijs = float(order["prijs"])

            categorie_omzet[categorie] += aantal * prijs

        loggerReport.info("De Omzet werd per categorie  berekend.")
        return {categorie: round(omzet, 2) for categorie, omzet in categorie_omzet.items()}


    def generate(self) -> ReportData:
        """Het voert alle berekeningen uit en retourneert één enkel ReportData-object."""
        return ReportData(
        totaal_aantal_orders = self.totaal_aantal_orders,
        totale_omzet=self.totale_omzet,
        top_5_klanten=self.top_5_klanten_op_besteed_bedrag,
        omzet_per_categorie=self.omzet_per_categorie,
        top_5_producten=self.top_5_producten_op_omzet,
        )



if __name__ == "__main__":
    data: list[dict[str, str]] = []
    test_reader = BriLoReport(data)
    print("Testing...")

