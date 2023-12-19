import json
import os
from typing import Union

from fastapi import APIRouter, Request, HTTPException
from pydantic_core import ValidationError
from starlette.responses import FileResponse

from src.commons import settings, data
from src.models.assistant_datamodel import RepoAssistantDataModel

router = APIRouter()


@router.get("/settings", include_in_schema=False)
async def get_settings():
    return settings


@router.get('/logs', include_in_schema=False)
async def get_log():
    return FileResponse(path=f"{os.environ['BASE_DIR']}/logs/rsas.log", filename="rsas.log", media_type='text/plain')


@router.get('/{name}')
def get_repositories_list(name: str):
    print(f'name: {name}')
    try:
        return data[name].model_dump_json(by_alias=True, exclude_none=True)
    except:
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
                                   f'uploaded-{repo_assistant.assistant_config_name}.json'), mode="w+") as file:
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
