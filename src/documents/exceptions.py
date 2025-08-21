"""
Excepciones específicas del módulo de documentos
"""
from ..exceptions import QAException


class DocumentNotFoundError(QAException):
    """Error cuando no se encuentra un documento"""
    pass


class InvalidDocumentFormatError(QAException):
    """Error cuando el formato del documento es inválido"""
    pass


class DocumentProcessingError(QAException):
    """Error durante el procesamiento del documento"""
    pass


class SearchNotReadyError(QAException):
    """Error cuando el sistema de búsqueda no está listo"""
    pass


class EmptyQueryError(QAException):
    """Error cuando la consulta está vacía"""
    pass
