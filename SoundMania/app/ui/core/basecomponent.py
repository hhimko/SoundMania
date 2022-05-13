from __future__ import annotations
from functools import cached_property

import pygame

from ui.core.type import _ColorRGB, _ColorRGBA, _Unit, _UnitRect
from core.core import EvalAttrProxy


def _read_size_from_rect(rect: _UnitRect | pygame.Rect) -> _UnitRect:
    if isinstance(rect, pygame.Rect):
        return rect.x, rect.y, rect.w, rect.h
    return rect
        
    
class UIComponent:
    """ Abstract class defining a renderable UI element. """
    def __init__(self, name: str, rect: _UnitRect | pygame.Rect, **kwargs):
        self.name = name
        self._parent: UIComponent | None = None
        
        self._hidden = False
        self.is_dirty = True # forces the surface to be redrawn on first render

        self._x, self._y, self._width, self._height = _read_size_from_rect(rect)
        self.surface = pygame.surface.Surface(self.size)

        # TODO: extract optional component modules 
        self._is_centered = False
        self._color: _ColorRGB | _ColorRGBA = (0,0,0)

        self._text = ''
        self._text_size = self._height
        self._text_color: _ColorRGB | _ColorRGBA = (0,0,0)

        self.config(**kwargs)
        
        
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
    def position(self, value: tuple[_Unit, _Unit]) -> None:
        self.x, self.y = value
        
        
    @property
    def x(self) -> float:
        attr = self._x
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr
    
    
    @x.setter
    def x(self, value: _Unit) -> None:
        self._x = value
        self._winpos_recompute()
        
        
    @property
    def y(self) -> float:
        attr = self._y
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr
    
    
    @y.setter
    def y(self, value: _Unit) -> None:
        self._y = value
        self._winpos_recompute()
        

    @property
    def width(self) -> float:
        attr = self._width
        if isinstance(attr, EvalAttrProxy):
            return attr.evaluate(self)
        
        return attr


    @width.setter
    def width(self, value: _Unit) -> None:
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
    def height(self, value: _Unit) -> None:
        self._height = value
        
        self.is_dirty = True
        if self.centered:
            self._winpos_recompute()
        
        
    @property
    def size(self) -> tuple[float, float]:
        return self.width, self.height
    
    
    @size.setter
    def size(self, value: tuple[_Unit, _Unit]) -> None:
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
    def color(self) -> _ColorRGB | _ColorRGBA:
        return self._color

    
    @color.setter
    def color(self, value: _ColorRGB | _ColorRGBA) -> None:
        self._color = value
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
    def text_color(self) -> _ColorRGB | _ColorRGBA:
        return self._text_color

    
    @text_color.setter
    def text_color(self, value: _ColorRGB | _ColorRGBA) -> None:
        self._text_color = value
        if self.text:
            self.is_dirty = True
            
            
    def get_rect(self) -> pygame.Rect:
        """ Return a new pygame `Rect` object of this components' size with position absolute to the screen. """
        return pygame.Rect(self._winpos, self.size)


    def config(self, **kwargs) -> None:
        """ Set all overwritable attributes passed as keyword arguments. """
        for k, v in kwargs.items():
            attr = getattr(type(self), k)

            if not isinstance(attr, property) and callable(attr):
                raise AttributeError(f"can't overwrite attribute '{k}' of object '{type(self).__name__}'")
                
            setattr(self, k, v)


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
        