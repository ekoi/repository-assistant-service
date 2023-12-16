import logging

from fastapi import APIRouter, HTTPException

from src.commons import data

router = APIRouter()


@router.get('/repositories')
def get_repositories_list():
    repos = [akm for akm in list(data.keys()) if akm != 'service-version']
    return {"repositories": repos}


@router.get('/')
def info():
    logging.info("Repository Selection and Advice Service")
    logging.debug("info")
    return {"name": "Repository Selection and Advice Service", "version": data["service-version"]}