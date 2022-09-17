import fastapi as fastapi

from routers import user_router
from routers import pictures_router
app = fastapi.FastAPI()
app.include_router(user_router.user_router, prefix="/user")
app.include_router(pictures_router.pictures_router, prefix="/photos")