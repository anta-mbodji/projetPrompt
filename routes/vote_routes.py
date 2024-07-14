from flask import Blueprint, request, jsonify
import models.init_db as db
import utils.auth

vote_bp = Blueprint('vote', __name__)

# Route pour voter pour l'activation d'un prompt
@vote_bp.route('/voter_prompt', methods=['POST'])
@utils.auth.login_required
def voter_prompt():
    data = request.get_json()
    id_prompt = data.get('id_prompt')
    id_user = data.get('id_user')
    valeur_vote = data.get('valeur_vote')

    if not id_prompt or not id_user or valeur_vote is None:
        return jsonify({"message": "Paramètres manquants"}), 400
    
    # Vérifier que l'utilisateur ne vote pas pour son propre prompt
    query = "SELECT id_user FROM prompt WHERE id_prompt = %s"
    prompt_owner = db.fetch_query(query, (id_prompt,))
    if not prompt_owner or prompt_owner[0]['id_user'] == id_user:
        return jsonify({"message": "Vous ne pouvez pas voter pour votre propre prompt"}), 403

    # Insérer le vote dans la table
    query = "INSERT INTO vote (id_prompt, id_user, valeur_vote) VALUES (%s, %s, %s)"
    db.execute_query(query, (id_prompt, id_user, valeur_vote))

    # Recalculer le total des votes pour le prompt
    query = """
    SELECT SUM(valeur_vote) as total_votes
    FROM vote
    WHERE id_prompt = %s
    """
    total_votes = db.fetch_query(query, (id_prompt,))[0]['total_votes']
    
    # Activer le prompt si le total des votes atteint 6 points
    if total_votes >= 6:
        query = "UPDATE prompt SET status = %s WHERE id_prompt = %s"
        db.execute_query(query, ('Activé', id_prompt))
        return jsonify({"message": "Prompt activé avec succès"}), 200

    return jsonify({"message": "Vote ajouté avec succès", "total_votes": total_votes}), 201
