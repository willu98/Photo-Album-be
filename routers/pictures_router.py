from typing import List
import os
import fastapi as fastapi
import sqlalchemy.orm as orm
import boto3 as b3
from dotenv import load_dotenv

import string
import random
import re
import schemas as schemas
import services as services
import sys
sys.path.append("..")
from auth import AuthHandler
load_dotenv()

pictures_router = fastapi.APIRouter()
auth_handler = AuthHandler()

def filename_generator(size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#name=fastapi.Depends(auth_handler.auth_wrapper)
@pictures_router.get("/")
async def get_photos(
    username=fastapi.Depends(auth_handler.auth_wrapper),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    photos = await services.get_photos_byUser(username=username,db=db)
    return {"response": photos}

@pictures_router.get("/id/{photo_id}")
async def get_photo(
    photo_id: int,
    db: orm.Session = fastapi.Depends(services.get_db),
    username=fastapi.Depends(auth_handler.auth_wrapper)
):
    photo = await services.get_photo_byID(db=db, photo_id=photo_id)
    if photo is None:
        return {"message": "Photo does not exist"}
    if photo.username != username:
        return {"message": "You are not authorized to view this photo"}
    return {"response": photo}

@pictures_router.post("/")
async def upload_photo(
    file: fastapi.UploadFile,
    user_filename: str,
    username=fastapi.Depends(auth_handler.auth_wrapper),
    db: orm.Session = fastapi.Depends(services.get_db)
):
    fileExtension = re.search(".[0-9a-z]+$", file.filename, re.IGNORECASE)
    print(fileExtension.group(0))
    if fileExtension is None:
        return {"message": f"Failed to parse extension for file: {file.filename}"}

    filename = f"{filename_generator()}{fileExtension.group(0)}"

    while ((await services.get_photo_by_filename(filename=filename, db=db)) != None):
        filename = f"{filename_generator()}{fileExtension.group(0)}"
        
    s3 = b3.resource('s3', aws_access_key_id=os.getenv('AWS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_KEY'))
    bucket = s3.Bucket(os.getenv('S3_BUCKET'))
    bucket.upload_fileobj(file.file, filename, ExtraArgs={"ACL":"public-read"})
    
    file_url=f"https://{os.getenv('S3_BUCKET')}.s3.us-east-2.amazonaws.com/{filename}"
    photo=schemas.User_Photos(username=username, file_url=file_url, user_filename=user_filename)
    await services.add_photo(_photo=photo, db=db)
    return {"response": {
        "file_url": photo.file_url,
    }}

@pictures_router.delete("/delete/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    photo = await services.get_photo_byID(photo_id, db)
    if photo is None:
        return {"message": f"Failed to find photo with ID: {photo_id}"}

    await services.delete_photo(photo)
    return {"response": "Success"}
