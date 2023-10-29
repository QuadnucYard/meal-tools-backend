from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.routers import deps
from app.schemas.food import FoodCreate, FoodRead

router = APIRouter()


@router.get("/", response_model=list[FoodRead])
async def get_foods(
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.food.get_many(db, limit=10000)


@router.post("/", response_model=FoodRead)
async def add_food(
    body: FoodCreate,
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.food.create(db, body)
