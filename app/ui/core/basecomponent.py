from __future__ import annotations
from functools import cached_property
from turtle import position

import pygame

from ui.core.type import _TupleI4, _ColorRGB, _ColorRGBA


def _read_size_from_rect(rect: _TupleI4 | pygame.Rect) -> _TupleI4:
        r = pygame.Rect(rect)
        return r.x, r.y, r.w, r.h
    
    
class UIComponent:
    """ Abstract class defining a renderable UI element. """
    def __init__(self, name: str, rect: _TupleI4 | pygame.Rect, **kwargs):
        self.name = name
        self._parent: UIComponent | None = None
        self.is_dirty = True # forces the surface to be redrawn on first render

        x, y, w, h = _read_size_from_rect(rect)
        self._pos = (x, y)
        self.surface = pygame.surface.Surface((w, h))

        # TODO: extract optional component modules 
        self._is_centered = False
        self._color: _ColorRGB | _ColorRGBA = (0,0,0)

        self._text = ''
        self._text_size = h
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
        self._winpos_recompute()
        
        
    @property
    def position(self) -> tuple[int, int]:
        return self._pos
    
    
    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self._pos = value
        self._winpos_recompute()
        
        
    @property
    def x(self) -> int:
        return self._pos[0]
    
    
    @x.setter
    def x(self, value: int) -> None:
        self.position = (value, self.y) # forces the absolute position to be recomputed
        
        
    @property
    def y(self) -> int:
        return self._pos[1]
    
    
    @y.setter
    def y(self, value: int) -> None:
        self.position = (self.x, value) # forces the absolute position to be recomputed
        

    @property
    def width(self) -> int:
        return self.surface.get_width()


    @width.setter
    def width(self, value: int) -> None:
        self.surface = pygame.surface.Surface((value, self.height))
        
        self.is_dirty = True
        if self.centered:
            self._winpos_recompute()


    @property
    def height(self) -> int:
        return self.surface.get_height()


    @height.setter
    def height(self, value: int) -> None:
        self.surface = pygame.surface.Surface((self.width, value))
        self.is_dirty = True
        
        
    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height
    
    
    @size.setter
    def size(self, value: tuple[int, int]) -> None:
        self.surface = pygame.surface.Surface(value)
        self.is_dirty = True
        

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
        return self._text_size

    
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
        if self.is_dirty:
            self._redraw_surface()
            
        surface.blit(self.surface, self._winpos)
        
        
    @cached_property
    def _winpos(self) -> tuple[int, int]:
        x, y = (self.x, self.y)
        
        if self.centered:
            pw, ph = self.parent.size if self.parent else pygame.display.get_window_size()
            sw, sh = self.size
            x, y = (pw//2 + x - sw//2, ph//2 + y - sh//2)
        
        return (x + self.parent._winpos[0], y + self.parent._winpos[1]) if self.parent else (x, y)
    
    
    def _winpos_recompute(self) -> None:
        try:
            del self._winpos
        except AttributeError:
            pass
        
        
    def _redraw_surface(self) -> None:
        self.surface.fill(self.color)
        if self.text:
            self._redraw_text()
            
        self.is_dirty = False


    def _redraw_text(self) -> None:
        overlay = pygame.font.Font(None, self.text_size).render(self.text, True, self.text_color)
        self.surface.blit(overlay, (0,0))
            
            

            