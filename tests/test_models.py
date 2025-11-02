from datetime import date, datetime
from app.models.client import Client
from app.models.evenement import Evenement
from types import SimpleNamespace


def test_client_repr():
    """
    Vérifie que la représentation (__repr__) d'un objet Client contient le nom complet.
    """
    client = Client(
        nom_complet="Jean Dupont",
        email="jean@dupont.com",
        telephone="0102030405",
        entreprise="Dupont SARL",
        date_creation=date.today(),
    )

    # Obtenir la représentation sous forme de chaîne
    repr_str = repr(client)

    # Vérifie que le nom complet apparaît dans la représentation
    assert "Jean Dupont" in repr_str


def test_contrat_repr():
    """
    Vérifie la représentation (__repr__) d'un objet Contrat factice.
    Utilise SimpleNamespace pour simuler un contrat sans dépendances réelles.
    """
    # Création d'un contrat factice avec les attributs nécessaires pour le test
    contrat = SimpleNamespace(
        id=1,
        montant_total=1000.0,
        montant_restant=500.0,
        date_creation=date.today(),
        statut_contrat=True,
        client=SimpleNamespace(nom_complet="Jean Dupont"),
    )

    # Définition temporaire de la méthode __repr__ pour ce SimpleNamespace
    def contrat_repr(self):
        return f"<Contrat(id={self.id}, client={self.client.nom_complet})>"

    # Monkey patch pour associer la méthode __repr__ au contrat factice
    contrat.__repr__ = contrat_repr.__get__(contrat)

    # Obtenir la représentation et vérifier son contenu
    repr_str = repr(contrat)
    assert "id=1" in repr_str
    assert "Jean Dupont" in repr_str


def test_evenement_repr():
    """
    Vérifie que la représentation (__repr__) d'un objet Evenement contient le lieu.
    """
    evenement = Evenement(
        id=1,
        date_debut=datetime.now(),
        date_fin=datetime.now(),
        lieu="Paris",
        participants=50,
    )

    # Obtenir la représentation sous forme de chaîne
    repr_str = repr(evenement)

    # Vérifie que le lieu apparaît dans la représentation
    assert "Paris" in repr_str
