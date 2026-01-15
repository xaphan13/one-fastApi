from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    nickname: str
    firstname: str | None = None
    surname: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nickname: str | None = None
    firstname: str | None = None
    surname: str | None = None
    password: str | None = None

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
