import argparse
import logging
import sys
from pathlib import Path

from BriLoExceptions import InvalidCsvError, MissingColumnError, MissingRowError
from reader import BriLoReader
from report import BriLoReport
from writer import BriLoWriter

# Modulespecifiek logobject (genaamd 'cli' of de modulenaam)
logger = logging.getLogger(__name__)

#EXIT CODES
EXIT_CODE_OK = 0
EXIT_CODE_INVOERPROBLEEM = 1
EXIT_CODE_CONFIGURATIEFOUT = 2

class BriLoCLI:
    """ Het is de hoofdklasse die het programma uitvoert.
    """

    #class maker
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            description="Brightstone Logistiek Orders Overzicht"
        )
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        """Defineert CLI arguments """
        self.parser.add_argument(
            "-m", "--method",
            default = "rapport",
            help="modus om te selecteren: rapport, scherm "
        )
        self.parser.add_argument(
            "-i", "--input",
            default="orders.csv",
            help="CSV-bestand dat verwerkt moet worden. -> 'orders.csv'"
        )
        self.parser.add_argument(
            "-o", "--output",
            default="rapport",
            help="Het uitvoerbestand waarin het rapport wordt opgeslagen."
        )
        self.parser.add_argument(
            "-f", "--format",
            help="Het bestandsformaat waarin het rapport wordt opgeslagen."
        )

    #logging configuratie
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    def run(self) -> None:
        """Het initieert en controleert de applicatiestroom."""
        args = self.parser.parse_args()
        try:
            # 1. lees de gegevens
            reader = BriLoReader(args.input)
            data = reader.read_data()
            logger.info(f"De bestellingen zijn succesvol opgehaald uit het '{args.input}' CSV-bestand.")

            # 2. bereikenen
            report = BriLoReport(data)
            report_data = report.generate()
            logger.info("Alle berekeningen zijn uitgevoerd en het ReportData-object is aangemaakt.")

            # 3. afdrukken
            writer = BriLoWriter(report_data)
            writer.write(output_path=Path(args.output), output_format=args.format)
            logger.info("Rapport is aangemaakt.")

            sys.exit(EXIT_CODE_OK)  # Exit Code: 0

        except InvalidCsvError as e:
            logger.error(f"Invoerfout: {e}")
            sys.exit(EXIT_CODE_INVOERPROBLEEM) # Exit Code: 1
        except MissingColumnError as e:
            logger.error(f"Configuratiefout: {e}")
            sys.exit(EXIT_CODE_CONFIGURATIEFOUT)  # Exit Code: 2
        except MissingRowError as e:
            logger.error(f"Configuratiefout: {e}")
            sys.exit(EXIT_CODE_CONFIGURATIEFOUT)  # Exit Code: 2
        except Exception as e:
            logger.error(f"{e} - Onverwachte fout: Er zijn geen geldige bestanden gevonden.")
            sys.exit(EXIT_CODE_INVOERPROBLEEM)



if __name__ == "__main__":
    app = BriLoCLI()
    app.run() #voer run functie