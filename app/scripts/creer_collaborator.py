from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash
from app.database import engine, Base
from app.models.collaborateur import Collaborateur, Role
from app.models.client import Client
from app.models.contrat import Contrat
from app.models.evenement import Evenement


# Liste de tous les modèles pour d'éventuelles opérations globales
all_models = [Client, Contrat, Evenement, Collaborateur, Role]

# Crée toutes les tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

# Démarre une session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


def creer_collaborateur(nom: str, email: str, mot_de_passe: str, nom_role: str):
    """
    Crée un nouveau collaborateur avec un rôle donné.
    """
    # Vérifie si le rôle existe
    role = session.query(Role).filter_by(role=nom_role).first()
    if not role:
        print(f"Le rôle '{nom_role}' n'existe pas.")
        return

    # Hache le mot de passe
    mot_de_passe_hache = generate_password_hash(mot_de_passe)

    # Crée le collaborateur
    nouveau_collab = Collaborateur(
        nom=nom, email=email, mot_de_passe=mot_de_passe_hache, role=role
    )

    # Ajoute et commit
    session.add(nouveau_collab)
    session.commit()
    print(f"Collaborateur '{nom}' créé avec succès !")


# Exemple d'utilisation
if __name__ == "__main__":
    creer_collaborateur(
        nom="Alice Dupont",
        email="alice.dupont@example.com",
        mot_de_passe="MotDePasse123",
        nom_role="commercial",
    )
