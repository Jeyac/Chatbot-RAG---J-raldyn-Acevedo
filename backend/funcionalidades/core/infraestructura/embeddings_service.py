"""
Servicio de embeddings alternativo usando sentence-transformers
Reemplaza LangChain para evitar problemas de compatibilidad
"""
import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from funcionalidades.core.exceptions.domain_exceptions import ProcessingError


class EmbeddingsService:
    """Servicio para generar y comparar embeddings usando sentence-transformers"""
    
    def __init__(self):
        try:
            # Usar un modelo más ligero y compatible
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.model_loaded = True
        except Exception as e:
            self.model = None
            self.model_loaded = False
            print(f"Warning: No se pudo cargar el modelo de embeddings: {e}")
    
    def generar_embedding(self, texto: str) -> List[float]:
        """
        Generar embedding para un texto
        
        Args:
            texto: Texto para generar embedding
            
        Returns:
            List[float]: Vector de embedding
            
        Raises:
            ProcessingError: Si hay error en el procesamiento
        """
        try:
            if not self.model_loaded:
                raise ProcessingError("Modelo de embeddings no está cargado")
            
            if not texto or not texto.strip():
                raise ProcessingError("El texto no puede estar vacío")
            
            # Limpiar y truncar texto si es muy largo
            texto_limpio = texto.strip()[:1000]  # Limitar a 1000 caracteres
            
            # Generar embedding
            embedding = self.model.encode(texto_limpio)
            
            return embedding.tolist()
            
        except Exception as e:
            raise ProcessingError(f"Error al generar embedding: {str(e)}")
    
    def calcular_similitud(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calcular similitud coseno entre dos embeddings
        
        Args:
            embedding1: Primer embedding
            embedding2: Segundo embedding
            
        Returns:
            float: Similitud coseno (0-1)
        """
        try:
            # Validar que los embeddings no estén vacíos
            if not embedding1 or not embedding2:
                raise ProcessingError("Los embeddings no pueden estar vacíos")
            
            if len(embedding1) == 0 or len(embedding2) == 0:
                raise ProcessingError("Los embeddings no pueden tener longitud 0")
            
            # Convertir a arrays numpy
            emb1 = np.array(embedding1).reshape(1, -1)
            emb2 = np.array(embedding2).reshape(1, -1)
            
            # Verificar que las dimensiones sean compatibles
            if emb1.shape[1] != emb2.shape[1]:
                raise ProcessingError(f"Dimensiones incompatibles: {emb1.shape[1]} vs {emb2.shape[1]}")
            
            # Calcular similitud coseno
            similitud = cosine_similarity(emb1, emb2)[0][0]
            
            return float(similitud)
            
        except Exception as e:
            raise ProcessingError(f"Error al calcular similitud: {str(e)}")
    
    def buscar_similares(self, query_embedding: List[float], documentos_embeddings: List[List[float]], 
                        limite: int = 5, umbral: float = 0.3) -> List[int]:
        """
        Buscar documentos similares a una consulta
        
        Args:
            query_embedding: Embedding de la consulta
            documentos_embeddings: Lista de embeddings de documentos
            limite: Número máximo de resultados
            umbral: Umbral mínimo de similitud
            
        Returns:
            List[int]: Índices de documentos similares
        """
        try:
            if not documentos_embeddings:
                return []
            
            if not query_embedding or len(query_embedding) == 0:
                return []
            
            similitudes = []
            
            for i, doc_embedding in enumerate(documentos_embeddings):
                # Verificar que el embedding del documento sea válido
                if not doc_embedding or len(doc_embedding) == 0:
                    continue
                
                try:
                    similitud = self.calcular_similitud(query_embedding, doc_embedding)
                    if similitud >= umbral:
                        similitudes.append((i, similitud))
                except Exception as e:
                    # Si hay error con un embedding específico, continuar con los demás
                    print(f"Error calculando similitud para documento {i}: {str(e)}")
                    continue
            
            # Ordenar por similitud descendente
            similitudes.sort(key=lambda x: x[1], reverse=True)
            
            # Retornar índices de los más similares
            return [idx for idx, _ in similitudes[:limite]]
            
        except Exception as e:
            raise ProcessingError(f"Error en búsqueda de similares: {str(e)}")
    
    def esta_disponible(self) -> bool:
        """Verificar si el servicio está disponible"""
        return self.model_loaded
