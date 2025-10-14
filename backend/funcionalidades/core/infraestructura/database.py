"""
Configuración de la base de datos
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def init_database(app):
    """Inicializar la base de datos"""
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.get_database_url()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db
