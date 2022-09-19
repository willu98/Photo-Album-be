import fastapi as fastapi
from fastapi.middleware.cors import CORSMiddleware

from routers import user_router, pictures_router
app = fastapi.FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.user_router, prefix="/user")
app.include_router(pictures_router.pictures_router, prefix="/photos")