from __future__ import annotations
from functools import cache

import logging
logger = logging.getLogger("ViewManager")

import pygame

import soundmania
import view


class ViewManager:
    """ Class responsible for rendering and managing views. """
    NO_OP = lambda *args, **kwargs: None
    
    def __init__(self):
        self._background = {
            "visible": False,
            "surface": self._get_display_surface_copy(),
            "color_back": (236, 60, 12),
            "color_front": (245, 172, 35)
        }
        
        self._transition = {
            "visible": False,
            "surface": self._get_display_surface_copy(),
            "callback": self.NO_OP,
            "time_elapsed": 0,
            "overlay_alpha": 0,
            "overlay_color": (26, 12, 12)
        }
    
    
    def get_current_view(self) -> view.View:
        try:
            return self._current_view
        except AttributeError:
            raise RuntimeError(f"ViewManager was not initialized with a view. Be sure to call `ViewManager.set_view()` first")
    
        
    @cache
    def get_view(self, view: type[view.View], root: soundmania.SoundMania) -> view.View:
        """ Cached getter of view objects. """
        logger.debug(f"Initializing view {view.__name__}")
        return view(root)
    
    
    def set_view(self, view: type[view.View], root: soundmania.SoundMania) -> None:
        """ Setter of the current view. """
        new_view = self.get_view(view, root)
        new_view.on_window_resize() # recalculate the view components sizes 
        new_view.prepare()
        
        self._current_view = new_view
        
        
    def transition_out(self, duration: int):
        """ Start a new screen-out transition. """
        
        def out_callback(dt: int):
            if self._transition["time_elapsed"] < duration:
                self._transition["overlay_alpha"] = round(255 * self._transition["time_elapsed"] / duration)
                self._transition["time_elapsed"] += dt
            else:
                self._transition["overlay_alpha"] = 255
                self.transition_stop()
                
        self._transition["visible"] = True
        self._transition["time_elapsed"] = 0
        self._transition["callback"] = out_callback
        
    
    def transition_in(self, duration: int):
        """ Start a new screen-in transition. """
        
        def in_callback(dt: int):
            if self._transition["time_elapsed"] < duration:
                self._transition["overlay_alpha"] = round(255 * (1 - (self._transition["time_elapsed"] / duration)))
                self._transition["time_elapsed"] += dt
            else:
                self._transition["overlay_alpha"] = 0
                self._transition["visible"] = False
                self.transition_stop()
                
        self._transition["time_elapsed"] = 0
        self._transition["callback"] = in_callback
    
    
    def transition_stop(self):
        """ Stop the currently played transition. """
        self._transition["callback"] = self.NO_OP
            
            
    def handle_events(self, event_list: list[pygame.event.Event]) -> None:
        current_view = self.get_current_view()
        
        unhandled = []
        for event in event_list:
            if event.type == pygame.VIDEORESIZE:
                self._transition["surface"] = self._get_display_surface_copy()
                self._background["surface"] = self._get_display_surface_copy()
                current_view.on_window_resize()
            else:
                unhandled.append(event)
                
        current_view.handle_input(unhandled)
        
        
    def update(self, dt: int) -> None:
        """ Update the current view state.

            Args:
                dt: elapsed time since the last frame
        """
        if self._background["visible"]:
            self._background_update(dt)
        
        current_view = self.get_current_view()
        current_view.update(dt)
        
        self._transition_update(dt)
        
        
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the view on screen, along with all requested overlays and backgrounds.

            Args:
                surface: display surface
        """
        if self._background["visible"]:
            surface.blit(self._background["surface"], (0,0))
        
        current_view = self.get_current_view()
        current_view.render(surface)
        
        if self._transition["visible"]:
            self._transition["surface"].fill(self._transition["overlay_color"])
            self._transition["surface"].set_alpha(self._transition["overlay_alpha"], pygame.RLEACCEL)
            surface.blit(self._transition["surface"], (0,0))
            
            
    def _background_update(self, dt: int) -> None:
        pass
    
    
    def _transition_update(self, dt: int) -> None:
        callback = self._transition["callback"]
        callback(dt)
        
    
    def _get_display_surface_copy(self) -> pygame.surface.Surface:
        return pygame.display.get_surface().copy()
    