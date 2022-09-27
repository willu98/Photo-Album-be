import fastapi as fastapi
from fastapi.middleware.cors import CORSMiddleware

from routers import main_router
app = fastapi.FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(main_router.main_router, prefix="/")
