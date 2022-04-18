import pygame

from ui.core import UIContainer
from ui.button import Button


class MenuItemList(UIContainer):
    """ Container class for Button components. """
    def __init__(self, name: str, rect: pygame.rect.Rect, *buttons: Button, **kwargs):
        super().__init__(name, rect, buttons, **kwargs)
        self.selected_index = 0

    
    def select_previous(self) -> None:
        self.selected_index -= 1
        self.selected_index %= len(self.buttons)

    
    def select_enter(self) -> None:
        self.buttons[self.selected_index].on_mouse_up()


    def select_next(self) -> None:
        self.selected_index += 1
        self.selected_index %= len(self.buttons)

