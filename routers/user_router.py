from typing import List

import fastapi as fastapi
import sqlalchemy.orm as orm

import schemas as schemas
import services as services
import sys
sys.path.append("..")
from auth import AuthHandler

user_router = fastapi.APIRouter()
auth_handler = AuthHandler()


@user_router.post("/register/", response_model=schemas.User, status_code=201)
async def create_user(
    user: schemas.User,
    db: orm.Session = fastapi.Depends(services.get_db),
):
    if await services.get_user_byName(username=user.username,  db=db) is not None:
        return {"Error":"Username already exists"}
    user.password = auth_handler.get_hashed_password(user.password)
    await services.create_user(user=user, db=db)
    return {"Success":"Account created"}


@user_router.post("/login/")
async def login_user(
    user: schemas.UserAcc,
    db: orm.Session = fastapi.Depends(services.get_db)
):
    user_db = await services.get_user_byName(username=user.username, db=db)
    if user_db is None:
        return {"Error":"Username not found"}
        
    if not auth_handler.verify_password(password=user.password, hashed_pass=user_db.password):
        raise fastapi.HTTPException(status_code=401, detail='Wrong password')
    token = auth_handler.encode_token(user.username)
    return { "token":token }



@user_router.get("/get_users/", response_model=List[schemas.User])
async def get_users(db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_all_users(db=db)


@user_router.get("/get_users/{user_id}/", response_model=schemas.User)
async def get_user(
    user_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.get_user_byID(db=db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User does not exist")

    return user


@user_router.delete("/delete/{user_id}/")
async def delete_contact(
    user_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.get_user_byID(db=db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="Contact does not exist")

    await services.delete_user(user, db=db)

    return "successfully deleted the user"


@user_router.put("/{user_id}/", response_model=schemas.User)
async def update_contact(
    user_id: int,
    user_data: schemas.User,
    db: orm.Session = fastapi.Depends(services.get_db),
):
    user = await services.get_user_byID(db=db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User does not exist")

    return await services.update_user(
        user_data=user_data, user=user, db=db
    )
