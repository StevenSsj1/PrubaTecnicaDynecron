"""
Dependencias para el módulo de documentos
"""
from fastapi import UploadFile, HTTPException
from typing import List
from src.config import settings
from src.utils import validate_file_extension, format_file_size
from .services import document_service, DocumentService


def get_document_service() -> DocumentService:
    """Dependency para obtener el servicio de documentos"""
    return document_service


def validate_uploaded_files(files: List[UploadFile]) -> List[UploadFile]:
    """
    Valida los archivos subidos
    
    Args:
        files: Lista de archivos subidos
        
    Returns:
        Lista de archivos validados
        
    Raises:
        HTTPException: Si los archivos no son válidos
    """
    if len(files) < settings.min_files or len(files) > settings.max_files:
        raise HTTPException(
            status_code=400,
            detail=f"Debe subir entre {settings.min_files} y {settings.max_files} archivos"
        )
    
    validated_files = []
    
    for file in files:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Todos los archivos deben tener un nombre"
            )
        if not validate_file_extension(file.filename, settings.allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Archivo {file.filename} no es válido. Solo se aceptan: {', '.join(settings.allowed_extensions)}"
            )
        if hasattr(file, 'size') and file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"Archivo {file.filename} es demasiado grande. Máximo: {format_file_size(settings.max_file_size)}"
            )
        
        validated_files.append(file)
    
    return validated_files
