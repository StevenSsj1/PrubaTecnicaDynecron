# Frontend - Mini Asistente de Q&A

Interfaz web moderna para el sistema de preguntas y respuestas basado en documentos.

## 🎨 Tecnologías

- **React 18**: Biblioteca de UI con las últimas características
- **TypeScript**: Tipado estático para mayor robustez
- **Vite**: Build tool rápido y moderno
- **Tailwind CSS**: Framework de utilidades CSS
- **Radix UI**: Componentes accesibles y personalizables
- **React Hook Form**: Manejo eficiente de formularios
- **React Query**: Gestión de estado del servidor
- **React Router**: Navegación del lado del cliente
- **Lucide React**: Iconos modernos y consistentes

## 🏗️ Estructura del Proyecto

```
frontend/
├── public/                 # Archivos estáticos
├── src/
│   ├── components/         # Componentes reutilizables
│   │   └── ui/            # Componentes base de UI
│   ├── pages/             # Páginas de la aplicación
│   ├── services/          # Servicios de API
│   ├── hooks/             # Custom hooks
│   ├── types/             # Definiciones de tipos
│   ├── utils/             # Utilidades
│   ├── App.tsx            # Componente principal
│   ├── main.tsx           # Punto de entrada
│   └── index.css          # Estilos globales
├── components.json        # Configuración de shadcn/ui
├── tailwind.config.ts     # Configuración de Tailwind
├── vite.config.ts         # Configuración de Vite
└── package.json           # Dependencias y scripts
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Node.js 18+
- npm o yarn
- Backend ejecutándose en `http://localhost:8000`

### Instalación

```bash
# Instalar dependencias
npm install

# O con yarn
yarn install
```

## ▶️ Scripts Disponibles

### Desarrollo

```bash
# Servidor de desarrollo con hot reload
npm run dev
# La aplicación estará disponible en http://localhost:5173
```

### Build y Producción

```bash
# Build para producción
npm run build

# Preview del build de producción
npm run preview

# Servir archivos estáticos (para deployment)
npm run start
```

## 🌟 Características

### Interfaz de Usuario
- ✅ **Diseño moderno y responsive**
- ✅ **Modo oscuro/claro**
- ✅ **Componentes accesibles**
- ✅ **Animaciones suaves**
- ✅ **Indicadores de carga**

### Funcionalidades
- ✅ **Subida de múltiples archivos** con drag & drop
- ✅ **Validación en tiempo real** de archivos
- ✅ **Búsqueda instantánea** con resultados destacados
- ✅ **Sistema de Q&A** con respuestas contextualizadas
- ✅ **Gestión de estado** eficiente
- ✅ **Manejo de errores** robusto

### UX/UI
- ✅ **Feedback visual** en todas las acciones
- ✅ **Estados de carga** informativos
- ✅ **Notificaciones toast** para acciones
- ✅ **Navegación intuitiva**
- ✅ **Responsive design** para móviles

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env.local` en la raíz del frontend:

```bash
# URL del backend
VITE_API_URL=http://localhost:8000

# Otras configuraciones
VITE_APP_NAME="Mini Asistente Q&A"
VITE_MAX_FILE_SIZE=10485760  # 10MB en bytes
VITE_MAX_FILES=10
VITE_MIN_FILES=3
```

### Tailwind CSS

La configuración está en `tailwind.config.ts` e incluye:
- Tema personalizado con variables CSS
- Configuración de colores
- Animaciones personalizadas
- Plugins de tipografía

### TypeScript

Configuración en `tsconfig.json` con:
- Strict mode habilitado
- Path mapping para imports
- Configuración optimizada para React

## 🎭 Componentes Principales

### Layout
- **App.tsx**: Layout principal con routing
- **Navigation**: Barra de navegación responsive

### Páginas
- **Index**: Página principal con subida de archivos
- **Search**: Interfaz de búsqueda
- **Chat**: Sistema de Q&A

### Servicios
- **api.ts**: Cliente HTTP con React Query
- **fileService**: Manejo de archivos
- **searchService**: Servicios de búsqueda


### Variables de Entorno en Producción

Asegúrate de configurar:
```bash
VITE_API_URL=https://tu-backend-url.com
```
