from pydantic import BaseModel


class LearnerIn(BaseModel):
    gender : str
    language : str
    prior_knowledge : str
    goal : str


class LearnerDB(BaseModel):
    id : int
    gender : str
    language : str
    prior_knowledge : str
    goal : str