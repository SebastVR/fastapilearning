# fastapilearning

Repository for learning framework fastapi
docker exec -it postgres_db psql -U postgresUSER -d postgresDB
docker-compose run backend alembic init alembic
docker-compose run backend alembic upgrade head
docker exec -it backend alembic revision --autogenerate -m "Create project and detection table"
docker exec -it backend alembic upgrade head
docker cp /home/integral/Downloads/python/best.pt backend:/app/data/staticfiles/
