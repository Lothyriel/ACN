docker build -t bot-acn .
docker run -d --env-file ./.env bot-acn
pause