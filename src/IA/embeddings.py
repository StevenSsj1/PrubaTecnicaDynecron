from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import Dict, Optional, List, Any
import sys
import os
import pickle
import json
from pathlib import Path

# Agregar el directorio padre al path para importar config y models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DocumentChunk, SearchResult
from config import settings


class EmbeddingsService:
    """Servicio avanzado para el manejo de embeddings y base de datos vectorial FAISS"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}  # Normalizar embeddings para mejor rendimiento
        )
        self.vector_db: Optional[FAISS] = None
        self.document_mapping: Dict[str, DocumentChunk] = {}
        self.index_path = Path(settings.vector_db_path)
        self.metadata_path = Path(settings.metadata_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
    
        self._load_existing_index()



    def create_vector_database(self, documents: List[DocumentChunk]) -> bool:
        """
        Crea la base de datos vectorial optimizada con FAISS
        
        Args:
            documents: Lista de chunks de documentos
            
        Returns:
            True si se creó exitosamente, False en caso contrario
        """
        try:
            if not documents:
                print("No hay documentos para procesar")
                return False
            
            langchain_docs = []
            for doc in documents:
                doc_id = f"{doc.document_name}_{doc.chunk_index}"
                
                # Metadatos enriquecidos para filtrado
                metadata = {
                    "source": doc.document_name,
                    "chunk_index": doc.chunk_index,
                    "doc_id": doc_id,
                    "created_at": doc.created_at.isoformat(),
                    "text_length": len(doc.text),
                    "file_type": self._get_file_type(doc.document_name)
                }
                
                langchain_doc = Document(
                    page_content=doc.text,
                    metadata=metadata
                )
                langchain_docs.append(langchain_doc)
                
                self.document_mapping[doc_id] = doc
            
            if self.vector_db is None:
                self.vector_db = FAISS.from_documents(langchain_docs, self.embeddings)
                print(f"Nueva base de datos vectorial creada con {len(documents)} documentos")
            else:
                new_vector_db = FAISS.from_documents(langchain_docs, self.embeddings)
                self.vector_db.merge_from(new_vector_db)
                print(f"Base de datos vectorial actualizada. {len(documents)} documentos agregados")
            
            self._save_index()
            
            return True
            
        except Exception as e:
            print(f"Error creando base de datos vectorial: {e}")
            return False

    def similarity_search(self, query: str, k: int = None, filter: Dict[str, Any] = None) -> List[SearchResult]:
        """
        Realiza búsqueda de similitud optimizada en la base de datos vectorial
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a retornar
            filter: Filtros de metadatos para la búsqueda
            
        Returns:
            Lista de resultados de búsqueda
        """
        if not self.vector_db:
            print("La base de datos vectorial no está inicializada")
            return []
            
        if k is None:
            k = settings.similarity_search_k
            
        try:
            docs_with_scores = self.vector_db.similarity_search_with_score(
                query, 
                k=k,
                filter=filter
            )
            
            results = []
            for doc, score in docs_with_scores:
                doc_id = doc.metadata.get("doc_id", "")
                chunk = self.document_mapping.get(doc_id)
                
                if chunk:
                    result = SearchResult(
                        text=chunk.text,
                        document_name=chunk.document_name,
                        score=float(score),
                        chunk_index=chunk.chunk_index
                    )
                    results.append(result)
                        
            return results
            
        except Exception as e:
            print(f"Error en búsqueda de similitud: {e}")
            return []

    def similarity_search_by_document(self, query: str, document_name: str, k: int = None) -> List[SearchResult]:
        """
        Busca similitud solo dentro de un documento específico
        
        Args:
            query: Consulta de búsqueda
            document_name: Nombre del documento para filtrar
            k: Número de resultados a retornar
            
        Returns:
            Lista de resultados de búsqueda filtrados por documento
        """
        filter_dict = {"source": document_name}
        return self.similarity_search(query, k, filter_dict)

    def similarity_search_by_file_type(self, query: str, file_type: str, k: int = None) -> List[SearchResult]:
        """
        Busca similitud filtrando por tipo de archivo
        
        Args:
            query: Consulta de búsqueda
            file_type: Tipo de archivo (.pdf, .txt)
            k: Número de resultados a retornar
            
        Returns:
            Lista de resultados de búsqueda filtrados por tipo
        """
        filter_dict = {"file_type": file_type}
        return self.similarity_search(query, k, filter_dict)

    def similarity_search_with_threshold(self, query: str, threshold: float = None, k: int = None) -> List[SearchResult]:
        """
        Busca similitud aplicando un umbral de score
        
        Args:
            query: Consulta de búsqueda
            threshold: Umbral mínimo de similitud
            k: Número de resultados a retornar
            
        Returns:
            Lista de resultados filtrados por umbral
        """
        if threshold is None:
            threshold = settings.similarity_threshold
            
        all_results = self.similarity_search(query, k)
        return [result for result in all_results if result.score <= threshold]

    def get_relevant_context(self, query: str, k: int = None, filter: Dict[str, Any] = None) -> str:
        """
        Obtiene el contexto relevante para una consulta con filtros opcionales
        
        Args:
            query: Consulta de búsqueda
            k: Número de resultados a considerar
            filter: Filtros de metadatos opcionales
            
        Returns:
            Contexto relevante como string
        """
        search_results = self.similarity_search(query, k, filter)
        
        if not search_results:
            return ""
            
        relevant_texts = [f"[{result.document_name}]: {result.text}" for result in search_results]
        return '\n\n'.join(relevant_texts)

    def get_database_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la base de datos vectorial
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.vector_db:
            return {
                "total_vectors": 0,
                "total_documents": 0,
                "unique_sources": 0,
                "index_exists": False
            }
        
        unique_sources = set()
        total_documents = len(self.document_mapping)
        
        for doc in self.document_mapping.values():
            unique_sources.add(doc.document_name)
        
        return {
            "total_vectors": self.vector_db.index.ntotal,
            "total_documents": total_documents,
            "unique_sources": len(unique_sources),
            "source_list": list(unique_sources),
            "index_exists": True,
            "embedding_dimension": self.vector_db.index.d if hasattr(self.vector_db.index, 'd') else None
        }

    def delete_documents_by_source(self, document_name: str) -> bool:
        """
        Elimina todos los chunks de un documento específico
        
        Args:
            document_name: Nombre del documento a eliminar
            
        Returns:
            True si se eliminó exitosamente
        """
        try:
            ids_to_remove = [
                doc_id for doc_id, chunk in self.document_mapping.items()
                if chunk.document_name == document_name
            ]
            
            if not ids_to_remove:
                print(f"No se encontraron documentos con el nombre: {document_name}")
                return False
            
            for doc_id in ids_to_remove:
                del self.document_mapping[doc_id]
            
            if self.vector_db and self.document_mapping:
                remaining_docs = []
                for chunk in self.document_mapping.values():
                    doc_id = f"{chunk.document_name}_{chunk.chunk_index}"
                    metadata = {
                        "source": chunk.document_name,
                        "chunk_index": chunk.chunk_index,
                        "doc_id": doc_id,
                        "created_at": chunk.created_at.isoformat(),
                        "text_length": len(chunk.text),
                        "file_type": self._get_file_type(chunk.document_name)
                    }
                    
                    remaining_docs.append(Document(
                        page_content=chunk.text,
                        metadata=metadata
                    ))
                
                self.vector_db = FAISS.from_documents(remaining_docs, self.embeddings)
                self._save_index()
            elif not self.document_mapping:
                self.reset_database()
            
            print(f"Documentos eliminados: {len(ids_to_remove)} chunks de '{document_name}'")
            return True
            
        except Exception as e:
            print(f"Error eliminando documentos: {e}")
            return False

    def reset_database(self):
        """Reinicia la base de datos vectorial y limpia la persistencia"""
        self.vector_db = None
        self.document_mapping.clear()
        
        try:
            if self.index_path.exists():
                import shutil
                shutil.rmtree(self.index_path.parent, ignore_errors=True)
            if self.metadata_path.exists():
                self.metadata_path.unlink()
        except Exception as e:
            print(f"Error limpiando archivos persistentes: {e}")
        
        print("Base de datos vectorial reiniciada completamente")

    def _get_file_type(self, filename: str) -> str:
        """Extrae el tipo de archivo de un nombre de archivo"""
        return Path(filename).suffix.lower()

    def _save_index(self):
        """Guarda el índice FAISS y metadatos en disco"""
        try:
            if self.vector_db:
                self.vector_db.save_local(str(self.index_path))
                
                metadata = {
                    doc_id: {
                        "text": chunk.text,
                        "document_name": chunk.document_name,
                        "chunk_index": chunk.chunk_index,
                        "created_at": chunk.created_at.isoformat()
                    }
                    for doc_id, chunk in self.document_mapping.items()
                }
                
                with open(self.metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                
                print(f"Índice guardado en: {self.index_path}")
                
        except Exception as e:
            print(f"Error guardando índice: {e}")

    def _load_existing_index(self):
        """Carga un índice FAISS existente si está disponible"""
        try:
            if self.index_path.exists() and self.metadata_path.exists():
                self.vector_db = FAISS.load_local(
                    str(self.index_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                from datetime import datetime
                for doc_id, data in metadata.items():
                    chunk = DocumentChunk(
                        text=data["text"],
                        document_name=data["document_name"],
                        chunk_index=data["chunk_index"],
                        created_at=datetime.fromisoformat(data["created_at"])
                    )
                    self.document_mapping[doc_id] = chunk
                
                print(f"Índice cargado exitosamente: {len(self.document_mapping)} documentos")
                
        except Exception as e:
            print(f"No se pudo cargar índice existente: {e}")
            self.vector_db = None
            self.document_mapping.clear()