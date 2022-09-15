import pydantic as pydantic

#CHANGE LATER!
class UserAcc(pydantic.BaseModel):
    username:str
    password:str

class User(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    username: str
    password: str
    class Config:
        orm_mode = True

