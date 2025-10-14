"""
Implementación del repositorio de mensajes
"""
from typing import List
from funcionalidades.chat.domain.entities.mensaje_entity import MensajeEntity
from funcionalidades.chat.domain.repositories.mensaje_repository import MensajeRepository
from funcionalidades.chat.infrastructure.mensaje_model import MensajeModel
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class MensajeRepositoryImpl(MensajeRepository):
    """Implementación del repositorio de mensajes"""
    
    def _crear_entidad_desde_modelo(self, modelo: MensajeModel) -> MensajeEntity:
        """Convertir modelo de base de datos a entidad del dominio"""
        return MensajeEntity(
            id=modelo.id,
            contenido=modelo.contenido,
            es_usuario=modelo.es_usuario,
            fecha_creacion=modelo.fecha_creacion,
            documento_id=modelo.documento_id
        )
    
    def _crear_modelo_desde_entidad(self, entidad: MensajeEntity) -> MensajeModel:
        """Convertir entidad del dominio a modelo de base de datos"""
        return MensajeModel(
            id=entidad.id,
            contenido=entidad.contenido,
            es_usuario=entidad.es_usuario,
            fecha_creacion=entidad.fecha_creacion,
            documento_id=entidad.documento_id
        )
    
    def agregar(self, mensaje: MensajeEntity) -> MensajeEntity:
        """Agregar un nuevo mensaje"""
        try:
            modelo = self._crear_modelo_desde_entidad(mensaje)
            db.session.add(modelo)
            db.session.commit()
            
            return self._crear_entidad_desde_modelo(modelo)
            
        except Exception as e:
            db.session.rollback()
            raise ProcessingError(f"Error al agregar mensaje: {str(e)}")
    
    def listar_ultimos(self, limite: int = 50) -> List[MensajeEntity]:
        """Listar los últimos mensajes"""
        try:
            modelos = MensajeModel.query.order_by(MensajeModel.fecha_creacion.desc()).limit(limite).all()
            return [self._crear_entidad_desde_modelo(modelo) for modelo in reversed(modelos)]
            
        except Exception as e:
            raise ProcessingError(f"Error al listar mensajes: {str(e)}")
    
    def listar_por_documento(self, documento_id: int, limite: int = 50) -> List[MensajeEntity]:
        """Listar mensajes de un documento específico"""
        try:
            modelos = MensajeModel.query.filter(
                MensajeModel.documento_id == documento_id
            ).order_by(MensajeModel.fecha_creacion.asc()).limit(limite).all()
            
            return [self._crear_entidad_desde_modelo(modelo) for modelo in modelos]
            
        except Exception as e:
            raise ProcessingError(f"Error al listar mensajes del documento: {str(e)}")
    
    def limpiar_historial(self) -> bool:
        """Limpiar el historial de mensajes"""
        try:
            MensajeModel.query.delete()
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise ProcessingError(f"Error al limpiar historial: {str(e)}")
