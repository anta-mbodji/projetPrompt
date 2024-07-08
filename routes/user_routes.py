from flask import Blueprint, request, jsonify
import models.init_db as db

# Créer un blueprint pour les routes utilisateur
user_bp = Blueprint('user', __name__)

# Route pour créer un nouvel utilisateur
@user_bp.route('/create', methods=['GET','POST'])
def create_user():
    data = request.get_json()  # Récupérer les données JSON de la requête
    query = "INSERT INTO utilisateur (id, nom, email, mot_de_pass, rôle) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(query, (data['id'], data['nom'], data['email'], data['mot_de_pass'], data['rôle']))  # Exécuter la requête pour insérer un nouvel utilisateur
    return jsonify({'message': 'User created successfully'}), 201  # Retourner une réponse JSON

# Route pour obtenir tous les utilisateurs
@user_bp.route('/recuperer', methods=['GET','POST'])
def get_users():
    query = "SELECT * FROM utilisateur"  # Requête pour sélectionner tous les utilisateurs
    user = db.fetch_query(query)  # Exécuter la requête et récupérer les résultats
    return jsonify(user), 200  # Retourner les utilisateurs sous forme de JSON
