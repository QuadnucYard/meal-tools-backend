from fastapi import APIRouter

from app.routers.endpoints import canteen, food, upload, weigh

api_router = APIRouter()
api_router.include_router(canteen.router, prefix="/canteen", tags=["canteen"])
api_router.include_router(food.router, prefix="/food", tags=["food"])
api_router.include_router(weigh.router, prefix="/weigh", tags=["weigh"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])


@api_router.get("/")
def ping():
    return "OK"
