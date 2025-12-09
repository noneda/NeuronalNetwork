.PHONY: help install test run clean coverage lint

help:
	@echo "Comandos disponibles:"
	@echo "  make install    - Instalar dependencias"
	@echo "  make test       - Ejecutar tests"
	@echo "  make run        - Iniciar API"
	@echo "  make clean      - Limpiar archivos temporales"
	@echo "  make coverage   - Generar reporte de cobertura"
	@echo "  make lint       - Ejecutar linter"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/ -v -m unit

test-integration:
	pytest tests/ -v -m integration

test-api:
	pytest tests/ -v -m api

run:
	python -m src2.api.app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build dist

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
	@echo "Reporte generado en htmlcov/index.html"

lint:
	flake8 src/ tests/ --max-line-length=100
	pylint src/ tests/