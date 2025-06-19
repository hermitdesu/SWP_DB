from pydantic import BaseModel, Field
from datetime import datetime


class MessaegeIn(BaseModel):
    user_id : int = Field(gt=0)
    text : str = Field(min_length=1, max_length=500)
    date : datetime


class MessageDB(BaseModel):
    id : id
    user_id : int = Field(gt=0)
    text : str = Field(min_length=1, max_length=500)
    date : datetime