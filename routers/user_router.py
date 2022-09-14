from typing import List

import fastapi as fastapi
import sqlalchemy.orm as orm

import schemas as schemas
import services as services

user_router = fastapi.APIRouter()

@user_router.post("/add/", response_model=schemas.User)
async def create_user(
    user: schemas.User,
    db: orm.Session = fastapi.Depends(services.get_db),
):
    return await services.create_user(user=user, db=db)


@user_router.get("/get_users/", response_model=List[schemas.User])
async def get_users(db: orm.Session = fastapi.Depends(services.get_db)):
    return await services.get_all_users(db=db)


@user_router.get("/get_users/{user_id}/", response_model=schemas.User)
async def get_user(
    user_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.get_User(db=db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User does not exist")

    return user


@user_router.delete("/delete/{user_id}/")
async def delete_contact(
    user_id: int, db: orm.Session = fastapi.Depends(services.get_db)
):
    user = await services.get_User(db=db, user_id=user_id)
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
    user = await services.get_User(db=db, user_id=user_id)
    if user is None:
        raise fastapi.HTTPException(status_code=404, detail="User does not exist")

    return await services.update_user(
        user_data=user_data, user=user, db=db
    )
