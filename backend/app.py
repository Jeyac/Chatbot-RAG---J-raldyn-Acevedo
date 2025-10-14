"""
Aplicación principal del chatbot con RAG
"""
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from funcionalidades.core.infraestructura.database import init_database
from funcionalidades.core.infraestructura.config import Config
from funcionalidades.documentos.presentation.controllers.documento_controller import documento_bp
from funcionalidades.chat.presentation.controllers.chat_controller import (
    chat_bp, on_connect, on_disconnect, on_unirse_sala, on_salir_sala,
    on_enviar_mensaje, on_solicitar_historial, on_limpiar_historial
)

# Crear aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Configurar límite de tamaño de archivo (1GB)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1GB en bytes

# Configurar CORS
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Inicializar base de datos
init_database(app)

# Registrar Blueprints
app.register_blueprint(documento_bp)
app.register_blueprint(chat_bp)

# Inicializar SocketIO después de registrar blueprints
socketio = SocketIO(
    app, 
    cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    logger=True,
    engineio_logger=True,
    async_mode='threading'
)

# Registrar eventos de WebSocket
socketio.on_event('connect', on_connect)
socketio.on_event('disconnect', on_disconnect)
socketio.on_event('unirse_sala', on_unirse_sala)
socketio.on_event('salir_sala', on_salir_sala)
socketio.on_event('enviar_mensaje', on_enviar_mensaje)
socketio.on_event('solicitar_historial', on_solicitar_historial)
socketio.on_event('limpiar_historial', on_limpiar_historial)


@app.route('/')
def index():
    """Endpoint de bienvenida"""
    return jsonify({
        'mensaje': 'Chatbot con RAG - API',
        'version': '1.0.0',
        'endpoints': {
            'documentos': '/api/documentos/',
            'chat': '/api/chat/',
            'websocket': 'ws://localhost:5000/socket.io/'
        }
    })


@app.route('/health')
def health_check():
    """Endpoint de verificación de salud"""
    try:
        from funcionalidades.core.infraestructura.openai_service import OpenAIService
        openai_service = OpenAIService()
        openai_status = 'connected' if openai_service.verificar_conexion() else 'disconnected'
    except Exception:
        openai_status = 'not_configured'
    
    return jsonify({
        'status': 'healthy',
        'environment': Config.ENVIRONMENT,
        'database': 'connected' if Config.get_database_url() else 'disconnected',
        'openai': openai_status
    })


@app.errorhandler(404)
def not_found(error):
    """Manejar errores 404"""
    return jsonify({'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejar errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500


if __name__ == '__main__':
    # Crear tablas si no existen
    with app.app_context():
        from funcionalidades.core.infraestructura.database import db
        db.create_all()
    
    # Ejecutar aplicación
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
