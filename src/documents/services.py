from typing import Dict, List
from fastapi import UploadFile
from src.models import DocumentChunk, ProcessedFile
from .document_loader import document_loader_service


class DocumentService:
    """Servicio para el módulo de documentos"""
    def __init__(self):
        self.documents: Dict[str, List[str]] = {}
        self.document_chunks: List[DocumentChunk] = []

    async def ingest_documents(self, files: List[UploadFile]) -> List[ProcessedFile]:
        """
        Ingesta documentos y los divide en fragmentos
        
        Args:
            files: Lista de archivos subidos
            
        Returns:
            Lista de archivos procesados
        """
        processed_files = []
        
        # Cargar documentos usando el document loader
        new_chunks = await document_loader_service.load_uploaded_files(files)
        
        # Procesar cada archivo
        file_chunks_count = {}
        file_sizes = {}
        
        for file in files:
            if file.filename:
                file_chunks_count[file.filename] = 0
                file_sizes[file.filename] = getattr(file, 'size', 0)
        
        # Contar chunks por archivo
        for chunk in new_chunks:
            if chunk.document_name in file_chunks_count:
                file_chunks_count[chunk.document_name] += 1
        
        # Agregar chunks a la colección
        self.document_chunks.extend(new_chunks)
        
        # Crear información de archivos procesados
        for filename, chunks_count in file_chunks_count.items():
            if chunks_count > 0:  # Solo incluir archivos procesados exitosamente
                processed_file = ProcessedFile(
                    filename=filename,
                    chunks_count=chunks_count,
                    file_size=file_sizes.get(filename, 0)
                )
                processed_files.append(processed_file)
        
        return processed_files

    def get_all_chunks(self) -> List[DocumentChunk]:
        """
        Obtiene todos los chunks de documentos
        
        Returns:
            Lista de todos los chunks
        """
        return self.document_chunks

    def get_chunks_by_document(self, document_name: str) -> List[DocumentChunk]:
        """
        Obtiene chunks de un documento específico
        
        Args:
            document_name: Nombre del documento
            
        Returns:
            Lista de chunks del documento
        """
        return [chunk for chunk in self.document_chunks if chunk.document_name == document_name]

    def get_document_names(self) -> List[str]:
        """
        Obtiene los nombres de todos los documentos procesados
        
        Returns:
            Lista de nombres de documentos
        """
        return list(set(chunk.document_name for chunk in self.document_chunks))

    def get_total_chunks_count(self) -> int:
        """
        Obtiene el total de chunks procesados
        
        Returns:
            Número total de chunks
        """
        return len(self.document_chunks)

    def clear_documents(self):
        """Limpia todos los documentos y chunks"""
        self.documents.clear()
        self.document_chunks.clear()


# Instancia global del servicio
document_service = DocumentService()