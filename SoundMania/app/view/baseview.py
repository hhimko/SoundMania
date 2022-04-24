from __future__ import annotations
from abc import ABC, abstractmethod

import pygame

import soundmania


class View(ABC):
    """ Abstract View class defining a common interface for creating app scenes. """
    def __init__(self, root: soundmania.SoundMania):
        self.root = root
        
        
    @abstractmethod
    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        """ Handle incoming user input. 
        
            Args:
                event_list: list of pygame Event objects. 
        """
        pass
    
    
    @abstractmethod    
    def update(self, dt: int) -> None:
        """ Update the current view state.

            Args:
                dt: elapsed time since the last frame.
        """
        pass
    
    
    @abstractmethod    
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the view on screen. 
        
            Args:
                surface: pygame Surface object on which to render. """
        pass
    
    
    @abstractmethod
    def on_window_resize(self) -> None:
        """ Singly-triggered event on window being resized by the user. """
        pass
    
    
    def prepare(self):
        """ Prepare the view to be properly displayed. """
        self.on_window_resize()
    