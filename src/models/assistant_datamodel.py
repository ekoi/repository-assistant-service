from __future__ import annotations

import json
from typing import List, Optional

from pydantic import BaseModel, Field


class TransformedMetadata(BaseModel):
    """
    Represents metadata for a transformed resource.

    Attributes:
    - name (str): The name of the transformed resource.
    - transformer_url (Optional[str]): The URL of the transformer, if applicable.
    - target_dir (str): The target directory for the transformed resource.
    - restricted (Optional[bool]): Indicates if the resource is restricted.
    """
    name: str
    transformer_url: Optional[str] = Field(None, alias='transformer-url')
    target_dir: Optional[str] = Field(None, alias='target-dir')
    restricted: Optional[bool] = None


class Metadata(BaseModel):
    """
    Represents metadata for a repository.

    Attributes:
    - specification (List[str]): A list of specifications associated with the repository.
    - transformed_metadata (List[TransformedMetadata]): A list of transformed metadata instances.
    """
    specification: List[str]
    transformed_metadata: List[TransformedMetadata] = Field(..., alias='transformed-metadata')


class Input(BaseModel):
    from_target_name: str = Field(default=None, alias='from-target-name')


class Target(BaseModel):
    """
    Represents a target in the repository assistant application.

    Attributes:
        repo_pid (str): A unique identifier for the repository. This field is required.
        repo_name (str): The name of the repository. This field is required.
        repo_display_name (str): The display name of the repository. This field is required.
        bridge_module_class (str): The class name of the bridge module. This field is required.
        base_url (str): The base URL of the repository. This field is required.
        target_url (str): The target URL of the repository. This field is required.
        username (str): The username for authentication. This field is required.
        password (str): The password for authentication. This field is required.
        metadata (Metadata): Metadata associated with the target repository. This field is required.
        initial_release_version (Optional[str]): The initial release version of the repository. This field is optional.
        input (Optional[Input]): Input data for the target. This field is optional.
    """
    repo_pid: str = Field(..., alias='repo-pid')
    repo_name: str = Field(..., alias='repo-name')
    repo_display_name: str = Field(..., alias='repo-display-name')
    bridge_module_class: str = Field(..., alias='bridge-module-class')
    base_url: str = Field(..., alias='base-url')
    target_url: str = Field(..., alias='target-url')
    username: str
    password: str
    metadata: Metadata
    initial_release_version: Optional[str] = Field(default=None, alias='initial-release-version')
    input: Optional[Input] = None


class FileConversion(BaseModel):
    """
    Represents a file conversion configuration.

    Attributes:
    - origin_type (str): The type of the original file.
    - target_type (str): The type of the target file after conversion.
    - conversion_url (str): The URL for the file conversion.
    """
    origin_type: str = Field(..., alias='origin-type')
    target_type: str = Field(..., alias='target-type')
    conversion_url: str = Field(..., alias='conversion-url')


class RepoAssistantDataModel(BaseModel):
    """
    Represents the configuration model for the repository assistant application.

    Attributes:
    - assistant_config_name (str): The name of the assistant configuration.
    - description (str): A description of the assistant configuration.
    - app_name (str): The name of the application.
    - app_config_url (str): The URL for the application configuration.
    - targets (List[Target]): A list of target configurations.
    - file_conversions (Optional[List[FileConversion]]): A list of file conversion configurations, if applicable.
    """
    assistant_config_name: str = Field(..., alias='assistant-config-name')
    description: str
    app_name: str = Field(..., alias='app-name')
    app_config_url: str = Field(..., alias='app-config-url')
    targets: List[Target]
    file_conversions: Optional[List[FileConversion]] = Field(None, alias='file-conversions')


json_rda = '''
{
    "assistant-config-name": "new-local.zenodo.org",
    "description": "",
    "app-name": "rda",
    "app-config-url": "https://",
    "targets": [
        {
            "repo-pid":"PLACE_HOLDER",
            "repo-name": "demo.zenodo.org",
            "repo-display-name": "Zenodo Dev Environment",
            "bridge-module-class": "ZenodoApiDepositor",
            "base-url": "https://zenodo.org",
            "target-url": "https://zenodo.org/api/deposit/depositions",
            "username": "PLACE_HOLDER",
            "password": "PLACE_HOLDER",
            "metadata": {
                "specification": [],
                "transformed-metadata": [
                    {
                        "name": "zenodo-dataset.json",
                        "transformer-url": "http://localhost:1745/transform/rda-form-metadata-to-zenodo-dataset-v1.xsl",
                        "target-dir": ""
                    },
                    {
                        "name": "zenodo-file.json",
                        "transformer-url": "http://localhost:1745/transform/form-metadata-to-dataverse-file-v1.xsl",
                        "target-dir": ""
                    }
                ]
            }
        }
    ],
    "file-conversions": [
        {
            "origin-type": "mov",
            "target-type": "mp4",
            "conversion-url": "https://"
        },
        {
            "origin-type": "mp4",
            "target-type": "mp3",
            "conversion-url": "https://"
        }
    ]
}

'''

# s = RepoAssistantDataModel(**json.loads(json_rda))
# print('xxx')
# t = s.model_dump_json(by_alias=True, exclude_none=True)
# # print(type(t))
# print(t)
