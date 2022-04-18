from functools import partial
from typing import Callable

import pygame
from pygame.font import Font
from pygame.rect import Rect

from ui.core import UIComponent


class _CallbackProperty(property):
    """ Descriptor class for callable properties. 

        CallbackProperty makes sure a property is always callable, giving it 
        a NO_OP method callback by default. 

        A CallbackProperty instance can be set to either a callable method or
        `None`, which works the same way as deleting the propetry with the `del`
        keyword and resets the callback to NO_OP.

        When setting a CallbackProperty to a callable, it's automatically injected
        with a `self`-like argument.
    """
    def __init__(self):
        """ Make a new descriptor property for callable types. """
        super().__init__(self.getter, self.setter, self.deleter)


    @staticmethod    
    def NO_OP(*args, **kwargs) -> None:
        pass
    
    
    def __set_name__(self, obj: type, name: str) -> None:
        self.callback_accessor = f"_{name}"
        setattr(obj, self.callback_accessor, self.NO_OP)


    def getter(self, obj: type) -> Callable: # type: ignore
        return getattr(obj, self.callback_accessor)
    
    
    def setter(self, obj: type, value: Callable | None) -> None: # type: ignore
        if value is None:
            return self.deleter(obj)
        
        if not callable(value):
            raise ValueError(f"callback property value must be a callable, not {type(value)}")

        injected = partial(value, obj)
        setattr(obj, self.callback_accessor, injected)
            
        
    def deleter(self, obj: type) -> None: # type: ignore
        setattr(obj, self.callback_accessor, self.NO_OP)




class Button(UIComponent):
    on_mouse_pressed = _CallbackProperty()
    on_mouse_over    = _CallbackProperty()
    on_mouse_down    = _CallbackProperty()
    on_mouse_up      = _CallbackProperty()

    def __init__(self, x: int, y: int, w: int, h: int, **kwargs):
        super().__init__(**kwargs)
        self.rect = Rect(x, y, w, h)

        self.is_mouse_pressed = False
        self.is_mouse_over    = False

        self._surface = Font(None, h).render("test text", True, (0,0,0))


    @property
    def text(self) -> str:
        return self._text


    @text.setter
    def text(self, value: str) -> None:
        self._text = value


    def update(self, dt: int) -> None:
        mouse_pos = pygame.mouse.get_pos()
        lmb_down = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            self.on_mouse_over()
            self.is_mouse_over = True

            if lmb_down:
                if not self.is_mouse_pressed:
                    self.on_mouse_down()

                self.on_mouse_pressed()
                self.is_mouse_pressed = True

            elif self.is_mouse_pressed:
                   self.is_mouse_pressed = False 
                   self.on_mouse_up()
        else:
            self.is_mouse_over = False
            self.is_mouse_pressed = False 


    def render(self, surface: pygame.surface.Surface) -> None:
        surface.blit(self._surface, (self.rect.x, self.rect.y))
