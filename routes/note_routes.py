from flask import Blueprint, request, jsonify
import models.init_db as db
import utils.auth

note_bp = Blueprint('note', __name__)

# Route pour noter un prompt
@note_bp.route('/noter_prompt', methods=['POST'])
@utils.auth.login_required
def noter_prompt():
    data = request.get_json()
    id_prompt = data.get('id_prompt')
    id_user = data.get('id_user')
    valeur_note = data.get('valeur_note')

    if not id_prompt or not id_user or valeur_note is None:
        return jsonify({"message": "Paramètres manquants"}), 400
    
    # Vérifier que l'utilisateur ne note pas son propre prompt
    query = "SELECT id_user FROM prompt WHERE id_prompt = %s"
    prompt_owner = db.fetch_query(query, (id_prompt,))
    if not prompt_owner or prompt_owner[0]['id_user'] == id_user:
        return jsonify({"message": "Vous ne pouvez pas noter votre propre prompt"}), 403

    # Insérer la note dans la table
    query = "INSERT INTO note (id_prompt, id_user, valeur_note) VALUES (%s, %s, %s)"
    db.execute_query(query, (id_prompt, id_user, valeur_note))

    # Recalculer la note moyenne du prompt
    query = """
    SELECT AVG(valeur_note) as moyenne_note
    FROM note
    WHERE id_prompt = %s
    """
    moyenne_note = db.fetch_query(query, (id_prompt,))[0]['moyenne_note']
    
    # Recalculer le prix du prompt
    nouveau_prix = 1000 * (1 + moyenne_note)
    query = "UPDATE prompt SET prix = %s WHERE id_prompt = %s"
    db.execute_query(query, (nouveau_prix, id_prompt))

    return jsonify({"message": "Prompt noté avec succès", "nouveau_prix": nouveau_prix}), 201
