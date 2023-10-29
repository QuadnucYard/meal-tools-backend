from pydantic import BaseModel

from app.crud.base import CRUDBase
from app.models.weigh import Weigh


class CRUDWeigh(CRUDBase[Weigh, BaseModel, BaseModel]):
    ...


weigh = CRUDWeigh(Weigh)
