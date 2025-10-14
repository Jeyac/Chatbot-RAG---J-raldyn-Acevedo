"""
Caso de uso para obtener historial de mensajes
"""
from typing import List
from funcionalidades.chat.domain.entities.mensaje_entity import MensajeEntity
from funcionalidades.chat.domain.repositories.mensaje_repository import MensajeRepository
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class ObtenerHistorialUseCase:
    """Caso de uso para obtener historial de mensajes"""
    
    def __init__(self, mensaje_repository: MensajeRepository):
        self.mensaje_repository = mensaje_repository
    
    def ejecutar(self, limite: int = 50) -> List[MensajeEntity]:
        """
        Ejecutar el caso de uso para obtener historial
        
        Args:
            limite: Número máximo de mensajes a obtener
            
        Returns:
            List[MensajeEntity]: Lista de mensajes del historial
            
        Raises:
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            mensajes = self.mensaje_repository.listar_ultimos(limite)
            return mensajes
            
        except Exception as e:
            raise ProcessingError(f"Error al obtener historial: {str(e)}")
