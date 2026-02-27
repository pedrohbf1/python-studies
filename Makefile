run:
	uvicorn app.main:app --reload

docker-up:
	docker compose --env-file .env up -d

migrate:
	alembic upgrade head