from flask import Flask
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp
from routes.prompt_routes import prompt_bp
from routes.visiteur_routes import visiteur_bp
from routes.note_routes import note_bp
from routes.vote_routes import vote_bp

def create_app():
    app = Flask(__name__)

    # Enregistrer les blueprints
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(prompt_bp, url_prefix='/prompt')
    app.register_blueprint(visiteur_bp, url_prefix='/visiteur')
    app.register_blueprint(note_bp, url_prefix='/note')
    app.register_blueprint(vote_bp, url_prefix='/vote')

    return app
