from typing import Callable

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.font import Font
from pygame.rect import Rect


class _CallbackProperty(property):
    """ Descriptor class for callable properties. 

        CallbackProperty makes sure a property is always callable, giving it 
        a NO_OP method callback by default. 

        A CallbackProperty instance can be set to either a callable method or
        `None`, which works the same way as deleting the propetry with the `del`
        keyword and resets the callback to NO_OP.
    """
    def __init__(self):
        """ Make a new descriptor property for callable types. """
        super().__init__(self.getter, self.setter, self.deleter)
        self.callback = self.NO_OP
        
        
    @staticmethod    
    def NO_OP(*args, **kwargs) -> None:
        pass
    

    def getter(self, obj: type) -> Callable:
        return self.callback
    
    
    def setter(self, obj: type, value: Callable | None) -> None:
        if value is None:
            self.deleter(obj)
        else:
            assert callable(value), "callback property value must be a callable"
            self.callback = value
            
        
    def deleter(self, obj: type) -> None:
        self.callback = self.NO_OP




class Button(Sprite):
    on_mouse_pressed = _CallbackProperty()
    on_mouse_over    = _CallbackProperty()
    on_mouse_down    = _CallbackProperty()
    on_mouse_up      = _CallbackProperty()

    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()
        self.rect = Rect()

        self.is_mouse_pressed = False
        self.is_mouse_over    = False

        self._surface = Font(None, h).render("test text", True, (0,0,0))
        self.rect.topleft = (x, y)


    @property
    def text(self) -> str:
        return self._text


    @text.setter
    def text(self, value: str):
        self._text = value


    def update(self, dt: int) -> None:
        mouse_pos = pygame.mouse.get_pos()
        lmb_down = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            self.on_mouse_over(self)
            self.is_mouse_over = True

            if lmb_down:
                if not self.is_mouse_pressed:
                    self.on_mouse_down(self)

                self.on_mouse_pressed(self)
                self.is_mouse_pressed = True

            elif self.is_mouse_pressed:
                   self.is_mouse_pressed = False 
                   self.on_mouse_up(self)
        else:
            self.is_mouse_over = False
            self.is_mouse_pressed = False 


    def render(self, surface: Surface) -> None:
        surface.blit(self._surface, (self.x, self.y))
