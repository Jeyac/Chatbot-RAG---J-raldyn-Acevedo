"""
Caso de uso para obtener un documento por ID
"""
from typing import Optional
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.exceptions.domain_exceptions import NotFoundError, ProcessingError


class ObtenerDocumentoUseCase:
    """Caso de uso para obtener un documento por ID"""
    
    def __init__(self, documento_repository: DocumentoRepository):
        self.documento_repository = documento_repository
    
    def ejecutar(self, documento_id: int) -> DocumentoEntity:
        """
        Ejecutar el caso de uso para obtener un documento
        
        Args:
            documento_id: ID del documento
            
        Returns:
            DocumentoEntity: Documento encontrado
            
        Raises:
            NotFoundError: Si el documento no existe
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            documento = self.documento_repository.get_by_id(documento_id)
            
            if not documento:
                raise NotFoundError(f"Documento con ID {documento_id} no encontrado")
            
            return documento
            
        except NotFoundError:
            raise
        except Exception as e:
            raise ProcessingError(f"Error al obtener el documento: {str(e)}")
