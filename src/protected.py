import json
import logging
import os
from typing import Union

from fastapi import APIRouter, Request, HTTPException
from pydantic_core import ValidationError
from starlette.responses import FileResponse

from src.commons import settings, data, installed_repos_configs, __version__
from src.models.assistant_datamodel import RepoAssistantDataModel

router = APIRouter()


@router.get("/settings", include_in_schema=False)
async def get_settings():
    return settings


@router.get('/logs', include_in_schema=False)
async def get_log():
    return FileResponse(path=f"{os.environ['BASE_DIR']}/logs/rsas.log", filename="rsas.log", media_type='text/plain')


@router.get("/refresh", include_in_schema=False)
async def do_refresh():
    logging.debug("do_refresh")
    logging.debug(f'Before clear: {list(data.keys())}')
    logging.debug("clear the data")
    data.clear()
    logging.debug(f'After clear: {list(data.keys())}')
    installed_repos_configs()
    logging.debug(f'Available repositories configurations: {sorted(list(data.keys()))}')
    print("update version")
    data.update({"service-version": f"{__version__}-refreshed"})
    repos = [akm for akm in list(data.keys()) if akm != 'service-version']
    logging.debug(data["service-version"])
    logging.debug(f'After refresh: {list(data.keys())}')
    return {"repositories": repos}


@router.get('/{name}')
def get_name_from_repositories_list(name: str):
    logging.debug(f'get_name_from_repositories_list - name: {name}')
    logging.debug(f'{data.keys()}')
    if name in data.keys():
        logging.debug(f'{name} FOUND')
        try:
            return data[name].model_dump_json(by_alias=True, exclude_none=True)
        except Exception as e:
            logging.error(f'{name} does not {e}')
    else:
        logging.debug(f'{name} does not exist')
    raise HTTPException(404, f"{name} not found")


@router.post('/upload-repo', status_code=201)
async def upload_repository(submitted_repo_conf: Request, overwrite: Union[bool, None] = False):
    content_type = submitted_repo_conf.headers['Content-Type']
    if content_type != 'application/json':
        raise HTTPException(status_code=400, detail=f'Content type {content_type} not supported')

    repo_conf_json = await submitted_repo_conf.json()
    try:
        repo_assistant = RepoAssistantDataModel.model_validate(repo_conf_json)
        if not overwrite and repo_assistant.assistant_config_name in data.keys():
            raise HTTPException(status_code=400, detail=f'Repository Configuration "'
                                                        f'{repo_assistant.assistant_config_name}" exist.'
                                                        f'You can use "/upload-repo?overwrite=true"')
        else:
            data.update({repo_assistant.assistant_config_name: repo_assistant})
            with open(os.path.join(settings.repositories_conf_dir,
                                   f'{repo_assistant.assistant_config_name}.json'), mode="w+") as file:
                file.write(json.dumps(repo_conf_json))
            return {"saved-conf": repo_assistant.assistant_config_name}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f'Repository Configuration {e.with_traceback(e.__traceback__)}')


@router.delete("/delete-repo/{name}")
def delete_repository(name: str):
    if name not in data:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")

    for repo_conf_filename in os.listdir(settings.repositories_conf_dir):
        repo_conf_file = os.path.join(settings.repositories_conf_dir, repo_conf_filename)
        with open(repo_conf_file, "r") as f:
            repo_conf_json = json.loads(f.read())
            if repo_conf_json['name'] == name:
                os.remove(repo_conf_json)
                data.pop(name)
                return {"deleted": name}
