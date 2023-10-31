from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.food import Food
from app.routers import deps
from app.schemas.food import FoodCreate, FoodRead, FoodUpdate

router = APIRouter()


async def dep_get_food(
    food_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    food = await crud.food.get(db, food_id)
    if not food:
        raise HTTPException(404, "Can't find food!")
    return food


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


@router.put("/{food_id}", response_model=FoodRead)
async def update_food(
    body: FoodUpdate,
    food: Food = Depends(dep_get_food),
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.food.update(db, db_obj=food, obj_in=body)


@router.get("/rec", response_model=list[FoodRead])
async def get_recommendations(
    db: AsyncSession = Depends(deps.get_db),
    limit: int = 10,
):
    return await crud.weigh.get_recent_foods(db, limit=limit)
