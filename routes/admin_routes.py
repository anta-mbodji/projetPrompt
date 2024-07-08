
from flask import Blueprint, jsonify, request
import models.init_db as db
import utils.auth

admin_bp = Blueprint('admin' , __name__)


@admin_bp.route('/create_user' , methods = ['GET','POST'])
def create_utilisateur():
    data = request.get_json()
    query = "INSERT INTO utilisateur (id_user,nom, email, mot_de_pass, rôle) VALUES (%s, %s, %s, %s, %s)"
    db.execute_query(query, (data['id_user'], data['nom'], data['email'], data['mot_de_pass'], data['rôle']))
    return jsonify({"message": "Utilisateur créé avec succès"}) , 201




@admin_bp.route('/recuperer_user', methods=['GET','POST'])
def get_utilisateur():
    query = "SELECT * FROM utilisateur"  # Requête pour sélectionner tous les utilisateurs
    admin = db.fetch_query(query)  # Exécuter la requête et récupérer les résultats
    return jsonify(admin), 200  # Retourner les utilisateurs sous forme de JSON



@admin_bp.route('/create_groupe' , methods = ['GET','POST'])
def create_groupe():
    data = request.get_json()
    query = "INSERT INTO groupe(id_groupe,name_groupe, nomb_membre) VALUES (%s, %s, %s)"
    db.execute_query(query, (data['id_groupe'], data['name_groupe'], data['nomb_membre']))
    return jsonify({"message": "groupe créé avec succès"}) , 201



@admin_bp.route('/recuperer_groupe', methods=['GET','POST'])
def get_groupe():
    query = "SELECT * FROM groupe"  # Requête pour sélectionner tous les utilisateurs
    admin = db.fetch_query(query)  # Exécuter la requête et récupérer les résultats
    return jsonify(admin), 200  # Retourner les utilisateurs sous forme de JSON



@admin_bp.route('/valider' , methods=['POST'])
@utils.auth.admin_required
def valider_prompt():
    data = request.get_json()
    prompt_id = data.get('id_prompt')

    if not prompt_id:
        return jsonify({"message": "absence de id_prompt"}), 400
    
    query = "UPDATE prompt SET status = %s WHERE id_prompt = %s"
    db.execute_query(query, ('Activé', prompt_id))

    return jsonify({"message": "prompt valide"}),200



@admin_bp.route('/recuperer_valid_prompts', methods=['GET','POST'])
def get_valide():
    query = "SELECT * FROM prompt"  # Requête pour sélectionner tous les utilisateurs
    admin = db.fetch_query(query)  # Exécuter la requête et récupérer les résultats
    return jsonify(admin), 200  # Retourner les utilisateurs sous forme de JSON



"""@admin_bp.route('/delete/<id_user>', methods=['GET','DELETE'])
def delete_utilisateur(id_user):
    query = "DELETE FROM user WHERE id_user = %s"
"""