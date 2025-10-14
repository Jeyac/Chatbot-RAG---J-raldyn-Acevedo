"""
Servicio para integración con OpenAI API
"""
import openai
from typing import List, Optional
from funcionalidades.core.infraestructura.config import Config
from funcionalidades.core.exceptions.domain_exceptions import OpenAIError


class OpenAIService:
    """Servicio para comunicación con OpenAI API"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            raise OpenAIError("OPENAI_API_KEY no está configurada")
        
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generar_embedding(self, texto: str) -> List[float]:
        """
        Generar embedding para un texto
        
        Args:
            texto: Texto para generar embedding
            
        Returns:
            List[float]: Vector de embedding
            
        Raises:
            OpenAIError: Si hay error en la API
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=texto
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            raise OpenAIError(f"Error al generar embedding: {str(e)}")
    
    def generar_respuesta(self, mensaje: str, contexto: str) -> str:
        """
        Generar respuesta usando GPT con contexto RAG
        
        Args:
            mensaje: Mensaje del usuario
            contexto: Contexto extraído de documentos
            
        Returns:
            str: Respuesta generada
            
        Raises:
            OpenAIError: Si hay error en la API
        """
        try:
            prompt = f"""
            Basándote únicamente en el siguiente contexto extraído de documentos:
            
            CONTEXTO:
            {contexto}
            
            Responde la siguiente pregunta del usuario de manera clara y concisa. 
            
            Si la pregunta es general (como "de qué trata", "resumen", "explica"), proporciona una respuesta comprehensiva basada en todo el contexto.
            Si la pregunta es específica, busca la información exacta en el contexto.
            
            Si la información no se encuentra en el contexto proporcionado, responde exactamente: "No poseo información sobre ese tema en el documento cargado."
            
            PREGUNTA: {mensaje}
            
            RESPUESTA:
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente que responde preguntas basándose únicamente en el contexto proporcionado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise OpenAIError(f"Error al generar respuesta: {str(e)}")
    
    def verificar_conexion(self) -> bool:
        """
        Verificar si la conexión con OpenAI funciona
        
        Returns:
            bool: True si la conexión es exitosa
        """
        try:
            # Hacer una llamada simple para verificar la conexión
            self.client.models.list()
            return True
        except Exception:
            return False
