# Frontend - Chatbot RAG

Frontend desarrollado con Nuxt 3 para el sistema de Chatbot RAG.

## Características

- **Interfaz moderna**: Diseño limpio con Tailwind CSS
- **Subida de PDFs**: Drag & drop y selección de archivos
- **Chat en tiempo real**: Comunicación via WebSockets
- **Gestión de documentos**: Lista, procesamiento y eliminación
- **Responsive**: Adaptable a diferentes tamaños de pantalla
- **Componentes reutilizables**: Arquitectura modular

## Instalación

### 1. Instalar dependencias
```bash
npm install
```

### 2. Configurar variables de entorno
```bash
 .env
```

Editar `.env` con las URLs del backend:
```
NUXT_PUBLIC_API_BASE=http://localhost:5000
NUXT_PUBLIC_SOCKET_URL=http://localhost:5000
```

### 3. Ejecutar en desarrollo
```bash
npm run dev
```

La aplicación estará disponible en: http://localhost:3000

## Estructura del Proyecto

```
frontend/
├── app/
│   └── app.vue              # Componente principal
├── assets/
│   └── css/
│       └── main.css         # Estilos globales
├── components/
│   ├── ChatInterface.vue    # Interfaz de chat
│   ├── DocumentList.vue     # Lista de documentos
│   └── DocumentUpload.vue   # Subida de documentos
├── composables/
│   ├── useApi.js           # Funciones de API
│   └── useSocket.js        # Conexión WebSocket
├── nuxt.config.ts          # Configuración de Nuxt
└── package.json            # Dependencias
```

## Componentes

### DocumentUpload
- Subida de archivos PDF con drag & drop
- Validación de tipo y tamaño
- Indicadores de progreso

### DocumentList
- Lista de documentos cargados
- Estados de procesamiento
- Acciones: procesar, seleccionar, eliminar

### ChatInterface
- Chat en tiempo real con WebSockets
- Indicador de escritura
- Historial de mensajes
- Estado de conexión

## Conexión con Backend

### API REST
- `POST /api/documentos/` - Subir documento
- `GET /api/documentos/` - Listar documentos
- `POST /api/documentos/{id}/procesar` - Procesar documento
- `DELETE /api/documentos/{id}` - Eliminar documento

### WebSockets
- `enviar_mensaje` - Enviar pregunta
- `respuesta_generada` - Recibir respuesta
- `error` - Manejo de errores

## Estilos

Utiliza Tailwind CSS con clases personalizadas:
- `.btn-primary` - Botón principal
- `.btn-secondary` - Botón secundario
- `.input-field` - Campo de entrada
- `.card` - Tarjeta contenedora

## Scripts Disponibles

```bash
npm run dev      # Desarrollo
npm run build    # Construcción
npm run preview  # Vista previa
```

## Responsive Design

- **Mobile**: Layout de una columna
- **Tablet**: Layout adaptativo
- **Desktop**: Layout de dos columnas (gestión + chat)

## Configuración

### Variables de Entorno
- `NUXT_PUBLIC_API_BASE`: URL base de la API
- `NUXT_PUBLIC_SOCKET_URL`: URL del servidor WebSocket

### Dependencias Principales
- **Nuxt 3**: Framework de Vue.js
- **Tailwind CSS**: Framework de estilos
- **Socket.io-client**: Cliente WebSocket
- **Headless UI**: Componentes accesibles
- **Heroicons**: Iconografía