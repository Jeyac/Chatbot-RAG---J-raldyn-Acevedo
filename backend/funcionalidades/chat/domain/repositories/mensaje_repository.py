"""
Interfaz del repositorio de mensajes
"""
from abc import ABC, abstractmethod
from typing import List
from funcionalidades.chat.domain.entities.mensaje_entity import MensajeEntity


class MensajeRepository(ABC):
    """Interfaz abstracta para el repositorio de mensajes"""
    
    @abstractmethod
    def agregar(self, mensaje: MensajeEntity) -> MensajeEntity:
        """Agregar un nuevo mensaje"""
        pass
    
    @abstractmethod
    def listar_ultimos(self, limite: int = 50) -> List[MensajeEntity]:
        """Listar los últimos mensajes"""
        pass
    
    @abstractmethod
    def listar_por_documento(self, documento_id: int, limite: int = 50) -> List[MensajeEntity]:
        """Listar mensajes de un documento específico"""
        pass
    
    @abstractmethod
    def limpiar_historial(self) -> bool:
        """Limpiar el historial de mensajes"""
        pass
