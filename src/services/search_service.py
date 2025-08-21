import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from documents.schemas import SearchPassage, SearchResultsResponse


def search_passages(embeddings_service, query: str, k: int = 5) -> SearchResultsResponse:
    """Busca pasajes relevantes"""
    
    if not embeddings_service.vector_db:
        raise ValueError("No hay documentos indexados. Primero sube archivos usando /ingest")
    
    if not query or query.strip() == "":
        raise ValueError("El parámetro 'q' es requerido y no puede estar vacío")
    
    search_results = embeddings_service.similarity_search(query.strip(), k)
    
    if not search_results:
        return SearchResultsResponse(query=query, passages=[], total_found=0)
    
    passages = []
    for result in search_results:
        passage = SearchPassage(
            text=result.text,
            document_name=result.document_name,
            relevance_score=round(1.0 / (1.0 + result.score), 4)
        )
        passages.append(passage)
    
    return SearchResultsResponse(
        query=query,
        passages=passages,
        total_found=len(passages)
    )
