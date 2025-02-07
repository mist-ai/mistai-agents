.PHONY: start
start:
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