from pydantic import BaseModel
from datetime import datetime


class engagementIn(BaseModel):
    learned_id : str
    activity_id : str
    type : str
    value : float
    start_date : datetime
    completion_date : datetime


class engagementDB(BaseModel):
    id : str
    learned_id : str
    activity_id : str
    type : str
    value : float
    start_date : datetime
    completion_date : datetime