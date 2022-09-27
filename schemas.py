import pydantic as pydantic
import fastapi

class Photo_Submission(pydantic.BaseModel):
    user_filename: str
    file: fastapi.UploadFile

class User_Photos(pydantic.BaseModel):
    username:str
    user_filename: str
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

