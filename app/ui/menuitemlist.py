from typing import Iterator

import pygame
from app.ui.core.basecomponent import UIComponent
from ui.core.type import _TupleI4
from ui.core import UIContainer
from ui.button import Button


class MenuItemList(UIContainer[Button]):
    """ Indexable container class for Button components. """
    def __init__(self, name: str, rect: _TupleI4 | pygame.Rect, *buttons: Button, **kwargs):
        super().__init__(name, rect, *buttons, **kwargs)
        self.selected_index = 0

    
    def select_previous(self) -> None:
        self.selected_index -= 1
        self.selected_index %= len(self.elements)

    
    def select_enter(self) -> None:
        self[self.selected_index].on_mouse_up()


    def select_next(self) -> None:
        self.selected_index += 1
        self.selected_index %= len(self.elements)
        
        
    def __iter__(self) -> Iterator[Button]:
        return iter(self.elements.values())
    
    
    def __getitem__(self, index: int) -> Button:
        return list(self.elements.values())[index]

