import csv
import os
from typing import ClassVar

from BriLoExceptions import InvalidCsvError, MissingColumnError, MissingRowError


class BriLoReader:
    """ Een klasse die wordt gebruikt om CSV-gegevens te lezen en te valideren.

        Attiributes:
            VERPLICHTE_COLUMNS (set[str]): Vereiste kolommen die in een CSV-bestand moeten worden opgenomen.
            file_path (str): Het pad naar het te verwerken CSV-bestand.
    """
    VERPLICHTE_COLUMNS: ClassVar[set[str]] = {'order_id',
                          'datum',
                          'klant',
                          'product',
                          'categorie',
                          'aantal',
                          'prijs'}


    def __init__(self, file_path: str) -> None:
        """ Start de BriLoReader-klasse.
        Args:
            file_path: Het pad naar het te lezen CSV-bestand.
        """
        self.file_path: str = file_path

    def validate_data(self) -> bool:
        """ Controleert of het bestand bestaat, de extensie heeft en de kolomstructuur aanpast.

        Returns:
            bool: De functie retourneert True als het bestand geldig is.

        Raises:
            InvalidCsvError: Als het bestand niet bestaat of de extensie niet .csv is.
            MissingColumnError: Als een van de verplichte kolommen ontbreekt.
        """
        # 1. Controleer of het bestand bestaat.
        if not os.path.exists(self.file_path):
            raise InvalidCsvError(f"Het orderbestand '{self.file_path}' niet worden gevonden.")

        # 2. Controleer of de bestandsextensie CSV is.
        if not self.file_path.endswith(".csv"):
            raise InvalidCsvError(f"Het geselecteerde bestand '{self.file_path}' is geen .csv-bestand.")

        # 3. Controleer de column namen
        with open (self.file_path, mode="r") as file:
            # lees de column titles
            reader = csv.DictReader(file, delimiter=";")
            headers: set[str] = set(reader.fieldnames or []) #verander fieldnames een Set

            # Controleer of er kolommen ontbreken.
            if not self.VERPLICHTE_COLUMNS.issubset(headers): # controleer alle kolumns is er in headers
                ontbrekend = self.VERPLICHTE_COLUMNS - headers # vastleggen welke columns is ontbrekend
                raise MissingColumnError(f"Ongeldige CSV-structuur! Ontbrekende kolommen: {ontbrekend}.")

        return True

    def read_data(self) -> list[dict[str, str]]:
        """ Het leest de gegevens uit het CSV-bestand en geeft deze terug als een woordenboeklijst.

        Returns:
            List[Dict[str, str]]: Een gegevenslijst waarbij elke rij een woordenboek is.
        """

        orders: list[dict[str, str]] = []
        # import csv kan csv files lezen.

        # controleer het orderbestand
        self.validate_data()

        # Read de csv bestaand
        with open(self.file_path, mode="r") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                if not isinstance(row["aantal"], int) or not isinstance(row["prijs"], float):
                    orders.append(row)
                else:
                    raise TypeError(f"'{row["prijs"]}' of '{row["aantal"]}' - Order prijs invalide!")


        if not orders :
            raise MissingRowError (f"Het geselecteerde bestand '{self.file_path}' heeft geen order.")

        return orders




if __name__ == "__main__":
    test_reader = BriLoReader("orders.csv")
    print("Testing...")