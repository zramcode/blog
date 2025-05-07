# Makefile


APP=app.main:app
CELERY_APP=app.tasks


run-redis:
	docker run -d --name redis-blog -p 6379:6379 redis


run-api:
	uvicorn $(APP) --reload


run-celery:
	celery -A $(CELERY_APP) worker --loglevel=info


stop-redis:
	docker stop redis-blog && docker rm redis-blog


start:
	@echo "Starting API and Celery in separate terminals..."
	@echo "Run 'make run-api' and 'make run-celery' in separate terminals."


install:
	pip install -r requirements.txt
