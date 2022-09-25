from typing import List
import os
import fastapi as fastapi
import sqlalchemy.orm as orm
import boto3 as b3
from dotenv import load_dotenv

import schemas as schemas
import services as services
import sys
sys.path.append("..")
from auth import AuthHandler
load_dotenv()

pictures_router = fastapi.APIRouter()
auth_handler = AuthHandler()

#name=fastapi.Depends(auth_handler.auth_wrapper)
@pictures_router.get("/photos/{username}")
async def get_photos(
    username:str,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    photos = await services.get_photos_byUser(username=username,db=db)
    return photos

@pictures_router.get("/photos/{photo_id}")
async def get_photo(
    photo_id: int,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    photo = await services.get_photo_byID(db=db, photo_id=photo_id)
    if photo is None:
        raise fastapi.HTTPException(status_code=404, detail="Photo does not exist")
    return photo

@pictures_router.post("/photos/")
async def upload_photo(
    file: fastapi.UploadFile,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    s3 = b3.resource('s3', aws_access_key_id=os.getenv('AWS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_KEY'))
    bucket = s3.Bucket(os.getenv('S3_BUCKET'))
    bucket.upload_fileobj(file.file, file.filename, ExtraArgs={"ACL":"public-read"})
    file_url=f"https://{os.getenv('S3_BUCKET')}.s3.us-east-2.amazonaws.com/{file.filename}"
    print(file_url)
    photo=schemas.User_Photos(username="TEST_USER", file_url=file_url)
    await services.add_photo(_photo=photo, db=db)
    return {"Success":"Picture uploaded"}