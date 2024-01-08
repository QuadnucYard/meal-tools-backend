from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.food import Food
from app.routers import deps
from app.schemas.food import FoodCreate, FoodRead, FoodReadWithStats, FoodReadWithVariants, FoodUpdate

router = APIRouter()


async def dep_get_food(
    food_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    return await crud.food.get_one(db, food_id)


async def dep_get_food_x(
    food_id: int,
    db: AsyncSession = Depends(deps.get_db),
):
    food = await crud.food.get_x(db, food_id)
    if not food:
        raise HTTPException(404, "Can't find food!")
    return food


@router.get("/", response_model=list[FoodReadWithStats])
async def get_foods(
    db: AsyncSession = Depends(deps.get_db),
):
    rows = await crud.food.get_with_weight(db)
    return await db.run_sync(
        lambda _: [
            FoodReadWithStats(
                **FoodReadWithVariants.model_validate(row[0]).model_dump(),
                weight_cnt=row[1],
                weight_avg=row[2],
                weight_std=row[3],
            )
            for row in rows
        ]
    )


@router.get("/{food_id}", response_model=FoodReadWithVariants)
async def get_food(
    food: Food = Depends(dep_get_food_x),
):
    return food


@router.post("/", response_model=FoodReadWithVariants)
async def add_food(
    body: FoodCreate,
    db: AsyncSession = Depends(deps.get_db),
):
    food = await crud.food.create(db, body)
    return await FoodReadWithVariants.model_validate_async(food)


@router.put("/{food_id}", response_model=FoodReadWithVariants)
async def update_food(
    body: FoodUpdate,
    food: Food = Depends(dep_get_food_x),
    db: AsyncSession = Depends(deps.get_db),
):
    if body.tags:
        food.tags = await crud.tag.get_ones(db, body.tags)
    return await crud.food.update(db, db_obj=food, obj_in=body, exclude={"tags"})


@router.get("/rec", response_model=list[FoodRead])
async def get_recommendations(
    db: AsyncSession = Depends(deps.get_db),
    limit: int = 10,
):
    return await crud.weigh.get_recent_foods(db, limit=limit)
