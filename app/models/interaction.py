from pydantic import BaseModel, Field
from datetime import datetime


class InteractionIn(BaseModel):
    user_id : int = Field(gt=0)
    activity_id : str = Field(min_length=1, max_length=50)
    type : str = Field(min_length=1, max_length=50)
    value : float
    start_date : datetime
    completion_date : datetime


class InteractiontDB(BaseModel):
    id : id
    user_id : int = Field(gt=0)
    activity_id : str = Field(min_length=1, max_length=50)
    type : str = Field(min_length=1, max_length=50)
    value : float
    start_date : datetime
    completion_date : datetime