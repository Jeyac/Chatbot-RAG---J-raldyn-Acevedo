# Chatbot con RAG - Jéraldyn Acevedo

Sistema de chatbot que utiliza RAG (Retrieval-Augmented Generation) para responder preguntas basándose en documentos PDF cargados.

## ✅ Requisitos Cumplidos

- ✅ **Selección del documento**: Sistema permite subir PDFs
- ✅ **Procesamiento del documento**: Genera embeddings usando sentence-transformers
- ✅ **Comunicación con OpenAI API**: Integración completa para respuestas contextualizadas
- ✅ **Condición de respuesta**: "No poseo información sobre ese tema en el documento cargado."
- ✅ **WebSockets**: Comunicación en tiempo real implementada

## 🚀 Instalación y Uso

### 1. Instalar dependencias
```powershell
.\install.ps1
```

### 2. Configurar OpenAI API Key
```powershell
notepad .env
# Editar: OPENAI_API_KEY=tu_clave_api_openai_aqui
```

### 3. Ejecutar aplicación
```powershell
python app.py
```

### 4. Usar el sistema
1. **Subir PDF**: `POST /api/documentos/` con archivo PDF
2. **Procesar**: `POST /api/documentos/{id}/procesar` (genera embeddings)
3. **Chat**: WebSocket en `ws://localhost:5000/socket.io/`

## 📋 Endpoints

- `POST /api/documentos/` - Subir documento PDF
- `GET /api/documentos/` - Listar documentos
- `GET /api/documentos/{id}` - Obtener documento
- `DELETE /api/documentos/{id}` - Eliminar documento
- `POST /api/documentos/{id}/procesar` - Procesar documento
- `POST /api/documentos/procesar-todos` - Procesar todos
- `GET /api/chat/historial` - Historial de chat
- `POST /api/chat/limpiar` - Limpiar historial
- `GET /health` - Estado del sistema

## 🔧 Tecnologías

- **Backend**: Flask, SQLAlchemy, WebSockets
- **IA**: OpenAI API, sentence-transformers, scikit-learn
- **Base de datos**: PostgreSQL/SQLite
- **Arquitectura**: Clean Architecture, DDD

## 📁 Estructura

```
backend/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias
├── env.example                     # Variables de entorno
├── install-complete.ps1            # Script de instalación
├── funcionalidades/                # Código fuente
│   ├── core/                       # Infraestructura compartida
│   ├── documentos/                 # Módulo de documentos
│   └── chat/                       # Módulo de chat
├── tests/                          # Tests
└── migrations/                     # Migraciones de BD
```

## 🎯 Flujo de Trabajo

1. **Subir PDF** → Extrae texto automáticamente
2. **Procesar** → Genera embeddings con sentence-transformers
3. **Chat** → Busca documentos similares y responde con OpenAI
4. **Respuesta** → Contextualizada o "No poseo información..."

## 👨‍💻 Autor

**Jéraldyn Acevedo**

Sistema implementado siguiendo Clean Architecture y Domain-Driven Design.