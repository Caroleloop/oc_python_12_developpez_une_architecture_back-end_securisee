from typer.testing import CliRunner
from app.cli import db_cli

runner = CliRunner()


def test_read_collaborateurs(monkeypatch):
    """
    Vérifie que la commande 'read-collaborateurs' fonctionne correctement.
    - Monkeypatch `verifier_permission` pour simuler une permission autorisée.
    - Monkeypatch `read_table` pour éviter l'accès réel à la base.
    - Vérifie que la sortie contient le message attendu.
    """
    # Simulation d'une permission accordée
    monkeypatch.setattr(db_cli, "verifier_permission", lambda *a, **kw: True)
    # Simulation de la lecture de la table sans effectuer de vraie requête
    monkeypatch.setattr(db_cli, "read_table", lambda *a, **kw: None)

    # Appel de la commande CLI
    result = runner.invoke(db_cli.app, ["read-collaborateurs"])

    # Vérifie que le message attendu est affiché
    assert "Lecture des collaborateurs" in result.output
