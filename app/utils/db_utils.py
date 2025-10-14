from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import Type


def lire_table(db: Session, modele: Type):
    """
    Lit et affiche le contenu d'une table SQLAlchemy.

    Args:
        db (Session): La session SQLAlchemy active.
        modele (Type): La classe du modèle (ex: Collaborateur, Client, etc.)

    Retourne:
        list[dict]: Liste des lignes sous forme de dictionnaires.
    """
    table_name = modele.__tablename__
    lignes = db.query(modele).all()

    if not lignes:
        print(f"Aucune donnée trouvée dans la table '{table_name}'.")
        return []

    # Récupère dynamiquement les noms des colonnes
    colonnes = [c.key for c in inspect(modele).mapper.column_attrs]

    # Affiche les résultats
    print(f"\nContenu de la table '{table_name}':\n")
    resultats = []
    for obj in lignes:
        data = {col: getattr(obj, col) for col in colonnes}
        resultats.append(data)
        print(" | ".join(f"{col}: {data[col]}" for col in colonnes))
    print("\nLecture terminée.")
    return resultats
