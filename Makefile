.DEFAULT_GOAL := help

run: ## Run the application using uvicorn with provided arguments or default
	docker compose up -d

makemigrations: ## Create migrations
	docker compose exec backend uv run alembic revision --autogenerate

migrate: ## Migrate migrations
	docker compose exec backend uv run alembic upgrade head

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##"}; {printf "  %-20s %s\n", $$1, $$2}'

