from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from fastapi import UploadFile
from typing import List, Optional
import tempfile
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DocumentChunk
from config import settings


class DocumentLoaderService:
    """Servicio para cargar y procesar documentos de diferentes tipos"""
    
    def __init__(self):
        self.supported_extensions = {
            '.pdf': self._load_pdf,
            '.txt': self._load_txt
        }

    async def load_uploaded_files(self, files: List[UploadFile]) -> List[DocumentChunk]:
        """
        Carga archivos subidos y los convierte a DocumentChunk
        
        Args:
            files: Lista de archivos subidos
            
        Returns:
            Lista de chunks de documentos
        """
        all_chunks = []
        
        for file in files:
            chunks = await self._process_uploaded_file(file)
            all_chunks.extend(chunks)
            
        return all_chunks

    async def _process_uploaded_file(self, file: UploadFile) -> List[DocumentChunk]:
        """
        Procesa un archivo subido individual
        
        Args:
            file: Archivo subido
            
        Returns:
            Lista de chunks del documento
        """
        if not file.filename:
            return []
            
        file_ext = os.path.splitext(file.filename.lower())[1]
        
        if file_ext not in self.supported_extensions:
            print(f"Tipo de archivo no soportado: {file_ext}")
            return []
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file.flush()
                
                chunks = self.supported_extensions[file_ext](temp_file.name, file.filename)
                
                os.unlink(temp_file.name)
                
                return chunks
                
        except Exception as e:
            print(f"Error procesando archivo {file.filename}: {e}")
            return []

    def _load_pdf(self, file_path: str, original_filename: str) -> List[DocumentChunk]:
        """
        Carga un archivo PDF
        
        Args:
            file_path: Ruta del archivo temporal
            original_filename: Nombre original del archivo
            
        Returns:
            Lista de chunks del documento
        """
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            
            chunks = []
            for i, page in enumerate(pages):
                chunk = DocumentChunk(
                    text=page.page_content,
                    document_name=original_filename,
                    chunk_index=i
                )
                chunks.append(chunk)
                
            return chunks
            
        except Exception as e:
            print(f"Error cargando PDF {original_filename}: {e}")
            return []

    def _load_txt(self, file_path: str, original_filename: str) -> List[DocumentChunk]:
        """
        Carga un archivo de texto
        
        Args:
            file_path: Ruta del archivo temporal
            original_filename: Nombre original del archivo
            
        Returns:
            Lista de chunks del documento
        """
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            chunks = []
            for doc in documents:
                text = doc.page_content
                
                if len(text) > settings.chunk_size:
                    text_chunks = self._split_text(text, settings.chunk_size, settings.chunk_overlap)
                    for i, chunk_text in enumerate(text_chunks):
                        chunk = DocumentChunk(
                            text=chunk_text,
                            document_name=original_filename,
                            chunk_index=i
                        )
                        chunks.append(chunk)
                else:
                    chunk = DocumentChunk(
                        text=text,
                        document_name=original_filename,
                        chunk_index=0
                    )
                    chunks.append(chunk)
                    
            return chunks
            
        except Exception as e:
            print(f"Error cargando texto {original_filename}: {e}")
            return []

    def _split_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Divide un texto en chunks con overlap
        
        Args:
            text: Texto a dividir
            chunk_size: Tamaño de cada chunk
            chunk_overlap: Solapamiento entre chunks
            
        Returns:
            Lista de chunks de texto
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            if end >= len(text):
                break
                
            start = end - chunk_overlap
            
        return chunks

    def get_supported_extensions(self) -> List[str]:
        """
        Obtiene las extensiones de archivo soportadas
        
        Returns:
            Lista de extensiones soportadas
        """
        return list(self.supported_extensions.keys())


document_loader_service = DocumentLoaderService()
