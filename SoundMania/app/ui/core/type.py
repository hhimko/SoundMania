from typing import Type

from core.core import EvalAttrProxy

_TupleI3 = tuple[int,int,int]
_TupleI4 = tuple[int,int,int,int]


_SizeUnitOrStr = float | EvalAttrProxy | str
_SizeRect = tuple[_SizeUnitOrStr, _SizeUnitOrStr, _SizeUnitOrStr, _SizeUnitOrStr]
