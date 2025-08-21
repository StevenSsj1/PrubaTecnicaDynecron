# Backend - Mini Asistente de Q&A

Sistema de preguntas y respuestas basado en documentos usando embeddings y LLM (Gemini).

## 🏗️ Arquitectura

El backend está diseñado con una arquitectura modular siguiendo el principio de responsabilidad única:

```
src/
├── app.py                 # Main de FastAPI con routers
├── config.py              # Configuración global
├── models.py              # Modelos de datos
├── utils.py               # Utilidades
├── exceptions.py          # Excepciones personalizadas
├── test_basic.py          # Pruebas básicas
├── services/              # 🎯 Servicios especializados (SRP)
│   ├── __init__.py
│   ├── search_service.py  # Servicio de búsqueda
│   └── qa_service.py      # Servicio de Q&A
├── IA/                    # Módulo de Inteligencia Artificial
│   ├── __init__.py
│   ├── embeddings.py      # Servicio de embeddings y base vectorial
│   └── llm_service.py     # Servicio del modelo de lenguaje
└── documents/             # Módulo de documentos
    ├── __init__.py        # Exporta router y servicios
    ├── router.py          # Router limpio (solo HTTP handling)
    ├── document_loader.py # Cargador de archivos
    ├── services.py        # Servicios de documentos
    ├── schemas.py         # Esquemas de API
    └── validator.py       # Validadores
```

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **LangChain**: Procesamiento de documentos y LLM
- **FAISS**: Base de datos vectorial optimizada
- **HuggingFace**: Embeddings de alta calidad
- **Google Gemini**: Modelo de lenguaje para respuestas
- **Pydantic**: Validación de datos y configuración
- **Uvicorn**: Servidor ASGI de alto rendimiento

## 📚 API Endpoints

### Salud y Estado
- **GET /health**: Verificación de salud del sistema
- **GET /**: Información de la API y endpoints disponibles
- **GET /api/v1/status**: Estado del sistema con estadísticas FAISS

### Gestión de Documentos
- **POST /api/v1/ingest**: Subir y procesar archivos (3-10 archivos .txt/.pdf)
- **DELETE /api/v1/documents**: Limpiar todos los documentos

### Búsqueda y Consultas
- **GET /api/v1/search?q=...**: Buscar pasajes relevantes con puntajes
- **POST /api/v1/ask**: Preguntas con respuestas de 3-4 líneas y citas

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.12+
- API key de Google Gemini

### Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
```bash
# Crear archivo .env en la raíz del proyecto
GEMINI_API_KEY=tu_api_key_aqui
```

### Configuración

Las configuraciones principales están en `src/config.py`:

```python
# Límites de archivos
min_files = 3          # Mínimo de archivos requeridos
max_files = 10         # Máximo de archivos permitidos
max_file_size = 10MB   # Tamaño máximo por archivo

# Formatos soportados
allowed_extensions = [".txt", ".pdf"]

# Procesamiento de texto
chunk_size = 500       # Tamaño de chunks de texto
chunk_overlap = 50     # Solapamiento entre chunks

# Búsqueda
similarity_search_k = 5        # Número de resultados de búsqueda
similarity_threshold = 0.7     # Umbral de similitud
```

## ▶️ Ejecución

### Desarrollo Local

```bash
# Desde la raíz del proyecto
cd src
python -m app

# O usando uvicorn directamente
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

El servidor estará disponible en `http://localhost:8000`

### Documentación de API

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Pruebas

Ejecutar las pruebas básicas:

```bash
cd src
python test_basic.py
```

## 🔧 Características Técnicas

### Procesamiento de Documentos
- ✅ Validación estricta de archivos (tipo, cantidad, tamaño)
- ✅ Extracción de texto optimizada para PDF y TXT
- ✅ Chunking inteligente con solapamiento
- ✅ Metadatos enriquecidos por documento

### Base de Datos Vectorial
- ✅ **FAISS optimizada** para búsquedas rápidas
- ✅ **Persistencia automática** del índice
- ✅ **Filtrado por metadatos** avanzado
- ✅ **Búsqueda con umbral** de similitud

### Inteligencia Artificial
- ✅ Embeddings de HuggingFace (sentence-transformers)
- ✅ Integración con Google Gemini
- ✅ Respuestas contextualizadas con citas
- ✅ Manejo de errores de LLM

### Arquitectura
- ✅ **Modular y escalable**
- ✅ **Separación de responsabilidades**
- ✅ **Manejo de errores robusto**
- ✅ **Configuración centralizada**

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de API Key:**
```bash
# Verificar que la variable esté configurada
echo $GEMINI_API_KEY
```

2. **Error de dependencias:**
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

3. **Error de permisos en data/:**
```bash
# Crear directorio con permisos
mkdir -p data
chmod 755 data
```

### Logs

Los logs del sistema están disponibles en:
- Consola durante desarrollo
- Docker logs: `docker-compose logs qa-assistant`

## 📊 Monitoreo

El endpoint `/api/v1/status` proporciona:
- Estado de FAISS
- Número de documentos indexados
- Estadísticas de memoria
- Tiempo de respuesta promedio
