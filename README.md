# repository-assistant-service

curl -X 'POST' -H "Authorization: Bearer APIKEY" -H 'Content-Type: application/json' 'https://repository-assistant.labs.dans.knaw.nl/upload-repo?overwrite=true' -d @/Users/akmi/git/ekoi/poc-4-wim/repository-assistant-service/resources/saved-repos-conf/ds-ssh-demo.json 
curl -X 'POST' -H "Authorization: Bearer APIKEY" -H 
'Content-Type: application/json' 'http://localhost:2810/upload-repo?overwrite=true' -d @/Users/akmi/git/ekoi/poc-4-wim/repository-assistant-service/resources/saved-repos-conf/ohsmart-local-new.json

docker build --platform linux/amd64


rm -rf dist; poetry install; poetry update; poetry build; docker rm -f repository-assistant-service; docker rmi ekoindarto/repository-assistant-service:0.1.6-arm64;  docker build --no-cache -t ekoindarto/repository-assistant-service:0.1.6-arm64 -f Dockerfile . ;docker run -v ./conf:/home/dans/repository-assistant-service/conf -d -p 2810:2810 --name repository-assistant-service ekoindarto/repository-assistant-service:0.1.6-arm64; docker exec -it repository-assistant-service /bin/bash
rm -rf dist; poetry install; poetry update; poetry build; docker rm -f repository-assistant-service; docker rmi ekoindarto/repository-assistant-service:0.1.6;  docker build --platform linux/amd64 --no-cache -t ekoindarto/repository-assistant-service:0.1.6 -f Dockerfile . ;docker run -v ./conf:/home/dans/repository-assistant-service/conf -d -p 2810:2810 --name repository-assistant-service ekoindarto/repository-assistant-service:0.1.6; docker exec -it repository-assistant-service /bin/bash

docker run -v ./conf:/home/dans/repository-assistant-servi ce/conf -d -p 2810:2810 --name repository-assistant-service ekoindarto/repository-assistant-service:0.1.6-arm64;

docker run -v ./conf:/home/dans/repository-assistant-service/conf -d -p 2810:2810 --name repository-assistant-service ekoindarto/repository-assistant-service:0.1.6-arm64;
docker run -v ./conf:/home/dans/repository-assistant-service/conf -d -p 2810:2810 --name repository-assistant-service