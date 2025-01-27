import logging
import random
import time

import httpx
from fastapi import APIRouter, HTTPException, Response, Request
from opentelemetry.propagate import inject

from src.commons import data, project_details

router = APIRouter()


@router.get('/repositories')
def get_repositories_list():
    repos = [akm for akm in list(data.keys()) if akm != 'service-version']
    return {"repositories": repos}


@router.get('/info')
def info():
    logging.info("Repository Selection and Advice Service")
    logging.debug("info")
    return project_details
