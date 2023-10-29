import sys
from inspect import Parameter, Signature, _empty, get_annotations
from typing import ForwardRef, Type

from sqlalchemy import inspect
from sqlalchemy.sql.schema import ScalarElementColumnDefault
from typing_extensions import _AnnotatedAlias

from app.models import *


def make_annotation(cls: Type[Base]):
    columns = cls.__table__.columns
    relationships = inspect(cls).relationships
    a = get_annotations(
        cls, globals=sys.modules[cls.__module__].__dict__ | sys.modules[Base.__module__].__dict__, locals=cls.__dict__
    )

    # cccc = a["rating"].__args__[0]
    def _get_annotation(a):
        if isinstance(a, _AnnotatedAlias):
            a = a.__args__[0]
        if isinstance(a, ForwardRef):
            a = a.__forward_arg__
        return a

    def _get_default(col):
        if isinstance(col.default, ScalarElementColumnDefault):
            return col.default.arg
        if col.nullable:
            return None
        if col.default or col.primary_key or col.foreign_keys:
            return ...
        # return getsource(d.expression._constructor) if hasattr(d, "expression")  else d
        return _empty

    # 有个问题现在relationship还没初始化完成
    sig = Signature(
        [Parameter("self", Parameter.POSITIONAL_OR_KEYWORD)]
        + [
            Parameter(
                col.key,
                kind=Parameter.KEYWORD_ONLY,
                default=_get_default(col),
                annotation=_get_annotation(a[col.key].__args__[0]),
            )
            for col in columns
        ]
        + [
            Parameter(
                rel.key,
                kind=Parameter.KEYWORD_ONLY,
                default=...,
                annotation=_get_annotation(a[rel.key].__args__[0]),
            )
            for rel in relationships
        ]
    )
    sig_str = str(sig).replace("Ellipsis", "...").replace("datetime.datetime", "datetime")
    print(cls.__name__)
    print(f"""    if TYPE_CHECKING:\n        def __init__{sig_str}: ...""")
    ...


def make_annotations():
    for t in Base.__subclasses__():
        make_annotation(t)


if __name__ == "__main__":
    ss = Base.__subclasses__()
    make_annotations()
