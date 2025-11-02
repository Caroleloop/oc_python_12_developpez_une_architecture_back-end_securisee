from typer.testing import CliRunner
from app.cli.__main__ import app

runner = CliRunner()


def test_main_cli_help():
    """
    Vérifie que la commande principale CLI affiche correctement l'aide.
    - Appelle `app --help`.
    - Vérifie que le code de sortie est 0.
    - Vérifie que la description globale de la CLI est présente dans la sortie.
    """
    result = runner.invoke(app, ["--help"])

    # Vérifie que la commande s'est exécutée avec succès
    assert result.exit_code == 0
    # Vérifie que le message d'aide contient la description attendue
    assert "CLI global du CRM" in result.output
