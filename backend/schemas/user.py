from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config():
        orm_mode = True
