from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.food import Food


class CRUDFood(CRUDBase[Food, BaseModel, BaseModel]):
    ...


food = CRUDFood(Food)
