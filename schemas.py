import pydantic as pydantic

#CHANGE LATER!
class UserAcc(pydantic.BaseModel):
    username:str
    password:str

class User(UserAcc):
    name: str
    class Config:
        orm_mode = True

