from flask import Blueprint, request, jsonify
import models.init_db as db
import utils.auth

# Créer un blueprint pour les routes utilisateur
user_bp = Blueprint('user', __name__)

# Route pour créer un nouvel utilisateur
@user_bp.route('/create', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  # Récupérer les données JSON de la requête
        if not data or not all(k in data for k in ("id", "nom", "email", "mot_de_pass", "rôle")):
            return jsonify({'message': 'Invalid data'}), 400

        query = "INSERT INTO utilisateur (id_user, nom, email, mot_de_pass, rôle) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(query, (data['id'], data['nom'], data['email'], data['mot_de_pass'], data['rôle']))
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour obtenir tous les utilisateurs
@user_bp.route('/recuperer', methods=['GET'])
def get_users():
    try:
        query = "SELECT * FROM utilisateur"
        users = db.fetch_query(query)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour proposer un nouveau prompt à vendre
@user_bp.route('/proposer_prompt', methods=['POST'])
@utils.auth.login_required
def proposer_prompt():
    try:
        data = request.get_json()
        user_id = utils.auth.get_user_id()  # Récupérer l'ID de l'utilisateur connecté

        if not data or 'content' not in data:
            return jsonify({'message': 'Invalid data'}), 400

        query = "INSERT INTO prompt (content, prix, note, status, user_id) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(query, (data['content'], 1000, 0, 'En attente', user_id))
        return jsonify({'message': 'Prompt proposé avec succès'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour voter pour l'activation des prompts en attente
@user_bp.route('/voter_prompt', methods=['POST'])
@utils.auth.login_required
def voter_prompt():
    try:
        data = request.get_json()
        user_id = utils.auth.get_user_id()
        prompt_id = data.get('id_prompt')

        if not prompt_id:
            return jsonify({'message': 'Absence de id_prompt'}), 400

        # Vérifier si l'utilisateur a déjà voté
        query = "SELECT * FROM vote WHERE user_id = %s AND prompt_id = %s"
        existing_vote = db.fetch_query(query, (user_id, prompt_id))
        if existing_vote:
            return jsonify({'message': 'Vous avez déjà voté pour ce prompt'}), 400

        # Insérer le vote
        query = "INSERT INTO vote (user_id, prompt_id, valeur_vote) VALUES (%s, %s, %s)"
        db.execute_query(query, (user_id, prompt_id, 1))  # Valeur du vote peut être ajustée

        # Vérifier le total des votes pour le prompt
        query = "SELECT COUNT(*) as total_votes FROM vote WHERE prompt_id = %s"
        total_votes = db.fetch_query(query, (prompt_id,))[0]['total_votes']

        # Activer le prompt si le total des votes atteint le seuil
        if total_votes >= 6:  # Seuil de votes à ajuster selon les règles de gestion
            query = "UPDATE prompt SET status = %s WHERE id_prompt = %s"
            db.execute_query(query, ('Activé', prompt_id))

        return jsonify({'message': 'Vote enregistré avec succès'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Route pour noter les prompts activés
@user_bp.route('/noter_prompt', methods=['POST'])
@utils.auth.login_required
def noter_prompt():
    try:
        data = request.get_json()
        user_id = utils.auth.get_user_id()
        prompt_id = data.get('id_prompt')
        note = data.get('valeur_note')

        if not prompt_id or note is None or not (-10 <= note <= 10):
            return jsonify({'message': 'Invalid data'}), 400

        # Vérifier que le prompt n'appartient pas à l'utilisateur
        query = "SELECT user_id FROM prompt WHERE id_prompt = %s"
        prompt_owner_id = db.fetch_query(query, (prompt_id,))[0]['user_id']
        if user_id == prompt_owner_id:
            return jsonify({'message': 'Vous ne pouvez pas noter votre propre prompt'}), 400

        # Insérer la note
        query = "INSERT INTO note (user_id, prompt_id, valeur_note) VALUES (%s, %s, %s)"
        db.execute_query(query, (user_id, prompt_id, note))

        # Calculer la nouvelle moyenne des notes
        query = "SELECT AVG(valeur_note) as moyenne_note FROM note WHERE prompt_id = %s"
        moyenne_note = db.fetch_query(query, (prompt_id,))[0]['moyenne_note']

        # Recalculer le prix du prompt
        nouveau_prix = 1000 * (1 + moyenne_note)
        query = "UPDATE prompt SET prix = %s WHERE id_prompt = %s"
        db.execute_query(query, (nouveau_prix, prompt_id))

        return jsonify({'message': 'Note enregistrée avec succès', 'nouveau_prix': nouveau_prix}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
