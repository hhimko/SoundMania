import pygame

from ui.core.type import _TupleI4
from ui.core import UIComponent, callbackproperty


class Button(UIComponent):
    on_mouse_pressed = callbackproperty()
    on_mouse_over    = callbackproperty()
    on_mouse_down    = callbackproperty()
    on_mouse_up      = callbackproperty()

    def __init__(self, name: str, rect: _TupleI4 | pygame.Rect, **kwargs):
        super().__init__(name, rect, **kwargs)
        self.is_mouse_pressed = False
        self.is_mouse_over    = False


    def update(self, dt: int) -> None:
        mouse_pos = pygame.mouse.get_pos()
        lmb_down = pygame.mouse.get_pressed()[0]

        if self.get_rect().collidepoint(mouse_pos):
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
        surface.blit(self.surface, (self.x, self.y))
