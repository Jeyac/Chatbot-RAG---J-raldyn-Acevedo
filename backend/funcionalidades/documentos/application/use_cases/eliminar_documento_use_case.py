"""
Caso de uso para eliminar un documento
"""
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.exceptions.domain_exceptions import NotFoundError, ProcessingError


class EliminarDocumentoUseCase:
    """Caso de uso para eliminar un documento"""
    
    def __init__(self, documento_repository: DocumentoRepository):
        self.documento_repository = documento_repository
    
    def ejecutar(self, documento_id: int) -> bool:
        """
        Ejecutar el caso de uso para eliminar un documento
        
        Args:
            documento_id: ID del documento a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            NotFoundError: Si el documento no existe
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            # Verificar que el documento existe
            documento = self.documento_repository.get_by_id(documento_id)
            if not documento:
                raise NotFoundError(f"Documento con ID {documento_id} no encontrado")
            
            # Eliminar el documento
            resultado = self.documento_repository.eliminar(documento_id)
            
            if not resultado:
                raise ProcessingError(f"No se pudo eliminar el documento con ID {documento_id}")
            
            return True
            
        except NotFoundError:
            raise
        except Exception as e:
            raise ProcessingError(f"Error al eliminar el documento: {str(e)}")
