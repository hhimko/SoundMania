from __future__ import annotations
from functools import cached_property
from typing import Iterable

import pygame

from ui.core.type import _SizeRect, _SizeUnitOrStr, _TupleI3, _TupleI4
from ui.core.units import ph, pw, vh, vw
from core.core import EvalAttrProxy
        
        
class UIComponent:
    """ Base class defining a renderable UI element. """
    def __init__(self, name: str, size_rect: _SizeRect | pygame.Rect, **kwargs):
        self.name = name
        self._parent: UIComponent | None = None
        
        self._hidden = False
        self.is_dirty = True # forces the surface to be redrawn on first render

        self._x, self._y, self._width, self._height = self._parse_size_rect(size_rect)
        self.surface = pygame.surface.Surface(self.size)

        # TODO: extract optional component modules 
        self._is_centered = False
        self._color: _TupleI4 = (0,0,0,0)

        self._text = ''
        self._text_size = self._height
        self._text_color: _TupleI4 = (0,0,0,0)

        self.config(**kwargs)
        self.postinit()
        
        
    @property
    def parent(self) -> UIComponent | None:
        return self._parent
    
    
    @parent.setter
    def parent(self, value: UIComponent | None) -> None:
        if self.parent and value != self.parent:
            raise ValueError(f"object {self} already has a parent {self.parent} assigned")
        
        self._parent = value
        self._on_window_resize() # mandatory for components with size units relative to their parents
        
        
    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y
    
    
    @position.setter
    def position(self, value: tuple[_SizeUnitOrStr, _SizeUnitOrStr]) -> None:
        self.x, self.y = value
        
        
    @property
    def x(self) -> float:
        attr = self._x
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr
    
    
    @x.setter
    def x(self, value: _SizeUnitOrStr) -> None:
        if isinstance(value, str):
            value = self._parse_unit_str(value)
        self._x = value
        self._winpos_recompute()
        
        
    @property
    def y(self) -> float:
        attr = self._y
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr
    
    
    @y.setter
    def y(self, value: _SizeUnitOrStr) -> None:
        if isinstance(value, str):
            value = self._parse_unit_str(value)
        self._y = value
        self._winpos_recompute()
        

    @property
    def width(self) -> float:
        attr = self._width
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr


    @width.setter
    def width(self, value: _SizeUnitOrStr) -> None:
        if isinstance(value, str):
            value = self._parse_unit_str(value)
        self._width = value
        
        self.is_dirty = True
        if self.centered:
            self._winpos_recompute()


    @property
    def height(self) -> float:
        attr = self._height
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr


    @height.setter
    def height(self, value: _SizeUnitOrStr) -> None:
        if isinstance(value, str):
            value = self._parse_unit_str(value)
        self._height = value
        
        self.is_dirty = True
        if self.centered:
            self._winpos_recompute()
        
        
    @property
    def size(self) -> tuple[float, float]:
        return self.width, self.height
    
    
    @size.setter
    def size(self, value: tuple[_SizeUnitOrStr, _SizeUnitOrStr]) -> None:
        self.width, self.height = value
        
        
    @property
    def hidden(self) -> bool:
        return self._hidden
    
    
    @hidden.setter
    def hidden(self, value: bool) -> None:
        self._hidden = value
        

    @property
    def centered(self) -> bool:
        return self._is_centered
    
    
    @centered.setter
    def centered(self, value: bool) -> None:
        self._is_centered = value
        self._winpos_recompute()
        

    @property
    def color(self) -> _TupleI3 | _TupleI4:
        return self._color[:3] if self._color[3] == 255 else self._color

    
    @color.setter
    def color(self, value: _TupleI3 | _TupleI4) -> None:
        self._color = value if len(value) == 4 else value + (255, )
        self.is_dirty = True


    @property
    def text(self) -> str:
        return self._text


    @text.setter
    def text(self, value: str) -> None:
        self._text = value.strip()
        self.is_dirty = True

    
    @property
    def text_size(self) -> int:
        attr = self._text_size
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return int(attr)

    
    @text_size.setter
    def text_size(self, value: int) -> None:
        self._text_size = value
        if self.text:
            self.is_dirty = True


    @property
    def text_color(self) -> _TupleI3 | _TupleI4:
        return self._text_color if self._text_color[3] == 255 else self._text_color

    
    @text_color.setter
    def text_color(self, value: _TupleI3 | _TupleI4) -> None:
        self._text_color = value if len(value) == 4 else value + (255, )
        if self.text:
            self.is_dirty = True
            
            
    def config(self, **kwargs) -> None:
        """ Set all overwritable attributes passed as keyword arguments. """
        for k, v in kwargs.items():
            attr = getattr(type(self), k)

            if not isinstance(attr, property) and callable(attr):
                raise AttributeError(f"can't overwrite attribute '{k}' of object '{type(self).__name__}'")
                
            setattr(self, k, v)
            
            
    def postinit(self) -> None:
        """ Special method called once right after the object initialization.
        
            By defalt this method does nothing and is supposed to be overwritten in child classes.
            `postinit()` was made to simplify child classes which do not need to override __init__. 
        """
        pass
            
            
    def get_rect(self) -> pygame.Rect:
        """ Return a new pygame `Rect` object of this components' size with position absolute to the screen. """
        return pygame.Rect(self._winpos, self.size)
    

    def update(self, dt: int) -> None:
        """ Update the current element state. 
        
            Args:
                dt: elapsed time since the last frame
        """
        pass


    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame `Surface` object on which to render
        """
        if not self.hidden:
            if self.is_dirty:
                self._redraw_surface()
                
            surface.blit(self.surface, self._winpos)
            
        
    @cached_property
    def _winpos(self) -> tuple[float, float]:
        x, y = self.position
        
        if self.centered:
            pw, ph = self.parent.size if self.parent else pygame.display.get_window_size()
            sw, sh = self.size
            x, y = (pw/2 + x - sw/2, ph/2 + y - sh/2)
        
        return (x + self.parent._winpos[0], y + self.parent._winpos[1]) if self.parent else (x, y)
    
    
    def _winpos_recompute(self) -> None:
        try:
            del self._winpos
        except AttributeError:
            pass
        
        
    def _redraw_surface(self) -> None:
        """ Executed before render when `self.is_dirty` is set to `True`. """
        self.surface.fill(self.color)
        if self.text:
            self._redraw_text()
            
        self.is_dirty = False


    def _redraw_text(self) -> None:
        overlay = pygame.font.Font(None, int(self.text_size)).render(self.text, True, self.text_color)
        self.surface.blit(overlay, (0,0))
        
        
    def _on_window_resize(self) -> None:
        self.surface = pygame.surface.Surface(self.size)
        self.is_dirty = True
        
        self._winpos_recompute()
        
        
    @staticmethod
    def _parse_size_rect(rect: _SizeRect | pygame.Rect) -> Iterable[float | EvalAttrProxy]:
        if isinstance(rect, pygame.Rect):
            return rect.x, rect.y, rect.w, rect.h
        
        size: list[float | EvalAttrProxy] = [0, 0, 0, 0]
        for i, value in enumerate(rect):
            if isinstance(value, (int, float, EvalAttrProxy)):
                size[i] = value 
            elif isinstance(value, str):
                size[i] = UIComponent._parse_unit_str(value)
            else:
                raise ValueError(f"invalid unit type. expected type 'float | Unit | str', got '{type(value)}'")
        return size
    
    
    @staticmethod
    def _parse_unit_str(value: str) -> float | EvalAttrProxy:
        str_to_unit: dict[str, type[EvalAttrProxy]] = {
            "vw": vw,
            "vh": vh,
            "pw": pw,
            "ph": ph
        }
        
        
        value = value.strip()
        if value[-2:] in str_to_unit:
            unit_wrapper = str_to_unit[value[-2:]]
            try:
                return unit_wrapper(float(value[:-2]))
            except ValueError:
                raise ValueError(f"invalid unit '{value}'")
        else:
            try:
                return float(value)
            except ValueError:
                raise ValueError(f"invalid unit '{value}'")
            