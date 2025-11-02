import pytest
import jwt
import os
from datetime import datetime, timedelta, timezone
from app.auth import core, utils


# --- FIXTURES GÉNÉRALES ---
# Fournissent des objets factices pour les rôles, utilisateurs et sessions DB


class DummyRole:
    """Classe factice pour simuler un rôle d'utilisateur."""

    def __init__(self, role):
        self.role = role


class DummyCollaborateur:
    """Classe factice pour simuler un collaborateur/utilisateur."""

    def __init__(
        self, id=1, email="test@example.com", mot_de_passe="hashed", role="gestion"
    ):
        self.id = id
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.role = DummyRole(role)


@pytest.fixture
def fake_db(monkeypatch):
    """
    Fixture pour simuler une session SQLAlchemy.
    - DummySession.query renvoie un DummyQuery.
    - DummyQuery.first() retourne l'utilisateur simulé.
    """

    class DummyQuery:
        def __init__(self, user):
            self.user = user

        def filter_by(self, **kwargs):
            return self

        def first(self):
            return self.user

    class DummySession:
        def __init__(self, user=None):
            self.user = user

        def query(self, model):
            return DummyQuery(self.user)

        def close(self):
            pass

    return DummySession


# --- TESTS LOGIN ---


def test_login_success(monkeypatch, fake_db):
    """
    Vérifie qu’un token JWT est renvoyé pour un utilisateur valide.
    - Monkeypatch SessionLocal, check_password_hash et SECRET_KEY.
    - Vérifie le contenu décodé du token.
    """
    user = DummyCollaborateur(mot_de_passe="hashed")

    monkeypatch.setattr(core, "SessionLocal", lambda: fake_db(user))
    monkeypatch.setattr(core, "check_password_hash", lambda h, p: True)
    monkeypatch.setattr(core, "SECRET_KEY", "test_secret")

    token = core.login("test@example.com", "password")
    decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
    assert decoded["email"] == "test@example.com"
    assert decoded["role"] == "gestion"
    assert "exp" in decoded


def test_login_invalid_email(monkeypatch, fake_db):
    """
    Vérifie que le login échoue si l’email n’existe pas.
    - Doit lever ValueError avec le message approprié.
    """
    monkeypatch.setattr(core, "SessionLocal", lambda: fake_db(user=None))
    monkeypatch.setattr(core, "check_password_hash", lambda h, p: True)
    with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
        core.login("bad@example.com", "password")


def test_login_wrong_password(monkeypatch, fake_db):
    """
    Vérifie que le login échoue si le mot de passe est incorrect.
    - Doit lever ValueError avec le message approprié.
    """
    user = DummyCollaborateur(mot_de_passe="hashed")
    monkeypatch.setattr(core, "SessionLocal", lambda: fake_db(user))
    monkeypatch.setattr(core, "check_password_hash", lambda h, p: False)
    with pytest.raises(ValueError, match="Email ou mot de passe incorrect"):
        core.login("test@example.com", "wrongpass")


# --- TESTS TOKEN UTILS ---


@pytest.fixture
def token_file(tmp_path):
    """
    Fixture qui crée un fichier .token temporaire pour les tests de tokens.
    - Remplace utils.TOKEN_FILE par ce fichier temporaire.
    """
    file_path = tmp_path / ".token"
    utils.TOKEN_FILE = str(file_path)
    return file_path


def test_verifier_token_valid(monkeypatch, token_file):
    """
    Vérifie qu’un token valide est décodé correctement.
    - Écrit un token JWT valide dans le fichier .token.
    - Vérifie que l'email décodé correspond.
    """
    payload = {
        "id": "1",
        "email": "toto@test.com",
        "role": "gestion",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, "secret", algorithm="HS256")
    monkeypatch.setattr(utils, "SECRET_KEY", "secret")

    token_file.write_text(token)
    result = utils.verifier_token(token)
    assert result["email"] == "toto@test.com"


def test_verifier_token_expired(monkeypatch, token_file):
    """
    Vérifie qu’un token expiré lève une PermissionError.
    """
    payload = {"id": "1", "exp": datetime.now(timezone.utc) - timedelta(seconds=1)}
    token = jwt.encode(payload, "secret", algorithm="HS256")
    monkeypatch.setattr(utils, "SECRET_KEY", "secret")

    token_file.write_text(token)
    with pytest.raises(PermissionError, match="session a expiré"):
        utils.verifier_token(token)


def test_verifier_token_invalid(monkeypatch, token_file):
    """
    Vérifie qu’un token corrompu lève une PermissionError.
    """
    monkeypatch.setattr(utils, "SECRET_KEY", "secret")
    token_file.write_text("invalid.token")
    with pytest.raises(PermissionError, match="Token invalide"):
        utils.verifier_token("invalid.token")


def test_verifier_token_file_missing(monkeypatch):
    """
    Vérifie que l’absence du fichier .token lève une PermissionError.
    """
    monkeypatch.setattr(utils, "TOKEN_FILE", "nonexistent.token")
    with pytest.raises(PermissionError, match="Aucun token trouvé"):
        utils.verifier_token("")


# --- TEST LOGOUT (simulé) ---


def test_logout_remove_token_file(token_file):
    """
    Simule la déconnexion en supprimant le fichier .token.
    - Vérifie que le fichier est créé puis supprimé correctement.
    """
    token_file.write_text("fake-token")
    assert os.path.exists(token_file)
    os.remove(token_file)
    assert not os.path.exists(token_file)
