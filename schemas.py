from pydantic import BaseModel


class SpiderBase(BaseModel):
    genus: str
    name: str | None = None
    molt: int | None = None
    size: float | None = None
    sex: str | None = None
    info: str | None = None


class Spider(SpiderBase):
    id: int
    owner_id = int

    class Config:
        orm_mode = True

class SpiderCreate(SpiderBase):
    pass


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Spider] = []

    class Config:
        orm_mode = True
        