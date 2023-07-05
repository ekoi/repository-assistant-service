# repository-assistant-service

poetry install; poetry update; poetry build; docker rm -f repository-assistant-service; docker rmi ekoindarto/repository-assistant-service:0.1.1;  docker build --no-cache -t ekoindarto/repository-assistant-service:0.1.1 -f Dockerfile . ;docker run -d -p 2810:2810 --name repository-assistant-service ekoindarto/repository-assistant-service:0.1.1; docker exec -it repository-assistant-service /bin/bash
