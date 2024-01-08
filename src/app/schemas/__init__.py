from .base import *
from .canteen import *
from .food import *
from .page import *
from .tag import *
from .weigh import *

FoodReadWithVariants.model_rebuild()
TagReadWithFoods.model_rebuild()
