from typer.testing import CliRunner
from app.cli import auth_cli

runner = CliRunner()


# ------------------- TEST LOGIN -------------------
def test_login_success(monkeypatch, tmp_path):
    """
    Vérifie que la commande 'login' fonctionne correctement avec des identifiants valides.
    - Crée un fichier token temporaire.
    - Monkeypatch la fonction login pour renvoyer un token fictif.
    - Vérifie la sortie et la création du fichier token.
    """
    token_path = tmp_path / ".token"
    # Redirige le chemin du token vers le tmp_path
    monkeypatch.setattr(auth_cli, "TOKEN_FILE", token_path)
    # Remplace la fonction login par un fake qui renvoie un token
    monkeypatch.setattr(auth_cli, "login", lambda e, m: "fake_jwt_token")

    # Appel de la commande CLI
    result = runner.invoke(
        auth_cli.app, ["login", "--email", "user@test.com", "--mot-de-passe", "123"]
    )

    # Vérifie que la commande s'est terminée avec succès
    assert result.exit_code == 0
    # Vérifie que le token a été écrit
    assert token_path.exists()
    # Vérifie le message de succès
    assert "Connexion réussie" in result.output


def test_login_failure(monkeypatch, tmp_path):
    """
    Vérifie que la commande 'login' affiche une erreur avec des identifiants invalides.
    - Monkeypatch la fonction login pour lever une exception.
    - Vérifie que le message d'erreur apparaît dans la sortie CLI.
    """
    # Remplace login par une fonction qui lève ValueError
    monkeypatch.setattr(
        auth_cli,
        "login",
        lambda e, m: (_ for _ in ()).throw(ValueError("Identifiants invalides")),
    )

    # Appel de la commande CLI avec identifiants invalides
    result = runner.invoke(
        auth_cli.app, ["login", "--email", "x", "--mot-de-passe", "y"]
    )

    # Vérifie le message d'erreur
    assert "Erreur de connexion" in result.output


# ------------------- TEST LOGOUT -------------------
def test_logout(monkeypatch, tmp_path):
    """
    Vérifie que la commande 'logout' supprime correctement le fichier token.
    - Crée un fichier token temporaire.
    - Monkeypatch TOKEN_FILE pour pointer sur ce fichier.
    - Vérifie la sortie et que le fichier a été supprimé.
    """
    token_path = tmp_path / ".token"
    token_path.write_text("abc")  # Crée un token fictif
    monkeypatch.setattr(auth_cli, "TOKEN_FILE", token_path)

    # Appel de la commande CLI
    result = runner.invoke(auth_cli.app, ["logout"])

    # Vérifie le message de succès
    assert "Déconnexion réussie" in result.output
    # Vérifie que le fichier token a été supprimé
    assert not token_path.exists()
