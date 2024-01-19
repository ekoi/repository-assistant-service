import logging
import os
from contextlib import asynccontextmanager

import multiprocessing
from gunicorn.app.wsgiapp import WSGIApplication

import emoji
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from src import protected, public
from src.commons import data, settings, installed_repos_configs, __version__

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


class RepoAssistantServiceApplication(WSGIApplication):
    def __init__(self, app_uri, options=None):
        self.options = options or {}
        self.app_uri = app_uri
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def run():
    options = {
        "bind": "0.0.0.0:2810",
        "workers": (multiprocessing.cpu_count() * 2) + 1,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    RepoAssistantServiceApplication("src.main:app", options).run()


if __name__ == "__main__":

    logging.info("Start")
    if os.environ.get('run-local'):
        uvicorn.run("src.main:app", host="0.0.0.0", port=2810, reload=False)

    else:
        run()
