from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.canteen import Canteen


class CRUDCanteen(CRUDBase[Canteen, BaseModel, BaseModel]):
    ...


canteen = CRUDCanteen(Canteen)
