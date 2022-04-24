from math import ceil

import pygame

from ui.core.core import EvalAttrProxy
from ui.core.basecomponent import UIComponent


class vw(EvalAttrProxy):
    def preprocess(self, value: float) -> float:
        return value / 100
    
    
    def evaluate(self, obj: UIComponent) -> float:
        return ceil(pygame.display.get_window_size()[0] * self.value)
    



class vh(EvalAttrProxy):
    def preprocess(self, value: float) -> float:
        return value / 100
    
    
    def evaluate(self, obj: UIComponent) -> float:
        return ceil(pygame.display.get_window_size()[1] * self.value)
