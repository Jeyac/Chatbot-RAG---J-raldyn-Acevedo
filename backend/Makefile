# Makefile para el proyecto Chatbot con RAG

.PHONY: help install run test test-cov clean migrate upgrade downgrade lint format

# Variables
PYTHON = python
PIP = pip
FLASK = flask
PYTEST = pytest

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependencias
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencias instaladas correctamente$(NC)"

run: ## Ejecutar la aplicación
	@echo "$(GREEN)Ejecutando aplicación...$(NC)"
	$(PYTHON) app.py

run-dev: ## Ejecutar la aplicación en modo desarrollo
	@echo "$(GREEN)Ejecutando aplicación en modo desarrollo...$(NC)"
	FLASK_ENV=development $(PYTHON) app.py

test: ## Ejecutar tests
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	$(PYTEST) tests/ -v

test-cov: ## Ejecutar tests con cobertura
	@echo "$(GREEN)Ejecutando tests con cobertura...$(NC)"
	$(PYTEST) tests/ --cov=funcionalidades --cov-report=html --cov-report=term-missing

test-entities: ## Ejecutar tests de entidades
	@echo "$(GREEN)Ejecutando tests de entidades...$(NC)"
	$(PYTEST) tests/entities/ -v

test-use-cases: ## Ejecutar tests de casos de uso
	@echo "$(GREEN)Ejecutando tests de casos de uso...$(NC)"
	$(PYTEST) tests/use_cases/ -v

clean: ## Limpiar archivos temporales
	@echo "$(GREEN)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "$(GREEN)Limpieza completada$(NC)"

migrate: ## Crear migración
	@echo "$(GREEN)Creando migración...$(NC)"
	$(FLASK) db migrate -m "Auto migration"

upgrade: ## Aplicar migraciones
	@echo "$(GREEN)Aplicando migraciones...$(NC)"
	$(FLASK) db upgrade

downgrade: ## Revertir última migración
	@echo "$(GREEN)Revirtiendo última migración...$(NC)"
	$(FLASK) db downgrade

init-db: ## Inicializar base de datos
	@echo "$(GREEN)Inicializando base de datos...$(NC)"
	$(FLASK) db init
	$(FLASK) db migrate -m "Initial migration"
	$(FLASK) db upgrade

lint: ## Ejecutar linter (si está disponible)
	@echo "$(GREEN)Ejecutando linter...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 funcionalidades/ tests/ app.py; \
	else \
		echo "$(YELLOW)flake8 no está instalado. Instalando...$(NC)"; \
		$(PIP) install flake8; \
		flake8 funcionalidades/ tests/ app.py; \
	fi

format: ## Formatear código (si está disponible)
	@echo "$(GREEN)Formateando código...$(NC)"
	@if command -v black >/dev/null 2>&1; then \
		black funcionalidades/ tests/ app.py; \
	else \
		echo "$(YELLOW)black no está instalado. Instalando...$(NC)"; \
		$(PIP) install black; \
		black funcionalidades/ tests/ app.py; \
	fi

setup: install init-db ## Configurar proyecto completo
	@echo "$(GREEN)Proyecto configurado correctamente$(NC)"

check: test lint ## Ejecutar tests y linter
	@echo "$(GREEN)Verificación completada$(NC)"

# Comandos de desarrollo
dev-setup: setup ## Configurar entorno de desarrollo
	@echo "$(GREEN)Entorno de desarrollo configurado$(NC)"

dev-run: run-dev ## Ejecutar en modo desarrollo

# Comandos de producción
prod-install: ## Instalar dependencias para producción
	@echo "$(GREEN)Instalando dependencias para producción...$(NC)"
	$(PIP) install -r requirements.txt --no-dev

# Comandos de Docker (si se implementa)
docker-build: ## Construir imagen Docker
	@echo "$(GREEN)Construyendo imagen Docker...$(NC)"
	docker build -t chatbot-rag .

docker-run: ## Ejecutar contenedor Docker
	@echo "$(GREEN)Ejecutando contenedor Docker...$(NC)"
	docker run -p 5000:5000 chatbot-rag

# Comandos de documentación
docs: ## Generar documentación (si se implementa)
	@echo "$(GREEN)Generando documentación...$(NC)"
	@echo "$(YELLOW)Documentación no implementada aún$(NC)"

# Comandos de backup
backup-db: ## Hacer backup de la base de datos
	@echo "$(GREEN)Haciendo backup de la base de datos...$(NC)"
	@echo "$(YELLOW)Backup no implementado aún$(NC)"

# Comandos de monitoreo
logs: ## Ver logs de la aplicación
	@echo "$(GREEN)Mostrando logs...$(NC)"
	@echo "$(YELLOW)Logs no implementados aún$(NC)"

status: ## Ver estado de la aplicación
	@echo "$(GREEN)Estado de la aplicación:$(NC)"
	@echo "  - Python: $(shell $(PYTHON) --version)"
	@echo "  - Flask: $(shell $(PYTHON) -c 'import flask; print(flask.__version__)' 2>/dev/null || echo 'No instalado')"
	@echo "  - Base de datos: $(shell $(PYTHON) -c 'from funcionalidades.core.infraestructura.config import Config; print(Config.get_database_url())' 2>/dev/null || echo 'No configurada')"