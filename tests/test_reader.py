import pytest
from reader import BriLoReader
from BriLoExceptions import InvalidCsvError, MissingColumnError, MissingRowError

# Volledige verplichte header op basis van je BriLoReader
HEADER = "order_id;datum;klant;product;aantal;prijs;categorie\n"


def test_valid_csv(tmp_path: pytest.TempPathFactory) -> None:
    """Test met een volledig en geldig CSV-bestand."""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(HEADER + "1;2026-01-01;Klant A;Laptop;1;999.99;Electronics\n")
    reader = BriLoReader(str(csv_file))
    reader.validate_data()
    data = reader.read_data()
    assert len(data) >= 1


def test_empty_csv(tmp_path: pytest.TempPathFactory) -> None:
    """Test voor een leeg bestand wat leidt tot MissingColumnError."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    reader = BriLoReader(str(csv_file))
    with pytest.raises((InvalidCsvError, MissingColumnError)):
        reader.read_data()


def test_missing_column_csv(tmp_path: pytest.TempPathFactory) -> None:
    """Test voor een CSV waarin verplichte kolommen ontbreken."""
    csv_file = tmp_path / "missing_col.csv"
    csv_file.write_text("order_id;datum\n1;2026-01-01\n")
    reader = BriLoReader(str(csv_file))
    with pytest.raises(MissingColumnError):
        reader.read_data()


def test_invalid_extension(tmp_path: pytest.TempPathFactory) -> None:
    """Test voor een bestand met de verkeerde extensie."""
    txt_file = tmp_path / "data.txt"
    txt_file.write_text("some content")
    reader = BriLoReader(str(txt_file))
    with pytest.raises(InvalidCsvError):
        reader.read_data()