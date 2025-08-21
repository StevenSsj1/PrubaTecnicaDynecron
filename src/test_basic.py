"""
Pruebas básicas para validar funcionalidad del sistema
"""
import os
import sys
import pytest
import tempfile
from fastapi.testclient import TestClient
from io import BytesIO

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import settings

client = TestClient(app)


class TestBasicFunctionality:
    """Pruebas básicas de funcionalidad"""
    
    def test_health_check(self):
        """Prueba el endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["app_name"] == settings.app_name
    
    def test_status_endpoint_empty(self):
        """Prueba el endpoint de status sin documentos"""
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        data = response.json()
        assert data["indexed_documents"] == 0
        assert data["total_chunks"] == 0
        assert data["available_documents"] == []
    
    def test_ask_without_documents(self):
        """Prueba hacer pregunta sin documentos indexados"""
        response = client.post("/api/v1/ask", json={"question": "¿Qué es esto?"})
        assert response.status_code == 400
        assert "No hay documentos indexados" in response.json()["detail"]
    
    def test_ingest_insufficient_files(self):
        """Prueba subir menos archivos de los requeridos"""
        # Crear un archivo de prueba
        test_content = b"Este es un contenido de prueba"
        files = [
            ("files", ("test1.txt", BytesIO(test_content), "text/plain"))
        ]
        
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 400
        assert "Debe subir entre" in response.json()["detail"]
    
    def test_ingest_invalid_file_extension(self):
        """Prueba subir archivo con extensión no válida"""
        test_content = b"Este es un contenido de prueba"
        files = []
        
        # Crear archivos con extensión inválida
        for i in range(3):
            files.append(
                ("files", (f"test{i}.docx", BytesIO(test_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
            )
        
        response = client.post("/api/v1/ingest", files=files)
        assert response.status_code == 400
        assert "no es válido" in response.json()["detail"]


class TestFileValidation:
    """Pruebas de validación de archivos"""
    
    def test_validate_file_extensions(self):
        """Prueba validación de extensiones de archivo"""
        from utils import validate_file_extension
        
        # Extensiones válidas
        assert validate_file_extension("test.pdf", [".pdf", ".txt"]) == True
        assert validate_file_extension("test.txt", [".pdf", ".txt"]) == True
        
        # Extensiones inválidas
        assert validate_file_extension("test.docx", [".pdf", ".txt"]) == False
        assert validate_file_extension("test.jpg", [".pdf", ".txt"]) == False
    
    def test_format_file_size(self):
        """Prueba formateo de tamaño de archivo"""
        from utils import format_file_size
        
        assert format_file_size(1024) == "1.0 KB"
        assert format_file_size(1024 * 1024) == "1.0 MB"
        assert format_file_size(500) == "500 B"


class TestDocumentLoader:
    """Pruebas del cargador de documentos"""
    
    def test_supported_extensions(self):
        """Prueba obtener extensiones soportadas"""
        from documents.document_loader import document_loader_service
        
        extensions = document_loader_service.get_supported_extensions()
        assert ".pdf" in extensions
        assert ".txt" in extensions
    
    def test_split_text(self):
        """Prueba división de texto en chunks"""
        from documents.document_loader import document_loader_service
        
        text = "Este es un texto muy largo que necesita ser dividido en chunks más pequeños para su procesamiento."
        chunks = document_loader_service._split_text(text, chunk_size=20, chunk_overlap=5)
        
        assert len(chunks) > 1
        assert len(chunks[0]) <= 20


def run_basic_tests():
    """Ejecuta las pruebas básicas manualmente"""
    print("=== Ejecutando Pruebas Básicas ===\n")
    
    try:
        # Test 1: Health Check
        print("1. Probando Health Check...")
        response = client.get("/health")
        if response.status_code == 200:
            print("   ✓ Health check exitoso")
        else:
            print(f"   ✗ Health check falló: {response.status_code}")
        
        # Test 2: Status sin documentos
        print("2. Probando Status sin documentos...")
        response = client.get("/api/v1/status")
        if response.status_code == 200 and response.json()["indexed_documents"] == 0:
            print("   ✓ Status sin documentos exitoso")
        else:
            print(f"   ✗ Status falló: {response.status_code}")
        
        # Test 3: Validación de archivos insuficientes
        print("3. Probando validación de archivos insuficientes...")
        test_content = b"Contenido de prueba"
        files = [("files", ("test.txt", BytesIO(test_content), "text/plain"))]
        response = client.post("/api/v1/ingest", files=files)
        if response.status_code == 400:
            print("   ✓ Validación de archivos insuficientes exitosa")
        else:
            print(f"   ✗ Validación falló: {response.status_code}")
        
        # Test 4: Pregunta sin documentos
        print("4. Probando pregunta sin documentos...")
        response = client.post("/api/v1/ask", json={"question": "¿Qué es esto?"})
        if response.status_code == 400:
            print("   ✓ Pregunta sin documentos exitosa")
        else:
            print(f"   ✗ Pregunta sin documentos falló: {response.status_code}")
        
        # Test 5: Estadísticas de base de datos
        print("5. Probando estadísticas de FAISS...")
        response = client.get("/api/v1/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✓ Estadísticas obtenidas: {stats['faiss_stats']['total_vectors']} vectores")
        else:
            print(f"   ✗ Estadísticas fallaron: {response.status_code}")
        
        # Test 6: Búsqueda de pasajes sin documentos
        print("6. Probando búsqueda de pasajes sin documentos...")
        response = client.get("/api/v1/search?q=test")
        if response.status_code == 400:
            print("   ✓ Búsqueda de pasajes sin documentos exitosa")
        else:
            print(f"   ✗ Búsqueda de pasajes falló: {response.status_code}")
        
        # Test 7: Búsqueda con parámetro vacío
        print("7. Probando búsqueda con parámetro vacío...")
        response = client.get("/api/v1/search?q=")
        if response.status_code == 400:
            print("   ✓ Validación de parámetro vacío exitosa")
        else:
            print(f"   ✗ Validación de parámetro vacío falló: {response.status_code}")
        
        print("\n=== Pruebas Básicas Completadas ===")
        
    except Exception as e:
        print(f"Error ejecutando pruebas: {e}")


if __name__ == "__main__":
    run_basic_tests()
