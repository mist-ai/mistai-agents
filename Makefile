# Load variables from .env file
ifneq (,$(wildcard .env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

load-env:
	@echo "Environment variables loaded"

start: load-env
	@echo $(NEO4J_URI)
	rm -rf server.log || echo "no logs, proceding..."
	rm ~/.letta/sqlite.db || echo "no db, proceeding..."
	@PID=$$(lsof -ti :8283); \
	if [ -n "$$PID" ]; then \
		echo "Killing process $$PID on port 8080"; \
		kill -9 $$PID; \
	fi
	letta server --ade --port=8283 > server.log &
	sleep 5
	python src/app.py

.PHONY: stop
stop:
	rm -rf server.log || echo "no logs, proceding..."
	rm ~/.letta/sqlite.db || echo "no db, proceeding..."
	@PID=$$(lsof -ti :8283); \
	if [ -n "$$PID" ]; then \
		echo "Killing process $$PID on port 8080"; \
		kill -9 $$PID; \
	fi

start-dependencies:
	docker compose down
	docker compose up -d
	@echo "migrate data to graph database..."
	python src/dependency/migrate-neo.py