from functools import wraps
from flask import request, jsonify

# Décorateur pour vérifier si le token est présent et valide
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')  # Récupérer le token de l'en-tête de la requête
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403  # Retourner une erreur si le token est manquant
        # Ajouter ici la validation du token
        return f(*args, **kwargs)  # Exécuter la fonction décorée
    return decorated




# Décorateur pour vérifier si l'utilisateur est administrateur
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        role = request.headers.get('role')
        if role != 'admin':
            return jsonify({'message': 'Permission!'}), 403

        return f(*args, **kwargs)  # Exécuter la fonction décorée
    return decorated
