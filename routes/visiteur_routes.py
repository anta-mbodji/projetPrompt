from flask import Blueprint, request, jsonify
import models.init_db as db

# Créer un blueprint pour les routes visiteur
visiteur_bp = Blueprint('visiteur', __name__)

# Route pour consulter un prompt
@visiteur_bp.route('/consulter_prompt/<int:prompt_id>', methods=['GET'])
def consulter_prompt(prompt_id):
    try:
        query = "SELECT * FROM prompt WHERE id_prompt = %s"
        prompt = db.fetch_query(query, (prompt_id,))
        if not prompt:
            return jsonify({'message': 'Prompt not found'}), 404
        return jsonify(prompt), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour rechercher des prompts par contenu ou mots-clés
@visiteur_bp.route('/rechercher_prompts', methods=['GET'])
def rechercher_prompts():
    try:
        search_query = request.args.get('q')
        if not search_query:
            return jsonify({'message': 'Query parameter "q" is required'}), 400
        
        query = "SELECT * FROM prompt WHERE content ILIKE %s"
        prompts = db.fetch_query(query, ('%' + search_query + '%',))
        return jsonify(prompts), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour acheter un prompt
@visiteur_bp.route('/acheter_prompt/<int:prompt_id>', methods=['POST'])
def acheter_prompt(prompt_id):
    try:
        # Simulate the purchase process (this is just an example, replace with actual purchase logic)
        query = "SELECT * FROM prompt WHERE id_prompt = %s"
        prompt = db.fetch_query(query, (prompt_id,))
        if not prompt:
            return jsonify({'message': 'Prompt not found'}), 404
        
        # Assuming the purchase is successful, return a success message
        return jsonify({'message': 'Prompt acheté avec succès', 'prompt': prompt}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
