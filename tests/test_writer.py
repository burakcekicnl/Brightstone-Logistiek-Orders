import pytest
import json
from writer import BriLoWriter


def test_json_output_format(tmp_path: pytest.TempPathFactory) -> None:
    """JSON uitvoerformaat testi."""
    output_file = tmp_path / "output.json"
    data = {"total_revenue": 1000.0}
    writer = BriLoWriter(str(output_file))
    writer.write_json(data)

    assert output_file.exists()
    content = json.loads(output_file.read_text())
    assert content["total_revenue"] == 1000.0


def test_txt_or_csv_output_format(tmp_path: pytest.TempPathFactory) -> None:
    """CSV veya Metin uitvoerformaat testi."""
    output_file = tmp_path / "output.csv"
    data = "category,amount\nElectronics,300.0"
    writer = BriLoWriter(str(output_file))
    writer.write_text(data)

    assert output_file.exists()
    assert "Electronics" in output_file.read_text()