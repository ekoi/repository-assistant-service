import logging
import os
from contextlib import asynccontextmanager

import multiprocessing
from typing import Annotated

from gunicorn.app.wsgiapp import WSGIApplication
from keycloak import KeycloakOpenID, KeycloakAuthenticationError


import emoji
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from starlette.middleware.cors import CORSMiddleware

import json
import jmespath

from src import protected, public
from src.commons import data, settings, installed_repos_configs, __version__

api_keys = [settings.DANS_REPO_ASSISTANT_SERVICE_API_KEY]
security = HTTPBearer()


def auth_header(request: Request, auth_cred: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    Simplified authentication header dependency function.
    """

    if not auth_cred or auth_cred.credentials not in api_keys:
        keycloak_env = settings.get(f"keycloak_{request.headers.get('auth-env-name', 'local')}")
        if not keycloak_env:
            logging.error(f"keycloak_env: {keycloak_env}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")

        keycloak_openid = KeycloakOpenID(server_url=keycloak_env.URL, client_id=keycloak_env.CLIENT_ID,
                                         realm_name=keycloak_env.REALMS)
        try:
            keycloak_openid.userinfo(auth_cred.credentials)
            logging.info(f"Keycloak: {keycloak_openid}")
        except KeycloakAuthenticationError:
            logging.error(f"KeycloakAuthenticationError: {keycloak_openid}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")
        except Exception as e:
            logging.inf(f"Error: {e}")

@asynccontextmanager
async def lifespan(application: FastAPI):
    logging.info('start up')
    installed_repos_configs()
    logging.info(f'Available repositories configurations: {sorted(list(data.keys()))}')
    data.update({"service-version": __version__})
    logging.info(emoji.emojize(':thumbs_up:'))
    # Load JSON data from the file
    with open(settings.repo_file_types) as file:
        file_types = json.load(file)
    # Use jmespath to retrieve all "values"
    values = jmespath.search('[*].value', file_types)
    data.update({"file-types": values})

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
    dependencies=[Depends(auth_header)]
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
