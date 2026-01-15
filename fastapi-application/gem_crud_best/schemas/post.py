from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostRead(PostBase):
    id: int
    time_created: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)
