# Chatbot RAG - Sistema de Preguntas y Respuestas con IA

Sistema completo de chatbot con RAG (Retrieval-Augmented Generation) implementado con Clean Architecture y Domain-Driven Design (DDD).

## 🎯 Características

- ✅ **Subida de PDFs**: Procesamiento de documentos PDF
- ✅ **RAG Implementation**: Búsqueda semántica con embeddings
- ✅ **Chat en Tiempo Real**: Comunicación via WebSockets
- ✅ **Clean Architecture**: Separación de capas (Domain, Application, Infrastructure, Presentation)
- ✅ **Frontend Moderno**: Interfaz desarrollada con Nuxt 3 y Tailwind CSS
- ✅ **Backend Robusto**: API REST con Flask y PostgreSQL/SQLite

## 🏗️ Arquitectura

```
├── backend/                    # Backend Flask
│   ├── funcionalidades/       # Módulos de negocio
│   │   ├── core/             # Infraestructura compartida
│   │   ├── documentos/       # Gestión de documentos
│   │   └── chat/            # Sistema de chat
│   ├── migrations/           # Migraciones de BD
│   └── app.py               # Aplicación principal
└── frontend/                 # Frontend Nuxt 3
    ├── pages/               # Páginas de la aplicación
    ├── components/          # Componentes Vue
    ├── composables/         # Lógica reutilizable
    └── layouts/            # Layouts de página
```

## 🚀 Instalación y Uso

### Backend (Flask)

1. **Navegar al directorio backend**
```bash
cd backend
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
copy env.example .env
# Editar .env con tu OPENAI_API_KEY
```

5. **Inicializar base de datos**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Ejecutar aplicación**
```bash
python app.py
```

### Frontend (Nuxt 3)

1. **Navegar al directorio frontend**
```bash
cd frontend
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
```bash
copy env.example .env
```

4. **Ejecutar en desarrollo**
```bash
npm run dev
```

## 📡 API Endpoints

### Documentos
- `POST /api/documentos/` - Subir documento PDF
- `GET /api/documentos/` - Listar documentos
- `POST /api/documentos/{id}/procesar` - Procesar documento
- `DELETE /api/documentos/{id}` - Eliminar documento

### WebSockets
- `enviar_mensaje` - Enviar pregunta al chatbot
- `respuesta_generada` - Recibir respuesta del chatbot

## 🛠️ Tecnologías

### Backend
- **Flask**: Framework web
- **SQLAlchemy**: ORM
- **PostgreSQL/SQLite**: Base de datos
- **OpenAI API**: Generación de respuestas
- **Sentence Transformers**: Embeddings
- **Scikit-learn**: Búsqueda de similitud
- **Flask-SocketIO**: WebSockets

### Frontend
- **Nuxt 3**: Framework Vue.js
- **Tailwind CSS**: Estilos
- **Socket.io-client**: Cliente WebSocket
- **Headless UI**: Componentes accesibles

## 📋 Flujo de Usuario

1. **Subir PDF**: El usuario sube un documento PDF
2. **Procesar**: El sistema extrae texto y genera embeddings
3. **Seleccionar**: El usuario selecciona el documento procesado
4. **Preguntar**: El usuario hace preguntas via chat
5. **Responder**: El sistema busca contexto relevante y genera respuestas

## 🔧 Configuración

### Variables de Entorno (Backend)
```
ENVIRONMENT=development
DATABASE_URL=sqlite:///chatbot_rag.db
OPENAI_API_KEY=tu_clave_api_openai
FLASK_SECRET_KEY=clave_secreta_flask
```

### Variables de Entorno (Frontend)
```
NUXT_PUBLIC_API_BASE=http://localhost:5000
NUXT_PUBLIC_SOCKET_URL=http://localhost:5000
```

## 📱 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **WebSocket**: ws://localhost:5000/socket.io/

## 🎨 Características de la Interfaz

- **Diseño Responsive**: Adaptable a móviles y desktop
- **Drag & Drop**: Subida intuitiva de archivos
- **Chat en Tiempo Real**: Comunicación instantánea
- **Estados Visuales**: Indicadores de conexión y procesamiento
- **Interfaz Limpia**: Diseño moderno con Tailwind CSS

## 📚 Documentación Adicional

- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
