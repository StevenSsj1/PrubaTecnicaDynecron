"""
Configuración global de la aplicación
"""
import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    app_name: str = "Mini Asistente de Q&A"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Configuración del servidor
    host: str = "0.0.0.0"
    port: int = int(os.environ.get("PORT", 8000))  # Railway usa PORT dinámico
    
    # Configuración CORS
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["*"]
    cors_headers: List[str] = ["*"]
    
    # Configuración de archivos
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = [".txt", ".pdf"]
    min_files: int = 3
    max_files: int = 10
    
    # Configuración de procesamiento de texto
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_search_results: int = 10
    
    # Configuración de LLM y Embeddings
    gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")
    embedding_model: str = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    llm_model: str = "gemini-2.0-flash-exp"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 1000
    llm_top_p: float = 1.0
    llm_top_k: int = 40
    
    # Configuración de búsqueda vectorial FAISS
    similarity_search_k: int = 7
    similarity_threshold: float = 0.8
    
    # Configuración de persistencia FAISS
    vector_db_path: str = "data/vector_db"
    metadata_path: str = "data/metadata.json"
    
    # Configuración avanzada de FAISS
    faiss_normalize_embeddings: bool = True
    faiss_device: str = "cpu"  # 'cpu' o 'gpu'
    
    class Config:
        env_file = ".env"


# Instancia global de configuración
settings = Settings()
