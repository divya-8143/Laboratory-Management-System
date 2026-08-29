.PHONY: help install start dev build test lint clean

help:
	@echo "AcuPath Enterprise LIS Management Commands:"
	@echo "  make install     - Install backend and frontend dependencies"
	@echo "  make dev         - Start development servers"
	@echo "  make start       - Start production backend server"
	@echo "  make build       - Build frontend application"
	@echo "  make test        - Run backend test suite"
	@echo "  make seed        - Populate database with default clinical data"

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

start:
	python main.py

dev:
	python main.py

build:
	cd frontend && npm run build

test:
	python -m pytest backend/tests/ -v

seed:
	python backend/seed_data.py
