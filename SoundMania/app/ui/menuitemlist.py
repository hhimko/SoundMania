import pygame

from ui.core.type import _SizeRect
from ui.core import UIContainer
from ui.button import Button


class MenuItemList(UIContainer[Button]):
    """ Indexable container class for Button components. """
    def __init__(self, name: str, rect: _SizeRect | pygame.Rect, *buttons: Button, **kwargs):
        super().__init__(name, rect, *buttons, **kwargs)
        self._selected_index = 0

    
    def select_previous(self, wrap: bool = True) -> None:
        """ Decrement the currenty selected button index.
            
            Args:
                wrap: tells whether to wrap the index around or clamp to the last item 
        """
        if len(self) == 0:
            return
        
        idx = self._selected_index - 1
        self._selected_index = idx % len(self) if wrap else max(idx, 0)
    
    
    def select_enter(self) -> None:
        """ Execute `Button.on_mouse_click()` callback on currently selected button. """
        if len(self) == 0:
            return

        self[self._selected_index].on_mouse_click()


    def select_next(self, wrap: bool = True) -> None:
        """ Increment the currenty selected button index.
            
            Args:
                wrap: tells whether to wrap the index around or clamp to the last item 
        """
        if len(self) == 0:
            return
        
        idx = self._selected_index + 1
        self._selected_index = idx % len(self) if wrap else min(idx, len(self)-1)
