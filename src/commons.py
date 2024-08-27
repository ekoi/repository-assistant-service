import importlib.metadata
import json
import logging
import os

from dynaconf import Dynaconf

from src.models.assistant_datamodel import RepoAssistantDataModel

settings = Dynaconf(settings_files=["conf/settings.toml", "conf/*.yaml", "conf/.secrets.toml"],
                    environments=True)
logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOG_LEVEL,
                    format=settings.LOG_FORMAT)
data = {}


def installed_repos_configs():
    logging.debug("startup")

    for repo_conf_filename in os.listdir(settings.repositories_conf_dir):
        if repo_conf_filename.endswith('.json'):
            with open(os.path.join(settings.repositories_conf_dir, repo_conf_filename)) as f:
                saved_repo_assistant = json.loads(f.read())
                repo_assistant = RepoAssistantDataModel.model_validate(saved_repo_assistant)
                data.update({repo_assistant.assistant_config_name: repo_assistant})


__version__ = importlib.metadata.metadata(settings.SERVICE_NAME)["version"]
