import os

# Classe de configuration pour l'application
class Config:
    DEBUG = True  # Activer le mode debug
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # Clé secrète pour les sessions Flask
    DATABASE_URI = 'postgresql://postgres:improvise@localhost/prompt_projet'  # URI de la base de données PostgreSQL
