"""
Caso de uso para listar documentos
"""
from typing import List
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class ListarDocumentosUseCase:
    """Caso de uso para listar documentos"""
    
    def __init__(self, documento_repository: DocumentoRepository):
        self.documento_repository = documento_repository
    
    def ejecutar(self) -> List[DocumentoEntity]:
        """
        Ejecutar el caso de uso para listar documentos
        
        Returns:
            List[DocumentoEntity]: Lista de documentos
            
        Raises:
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            documentos = self.documento_repository.listar()
            return documentos
            
        except Exception as e:
            raise ProcessingError(f"Error al listar documentos: {str(e)}")
