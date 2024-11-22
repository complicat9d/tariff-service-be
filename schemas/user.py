from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    password: str
    username: str


class UserSchema(UserBaseSchema):
    id: int


class UserCreateSchema(UserBaseSchema):
    pass
