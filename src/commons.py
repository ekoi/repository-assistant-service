import importlib.metadata
import json
import logging
import os

import tomli
from dynaconf import Dynaconf
from pydantic import ValidationError

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
                try:
                    print(f'repo_conf_filename: {repo_conf_filename}')
                    saved_repo_assistant = json.loads(f.read())
                    repo_assistant = RepoAssistantDataModel.model_validate(saved_repo_assistant)
                    if repo_assistant.assistant_config_name in data:
                        logging.warning(
                            f"Configuration {repo_assistant.assistant_config_name} already exists and will be overwritten.")
                        print(f'>>>> Configuration {repo_assistant.assistant_config_name} already exists and will be overwritten.')
                    data.update({repo_assistant.assistant_config_name: repo_assistant})
                    logging.info(f"Loaded valid: {repo_assistant.assistant_config_name} in {repo_conf_filename}")
                    print(f"Loaded valid: {repo_assistant.assistant_config_name} in {repo_conf_filename}")
                except json.JSONDecodeError as e:
                    logging.error(f"Error loading {repo_conf_filename}: {e}")
                    print(f">>> Error: {repo_conf_filename}, caused by {e}")
                    continue
                except ValidationError as e:
                    logging.error(f"Error validating: {e}")
                    print(f">>> Error: {repo_conf_filename}, caused by {e}")
                    continue
                


def get_version():
    with open(os.path.join(os.getenv("BASE_DIR"), 'pyproject.toml'), 'rb') as file:
        package_details = tomli.load(file)
    return package_details['tool']['poetry']['version']

def get_name():
    with open(os.path.join(os.getenv("BASE_DIR"), 'pyproject.toml'), 'rb') as file:
        package_details = tomli.load(file)
    return package_details['tool']['poetry']['name']
