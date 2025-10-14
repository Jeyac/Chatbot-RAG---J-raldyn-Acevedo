# Script de instalación simple para el Chatbot RAG
Write-Host "=== Instalación del Chatbot RAG ===" -ForegroundColor Green

# Actualizar pip
Write-Host "Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Instalar dependencias básicas
Write-Host "Instalando dependencias básicas..." -ForegroundColor Yellow
python -m pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 Flask-Migrate==4.0.5
python -m pip install pytest==7.4.3 pytest-cov==4.1.0 python-dotenv==1.0.1
python -m pip install flask-socketio==5.3.6 pypdf2==3.0.1 openai==1.6.1

# Instalar numpy
Write-Host "Instalando numpy..." -ForegroundColor Yellow
python -m pip install "numpy>=1.24.0"

# Instalar dependencias de ML
Write-Host "Instalando dependencias de Machine Learning..." -ForegroundColor Yellow
python -m pip install "scikit-learn>=1.3.0" "sentence-transformers>=2.2.0"

# Instalar PostgreSQL (opcional)
Write-Host "Instalando PostgreSQL..." -ForegroundColor Yellow
python -m pip install "psycopg[binary]==3.2.10"

# Crear archivo .env
Write-Host "Creando archivo .env..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    @"
ENVIRONMENT=development
DB_NAME=chatbot_rag_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=tu_clave_api_openai_aqui
FLASK_SECRET_KEY=clave_secreta_flask_para_sesiones
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "Archivo .env creado" -ForegroundColor Green
} else {
    Write-Host "Archivo .env ya existe" -ForegroundColor Yellow
}

# Inicializar base de datos
Write-Host "Inicializando base de datos..." -ForegroundColor Yellow
try {
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    Write-Host "Base de datos inicializada correctamente" -ForegroundColor Green
} catch {
    Write-Host "Error al inicializar base de datos: $($_.Exception.Message)" -ForegroundColor Red
}

# Probar instalación
Write-Host "Probando instalación..." -ForegroundColor Yellow
try {
    python -c "import flask, numpy, openai, sentence_transformers, sklearn; print('✅ Todas las dependencias instaladas correctamente')"
    Write-Host "" -ForegroundColor White
    Write-Host "=== ¡INSTALACIÓN EXITOSA! ===" -ForegroundColor Green
    Write-Host "Próximos pasos:" -ForegroundColor Yellow
    Write-Host "1. Editar .env con tu OPENAI_API_KEY" -ForegroundColor White
    Write-Host "2. Ejecutar: python app.py" -ForegroundColor White
    Write-Host "3. Ir a: http://localhost:5000" -ForegroundColor White
} catch {
    Write-Host "Error en prueba de instalación: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Algunas dependencias pueden no estar instaladas correctamente" -ForegroundColor Yellow
}

