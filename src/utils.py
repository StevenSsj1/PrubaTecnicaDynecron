"""
Utilidades globales de la aplicación
"""
import re
import math
from typing import List



def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Valida si la extensión del archivo está permitida
    """
    if not filename:
        return False
    
    file_extension = '.' + filename.split('.')[-1].lower()
    return file_extension in [ext.lower() for ext in allowed_extensions]


def format_file_size(size_bytes: int) -> str:
    """
    Formatea el tamaño de archivo en formato legible
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"
