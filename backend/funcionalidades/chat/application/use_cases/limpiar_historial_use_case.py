"""
Caso de uso para limpiar historial de mensajes
"""
from funcionalidades.chat.domain.repositories.mensaje_repository import MensajeRepository
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class LimpiarHistorialUseCase:
    """Caso de uso para limpiar historial de mensajes"""
    
    def __init__(self, mensaje_repository: MensajeRepository):
        self.mensaje_repository = mensaje_repository
    
    def ejecutar(self) -> bool:
        """
        Ejecutar el caso de uso para limpiar historial
        
        Returns:
            bool: True si se limpió correctamente
            
        Raises:
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            resultado = self.mensaje_repository.limpiar_historial()
            return resultado
            
        except Exception as e:
            raise ProcessingError(f"Error al limpiar historial: {str(e)}")
