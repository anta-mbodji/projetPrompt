import psycopg2
from psycopg2.extras import RealDictCursor


def connect():

    conn = psycopg2.connect(database="prompt_projet",
                             host="localhost",
                             user="postgres",
                             password="improvise")
    return conn

# Fonction pour exécuter des requêtes SQL qui modifient la base de données
def execute_query(query, params=None):
    conn = connect()  # Se connecter à la base de données
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # Utiliser RealDictCursor pour obtenir des résultats sous forme de dictionnaire
    cursor.execute(query, params)  # Exécuter la requête avec les paramètres
    conn.commit()  # Valider les modifications
    conn.close()  # Fermer la connexion

# Fonction pour récupérer des données de la base de données
def fetch_query(query, params=None):
    conn = connect()  # Se connecter à la base de données
    cursor = conn.cursor(cursor_factory=RealDictCursor)  # Utiliser RealDictCursor pour obtenir des résultats sous forme de dictionnaire
    cursor.execute(query, params)  # Exécuter la requête avec les paramètres
    result = cursor.fetchall()  # Récupérer tous les résultats
    conn.close()  # Fermer la connexion
    return result  # Retourner les résultats


