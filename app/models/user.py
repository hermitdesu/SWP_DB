from pydantic import BaseModel, Field, ConfigDict, GetJsonSchemaHandler
from bson import ObjectId
from typing import Optional, Literal, List, Any
from datetime import datetime
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler: GetJsonSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> dict:
        return {
            "type": "string",
            "format": "objectid",
        }


class Message(BaseModel):
    sender: Literal["user", "bot"]
    text: str = Field(min_length=1)
    time: datetime

    model_config = ConfigDict(extra="forbid")


class Conversation(BaseModel):
    messages: List[Message]

    model_config = ConfigDict(extra="forbid")


class UserIn(BaseModel):
    tg_id: int = Field(default=None, ge=0)
    name: str = Field(default=None, min_length=1, max_length=50)
    surname: str = Field(default=None, min_length=1, max_length=50)
    gender: Literal["male", "female"]
    language: Literal["ru", "en"]
    recommendation_method: Optional[Literal["fixed", "kb", "cf"]] = None
    launch_count: int = 0
    current_bundle_version: Optional[int] = None
    bundle_version_at_install: Optional[int] = None

    model_config = ConfigDict(extra="forbid")


class UserDB(UserIn):
    id: PyObjectId = Field(default=None, alias="_id")
    conversations: List[Conversation] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class UserOut(UserIn):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True)
