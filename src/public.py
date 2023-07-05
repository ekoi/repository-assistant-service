import logging

from fastapi import APIRouter, HTTPException

import src
from src.commons import settings, data


router = APIRouter()

@router.get('/')
def info():
    logging.info("Repository Selection and Advice Service")
    logging.debug("info")
    return {"name": "Repository Selection and Advice Service", "version": src.main.__version__}



@router.get('/repositories')
def get_repositories_list():
    return data


@router.get('/repository/{name}')
def get_repositories_list(name: str):
    try:
        return data[name]
    except:
        raise HTTPException(404, f"{name} not found")