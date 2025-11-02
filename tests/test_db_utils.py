import pytest
from unittest.mock import patch, mock_open
from datetime import datetime
import typer

from app.utils import db_utils


# ------------------- TEST validate_* -------------------
# Tests pour les fonctions de validation : email, nombres positifs, dates, participants, montants


def test_validate_email_ok():
    """Vérifie qu'un email valide est retourné tel quel."""
    assert db_utils.validate_email("test@example.com") == "test@example.com"


def test_validate_email_invalid():
    """Vérifie qu'un email invalide lève une exception BadParameter."""
    with pytest.raises(typer.BadParameter):
        db_utils.validate_email("invalid-email")


def test_validate_positive_float():
    """Vérifie qu'une valeur positive est acceptée par validate_positive_float."""
    assert db_utils.validate_positive_float(10.5) == 10.5


def test_validate_positive_float_invalid():
    """Vérifie qu'une valeur négative lève une exception BadParameter."""
    with pytest.raises(typer.BadParameter):
        db_utils.validate_positive_float(-1)


def test_validate_montant_restant_valid():
    """Vérifie que le montant restant est valide quand 0 <= restant <= total."""
    assert db_utils.validate_montant_restant(100, 50) == 50


@pytest.mark.parametrize("total, restant", [(100, -1), (100, 150)])
def test_validate_montant_restant_invalid(total, restant):
    """Vérifie que des montants restants invalides lèvent une exception BadParameter."""
    with pytest.raises(typer.BadParameter):
        db_utils.validate_montant_restant(total, restant)


def test_validate_single_date_ok():
    """Vérifie qu'une date au format attendu est correctement convertie en datetime."""
    d = db_utils.validate_single_date("2024-01-01 10:00:00")
    assert isinstance(d, datetime)


def test_validate_single_date_invalid():
    """Vérifie qu'une date au mauvais format lève une exception BadParameter."""
    with pytest.raises(typer.BadParameter):
        db_utils.validate_single_date("01-01-2024")


def test_validate_participants_ok():
    """Vérifie que le nombre de participants est correct si valide."""
    assert db_utils.validate_participants(10, 5) == (10, 5)


@pytest.mark.parametrize("p, a", [(-1, 0), (10, -1), (5, 6)])
def test_validate_participants_invalid(p, a):
    """Vérifie que des nombres de participants invalides lèvent une exception BadParameter."""
    with pytest.raises(typer.BadParameter):
        db_utils.validate_participants(p, a)


# ------------------- TEST verifier_connexion -------------------
# Tests pour la fonction de vérification de connexion et lecture de token


@patch("builtins.open", new_callable=mock_open, read_data="fake_token")
@patch("os.path.exists", return_value=True)
@patch(
    "app.utils.db_utils.verifier_token",
    return_value={"email": "test@example.com", "role": "gestion"},
)
@patch("app.utils.db_utils.console.print")
def test_verifier_connexion(mock_console, mock_verif, mock_exists, mock_open_file):
    """Vérifie qu'un utilisateur avec token valide est correctement identifié."""
    payload = db_utils.verifier_connexion()
    assert payload["role"] == "gestion"
    mock_console.assert_called()


@patch("os.path.exists", return_value=False)
@patch("app.utils.db_utils.console.print")
def test_verifier_connexion_no_token(mock_console, mock_exists):
    """Vérifie qu'une absence de token provoque une sortie du programme (typer.Exit)."""
    with pytest.raises(typer.Exit):
        db_utils.verifier_connexion()
    mock_console.assert_called()


# ------------------- TEST verifier_permission -------------------
# Tests pour la vérification des permissions selon le rôle de l'utilisateur


@patch("app.utils.db_utils.verifier_connexion", return_value={"role": "gestion"})
@patch("app.utils.db_utils.console.print")
def test_verifier_permission_allowed(mock_console, mock_connexion):
    """Vérifie qu'un utilisateur avec le rôle 'gestion' peut lire un client."""
    assert db_utils.verifier_permission("lire", "client")


@patch("app.utils.db_utils.verifier_connexion", return_value={"role": "support"})
@patch("app.utils.db_utils.console.print")
def test_verifier_permission_denied(mock_console, mock_connexion):
    """Vérifie qu'un utilisateur sans permission ne peut pas créer un client."""
    assert not db_utils.verifier_permission("creer", "client")
    mock_console.assert_called()


# ------------------- TEST log_sentry -------------------
# Tests pour le décorateur log_sentry, capture de messages et exceptions Sentry


@patch("app.utils.db_utils.sentry_sdk.capture_message")
@patch("app.utils.db_utils.sentry_sdk.capture_exception")
def test_log_sentry_success(mock_exception, mock_message):
    """Vérifie que le message Sentry est capturé lors de l'exécution réussie."""

    @db_utils.log_sentry("Résultat : {result}")
    def f():
        return "OK"

    assert f() == "OK"
    mock_message.assert_called()


@patch("app.utils.db_utils.sentry_sdk.capture_message")
@patch("app.utils.db_utils.sentry_sdk.capture_exception")
def test_log_sentry_exception(mock_exception, mock_message):
    """Vérifie que l'exception Sentry est capturée en cas d'erreur."""

    @db_utils.log_sentry("Résultat : {result}")
    def f():
        raise ValueError("error")

    with pytest.raises(ValueError):
        f()
    mock_exception.assert_called()


# ------------------- TEST verifier_modifications -------------------
# Test pour vérifier si des modifications sont présentes


@patch("app.utils.db_utils.console.print")
def test_verifier_modifications(mock_console):
    """Vérifie que la fonction détecte correctement les modifications entre deux valeurs."""
    assert db_utils.verifier_modifications(a=1, b=None)
    assert not db_utils.verifier_modifications(a=None, b=None)
    mock_console.assert_called()


# ------------------- TEST can_create_evenement -------------------
# Tests pour la création d'événements selon le rôle et le contrat


class DummyContrat:
    """Classe dummy pour simuler un contrat."""

    def __init__(self, statut_contrat=True, contact_commercial_id=1):
        self.statut_contrat = statut_contrat
        self.contact_commercial_id = contact_commercial_id


@patch("app.utils.db_utils.Console.print")
def test_can_create_evenement(mock_print):
    """Vérifie qu'un commercial peut créer un événement sur son contrat."""
    payload = {"role": "commercial", "id": 1}
    contrat = DummyContrat()
    assert db_utils.can_create_evenement(payload, contrat)


@patch("app.utils.db_utils.Console.print")
def test_can_create_evenement_denied(mock_print):
    """Vérifie qu'un rôle non autorisé ne peut pas créer d'événement."""
    payload = {"role": "support", "id": 1}
    contrat = DummyContrat()
    assert not db_utils.can_create_evenement(payload, contrat)
    mock_print.assert_called()


# ------------------- TEST can_update_contrat -------------------
# Tests pour la mise à jour des contrats selon le rôle


@patch("app.utils.db_utils.Console.print")
def test_can_update_contrat_gestion(mock_print):
    """Vérifie que le rôle 'gestion' peut mettre à jour n'importe quel contrat."""
    assert db_utils.can_update_contrat({"role": "gestion"}, None)


@patch("app.utils.db_utils.Console.print")
def test_can_update_contrat_bad_role(mock_print):
    """Vérifie qu'un rôle non autorisé ne peut pas mettre à jour un contrat."""
    payload = {"role": "support", "id": 1}
    assert not db_utils.can_update_contrat(payload, None)
    mock_print.assert_called()


# ------------------- TEST can_update_client -------------------
# Tests pour la mise à jour des clients selon le rôle et le commercial associé


class DummyClient:
    """Classe dummy pour simuler un client."""

    def __init__(self, contact_commercial_id=1):
        self.contact_commercial_id = contact_commercial_id


@patch("app.utils.db_utils.Console.print")
def test_can_update_client_gestion(mock_print):
    """Vérifie qu'un gestionnaire peut mettre à jour n'importe quel client."""
    assert db_utils.can_update_client({"role": "gestion", "id": 1}, DummyClient())


@patch("app.utils.db_utils.Console.print")
def test_can_update_client_commercial_ok(mock_print):
    """Vérifie qu'un commercial peut mettre à jour un client dont il est le contact."""
    payload = {"role": "commercial", "id": 1}
    assert db_utils.can_update_client(payload, DummyClient())


@patch("app.utils.db_utils.Console.print")
def test_can_update_client_commercial_invalid(mock_print):
    """Vérifie qu'un commercial ne peut pas mettre à jour un client qui n'est pas le sien."""
    payload = {"role": "commercial", "id": 2}
    assert not db_utils.can_update_client(payload, DummyClient(1))
    mock_print.assert_called()


@patch("app.utils.db_utils.Console.print")
def test_can_update_client_support(mock_print):
    """Vérifie qu'un support ne peut pas mettre à jour un client."""
    payload = {"role": "support", "id": 1}
    assert not db_utils.can_update_client(payload, DummyClient())
    mock_print.assert_called()
