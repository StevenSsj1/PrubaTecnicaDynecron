# 🤖 Mini Asistente de Q&A

Sistema inteligente de preguntas y respuestas basado en documentos usando embeddings vectoriales y LLM (Google Gemini).

## 📋 Descripción

Esta aplicación permite subir múltiples documentos (PDF/TXT), procesarlos con embeddings para crear una base de conocimiento y realizar consultas inteligentes sobre el contenido con respuestas contextualizadas y citadas.

## 🏗️ Arquitectura del Sistema

```
proyecto/
├── src/                   # 🔧 Backend (FastAPI + IA)
│   ├── app.py            # Servidor principal
│   ├── config.py         # Configuración
│   ├── services/         # Servicios especializados
│   ├── IA/              # Módulos de IA
│   └── documents/       # Gestión de documentos
├── frontend/             # 🎨 Frontend (React + TypeScript)
│   ├── src/             # Código fuente
│   ├── components/      # Componentes UI
│   └── services/        # Servicios de API
└── docs/                # 📚 Documentación adicional
```

## 🚀 Instrucciones de Ejecución

### Prerrequisitos

- **Python 3.9+** para el backend
- **Node.js 18+** para el frontend  
- **API Key de Google Gemini**

### ⚡ Ejecución Rápida con Docker
Para el backend, el frontend debera ser levatando dentro de la carpeta frontend con el comando npm run dev.

```bash
# 1. Configurar variables de entorno
echo "GEMINI_API_KEY=tu_api_key_aqui" > .env

# 2. Ejecutar con Docker Compose
docker-compose up --build

# 3. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 🛠️ Ejecución Manual

#### Backend

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
export GEMINI_API_KEY=tu_api_key_aqui

# Ejecutar servidor
cd src
python -m app

# Servidor disponible en http://localhost:8000
```

#### Frontend

```bash
# Instalar dependencias
cd frontend
npm install

# Ejecutar en desarrollo
npm run dev

# Aplicación disponible en http://localhost:5173
```

## 🎯 Decisiones Técnicas y Supuestos

### Tecnologías Backend

- **FastAPI**: Elegido por su alto rendimiento, documentación automática y tipado estático
- **FAISS**: Base de datos vectorial optimizada para búsquedas de similitud a gran escala
- **LangChain**: Framework robusto para aplicaciones LLM con abstracciones útiles
- **Sentence Transformers**: Modelos pre-entrenados de alta calidad para embeddings
- **Google Gemini**: LLM potente con buen balance calidad/costo

### Tecnologías Frontend

- **React + TypeScript**: Ecosistema maduro con tipado estático
- **Vite**: Build tool moderno y rápido
- **Tailwind + Radix UI**: Diseño consistente y accesible
- **React Query**: Gestión eficiente del estado del servidor
- **React Hook Form**: Manejo optimizado de formularios

### Supuestos de Negocio

- **Límites de archivos**: 3-10 archivos por sesión (balance entre utilidad y rendimiento)
- **Tamaño máximo**: 10MB por archivo (prevenir abuso de recursos)
- **Formatos soportados**: PDF y TXT (formatos más comunes de documentos)
- **Idioma**: Optimizado para español pero funciona con múltiples idiomas
- **Persistencia**: Base vectorial se mantiene durante la sesión (no persistencia a largo plazo)

### Decisiones de UX/UI

- **Flujo lineal**: Subir → Procesar → Consultar (flujo intuitivo)
- **Feedback visual**: Indicadores de progreso y estados de carga
- **Responsive design**: Optimizado para desktop y móvil
- **Accesibilidad**: Componentes accesibles con soporte para lectores de pantalla

## ⏰ Tiempo Real Invertido

### Desarrollo Backend 

- **Arquitectura inicial**:
  - Diseño de módulos y servicios
  - Configuración de FastAPI
  - Estructura de carpetas

- **Servicios de IA**:
  - Integración con embeddings
  - Configuración de FAISS
  - Integración con Gemini LLM

- **APIs y validación**: 
  - Endpoints REST
  - Validación de archivos
  - Manejo de errores

- **Testing y refinamiento**:
  - Pruebas básicas
  - Optimización de respuestas

### Desarrollo Frontend 

- **Setup y configuración**: 
  - Configuración de Vite + React
  - Setup de Tailwind y componentes

- **Componentes UI**:
  - Diseño de interfaces
  - Componentes reutilizables
  - Sistema de diseño

- **Integración con API**
  - Servicios de API
  - Gestión de estado
  - Manejo de errores

- **UX y pulido**: 
  - Responsive design
  - Animaciones
  - Estados de carga

### DevOps y Documentación 

- **Docker y deployment**: 1 hora
- **Documentación técnica**: 1 hora

**Total: 7:30 horas**

## 📸 Capturas de Pantalla y Demo

### Interfaz Principal
![Home](/images/Home.png)


### Sistema de Búsqueda
![Search](/images/Search.png)

### Sistema de Q&A
![QA](/images/QA.png)


### Sistema de Estado
![Sistema de estado](/images/Estado.png)

### Demo
Frontend: https://insightful-playfulness-production.up.railway.app/
Backend: https://qa-pdf-production.up.railway.app/docs

---

## 📚 Documentación Adicional

- **[Backend README](src/README.md)**: Documentación técnica detallada del backend
- **[Frontend README](frontend/README.md)**: Guía de desarrollo del frontend  

## 🔗 Enlaces Útiles

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:5173 (desarrollo) / http://localhost:3000 (producción)

## 🤝 Contribución

Para contribuir al proyecto, consulta la documentación específica de cada módulo:
- Backend: `src/README.md`
- Frontend: `frontend/README.md`








