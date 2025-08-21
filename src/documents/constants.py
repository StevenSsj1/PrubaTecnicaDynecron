"""
Constantes para el módulo de documentos
"""

# Mensajes de respuesta
MESSAGES = {
    "NO_DOCUMENTS": "No encuentro esa información en los documentos cargados.",
    "INGEST_SUCCESS": "Se procesaron {count} archivos exitosamente",
    "SEARCH_NO_RESULTS": "No se encontraron resultados para la búsqueda.",
    "INVALID_FILE_TYPE": "Archivo {filename} no es válido. Solo se aceptan .txt y .pdf",
    "FILE_COUNT_ERROR": "Debe subir entre {min_files} y {max_files} archivos",
    "PROCESSING_ERROR": "Error procesando documentos: {error}",
    "SEARCH_ERROR": "Error en la búsqueda: {error}",
    "QUESTION_ERROR": "Error procesando la pregunta: {error}"
}

# Configuración por defecto
DEFAULT_SEARCH_LIMIT = 10
DEFAULT_ANSWER_LENGTH = 500
MAX_CITATIONS = 3
MAX_SENTENCES_PER_PASSAGE = 2
