"""
Controlador REST para documentos
"""
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
from io import BytesIO
from funcionalidades.documentos.application.use_cases.crear_documento_use_case import CrearDocumentoUseCase
from funcionalidades.documentos.application.use_cases.listar_documentos_use_case import ListarDocumentosUseCase
from funcionalidades.documentos.application.use_cases.obtener_documento_use_case import ObtenerDocumentoUseCase
from funcionalidades.documentos.application.use_cases.eliminar_documento_use_case import EliminarDocumentoUseCase
from funcionalidades.documentos.application.use_cases.procesar_documento_use_case import ProcesarDocumentoUseCase
from funcionalidades.documentos.infrastructure.documento_repository_impl import DocumentoRepositoryImpl
from funcionalidades.core.infraestructura.embeddings_service import EmbeddingsService
from funcionalidades.core.exceptions.domain_exceptions import ValidationError, NotFoundError, ProcessingError

# Crear Blueprint
documento_bp = Blueprint('documentos', __name__, url_prefix='/api/documentos')

# Inicializar repositorio y casos de uso
documento_repository = DocumentoRepositoryImpl()
embeddings_service = EmbeddingsService()
crear_documento_use_case = CrearDocumentoUseCase(documento_repository)
listar_documentos_use_case = ListarDocumentosUseCase(documento_repository)
obtener_documento_use_case = ObtenerDocumentoUseCase(documento_repository)
eliminar_documento_use_case = EliminarDocumentoUseCase(documento_repository)
procesar_documento_use_case = ProcesarDocumentoUseCase(documento_repository, embeddings_service)


@documento_bp.route('/', methods=['POST'])
def crear_documento():
    """Crear un nuevo documento desde archivo PDF"""
    try:
        if 'archivo' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo'}), 400
        
        archivo = request.files['archivo']
        if archivo.filename == '':
            return jsonify({'error': 'No se seleccionó archivo'}), 400
        
        # Validar extensión del archivo (solo PDF)
        file_extension = '.' + archivo.filename.split('.')[-1].lower()
        
        if file_extension != '.pdf':
            return jsonify({'error': 'Solo se permiten archivos PDF'}), 400
        
        # Validar tamaño del archivo (1GB máximo)
        archivo.seek(0, 2)  # Ir al final del archivo
        file_size = archivo.tell()  # Obtener tamaño
        archivo.seek(0)  # Volver al inicio
        
        max_size = 1024 * 1024 * 1024  # 1GB en bytes
        if file_size > max_size:
            return jsonify({'error': f'El archivo no puede ser mayor a 1GB. Tamaño actual: {file_size / (1024*1024*1024):.2f}GB'}), 400
        
        # Leer contenido del archivo PDF
        contenido = _extraer_texto_pdf(archivo)
        if not contenido.strip():
            return jsonify({'error': 'No se pudo extraer texto del archivo PDF'}), 400
        
        # Crear documento
        documento = crear_documento_use_case.ejecutar(
            nombre=secure_filename(archivo.filename),
            contenido=contenido
        )
        
        return jsonify({
            'id': documento.id,
            'nombre': documento.nombre,
            'fecha_creacion': documento.fecha_creacion.isoformat(),
            'fecha_actualizacion': documento.fecha_actualizacion.isoformat(),
            'tiene_embeddings': documento.tiene_embeddings(),
            'procesado': documento.tiene_embeddings(),
            'embeddings_generados': documento.tiene_embeddings(),
            'tamaño': len(documento.contenido.encode('utf-8')) if documento.contenido else 0,
            'mensaje': 'Documento creado exitosamente'
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@documento_bp.route('/', methods=['GET'])
def listar_documentos():
    """Listar todos los documentos"""
    try:
        documentos = listar_documentos_use_case.ejecutar()
        
        return jsonify({
            'documentos': [{
                'id': doc.id,
                'nombre': doc.nombre,
                'fecha_creacion': doc.fecha_creacion.isoformat(),
                'fecha_actualizacion': doc.fecha_actualizacion.isoformat(),
                'tiene_embeddings': doc.tiene_embeddings(),
                'procesado': doc.tiene_embeddings(),  # Un documento está procesado si tiene embeddings
                'embeddings_generados': doc.tiene_embeddings(),  # Alias para consistencia con frontend
                'tamaño': len(doc.contenido.encode('utf-8')) if doc.contenido else 0  # Tamaño en bytes
            } for doc in documentos]
        }), 200
        
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@documento_bp.route('/<int:documento_id>', methods=['GET'])
def obtener_documento(documento_id):
    """Obtener un documento por ID"""
    try:
        documento = obtener_documento_use_case.ejecutar(documento_id)
        
        return jsonify({
            'id': documento.id,
            'nombre': documento.nombre,
            'contenido': documento.contenido,
            'fecha_creacion': documento.fecha_creacion.isoformat(),
            'fecha_actualizacion': documento.fecha_actualizacion.isoformat(),
            'tiene_embeddings': documento.tiene_embeddings()
        }), 200
        
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@documento_bp.route('/<int:documento_id>', methods=['DELETE'])
def eliminar_documento(documento_id):
    """Eliminar un documento"""
    try:
        eliminar_documento_use_case.ejecutar(documento_id)
        
        return jsonify({'mensaje': 'Documento eliminado exitosamente'}), 200
        
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@documento_bp.route('/<int:documento_id>/procesar', methods=['POST'])
def procesar_documento(documento_id):
    """Procesar un documento y generar embeddings"""
    try:
        documento_procesado = procesar_documento_use_case.ejecutar(documento_id)
        
        return jsonify({
            'id': documento_procesado.id,
            'nombre': documento_procesado.nombre,
            'tiene_embeddings': documento_procesado.tiene_embeddings(),
            'procesado': documento_procesado.tiene_embeddings(),
            'embeddings_generados': documento_procesado.tiene_embeddings(),
            'tamaño': len(documento_procesado.contenido.encode('utf-8')) if documento_procesado.contenido else 0,
            'fecha_actualizacion': documento_procesado.fecha_actualizacion.isoformat(),
            'mensaje': 'Documento procesado exitosamente'
        }), 200
        
    except NotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


@documento_bp.route('/procesar-todos', methods=['POST'])
def procesar_todos_documentos():
    """Procesar todos los documentos que no tienen embeddings"""
    try:
        documentos_procesados = procesar_documento_use_case.procesar_todos_los_documentos()
        
        return jsonify({
            'documentos_procesados': len(documentos_procesados),
            'mensaje': f'Se procesaron {len(documentos_procesados)} documentos exitosamente'
        }), 200
        
    except ProcessingError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500


def _extraer_texto_pdf(archivo):
    """Extraer texto de un archivo PDF"""
    try:
        # Leer el archivo en memoria
        archivo_bytes = archivo.read()
        archivo.seek(0)  # Resetear posición del archivo
        
        # Crear objeto PDF
        pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_bytes))
        
        # Extraer texto de todas las páginas
        texto_completo = ""
        for pagina in pdf_reader.pages:
            texto_completo += pagina.extract_text() + "\n"
        
        return texto_completo.strip()
        
    except Exception as e:
        raise ProcessingError(f"Error al extraer texto del PDF: {str(e)}")


