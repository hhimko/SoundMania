from __future__ import annotations
from math import cos, sin, radians
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
            "color_back": (167, 0, 29),
            "color_front": (216, 19, 51),
            "should_update": True,
            "animation_duration": 1000,
            "animation_time_elapsed": 0
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
        new_view = self.get_view(view, root) # type: ignore
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
            if self._background["should_update"]:
                self._background_update(dt)
            self._background["should_update"] = not self._background["should_update"] # background is being updated every 2 frames
        
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
        bgs = self._background["surface"]
        bgs.fill(self._background["color_back"])
        
        display_w, display_h = pygame.display.get_window_size()
        anchor_x, anchor_y = (-display_w*0.03, display_h*1.2)
        circle_radius = display_h//1.4
        
        pygame.draw.circle(bgs, self._background["color_front"], (anchor_x, anchor_y), circle_radius, draw_top_right=True)
        
        self._background["animation_time_elapsed"] += dt / self._background["animation_duration"]
        self._background["animation_time_elapsed"] %= 1
        
        line_count = 6
        line_length = max(display_w, display_h) 
        angle_offset = 8
        for i in range(line_count):
            angle = radians(-95/line_count*(i + self._background["animation_time_elapsed"]) - angle_offset/2)
            slope_l = cos(angle), sin(angle)
            angle += radians(angle_offset)
            slope_r = cos(angle), sin(angle)
            
            start_l = (anchor_x + slope_l[0]*(circle_radius-20), anchor_y + slope_l[1]*(circle_radius-20))
            end_l = (anchor_x + slope_l[0]*(line_length + circle_radius), anchor_y + slope_l[1]*(line_length + circle_radius))
            
            start_r = (anchor_x + slope_r[0]*(circle_radius-20), anchor_y + slope_r[1]*(circle_radius-20))
            end_r = (anchor_x + slope_r[0]*(line_length + circle_radius), anchor_y + slope_r[1]*(line_length + circle_radius))
            
            pygame.draw.polygon(bgs, self._background["color_front"], (start_l, end_l, end_r, start_r))  
    
    
    def _transition_update(self, dt: int) -> None:
        callback = self._transition["callback"]
        callback(dt)
        
    
    def _get_display_surface_copy(self) -> pygame.surface.Surface:
        return pygame.display.get_surface().copy()
    