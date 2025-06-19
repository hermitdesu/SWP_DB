from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId


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


class LogIn(BaseModel):
    user_id: str
    activity_id: str
    type: str = Field(min_length=1, max_length=50)
    value: float
    start_time: datetime
    completion_time: datetime
    build_version: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class LogDB(LogIn):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)