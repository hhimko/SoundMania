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
        self._overlay_alpha = 0
        self._overlay = self._get_overlay_surface()
        
        self._transition_update_callback = self.NO_OP
        self._transition_time = 0
    
    
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
        self._current_view = self.get_view(view, root)
        self._current_view.prepare()
        
        
    def transition_out(self, duration: int):
        """ Start a new screen-out transition. """
        def out_callback(dt: int):
            if self._transition_time < duration:
                self._overlay_alpha = round(255 * self._transition_time / duration)
                self._transition_time += dt
            else:
                self._overlay_alpha = 255
                self.transition_stop()
        
        
        self._transition_update_callback = out_callback
    
    
    def transition_stop(self):
        """ Stop the currently played transition. """
        self._transition_callback = self.NO_OP
        self._transition_time = 0
            
            
    def handle_events(self, event_list: list[pygame.event.Event]) -> None:
        current_view = self.get_current_view()
        
        unhandled = []
        for event in event_list:
            if event.type == pygame.VIDEORESIZE:
                self._overlay = self._get_overlay_surface()
                current_view.on_window_resize()
            else:
                unhandled.append(event)
                
        current_view.handle_input(unhandled)
        
        
    def update(self, dt: int) -> None:
        """ Update the current view state.

            Args:
                dt: elapsed time since the last frame
        """
        current_view = self.get_current_view()
        current_view.update(dt)
        
        self._transition_update_callback(dt)
        
        
    def render(self, surface: pygame.surface.Surface) -> None:
        """ Draw the view on screen.

            Args:
                surface: display surface
        """
        current_view = self.get_current_view()
        current_view.render(surface)
        
        if self._overlay_alpha:
            self._overlay.set_alpha(self._overlay_alpha)
            surface.blit(self._overlay, (0,0))
        
        
    def _get_overlay_surface(self) -> pygame.surface.Surface:
        ov = pygame.display.get_surface().copy()
        ov.set_alpha(self._overlay_alpha, pygame.RLEACCEL)
        return ov