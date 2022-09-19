import pydantic as pydantic

class User_Photos(pydantic.BaseModel):
    username:str
    file_url:str
    class Config:
        orm_mode = True
            
class UserAcc(pydantic.BaseModel):
    username:str
    password:str

class User(UserAcc):
    name: str
    class Config:
        orm_mode = True

