"""
Entidad Mensaje del dominio
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from funcionalidades.core.exceptions.domain_exceptions import ValidationError


@dataclass
class MensajeEntity:
    """Entidad que representa un mensaje del chat"""
    
    id: Optional[int]
    contenido: str
    es_usuario: bool
    fecha_creacion: datetime
    documento_id: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if not self.contenido or not self.contenido.strip():
            raise ValidationError("El contenido del mensaje es obligatorio")
        
        if len(self.contenido) > 10000:  # 10KB de texto
            raise ValidationError("El contenido del mensaje es demasiado largo")
        
        # Limpiar datos
        self.contenido = self.contenido.strip()
    
    def es_mensaje_usuario(self) -> bool:
        """Verificar si es un mensaje del usuario"""
        return self.es_usuario
    
    def es_mensaje_bot(self) -> bool:
        """Verificar si es un mensaje del bot"""
        return not self.es_usuario
