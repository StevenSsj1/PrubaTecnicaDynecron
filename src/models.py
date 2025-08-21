"""
Modelos globales de la aplicación
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentChunk(BaseModel):
    """Modelo para un fragmento de documento"""
    text: str
    document_name: str
    chunk_index: int
    created_at: datetime = datetime.now()


class SearchResult(BaseModel):
    """Resultado individual de búsqueda"""
    text: str
    document_name: str
    score: float
    chunk_index: int


class Citation(BaseModel):
    """Cita de un documento"""
    text: str
    document_name: str
    score: float


class ProcessedFile(BaseModel):
    """Información de archivo procesado"""
    filename: str
    chunks_count: int
    file_size: int


class HealthCheck(BaseModel):
    """Modelo para health check"""
    status: str
    app_name: str
    version: str
    timestamp: datetime = datetime.now()
