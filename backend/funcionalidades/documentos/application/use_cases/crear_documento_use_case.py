"""
Caso de uso para crear un documento
"""
from typing import Optional
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.core.exceptions.domain_exceptions import ValidationError, ProcessingError


class CrearDocumentoUseCase:
    """Caso de uso para crear un documento"""
    
    def __init__(self, documento_repository: DocumentoRepository):
        self.documento_repository = documento_repository
    
    def ejecutar(self, nombre: str, contenido: str) -> DocumentoEntity:
        """
        Ejecutar el caso de uso para crear un documento
        
        Args:
            nombre: Nombre del documento
            contenido: Contenido del documento
            
        Returns:
            DocumentoEntity: Documento creado
            
        Raises:
            ValidationError: Si los datos son inválidos
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            # Crear la entidad
            documento = DocumentoEntity(
                id=None,
                nombre=nombre,
                contenido=contenido,
                embeddings=None,
                fecha_creacion=None,
                fecha_actualizacion=None
            )
            
            # Guardar en el repositorio
            documento_creado = self.documento_repository.agregar(documento)
            
            return documento_creado
            
        except ValidationError:
            raise
        except Exception as e:
            raise ProcessingError(f"Error al crear el documento: {str(e)}")
