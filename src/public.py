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
    logging.debug("get_repositories_list")
    repos = [akm for akm in list(data.keys()) if akm != 'service-version']
    return {"repositories": repos}


@router.get('/info')
def info():
    logging.info("Repository Selection and Advice Service")
    logging.debug("info")
    return project_details

@router.get('/error')
def error():
    logging.error("Repository Selection and Advice Service")
    logging.debug("error")
    return HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/error2')
def error2():
    logging.error("------Repository Selection and Advice Service-----")
    x = 1 / 0
    logging.error("This will not be logged")
    return HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/error_test")
async def error_test(response: Response):
    logging.error("got error!!!!")
    raise ValueError("value error")