docker build -t bot-acn . --network="host"
docker run -d --network="host" --env-file ./.env bot-acn
pause
