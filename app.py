from flask import Flask
import models.init_db as db
from routes.user_routes import user_bp  # Importer le blueprint des utilisateurs
from routes.prompt_routes import prompt_bp  # Importer le blueprint des prompts
from routes.admin_routes import admin_bp
from routes.visiteur_routes import visiteur_bp
from routes.note_routes import note_bp
from routes.vote_routes import vote_bp
 
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def firstname() :
    print(db.connect())
    return "Hello World"


# Enregistrer les blueprints
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(prompt_bp, url_prefix='/prompts')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(visiteur_bp, url_prefix='/visiteur')
app.register_blueprint(note_bp, url_prefix='/note')
app.register_blueprint(vote_bp, url_prefix='/vote')

if __name__ == '__main__' :
    app.run(debug=True)