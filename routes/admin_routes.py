from flask import Blueprint, jsonify, request
import models.init_db as db
import utils.auth

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/create_user', methods=['POST'])
def create_utilisateur():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("id_user", "nom", "email", "mot_de_pass", "rôle")):
            return jsonify({"message": "Invalid data"}), 400
        
        query = "INSERT INTO utilisateur (id_user, nom, email, mot_de_pass, rôle) VALUES (%s, %s, %s, %s, %s)"
        db.execute_query(query, (data['id_user'], data['nom'], data['email'], data['mot_de_pass'], data['rôle']))
        
        return jsonify({"message": "Utilisateur créé avec succès"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/recuperer_user', methods=['GET'])
def get_utilisateur():
    try:
        query = "SELECT * FROM utilisateur"
        users = db.fetch_query(query)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/create_groupe', methods=['POST'])
def create_groupe():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("id_groupe", "name_groupe", "nomb_membre")):
            return jsonify({"message": "Invalid data"}), 400
        
        query = "INSERT INTO groupe(id_groupe, name_groupe, nomb_membre) VALUES (%s, %s, %s)"
        db.execute_query(query, (data['id_groupe'], data['name_groupe'], data['nomb_membre']))
        
        return jsonify({"message": "Groupe créé avec succès"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/recuperer_groupe', methods=['GET'])
def get_groupe():
    try:
        query = "SELECT * FROM groupe"
        groupes = db.fetch_query(query)
        return jsonify(groupes), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/valider', methods=['POST'])
@utils.auth.admin_required
def valider_prompt():
    try:
        data = request.get_json()
        prompt_id = data.get('id_prompt')

        if not prompt_id:
            return jsonify({"message": "Absence de id_prompt"}), 400
        
        query = "UPDATE prompt SET status = %s WHERE id_prompt = %s"
        db.execute_query(query, ('Activé', prompt_id))

        return jsonify({"message": "Prompt validé"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/recuperer_valid_prompts', methods=['GET'])
def get_valid_prompts():
    try:
        query = "SELECT * FROM prompt WHERE status = 'Activé'"
        prompts = db.fetch_query(query)
        return jsonify(prompts), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/demander_modification', methods=['POST'])
@utils.auth.admin_required
def demander_modification():
    try:
        data = request.get_json()
        prompt_id = data.get('id_prompt')

        if not prompt_id:
            return jsonify({"message": "Absence de id_prompt"}), 400
        
        query = "UPDATE prompt SET status = %s WHERE id_prompt = %s"
        db.execute_query(query, ('À revoir', prompt_id))

        return jsonify({"message": "Demande de modification envoyée"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@admin_bp.route('/supprimer_prompt', methods=['DELETE'])
@utils.auth.admin_required
def supprimer_prompt():
    try:
        data = request.get_json()
        prompt_id = data.get('id_prompt')

        if not prompt_id:
            return jsonify({"message": "Absence de id_prompt"}), 400
        
        query = "DELETE FROM prompt WHERE id_prompt = %s"
        db.execute_query(query, (prompt_id,))

        return jsonify({"message": "Prompt supprimé"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
