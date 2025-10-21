# Permissions par défaut
DEFAULT_PERMISSIONS = {
    "gestion": {
        "collaborateur": ["read", "create", "update", "delete"],
        "client": ["read"],
        "contrat": ["read", "create", "update", "delete"],
        "evenement": ["read", "update"],
    },
    "commercial": {
        "client": ["read", "create", "update"],
        "contrat": ["read", "create", "update"],
        "evenement": ["read", "create"],
    },
    "support": {
        "client": ["read"],
        "contrat": ["read"],
        "evenement": ["read", "update"],
    },
}
