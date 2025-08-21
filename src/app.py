"""
Aplicación principal - Mini Asistente de Q&A
Main de FastAPI con routers modulares
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.config import settings
from src.models import HealthCheck
from src.documents.router import router as documents_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description="Sistema de preguntas y respuestas basado en documentos usando embeddings y LLM"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

app.include_router(documents_router)


@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check():
    """Endpoint de verificación de salud del sistema"""
    return HealthCheck(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version
    )


@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "ingest": "POST /api/v1/ingest - Subir archivos",
            "ask": "POST /api/v1/ask - Hacer preguntas",
            "status": "GET /api/v1/status - Estado del sistema",
            "clear": "DELETE /api/v1/documents - Limpiar documentos"
        }
    }


def main():
    """
    Función principal - ejecuta la API REST
    
    La aplicación funciona como una API REST con los siguientes endpoints:
    
    - GET /health: Verificación de salud
    - GET /: Información de la API
    - POST /api/v1/ingest: Subir archivos (3-10 archivos .txt/.pdf)
    - POST /api/v1/ask: Hacer preguntas sobre documentos indexados
    - GET /api/v1/status: Estado del sistema
    - DELETE /api/v1/documents: Limpiar documentos
    
    Para usar la aplicación:
    1. Ejecuta este archivo para iniciar el servidor
    2. Visita http://localhost:8000/docs para la documentación interactiva
    3. Usa los endpoints para subir archivos y hacer preguntas
    """
    
    print("=== Mini Asistente de Q&A - API REST ===")
    print(f"Iniciando servidor en http://{settings.host}:{settings.port}")
    print("\nEndpoints disponibles:")
    print("- GET /health - Verificación de salud")
    print("- GET /docs - Documentación interactiva")
    print("- POST /api/v1/ingest - Subir archivos")
    print("- POST /api/v1/ask - Hacer preguntas")
    print("- GET /api/v1/status - Estado del sistema")
    print("- DELETE /api/v1/documents - Limpiar documentos")
    print("\nPresiona Ctrl+C para detener el servidor")
    
    # Ejecutar servidor
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )


if __name__ == "__main__":
    main()