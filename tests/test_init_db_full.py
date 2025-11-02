from unittest.mock import patch, MagicMock, ANY
from app.init_db_full import create_database, DB_NAME


# ------------------- TEST create_database -------------------
# Tests pour la fonction create_database qui crée la base si elle n'existe pas


@patch("psycopg2.connect")
def test_create_database_new(mock_connect):
    """
    Vérifie que create_database crée la base de données si elle n'existe pas.
    """
    # Création de mocks pour la connexion et le curseur
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.autocommit = True

    # Simule que la base n'existe pas
    mock_cursor.fetchone.return_value = None

    # Appel de la fonction à tester
    create_database()

    # Vérifie que la commande SELECT pour vérifier l'existence a été appelée
    mock_cursor.execute.assert_any_call(ANY, [DB_NAME])

    # Vérifie que la commande CREATE DATABASE a été appelée
    from psycopg2 import sql

    mock_cursor.execute.assert_any_call(
        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME))
    )


@patch("psycopg2.connect")
def test_create_database_exists(mock_connect):
    """
    Vérifie que create_database ne tente pas de créer la base si elle existe déjà.
    """
    # Création de mocks pour la connexion et le curseur
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.autocommit = True

    # Simule que la base existe déjà
    mock_cursor.fetchone.return_value = (1,)

    # Appel de la fonction à tester
    create_database()

    # Vérifie que CREATE DATABASE n'a pas été exécutée
    from psycopg2 import sql

    # Récupère toutes les requêtes exécutées
    calls = [call[0][0] for call in mock_cursor.execute.call_args_list]

    # Vérifie que la commande CREATE DATABASE n'est pas dans les appels
    assert sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)) not in calls
