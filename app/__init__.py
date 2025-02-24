from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Importar base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config.from_object(Config)

    # Inicializzar extensiones
    db.init_app(app)

    from app.forms import LoginForm, RegisterForm
    from .routes import register_routes
    register_routes(app)
    
    return app
