from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .schemas import IngestResponse, QuestionRequest, AskResponse, StatusResponse, SearchResultsResponse
from src.models import ProcessedFile
from .validator import validate_uploaded_files
from IA.embeddings import EmbeddingsService
from IA.llm_service import LLMService
from services import search_passages, answer_question

router = APIRouter(prefix="/api/v1", tags=["documents"])
embeddings_service = EmbeddingsService()
llm_service = LLMService()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    files: List[UploadFile] = File(..., description="Archivos a procesar (.txt o .pdf)")
):
    """
    Ingesta múltiples archivos, los procesa y los indexa
    
    - Acepta entre 3 y 10 archivos
    - Formatos soportados: .txt, .pdf
    - Procesa los archivos y crea embeddings
    - Almacena automáticamente en FAISS + metadata.json
    """
    try:
        validated_files = validate_uploaded_files(files)
        from .document_loader import document_loader_service
        all_chunks = await document_loader_service.load_uploaded_files(validated_files)
        
        if not all_chunks:
            raise HTTPException(
                status_code=400,
                detail="No se pudieron procesar los archivos"
            )
        
        if not embeddings_service.create_vector_database(all_chunks):
            raise HTTPException(
                status_code=500,
                detail="Error creando la base de datos vectorial"
            )
        
        processed_files = []
        file_chunks_count = {}
        
        for chunk in all_chunks:
            if chunk.document_name not in file_chunks_count:
                file_chunks_count[chunk.document_name] = 0
            file_chunks_count[chunk.document_name] += 1
        
        for filename, chunks_count in file_chunks_count.items():
            file_size = 0
            for file in validated_files:
                if file.filename == filename:
                    file_size = getattr(file, 'size', 0)
                    break
            
            processed_files.append(ProcessedFile(
                filename=filename,
                chunks_count=chunks_count,
                file_size=file_size
            ))
        
        total_chunks = len(all_chunks)
        
        return IngestResponse(
            message=f"Se procesaron exitosamente {len(processed_files)} archivos",
            files_processed=processed_files,
            total_chunks=total_chunks
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/ask", response_model=AskResponse)
async def ask_endpoint(request: QuestionRequest):
    """
    Realiza una pregunta sobre los documentos indexados
    
    - Recibe: { "question": "string" }
    - Responde en 3-4 líneas con 1-3 citas de respaldo
    - Dice "No encuentro esa información" si no hay contexto suficiente
    - Incluye referencias a los documentos fuente
    """
    try:
        return answer_question(llm_service, embeddings_service, request.question)
    except ValueError as e:
        if "llm no está disponible" in str(e).lower():
            raise HTTPException(status_code=503, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la pregunta: {str(e)}")


@router.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Obtiene el estado actual del sistema desde FAISS (fuente única de verdad)
    
    - Número de documentos indexados
    - Total de chunks procesados
    - Lista de documentos disponibles
    - Vectores indexados en FAISS
    - Disponibilidad del LLM
    """
    try:
        db_stats = embeddings_service.get_database_stats()
        total_docs = db_stats.get("unique_sources", 0)
        total_chunks = db_stats.get("total_documents", 0)
        available_docs = db_stats.get("source_list", [])
        total_vectors = db_stats.get("total_vectors", 0)
        
        return StatusResponse(
            indexed_documents=total_docs,
            total_chunks=total_chunks,
            available_documents=available_docs,
            indexed_vectors=total_vectors,
            total_documents=total_chunks,
            llm_available=llm_service.is_available()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo el estado: {str(e)}"
        )


@router.delete("/documents")
async def clear_documents():
    """
    Limpia todos los documentos indexados del sistema
    
    - Elimina todos los documentos del índice FAISS
    - Borra los metadatos almacenados
    - Resetea la base de datos vectorial
    - Limpia la persistencia en disco
    """
    try:
        embeddings_service.reset_database()
        return {"message": "Todos los documentos han sido eliminados"}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error limpiando documentos: {str(e)}"
        )

@router.get("/search", response_model=SearchResultsResponse)
async def search_endpoint(q: str, k: int = 5):
    """
    Búsqueda de pasajes relevantes en los documentos
    
    - q: Consulta de búsqueda (requerido)
    - k: Número máximo de pasajes a devolver (por defecto 5)
    - Devuelve: texto del fragmento, nombre del documento, puntaje de relevancia
    """
    try:
        return search_passages(embeddings_service, q, k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")


@router.get("/stats")
async def get_stats():
    """
    Obtiene estadísticas detalladas de FAISS y LLM
    
    - Estadísticas de la base de datos vectorial
    - Estado de persistencia (memoria vs disco)
    - Información del modelo de embeddings
    - Estado del servicio de LLM
    - Métricas de rendimiento
    """
    try:
        faiss_stats = embeddings_service.get_database_stats()
        
        return {
            "faiss_stats": faiss_stats,
            "llm_available": llm_service.is_available(),
            "system_status": {
                "has_data": faiss_stats.get("total_vectors", 0) > 0,
                "storage": "persistent",
                "embedding_model": "all-MiniLM-L6-v2"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")
