"""
Excepciones globales de la aplicación
"""
from fastapi import HTTPException
from typing import Any, Dict, Optional


class QAException(Exception):
    """Excepción base para la aplicación Q&A"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class DocumentProcessingError(QAException):
    """Error en el procesamiento de documentos"""
    pass


class SearchError(QAException):
    """Error en la búsqueda"""
    pass


class InvalidFileError(QAException):
    """Error de archivo inválido"""
    pass


class FileSizeError(QAException):
    """Error de tamaño de archivo"""
    pass


# HTTP Exceptions
def create_http_exception(status_code: int, message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Crear una HTTPException con formato estándar"""
    return HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "details": details or {}
        }
    )


def bad_request_exception(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Crear excepción de solicitud incorrecta (400)"""
    return create_http_exception(400, message, details)


def not_found_exception(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Crear excepción de no encontrado (404)"""
    return create_http_exception(404, message, details)


def internal_server_exception(message: str, details: Optional[Dict[str, Any]] = None) -> HTTPException:
    """Crear excepción de error interno del servidor (500)"""
    return create_http_exception(500, message, details)
