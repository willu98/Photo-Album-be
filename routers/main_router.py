import fastapi
import user_router, pictures_router
main_router = fastapi.APIRouter()

main_router.include_router(user_router.user_router, prefix="/user")
main_router.include_router(pictures_router.pictures_router, prefix="/photos")