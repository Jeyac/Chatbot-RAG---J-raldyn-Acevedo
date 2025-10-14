"""
Interfaz del repositorio de documentos
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity


class DocumentoRepository(ABC):
    """Interfaz abstracta para el repositorio de documentos"""
    
    @abstractmethod
    def agregar(self, documento: DocumentoEntity) -> DocumentoEntity:
        """Agregar un nuevo documento"""
        pass
    
    @abstractmethod
    def listar(self) -> List[DocumentoEntity]:
        """Listar todos los documentos"""
        pass
    
    @abstractmethod
    def get_by_id(self, documento_id: int) -> Optional[DocumentoEntity]:
        """Obtener un documento por ID"""
        pass
    
    @abstractmethod
    def modificar(self, documento: DocumentoEntity) -> DocumentoEntity:
        """Modificar un documento existente"""
        pass
    
    @abstractmethod
    def eliminar(self, documento_id: int) -> bool:
        """Eliminar un documento"""
        pass
    
    @abstractmethod
    def buscar_por_similitud(self, query_embedding: List[float], limite: int = 5) -> List[DocumentoEntity]:
        """Buscar documentos por similitud de embeddings"""
        pass
    
    @abstractmethod
    def buscar_por_similitud_en_documento(self, query_embedding: List[float], documento_id: int, limite: int = 5) -> List[DocumentoEntity]:
        """Buscar por similitud solo en un documento específico"""
        pass