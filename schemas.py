import pydantic as pydantic


class User(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    class Config:
        orm_mode = True

