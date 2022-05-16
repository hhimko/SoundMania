from __future__ import annotations
from math import ceil

import pygame

from core.core import EvalAttrProxy
import ui.core.basecomponent


class vw(EvalAttrProxy):
    """ Graphic unit representing a 1% of the absolute viewport width. """
    def evaluate(self, obj: ui.core.basecomponent.UIComponent) -> float:
        return ceil(pygame.display.get_window_size()[0] * self.value / 100)
    



class vh(EvalAttrProxy):
    """ Graphic unit representing a 1% of the absolute viewport height. """
    def evaluate(self, obj: ui.core.basecomponent.UIComponent) -> float:
        return ceil(pygame.display.get_window_size()[1] * self.value / 100)
    
    
    

class pw(EvalAttrProxy):
    """ Graphic unit representing a 1% of the relative parent width. """
    def evaluate(self, obj: ui.core.basecomponent.UIComponent) -> float:
        if not obj.parent:
            return ceil(pygame.display.get_window_size()[0] * self.value / 100)
        
        return obj.parent.width * self.value / 100
    
    
    
    
class ph(EvalAttrProxy):
    """ Graphic unit representing a 1% of the relative parent height. """
    def evaluate(self, obj: ui.core.basecomponent.UIComponent) -> float:
        if not obj.parent:
            return ceil(pygame.display.get_window_size()[1] * self.value / 100)
        
        return obj.parent.height * self.value / 100
