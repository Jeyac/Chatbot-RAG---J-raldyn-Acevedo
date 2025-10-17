"""
Implementación del repositorio de documentos
"""
from typing import List, Optional
import numpy as np
from funcionalidades.documentos.domain.entities.documento_entity import DocumentoEntity
from funcionalidades.documentos.domain.repositories.documento_repository import DocumentoRepository
from funcionalidades.documentos.infrastructure.documento_model import DocumentoModel
from funcionalidades.core.infraestructura.database import db
from funcionalidades.core.infraestructura.embeddings_service import EmbeddingsService
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class DocumentoRepositoryImpl(DocumentoRepository):
    """Implementación del repositorio de documentos"""
    
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
        self.documentos_embeddings = []  # Lista de embeddings de documentos
    
    def _crear_entidad_desde_modelo(self, modelo: DocumentoModel) -> DocumentoEntity:
        """Convertir modelo de base de datos a entidad del dominio"""
        return DocumentoEntity(
            id=modelo.id,
            nombre=modelo.nombre,
            contenido=modelo.contenido,
            embeddings=modelo.embeddings,
            fecha_creacion=modelo.fecha_creacion,
            fecha_actualizacion=modelo.fecha_actualizacion
        )
    
    def _crear_modelo_desde_entidad(self, entidad: DocumentoEntity) -> DocumentoModel:
        """Convertir entidad del dominio a modelo de base de datos"""
        return DocumentoModel(
            id=entidad.id,
            nombre=entidad.nombre,
            contenido=entidad.contenido,
            embeddings=entidad.embeddings,
            fecha_creacion=entidad.fecha_creacion,
            fecha_actualizacion=entidad.fecha_actualizacion
        )
    
    def agregar(self, documento: DocumentoEntity) -> DocumentoEntity:
        """Agregar un nuevo documento"""
        try:
            modelo = self._crear_modelo_desde_entidad(documento)
            db.session.add(modelo)
            db.session.commit()
            
            return self._crear_entidad_desde_modelo(modelo)
            
        except Exception as e:
            db.session.rollback()
            raise ProcessingError(f"Error al agregar documento: {str(e)}")
    
    def listar(self) -> List[DocumentoEntity]:
        """Listar todos los documentos"""
        try:
            modelos = DocumentoModel.query.all()
            return [self._crear_entidad_desde_modelo(modelo) for modelo in modelos]
            
        except Exception as e:
            raise ProcessingError(f"Error al listar documentos: {str(e)}")
    
    def get_by_id(self, documento_id: int) -> Optional[DocumentoEntity]:
        """Obtener un documento por ID"""
        try:
            modelo = DocumentoModel.query.get(documento_id)
            if modelo:
                return self._crear_entidad_desde_modelo(modelo)
            return None
            
        except Exception as e:
            raise ProcessingError(f"Error al obtener documento: {str(e)}")
    
    def modificar(self, documento: DocumentoEntity) -> DocumentoEntity:
        """Modificar un documento existente"""
        try:
            modelo = DocumentoModel.query.get(documento.id)
            if not modelo:
                raise ProcessingError(f"Documento con ID {documento.id} no encontrado")
            
            modelo.nombre = documento.nombre
            modelo.contenido = documento.contenido
            modelo.embeddings = documento.embeddings
            modelo.fecha_actualizacion = documento.fecha_actualizacion
            
            db.session.commit()
            
            return self._crear_entidad_desde_modelo(modelo)
            
        except Exception as e:
            db.session.rollback()
            raise ProcessingError(f"Error al modificar documento: {str(e)}")
    
    def eliminar(self, documento_id: int) -> bool:
        """Eliminar un documento"""
        try:
            modelo = DocumentoModel.query.get(documento_id)
            if not modelo:
                return False
            
            # Eliminar mensajes asociados al documento primero
            from funcionalidades.chat.infrastructure.mensaje_model import MensajeModel
            MensajeModel.query.filter(MensajeModel.documento_id == documento_id).delete()
            
            # Eliminar el documento
            db.session.delete(modelo)
            db.session.commit()
            
            return True
            
        except Exception as e:
            db.session.rollback()
            raise ProcessingError(f"Error al eliminar documento: {str(e)}")
    
    def buscar_por_similitud(self, query_embedding: List[float], limite: int = 5) -> List[DocumentoEntity]:
        """Buscar documentos por similitud de embeddings"""
        try:
            # Obtener todos los documentos con embeddings válidos
            modelos = DocumentoModel.query.filter(
                DocumentoModel.embeddings.isnot(None)
            ).all()
            
            if not modelos:
                return []
            
            # Filtrar solo documentos con embeddings válidos
            modelos_con_embeddings = []
            for modelo in modelos:
                if modelo.embeddings and len(modelo.embeddings) > 0:
                    modelos_con_embeddings.append(modelo)
            
            if not modelos_con_embeddings:
                return []
            
            # Reconstruir lista de embeddings
            self._reconstruir_embeddings(modelos_con_embeddings)
            
            # Verificar que tenemos embeddings válidos
            if not self.documentos_embeddings:
                return []
            
            # Buscar documentos similares usando el servicio de embeddings
            indices_similares = self.embeddings_service.buscar_similares(
                query_embedding, 
                self.documentos_embeddings, 
                limite=limite
            )
            
            # Obtener documentos correspondientes
            documentos_similares = []
            for idx in indices_similares:
                if idx < len(modelos_con_embeddings):
                    documento = self._crear_entidad_desde_modelo(modelos_con_embeddings[idx])
                    documentos_similares.append(documento)
            
            return documentos_similares
            
        except Exception as e:
            raise ProcessingError(f"Error en búsqueda por similitud: {str(e)}")
    
    def buscar_por_similitud_en_documento(self, query_embedding: List[float], documento_id: int, limite: int = 5) -> List[DocumentoEntity]:
        """Buscar por similitud solo en un documento específico"""
        try:
            print(f"🔍 Buscando en documento específico ID: {documento_id}")
            
            # Obtener solo el documento específico
            modelo = DocumentoModel.query.filter(
                DocumentoModel.id == documento_id,
                DocumentoModel.embeddings.isnot(None)
            ).first()
            
            if not modelo:
                print(f"Documento ID {documento_id} no encontrado o sin embeddings")
                return []
            
            # Verificar que tiene embeddings válidos
            if not modelo.embeddings or len(modelo.embeddings) == 0:
                print(f"Documento ID {documento_id} no tiene embeddings válidos")
                return []
            
            print(f"Documento ID {documento_id} encontrado: {modelo.nombre}")
            
            # Crear lista con solo este documento
            modelos_con_embeddings = [modelo]
            
            # Reconstruir lista de embeddings con solo este documento
            self._reconstruir_embeddings(modelos_con_embeddings)
            
            # Verificar que tenemos embeddings válidos
            if not self.documentos_embeddings:
                print(f"No se pudieron reconstruir embeddings para documento ID {documento_id}")
                return []
            
            # Buscar documentos similares usando el servicio de embeddings
            # Usar umbral más bajo para preguntas generales
            indices_similares = self.embeddings_service.buscar_similares(
                query_embedding, 
                self.documentos_embeddings, 
                limite=limite,
                umbral=0.1  # Umbral más bajo para capturar más contenido
            )
            
            print(f"Encontrados {len(indices_similares)} fragmentos similares en documento ID {documento_id}")
            
            # Obtener documentos correspondientes (solo el documento seleccionado)
            documentos_similares = []
            for idx in indices_similares:
                if idx < len(modelos_con_embeddings):
                    documento = self._crear_entidad_desde_modelo(modelos_con_embeddings[idx])
                    documentos_similares.append(documento)
            
            return documentos_similares
            
        except Exception as e:
            raise ProcessingError(f"Error en búsqueda por similitud en documento: {str(e)}")
    
    def _reconstruir_embeddings(self, modelos: List[DocumentoModel]):
        """Reconstruir la lista de embeddings"""
        try:
            self.documentos_embeddings = []
            
            for modelo in modelos:
                if modelo.embeddings and len(modelo.embeddings) > 0:
                    self.documentos_embeddings.append(modelo.embeddings)
                # No agregar nada si no tiene embeddings válidos
            
        except Exception as e:
            raise ProcessingError(f"Error al reconstruir embeddings: {str(e)}")
