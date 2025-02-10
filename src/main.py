import json
import logging
import os
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from typing import Annotated

import emoji
import jmespath
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from keycloak import KeycloakOpenID, KeycloakAuthenticationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from src import protected, public
from src.commons import data, settings, installed_repos_configs, project_details

api_keys = [settings.DANS_REPO_ASSISTANT_SERVICE_API_KEY]
security = HTTPBearer()

from akmi_utils import otel, logging as akmi_logging

APP_NAME = os.environ.get("APP_NAME", "Repository Assistant Service")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 2810)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://localhost:4317")

def auth_header(request: Request, auth_cred: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
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
            logging.info(f"Error: {e}")

@asynccontextmanager
async def lifespan(application: FastAPI):
    logging.info('start up')
    installed_repos_configs()
    logging.info(f'Available repositories configurations: {sorted(list(data.keys()))}')
    logging.info(emoji.emojize(':thumbs_up:'))
    with open(settings.repo_file_types) as file:
        file_types = json.load(file)
    values = jmespath.search('[*].value', file_types)
    data.update({"file-types": values})

    yield

app = FastAPI(title= project_details['title'], description = project_details['description'],
              version= project_details['version'], lifespan=lifespan)

LOG_FILE = settings.LOG_FILE

app.add_middleware(otel.PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", otel.metrics)

otel.setting_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)

logging.getLogger("uvicorn.access").addFilter(otel.MetricsEndpointFilter())
logging.getLogger("uvicorn.access").addFilter(otel.TraceContextFilter())

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [%(funcName)s] "
    "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=10)
file_handler.setFormatter(logging.Formatter(log_config["formatters"]["access"]["fmt"]))
logging.getLogger().addHandler(file_handler)
# Set the logging level for h11 to ERROR
logging.getLogger("h11").setLevel(logging.ERROR)
file_handler.setLevel(logging.INFO)


@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        logging.error(f"404 Not Found: {request.url}")
        return JSONResponse(
            status_code=404,
            content={"message": "Endpoint not found"}
        )
    logging.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    return await akmi_logging.log_requests(request, call_next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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




if __name__ == "__main__":


    uvicorn.run(app, host="0.0.0.0", port=EXPOSE_PORT, log_config=log_config)