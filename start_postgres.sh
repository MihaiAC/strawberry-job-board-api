docker build -t local-postgres .
docker rm postgres-container
docker run -d --name postgres-container --env-file .env -p 5432:5432 local-postgres