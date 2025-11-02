# Permissions par défaut
DEFAULT_PERMISSIONS = {
    "gestion": {
        "collaborateur": ["lire", "creer", "modifier", "supprimer"],
        "client": ["lire"],
        "contrat": ["lire", "creer", "modifier"],
        "evenement": ["lire", "modifier"],
        "role": ["lire", "creer", "modifier", "supprimer"],
    },
    "commercial": {
        "client": ["lire", "creer", "modifier"],
        "contrat": ["lire", "creer", "modifier"],
        "evenement": ["lire", "creer"],
    },
    "support": {
        "client": ["lire"],
        "contrat": ["lire"],
        "evenement": ["lire", "modifier"],
    },
}


def get_default_permissions(role_name: str):
    # retourne un dict JSON simulant les permissions
    return {"read": True, "write": False}
