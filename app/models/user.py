from pydantic import BaseModel, Field
from typing import Literal


class UserIn(BaseModel):
    telegram_id : int = Field(gt=0)
    name: str = Field(min_length=1, max_length=50)
    surname : str = Field(min_length=1, max_length=50)
    gender : Literal["male", "female"]
    language : Literal["ru", "eng"]
    
    recommendation_method : Literal[""] | None
    launch_count : int = 0
    current_bundle_version : None
    bundle_version_at_install : None


class UserDB(BaseModel):
    id : id
    telegram_id : int = Field(gt=0)
    name: str = Field(min_length=1, max_length=50)
    surname : str = Field(min_length=1, max_length=50)
    gender : Literal["male", "female"]
    language : Literal["ru", "eng"]

    recommendation_method : Literal[""] | None
    launch_count : int = 0
    current_bundle_version : None
    bundle_version_at_install : None