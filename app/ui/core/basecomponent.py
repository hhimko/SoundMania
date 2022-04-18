import pygame

from abc import ABC, abstractmethod


class UIComponent(ABC):
    """ Abstract class defining a renderable UI element. """
    def __init__(self, name: str, rect: pygame.rect.Rect, **kwargs):
        self._name = name
        self.x = rect.x
        self.y = rect.y

        self.surface = pygame.surface.Surface((rect.w, rect.h))

        self.config(**kwargs)


    @property
    def name(self) -> str:
        return self._name


    @property
    def width(self) -> int:
        return self.surface.get_width()


    @width.setter
    def width(self, value: int) -> None:
        self.surface = pygame.surface.Surface((value, self.height))


    @property
    def height(self) -> int:
        return self.surface.get_height()


    @height.setter
    def height(self, value: int) -> None:
        self.surface = pygame.surface.Surface((self.width, value))


    def config(self, **kwargs) -> None:
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