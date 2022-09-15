import fastapi as fastapi

from routers import user_router

app = fastapi.FastAPI()
app.include_router(user_router.user_router, prefix="/user")
