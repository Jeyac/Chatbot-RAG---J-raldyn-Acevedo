"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base"""
    
    # Base de datos
    DB_NAME = os.getenv('DB_NAME', 'chatbot_rag_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'clave_secreta_flask')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Detectar driver de PostgreSQL
    try:
        import psycopg
        DB_DRIVER = 'psycopg'
    except ImportError:
        try:
            import psycopg2
            DB_DRIVER = 'psycopg2'
        except ImportError:
            DB_DRIVER = 'sqlite'
    
    @classmethod
    def get_database_url(cls):
        """Obtener URL de conexión a la base de datos"""
        if cls.DB_DRIVER == 'sqlite':
            return 'sqlite:///chatbot_rag.db'
        
        return f"postgresql+{cls.DB_DRIVER}://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
