"""
Entidad Documento del dominio
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from funcionalidades.core.exceptions.domain_exceptions import ValidationError
from funcionalidades.core.infraestructura.datetime_utils import get_local_now_naive


@dataclass
class DocumentoEntity:
    """Entidad que representa un documento"""
    
    id: Optional[int]
    nombre: str
    contenido: str
    embeddings: Optional[List[float]]
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.nombre or not self.nombre.strip():
            raise ValidationError("El nombre del documento es obligatorio")
        
        if not self.contenido or not self.contenido.strip():
            raise ValidationError("El contenido del documento es obligatorio")
        
        if len(self.nombre) > 255:
            raise ValidationError("El nombre del documento no puede exceder 255 caracteres")
        
        if len(self.contenido) > 1000000:  # 1MB de texto
            raise ValidationError("El contenido del documento es demasiado grande")
        
        # Limpiar datos
        self.nombre = self.nombre.strip()
        self.contenido = self.contenido.strip()
    
    def actualizar_contenido(self, nuevo_contenido: str):
        """Actualizar el contenido del documento"""
        if not nuevo_contenido or not nuevo_contenido.strip():
            raise ValidationError("El contenido del documento es obligatorio")
        
        if len(nuevo_contenido) > 1000000:
            raise ValidationError("El contenido del documento es demasiado grande")
        
        self.contenido = nuevo_contenido.strip()
        self.fecha_actualizacion = get_local_now_naive()
    
    def actualizar_embeddings(self, embeddings: List[float]):
        """Actualizar los embeddings del documento"""
        if not embeddings:
            raise ValidationError("Los embeddings no pueden estar vacíos")
        
        self.embeddings = embeddings
        self.fecha_actualizacion = get_local_now_naive()
    
    def tiene_embeddings(self) -> bool:
        """Verificar si el documento tiene embeddings"""
        return self.embeddings is not None and len(self.embeddings) > 0
