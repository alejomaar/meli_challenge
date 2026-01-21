SHELL := /bin/bash
.ONESHELL:
# Variables
DB_CONTAINER=meli_db
DB_USER=root
DB_NAME=postgres
BACKUP_FILE=backup.sql


run:
	set -a
	. $(CURDIR)/.env
	set +a
	uvicorn api:app --host 127.0.0.1 --port 3000 --log-level debug --reload

# 🧾 Dump the Postgres database to backup.sql
backup:
	@echo "📦 Exporting database from container '$(DB_CONTAINER)'..."
	docker exec -t $(DB_CONTAINER) pg_dump -U $(DB_USER) $(DB_NAME) > $(BACKUP_FILE)
	@echo "✅ Backup created: $(BACKUP_FILE)"