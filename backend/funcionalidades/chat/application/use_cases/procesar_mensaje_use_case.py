"""
Caso de uso para procesar mensajes del chat
"""
from typing import List, Optional
from funcionalidades.chat.domain.entities.mensaje_entity import MensajeEntity
from funcionalidades.chat.domain.repositories.mensaje_repository import MensajeRepository
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.infraestructura.openai_service import OpenAIService
from funcionalidades.core.infraestructura.embeddings_service import EmbeddingsService
from funcionalidades.core.exceptions.domain_exceptions import ValidationError, ProcessingError, NotFoundError, OpenAIError


class ProcesarMensajeUseCase:
    """Caso de uso para procesar mensajes del chat"""
    
    def __init__(self, mensaje_repository: MensajeRepository, documento_repository: DocumentoRepository, 
                 openai_service: OpenAIService, embeddings_service: EmbeddingsService):
        self.mensaje_repository = mensaje_repository
        self.documento_repository = documento_repository
        self.openai_service = openai_service
        self.embeddings_service = embeddings_service
    
    def ejecutar(self, contenido_mensaje: str, documento_id: int = None) -> MensajeEntity:
        """
        Ejecutar el caso de uso para procesar un mensaje
        
        Args:
            contenido_mensaje: Contenido del mensaje del usuario
            
        Returns:
            MensajeEntity: Respuesta del bot
            
        Raises:
            ValidationError: Si el mensaje es inválido
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            # Validar mensaje
            if not contenido_mensaje or not contenido_mensaje.strip():
                raise ValidationError("El mensaje no puede estar vacío")
            
            # Guardar mensaje del usuario
            mensaje_usuario = MensajeEntity(
                id=None,
                contenido=contenido_mensaje.strip(),
                es_usuario=True,
                fecha_creacion=None,
                documento_id=documento_id
            )
            mensaje_usuario_guardado = self.mensaje_repository.agregar(mensaje_usuario)
            
            # Procesar mensaje y generar respuesta
            respuesta = self._generar_respuesta(contenido_mensaje.strip(), documento_id)
            
            # Guardar respuesta del bot
            mensaje_bot = MensajeEntity(
                id=None,
                contenido=respuesta,
                es_usuario=False,
                fecha_creacion=None,
                documento_id=documento_id
            )
            mensaje_bot_guardado = self.mensaje_repository.agregar(mensaje_bot)
            
            return mensaje_bot_guardado
            
        except ValidationError:
            raise
        except Exception as e:
            raise ProcessingError(f"Error al procesar mensaje: {str(e)}")
    
    def _es_pregunta_general(self, mensaje: str) -> bool:
        """Detectar si es una pregunta general sobre el documento"""
        mensaje_lower = mensaje.lower().strip()
        
        # Palabras clave que indican preguntas generales
        palabras_generales = [
            'de qué trata',
            'de que trata',
            'qué es',
            'que es',
            'resumen',
            'resumir',
            'explica',
            'explicar',
            'describe',
            'describir',
            'cuéntame',
            'cuentame',
            'habla sobre',
            'habla de',
            'información general',
            'informacion general',
            'tema principal',
            'temas principales',
            'contenido',
            'sobre qué',
            'sobre que'
        ]
        
        # Verificar si el mensaje contiene alguna de estas palabras clave
        for palabra in palabras_generales:
            if palabra in mensaje_lower:
                return True
        
        # Verificar si es una pregunta muy corta (probablemente general)
        if len(mensaje.split()) <= 3 and ('?' in mensaje or '¿' in mensaje):
            return True
            
        return False
    
    def _generar_respuesta(self, mensaje: str, documento_id: int = None) -> str:
        """
        Generar respuesta basada en RAG
        
        Args:
            mensaje: Mensaje del usuario
            
        Returns:
            str: Respuesta generada
        """
        try:
            # Si se especifica un documento, usarlo; sino usar todos
            if documento_id:
                documento = self.documento_repository.get_by_id(documento_id)
                if not documento:
                    return "El documento seleccionado no existe."
                
                if not documento.tiene_embeddings():
                    return "El documento seleccionado no ha sido procesado aún. Por favor, procesa el documento primero."
                
                documentos = [documento]
            else:
                # Obtener documentos disponibles
                documentos = self.documento_repository.listar()
                
                if not documentos:
                    return "No hay documentos cargados en el sistema. Por favor, carga un documento PDF primero."
                
                # Verificar si hay documentos con embeddings
                documentos_con_embeddings = [doc for doc in documentos if doc.tiene_embeddings()]
                
                if not documentos_con_embeddings:
                    return "Los documentos cargados no han sido procesados aún. Por favor, espera a que se procesen los embeddings."
                
                documentos = documentos_con_embeddings
            
            # Detectar si es una pregunta general sobre el documento
            es_pregunta_general = self._es_pregunta_general(mensaje)
            
            if es_pregunta_general and documento_id:
                # Para preguntas generales, usar todo el contenido del documento
                print(f"Pregunta general detectada, usando todo el contenido del documento ID: {documento_id}")
                documento_completo = self.documento_repository.get_by_id(documento_id)
                if documento_completo and documento_completo.contenido:
                    contexto = documento_completo.contenido
                    respuesta = self.openai_service.generar_respuesta(mensaje, contexto)
                    return respuesta
                else:
                    return "No poseo información sobre ese tema en el documento cargado."
            
            # Generar embedding del mensaje del usuario
            query_embedding = self.embeddings_service.generar_embedding(mensaje)
            
            # Buscar documentos similares
            if documento_id:
                # Si se especifica un documento, buscar solo en ese documento
                print(f"Buscando solo en documento ID: {documento_id}")
                documentos_similares = self.documento_repository.buscar_por_similitud_en_documento(query_embedding, documento_id, limite=3)
            else:
                # Si no se especifica documento, buscar en todos
                print("Buscando en todos los documentos")
                documentos_similares = self.documento_repository.buscar_por_similitud(query_embedding, limite=3)
            
            if not documentos_similares:
                # Si no se encuentran fragmentos similares, usar todo el contenido del documento
                if documento_id:
                    print(f"No se encontraron fragmentos similares, usando todo el contenido del documento ID: {documento_id}")
                    documento_completo = self.documento_repository.get_by_id(documento_id)
                    if documento_completo and documento_completo.contenido:
                        contexto = documento_completo.contenido
                    else:
                        return "No poseo información sobre ese tema en el documento cargado."
                else:
                    return "No poseo información sobre ese tema en el documento cargado."
            else:
                # Construir contexto con documentos similares
                contexto = "\n\n".join([doc.contenido for doc in documentos_similares])
            
            # Generar respuesta usando OpenAI
            respuesta = self.openai_service.generar_respuesta(mensaje, contexto)
            
            return respuesta
            
        except OpenAIError as e:
            return f"Error al comunicarse con OpenAI: {str(e)}"
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"
