"""
Excepciones del dominio para el sistema de chatbot RAG
"""


class DomainException(Exception):
    """Excepción base del dominio"""
    pass


class BadRequestError(DomainException):
    """Error de solicitud incorrecta"""
    pass


class NotFoundError(DomainException):
    """Error de recurso no encontrado"""
    pass


class ValidationError(DomainException):
    """Error de validación"""
    pass


class ProcessingError(DomainException):
    """Error en el procesamiento de documentos"""
    pass


class OpenAIError(DomainException):
    """Error en la comunicación con OpenAI"""
    pass
