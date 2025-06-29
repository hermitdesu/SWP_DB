from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal


class UserIn(BaseModel):
    id: Optional[int] = Field(default=None, alias="_id")
    name: str = Field(min_length=1, max_length=50)

    model_config = ConfigDict(extra="forbid")


class UserDB(UserIn):
    gender: Optional[Literal["male", "female"]] = None
    language: Optional[Literal["ru", "en"]] = None
    recommendation_method: Optional[Literal["fixed", "kb", "cf"]] = None
    launch_count: int = 0
    current_bundle_version: Optional[int] = None
    bundle_version_at_install: Optional[int] = None

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class UserOut(UserDB):
    pass