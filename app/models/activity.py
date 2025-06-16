from pydantic import BaseModel
from typing import List, Optional


class ActivityIn(BaseModel):
    type : str
    items : Optional[List["ActivityDB"]] = None
    title : str


class ActivityDB(BaseModel):
    id : str
    type : str
    items : Optional[List["ActivityDB"]] = None
    title : str