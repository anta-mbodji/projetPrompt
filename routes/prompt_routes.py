from flask import Blueprint, render_template,redirect, request, jsonify
import models.init_db as db

# Créer un blueprint pour les routes des prompts
prompt_bp = Blueprint('prompt', __name__)

# Route pour créer un nouveau prompt
@prompt_bp.route('/create', methods=['GET','POST'])
def create_prompt():
    data = request.get_json()  # Récupérer les données JSON de la requête
    query = "INSERT INTO prompt (id_prompt, content, prix, note, status) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(query, (data['id_prompt'],data['content'],data['prix'],data['note'],data['status']))  # Exécuter la requête pour insérer un nouveau prompt
    return jsonify({'message': 'Prompt created successfully'}), 201  # Retourner une réponse JSON

# Route pour obtenir tous les prompts
@prompt_bp.route('/recuperer', methods=['GET','POST'])
def get_prompts():

    query = "SELECT * FROM prompt"  # Requête pour sélectionner tous les prompts
    prompts = db.fetch_query(query)  # Exécuter la requête et récupérer les résultats
    return jsonify(prompts), 200  # Retourner les prompts sous forme de JSON
