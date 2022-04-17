import pygame

from abc import ABC, abstractmethod


class UIComponent(ABC):
    """ Abstract class defining a renderable UI element. """
    def __init__(self, **kwargs):
        self.config(**kwargs)


    def config(self, **kwargs):
        """ Set all overwritable attributes passed as keyword arguments. """
        for k, v in kwargs.items():
            attr = getattr(type(self), k)

            if not isinstance(attr, property) and callable(attr):
                raise AttributeError(f"can't overwrite attribute '{k}' of object '{type(self).__name__}'")
                
            setattr(self, k, v)


    @abstractmethod
    def update(self, dt: int) -> None:
        """ Update the current element state. 
        
            Args:
                dt: elapsed time since the last frame.
        """
        pass


    @abstractmethod
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame Surface object on which to render. """
        pass