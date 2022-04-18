import pygame

from abc import ABC, abstractmethod


_ColorRGB = tuple[int, int, int, int]
_ColorRGBA = tuple[int, int, int]

class UIComponent(ABC):
    """ Abstract class defining a renderable UI element. """
    def __init__(self, name: str, rect: pygame.rect.Rect, **kwargs):
        self._name = name
        self.surface = pygame.surface.Surface((rect.w, rect.h))
        self.x = rect.x
        self.y = rect.y

        # TODO: extract optional component modules 
        self._color: _ColorRGB | _ColorRGBA = (0,0,0,0)
        self._text = ''
        self._text_size = rect.h
        self._text_color: _ColorRGB | _ColorRGBA = (0,0,0)

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


    @property
    def color(self) -> _ColorRGB | _ColorRGBA:
        return self._color

    
    @color.setter
    def color(self, value: _ColorRGB | _ColorRGBA) -> None:
        self._color = value
        self.surface.fill(value)
        if self.text:
            self._render_text()


    @property
    def text(self) -> str:
        return self._text


    @text.setter
    def text(self, value: str) -> None:
        self._text = value.strip()
        self._render_text()

    
    @property
    def text_size(self) -> int:
        return self._text_size

    
    @text_size.setter
    def text_size(self, value: int) -> None:
        self._text_size = value
        if self.text:
            self._render_text()


    @property
    def text_color(self) -> _ColorRGB | _ColorRGBA:
        return self._text_color

    
    @text_color.setter
    def text_color(self, value: _ColorRGB | _ColorRGBA) -> None:
        self._text_color = value
        if self.text:
            self._render_text()


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
                dt: elapsed time since the last frame
        """
        pass


    @abstractmethod
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the component on screen. 
        
            Args:
                surface: pygame `Surface` object on which to render
        """
        pass


    def get_rect(self) -> pygame.rect.Rect:
        """ Return a new pygame `Rect` object of this components' size. """
        return pygame.rect.Rect(self.x, self.y, self.width, self.height)


    def _render_text(self) -> None:
        if self.text:
            overlay = pygame.font.Font(None, self.text_size).render(self.text, True, self.text_color)
            self.surface.blit(overlay, (0,0))
