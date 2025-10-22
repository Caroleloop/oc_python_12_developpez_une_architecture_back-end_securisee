# Permissions par défaut
DEFAULT_PERMISSIONS = {
    "gestion": {
        "collaborateur": ["lire", "creer", "modifier", "supprimer"],
        "client": ["lire"],
        "contrat": ["lire", "creer", "modifier", "supprimer"],
        "evenement": ["lire", "modifier"],
        "role": ["lire"],
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
