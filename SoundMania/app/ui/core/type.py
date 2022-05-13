from typing import Type

from core.core import EvalAttrProxy

_TupleI3 = tuple[int,int,int]
_TupleI4 = tuple[int,int,int,int]

_ColorRGBA = _TupleI3
_ColorRGB = _TupleI4

_Unit = float | EvalAttrProxy
_UnitRect = tuple[_Unit, _Unit, _Unit, _Unit]
