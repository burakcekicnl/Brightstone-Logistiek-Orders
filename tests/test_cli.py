import pytest
from unittest.mock import patch
from cli import BriLoCLI, EXIT_CODE_OK, EXIT_CODE_INVOERPROBLEEM, EXIT_CODE_CONFIGURATIEFOUT
from BriLoExceptions import InvalidCsvError

HEADER = "order_id;datum;klant;product;aantal;prijs;categorie\n"


def test_cli_help_option() -> None:
    """Controleert of de help-optie van de commandoregel werkt."""
    cli = BriLoCLI()
    assert cli.parser is not None


def test_cli_successful_run(tmp_path: pytest.TempPathFactory) -> None:
    """Testen of de CLI succesvol afsluit (exitcode 0) met de opgegeven parameters."""
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text(HEADER + "1;2026-01-01;Klant A;Laptop;1;999.99;Electronics\n")

    # We simuleren opdrachtregelargumenten (-i valid.csv)
    test_args = ["cli.py", "-i", str(csv_file)]

    with patch("sys.argv", test_args):
        cli = BriLoCLI()
        # SystemExit 0 wordt verwacht.
        with pytest.raises(SystemExit) as exc_info:
            cli.run()
        assert exc_info.value.code == EXIT_CODE_OK


def test_cli_invoerprobleem_exit_code(tmp_path: pytest.TempPathFactory) -> None:
    """Testen of de CLI exitcode 1 retourneert wanneer een onjuist bestand wordt ingevoerd."""
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text("invalid content")

    test_args = ["cli.py", "-i", str(csv_file)]

    with patch("sys.argv", test_args):
        cli = BriLoCLI()
        with pytest.raises(SystemExit) as exc_info:
            cli.run()
        assert exc_info.value.code == EXIT_CODE_CONFIGURATIEFOUT