"""
Controlador para chat con WebSockets
"""
from flask import Blueprint, request, jsonify
from flask_socketio import emit, join_room, leave_room
from funcionalidades.chat.application.use_cases.procesar_mensaje_use_case import ProcesarMensajeUseCase
from funcionalidades.chat.application.use_cases.obtener_historial_use_case import ObtenerHistorialUseCase
from funcionalidades.chat.application.use_cases.limpiar_historial_use_case import LimpiarHistorialUseCase
from funcionalidades.chat.infrastructure.mensaje_repository_impl import MensajeRepositoryImpl
from funcionalidades.documentos.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.core.infraestructura.openai_service import OpenAIService
from funcionalidades.core.infraestructura.embeddings_service import EmbeddingsService
from funcionalidades.core.exceptions.domain_exceptions import ValidationError, ProcessingError, OpenAIError

# Crear Blueprint
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Inicializar repositorios y casos de uso
mensaje_repository = MensajeRepositoryImpl()
documento_repository = DocumentoRepositoryImpl()
openai_service = OpenAIService()
embeddings_service = EmbeddingsService()
procesar_mensaje_use_case = ProcesarMensajeUseCase(mensaje_repository, documento_repository, openai_service, embeddings_service)
obtener_historial_use_case = ObtenerHistorialUseCase(mensaje_repository)
limpiar_historial_use_case = LimpiarHistorialUseCase(mensaje_repository)


@chat_bp.route('/historial', methods=['GET'])
def obtener_historial():
    """Obtener historial de mensajes"""
    try:
        limite = request.args.get('limite', 50, type=int)
        mensajes = obtener_historial_use_case.ejecutar(limite)
        
        return jsonify([{
            'id': msg.id,
            'contenido': msg.contenido,
            'es_usuario': msg.es_usuario,
            'fecha_creacion': msg.fecha_creacion.isoformat(),
            'documento_id': msg.documento_id
        } for msg in mensajes]), 200
        
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@chat_bp.route('/historial/<int:documento_id>', methods=['GET'])
def obtener_historial_documento(documento_id):
    """Obtener historial de mensajes de un documento específico"""
    try:
        limite = request.args.get('limite', 50, type=int)
        mensajes = mensaje_repository.listar_por_documento(documento_id, limite)
        
        return jsonify([{
            'id': msg.id,
            'contenido': msg.contenido,
            'es_usuario': msg.es_usuario,
            'fecha_creacion': msg.fecha_creacion.isoformat(),
            'documento_id': msg.documento_id
        } for msg in mensajes]), 200
        
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@chat_bp.route('/limpiar', methods=['POST'])
def limpiar_historial():
    """Limpiar historial de mensajes"""
    try:
        limpiar_historial_use_case.ejecutar()
        
        return jsonify({'mensaje': 'Historial limpiado exitosamente'}), 200
        
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


# Eventos de WebSocket
def on_connect():
    """Manejar conexión de WebSocket"""
    print('Cliente conectado')
    emit('conectado', {'mensaje': 'Conectado al chat'})


def on_disconnect():
    """Manejar desconexión de WebSocket"""
    print('Cliente desconectado')


def on_unirse_sala(sala):
    """Manejar unión a sala de chat"""
    join_room(sala)
    emit('unido_sala', {'sala': sala, 'mensaje': f'Te has unido a la sala {sala}'})


def on_salir_sala(sala):
    """Manejar salida de sala de chat"""
    leave_room(sala)
    emit('salido_sala', {'sala': sala, 'mensaje': f'Has salido de la sala {sala}'})


def on_enviar_mensaje(data):
    """Manejar envío de mensaje"""
    try:
        contenido = data.get('mensaje', '').strip()
        documento_id = data.get('documento_id')
        
        if not contenido:
            emit('error', {'mensaje': 'El mensaje no puede estar vacío'})
            return
        
        # Procesar mensaje
        respuesta = procesar_mensaje_use_case.ejecutar(contenido, documento_id)
        
        # Emitir respuesta
        emit('mensaje_recibido', {
            'id': respuesta.id,
            'contenido': respuesta.contenido,
            'es_usuario': respuesta.es_usuario,
            'fecha_creacion': respuesta.fecha_creacion.isoformat(),
            'documento_id': respuesta.documento_id
        })
        
    except ValidationError as e:
        emit('error', {'mensaje': str(e)})
    except ProcessingError as e:
        emit('error', {'mensaje': str(e)})
    except Exception as e:
        emit('error', {'mensaje': f'Error interno: {str(e)}'})


def on_solicitar_historial(data):
    """Manejar solicitud de historial"""
    try:
        limite = data.get('limite', 50)
        mensajes = obtener_historial_use_case.ejecutar(limite)
        
        emit('historial_enviado', [{
            'id': msg.id,
            'contenido': msg.contenido,
            'es_usuario': msg.es_usuario,
            'fecha_creacion': msg.fecha_creacion.isoformat(),
            'documento_id': msg.documento_id
        } for msg in mensajes])
        
    except ProcessingError as e:
        emit('error', {'mensaje': str(e)})
    except Exception as e:
        emit('error', {'mensaje': f'Error interno: {str(e)}'})


def on_limpiar_historial():
    """Manejar limpieza de historial"""
    try:
        limpiar_historial_use_case.ejecutar()
        emit('historial_limpiado', {'mensaje': 'Historial limpiado exitosamente'})
        
    except ProcessingError as e:
        emit('error', {'mensaje': str(e)})
    except Exception as e:
        emit('error', {'mensaje': f'Error interno: {str(e)}'})
