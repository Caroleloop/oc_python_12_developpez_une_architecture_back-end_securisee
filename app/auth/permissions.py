from functools import wraps


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


#  Fonctions utilitaires
def has_permission(user, resource, action):
    """
    Vérifie si l'utilisateur a la permission d'effectuer une action sur une ressource.
    :param user: instance de Collaborateur (avec user.role et role.permissions)
    :param resource: str, ex: "client", "contrat", "evenement"
    :param action: str, ex: "read", "create", "update", "delete"
    """
    if not user or not user.role:
        return False

    role_permissions = user.role.permissions or {}
    actions = role_permissions.get(resource, [])
    return action in actions


def require_permission(resource, action):
    """
    Décorateur à appliquer sur une fonction (par ex. un service ou une route Flask)
    pour vérifier les droits d'accès.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if not has_permission(user, resource, action):
                raise PermissionError(
                    f"Accès refusé : le rôle '{user.role.nom}' n'a pas la permission "
                    f"'{action}' sur '{resource}'."
                )
            return func(user, *args, **kwargs)

        return wrapper

    return decorator


def filter_query_for_user(query, user, model):
    """
    Restreint les résultats SQLAlchemy selon le rôle.
    Exemple :
        query = session.query(Client)
        query = filter_query_for_user(query, current_user, Client)
    """
    role = user.role.nom.lower()

    # --- Commercial ---
    if role == "commercial":
        if hasattr(model, "contact_commercial_id"):
            return query.filter_by(contact_commercial_id=user.id)

    # --- Support ---
    elif role == "support":
        if hasattr(model, "support_contact_id"):
            return query.filter_by(support_contact_id=user.id)

    # --- Gestion ---
    return query  # Accès complet


def get_default_permissions(role_name):
    """Retourne les permissions par défaut d’un rôle donné."""
    return DEFAULT_PERMISSIONS.get(role_name.lower(), {})
