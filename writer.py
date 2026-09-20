import datetime
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from report import ReportData


class BriLoWriter:
    """Schrijft een ReportData-object weg naar een bestand in het gewenste formaat.

        Attributes:
            report_data (ReportData): Het geaggregeerde rapport met berekende gegevens.
        """

    def __init__(self, report_data: ReportData) -> None:
        """Initialiseert de ReportWriter met rapportgegevens.

        Args:
            report_data (ReportData): Het rapportobject dat geëxporteerd moet worden.
        """
        self.report_data = report_data

    def _to_json (self) -> str:
        """Converteert de ReportData naar een geformatteerde JSON-string.

        Returns:
            str: Een JSON-representatie van de rapportgegevens.
        """
        data_dict: dict[str, Any] = asdict(self.report_data)
        return json.dumps(data_dict, indent=4, ensure_ascii=False)

    def _to_markdown(self) -> str:
        """Converteert de ReportData naar een geformatteerde Markdown-string.

        Returns:
            str: Een Markdown-representatie van de rapportgegevens.
        """
        md_totale_omzet = f"{self.report_data.totale_omzet:,.2f}"
        md_totale_omzet = md_totale_omzet.replace(",", "X").replace(".", ",").replace("X", ".")

        md_date = datetime.datetime.now(tz=datetime.timezone.utc)
        md_date_str = f"{md_date.strftime('%d.%m.%Y')}"
        lines: list[str] = [
            f"# <span style='color: #0d6efd;'>Brigtstone Logistiek Rapportage - {md_date_str}</span>",
            "",
            "## Algemeen Overzicht",
            f"- **Totaal aantal orders:** {self.report_data.totaal_aantal_orders}",
            f"- **Totale omzet:** € {md_totale_omzet}",
            "",
            "## Top 5 Klanten op Besteed Bedrag",
            "| Klant | Omzet (€) |",
            "| :--- | ---: |",
        ]

        for klant, omzet in self.report_data.top_5_klanten:
            md_omzet = f"{omzet:,.2f}"
            md_omzet = md_omzet.replace(",", "X").replace(".", ",").replace("X", ".")
            lines.append(f"| {klant} | € {md_omzet} |")

        lines.extend([
            "",
            "## Omzet per Categorie",
            "| Categorie | Omzet (€) |",
            "| :--- | ---: |",
        ])

        for categorie, omzet in self.report_data.omzet_per_categorie.items():
            md_omzet = f"{omzet:,.2f}"
            md_omzet = md_omzet.replace(",", "X").replace(".", ",").replace("X", ".")
            lines.append(f"| {categorie} | {md_omzet} |")

        lines.extend([
            "",
            "## Top 5 Producten op Omzet",
            "| Product | Omzet (€) |",
            "| :--- | ---: |",
        ])

        for product, omzet in self.report_data.top_5_producten:
            md_omzet = f"{omzet:,.2f}"
            md_omzet = md_omzet.replace(",", "X").replace(".", ",").replace("X", ".")
            lines.append(f"| {product} | {md_omzet} |")

        return "\n".join(lines)


    def write(self, output_path: Path, output_format: str) -> None:
        """Schrijft het rapport weg naar de opgegeven bestandslocatie.

        Args:
            output_path (Path): Het doelbestandspad waar het rapport wordt opgeslagen.
            output_format (str): Het gewenste formaat ('markdown' of 'json').

        Raises:
            ValueError: Als een niet-ondersteund formaat wordt opgegeven.
        """
        format: str = output_format.lower().strip()

        if format in ("markdown", "md"):
            content: str = self._to_markdown()
        elif format == "json":
            content = self._to_json()
        else:
            raise ValueError (f"Niet-ondersteund formaat: {output_format}. Kies 'markdown' of 'json'.")

        output_path.write_text(content, encoding="utf-8")
