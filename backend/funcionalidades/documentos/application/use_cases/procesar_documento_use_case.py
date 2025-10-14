"""
Caso de uso para procesar documento y generar embeddings
"""
from typing import List
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.infraestructura.embeddings_service import EmbeddingsService
from funcionalidades.core.exceptions.domain_exceptions import NotFoundError, ProcessingError


class ProcesarDocumentoUseCase:
    """Caso de uso para procesar documento y generar embeddings"""
    
    def __init__(self, documento_repository: DocumentoRepository, embeddings_service: EmbeddingsService):
        self.documento_repository = documento_repository
        self.embeddings_service = embeddings_service
    
    def ejecutar(self, documento_id: int) -> DocumentoEntity:
        """
        Ejecutar el caso de uso para procesar un documento
        
        Args:
            documento_id: ID del documento a procesar
            
        Returns:
            DocumentoEntity: Documento procesado con embeddings
            
        Raises:
            NotFoundError: Si el documento no existe
            ProcessingError: Si hay error en el procesamiento
            OpenAIError: Si hay error con OpenAI
        """
        try:
            # Obtener documento
            documento = self.documento_repository.get_by_id(documento_id)
            if not documento:
                raise NotFoundError(f"Documento con ID {documento_id} no encontrado")
            
            # Verificar si ya tiene embeddings
            if documento.tiene_embeddings():
                return documento
            
            # Generar embedding del contenido
            embedding = self.embeddings_service.generar_embedding(documento.contenido)
            
            # Actualizar documento con embeddings
            documento.actualizar_embeddings(embedding)
            
            # Guardar en repositorio
            documento_actualizado = self.documento_repository.modificar(documento)
            
            return documento_actualizado
            
        except NotFoundError:
            raise
        except Exception as e:
            raise ProcessingError(f"Error al procesar documento: {str(e)}")
    
    def procesar_todos_los_documentos(self) -> List[DocumentoEntity]:
        """
        Procesar todos los documentos que no tienen embeddings
        
        Returns:
            List[DocumentoEntity]: Lista de documentos procesados
            
        Raises:
            ProcessingError: Si hay error en el procesamiento
            OpenAIError: Si hay error con OpenAI
        """
        try:
            documentos = self.documento_repository.listar()
            documentos_sin_embeddings = [doc for doc in documentos if not doc.tiene_embeddings()]
            
            documentos_procesados = []
            for documento in documentos_sin_embeddings:
                try:
                    documento_procesado = self.ejecutar(documento.id)
                    documentos_procesados.append(documento_procesado)
                except Exception as e:
                    # Continuar con otros documentos si uno falla
                    print(f"Error procesando documento {documento.id}: {str(e)}")
                    continue
            
            return documentos_procesados
            
        except Exception as e:
            raise ProcessingError(f"Error al procesar documentos: {str(e)}")
