import sys
import logging
import argparse
from reader import BriLoReader
from report import BriLoReport
from writer import BriLoWriter
from BriLoExceptions import InvalidCsvError, MissingColumnError, MissingRowError
from typing import Dict, List

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
            # 1. Veriyi Oku
            reader = BriLoReader(args.input)
            data = reader.read_data()
            print(data)
            logging.info(f"De bestellingen zijn succesvol opgehaald uit het '{args.input}' CSV-bestand.")
            sys.exit(EXIT_CODE_OK) # Exit Code: 0

            # 2. İş Mantığını Çalıştır
            #reporter = BriLoReport()#data)
            #if args.customer:
                #result = reporter.get_customer_report(args.customer)
            #else:
                #result = reporter.get_summary_report()

            # 3. Sonucu Yazdır veya Kaydet
            #if args.output:
            #    writer = BriLoWriter()#args.output)
            #    writer.export(result)
            #    print(f"Rapor başarıyla kaydedildi: {args.output}")
            #else:
            #    print(result)
        except InvalidCsvError as e:
            logging.error(f"Invoerfout: {e}")
            sys.exit(EXIT_CODE_INVOERPROBLEEM) # Exit Code: 1
        except MissingColumnError as e:
            logging.error(f"Configuratiefout: {e}")
            sys.exit(EXIT_CODE_CONFIGURATIEFOUT)  # Exit Code: 2
        except MissingRowError as e:
            logging.error(f"Configuratiefout: {e}")
            sys.exit(EXIT_CODE_CONFIGURATIEFOUT)  # Exit Code: 2
        except Exception as e:
            logging.error(f"Onverwachte fout: Er zijn geen geldige bestanden gevonden.")
            sys.exit(EXIT_CODE_INVOERPROBLEEM)



if __name__ == "__main__":
    app = BriLoCLI()
    app.run() #voer run functie