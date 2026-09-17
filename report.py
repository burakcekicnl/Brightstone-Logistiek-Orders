from typing import List, Dict


class BriLoReport:
    """ Het is de klasse die de gegevens verwerkt.

        Attiributes:
            VERPLICHTE_COLUMNS (set[str]): Vereiste kolommen die in een CSV-bestand moeten worden opgenomen.
            file_path (str): Het pad naar het te verwerken CSV-bestand.
    """
    def __init__(self, orders: List[Dict[str, str]]) -> None:
        """ Start de BriLoReader-klasse.
        Args:
            orders: Het pad naar het te lezen CSV-bestand.
        """
        self.orders_data: List[Dict[str,str]] = orders

   def 


if __name__ == "__main__":
    data=[]
    test_reader = BriLoReport(data)
    print("Testing...")

