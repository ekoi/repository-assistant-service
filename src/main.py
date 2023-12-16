import importlib.metadata
import json
import logging
import os
from contextlib import asynccontextmanager

import emoji
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src import protected, public
from src.commons import data, settings

__version__ = importlib.metadata.metadata(settings.SERVICE_NAME)["version"]

from src.models.assistant_datamodel import RepoAssistantModel

api_keys = [
    settings.DANS_REPO_ASSISTANT_SERVICE_API_KEY
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


@asynccontextmanager
async def lifespan(application: FastAPI):
    print('start up')
    installed_repos_configs()
    print(f'Available repositories configurations: {sorted(list(data.keys()))}')
    data.update({"service-version": __version__})
    print(emoji.emojize(':thumbs_up:'))

    yield

app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__, lifespan=lifespan)

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


def installed_repos_configs():
    logging.debug("startup")

    for repo_conf_filename in os.listdir(settings.repositories_conf_dir):
        if repo_conf_filename.endswith('.json'):
            with open(os.path.join(settings.repositories_conf_dir, repo_conf_filename)) as f:
                saved_repo_assistant = json.loads(f.read())
                repo_assistant = RepoAssistantModel.model_validate(saved_repo_assistant)
                data.update({repo_assistant.assistant_config_name: repo_assistant})


if __name__ == "__main__":
    logging.info("Start")

    uvicorn.run("src.main:app", host="0.0.0.0", port=2810, reload=False)
