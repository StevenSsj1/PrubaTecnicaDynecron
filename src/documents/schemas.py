from pydantic import BaseModel, Field
from typing import List
from src.models import SearchResult, Citation, ProcessedFile

class QuestionRequest(BaseModel):
    """Solicitud de pregunta"""
    question: str = Field(
        min_length=1,
        max_length=250,
        description="Pregunta que debe tener entre 1 y 500 caracteres"
    )


class QuestionResponse(BaseModel):
    """Respuesta de pregunta"""
    answer: str = Field(
        description="Respuesta a la pregunta"
    )
    citations: List[Citation] = Field(
        description="Citas utilizadas para la respuesta"
    )


class SearchResponse(BaseModel):
    """Solicitud de búsqueda"""
    query: str = Field(
        min_length=1,
        max_length=250,
        description="Consulta que debe tener entre 1 y 500 caracteres"
    )
    results: List[SearchResult] = Field(
        description="Resultados de la búsqueda"
    )

    total_results: int = Field(
        description="Total de resultados de la búsqueda"
    )

class SearchPassage(BaseModel):
    """Pasaje relevante de búsqueda"""
    text: str = Field(
        description="Texto del fragmento"
    )
    document_name: str = Field(
        description="Nombre del documento"
    )
    relevance_score: float = Field(
        description="Puntaje de relevancia"
    )


class SearchResultsResponse(BaseModel):
    """Respuesta del endpoint de búsqueda"""
    query: str = Field(
        description="Consulta realizada"
    )
    passages: List[SearchPassage] = Field(
        description="Pasajes más relevantes encontrados"
    )
    total_found: int = Field(
        description="Total de pasajes encontrados"
    )


class AskResponse(BaseModel):
    """Respuesta del endpoint de preguntas"""
    question: str = Field(
        description="Pregunta realizada"
    )
    answer: str = Field(
        description="Respuesta en 3-4 líneas"
    )
    citations: List[Citation] = Field(
        description="1-3 citas de respaldo",
        min_items=0,
        max_items=3
    )
    has_sufficient_context: bool = Field(
        description="Indica si se encontró suficiente contexto para responder"
    )


class IngestResponse(BaseModel):
    """Respuesta del endpoint de ingestión"""
    message: str = Field(
        description="Mensaje de respuesta"
    )
    files_processed: List[ProcessedFile] = Field(
        description="Archivos procesados"
    )
    total_chunks: int = Field(
        description="Total de fragmentos procesados"
    )


class StatusResponse(BaseModel):
    """Respuesta del endpoint de estado"""
    indexed_documents: int = Field(
        description="Total de documentos indexados"
    )
    total_chunks: int = Field(
        description="Total de fragmentos procesados"
    )
    available_documents: List[str] = Field(
        description="Documentos disponibles"
    )
    indexed_vectors: int = Field(
        description="Total de vectores indexados"
    )
    total_documents: int = Field(
        description="Total de documentos"
    )
    llm_available: bool = Field(
        description="Disponibilidad del LLM"
    )