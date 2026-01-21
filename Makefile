SHELL := /bin/bash
.ONESHELL:

run:
	set -a
	. $(CURDIR)/.env
	set +a
	uvicorn api:app --host 127.0.0.1 --port 3000 --log-level debug --reload
