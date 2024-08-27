from __future__ import annotations

from enum import StrEnum, auto
from typing import Optional

from pydantic import BaseModel, HttpUrl, Field


class DepositType(StrEnum):
    DATASET = auto()
    CODE = auto()
    REPORT = auto()
    PUBLICATION = auto()


class RepositoryAdviceModel(BaseModel):
    affiliation: HttpUrl
    domain: HttpUrl
    deposit_type: DepositType = Field(..., alias='deposit-type')
    file_type: Optional[str] = Field(None, alias='file-type')