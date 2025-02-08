from typing import TYPE_CHECKING, List

import database.database as db_
import database.db_models as models
import schemas as schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def _add_tables():
    return db_.Base.metadata.create_all(bind=db_.engine)

    
def get_db():
    db = db_.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def create_user(
    user: schemas.User, 
    db: "Session"
) -> schemas.User:
    user = models.User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.User.from_orm(user)


async def get_all_users(db: "Session") -> List[schemas.User]:
    users = db.query(models.User).all()
    return list(map(schemas.User.from_orm, users))


async def get_user_byID(user_id: int, db: "Session"):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user

async def get_user_byName(username: str, db: "Session") -> schemas.User:
    user = db.query(models.User).filter(models.User.username == username).first()
    return user
    
async def delete_user(user: models.User, db: "Session"):
    db.delete(user)
    db.commit()


async def update_user(
    user_data: schemas.User, 
    user: models.User, 
    db: "Session"
) -> schemas.User:
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name
    user.email = user_data.email
    user.phone_number = user_data.phone_number

    db.commit()
    db.refresh(user)

    return schemas.User.from_orm(user)

async def get_photo_byID(
    photo_id:int,
    db: "Session"
):
    photo = db.query(models.User_Photos).get(photo_id)
    return photo

async def get_photos_byUser(
    username: str,
    db: "Session"
) -> List[schemas.User_Photos]:
    photos = db.query(models.User_Photos).filter(models.User_Photos.username == username).all()
    return list(map(schemas.User_Photos.from_orm, photos))

async def get_photo_by_filename(
    filename: str,
    db: "Session"
):
    return db.query(models.User_Photos).filter(models.User_Photos.user_filename == filename).first()
    
async def get_photo_by_file_url(
    file_url: str,
    db: "Session"
):
    return db.query(models.User_Photos).filter(models.User_Photos.file_url == file_url).first()

async def add_photo(
    _photo: schemas.User_Photos,
    db: "Session"
): 
    photo=models.User_Photos(**_photo.dict())
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return schemas.User_Photos.from_orm(photo)

async def delete_photo(photo:schemas.User_Photos,db:"Session"):
    db.delete(photo)
    db.commit()