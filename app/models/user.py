from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from typing import Optional, Literal, List
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source, _handler):
        import pydantic_core
        return pydantic_core.core_schema.str_schema()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class Message(BaseModel):
    sender: Literal["user", "bot"]
    text: str = Field(min_length=1)
    time: datetime

    model_config = ConfigDict(extra="forbid")


class Conversation(BaseModel):
    messages: List[Message]

    model_config = ConfigDict(extra="forbid")


class UserIn(BaseModel):
    tg_id: Optional[int] = Field(gt=0)
    name: Optional[str] = Field(min_length=1, max_length=50)
    surname: Optional[str] = Field(min_length=1, max_length=50)
    gender: Literal["male", "female"]
    language: Literal["ru", "en"]
    recommendation_method: Optional[Literal["fixed", "kb", "cf"]] = None
    launch_count: int = 0
    current_bundle_version: Optional[int] = None
    bundle_version_at_install: Optional[int] = None

    model_config = ConfigDict(extra="forbid")


class UserDB(UserIn):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    conversations: List[Conversation] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
