import importlib.metadata
import logging
import os

import requests
import uvicorn
from dynaconf import Dynaconf
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jsonpath_ng.ext import parse
from starlette import status
import json

from starlette.middleware.cors import CORSMiddleware

from src import protected, public
from src.commons import data, settings

__version__ = importlib.metadata.metadata(settings.SERVICE_NAME)["version"]

api_keys = [
    settings.DANS_TYPE_REGISTRY_SERVICE_API_KEY
]  #

# Authorization Form: It doesn't matter what you type in the form, it won't work yet. But we'll get there.
# See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__)


app.include_router(
    public.router,
    tags=["Public"],
    prefix=""
)

app.include_router(
    protected.router,
    tags=["Protected"],
    prefix="",
    dependencies=[Depends(api_key_auth)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def common_data():
    logging.debug("startup")

    # # Opening JSON file
    # f = open(settings.REPOSITORIES_CONF)
    # data.update({"repositories" : json.load(f)})
    for repo_conf_filename in os.listdir(settings.repositories_conf_dir):
        with open(os.path.join(settings.repositories_conf_dir, repo_conf_filename)) as f:
            repo_conf_json = json.loads(f.read())
            data.update({repo_conf_json['name']: repo_conf_json})


if __name__ == "__main__":
    logging.info("Start")

    uvicorn.run("src.main:app", host="0.0.0.0", port=2810, reload=False)
