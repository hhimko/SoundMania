from functools import partial
from typing import Literal

import pygame

from core.input.inputmanager import InputManager
from core.requestqueue import RequestQueue
from core.viewmanager import ViewManager
from core.mapmanager import MapManager
from core.configio import ConfigIO

import view  # import just the module name to avoid circular import


class SoundMania:
    """ Root application class responsible for handling communication between views and managers. """
    WINDOW_WIDTH: int  = 1600
    WINDOW_HEIGHT: int = 900
    
    def __init__(self):
        pygame.init()
        self.display_surface = self._get_display()
        self.clock = pygame.time.Clock()
        
        self.config = ConfigIO()
        md = self.config.get_user_map_directory()
        
        self.request_queue = RequestQueue()
        self.input_manager = InputManager()
        self.view_manager = ViewManager()
        self.map_manager = MapManager(md)
        
        
    def run(self) -> None:
        """ Set up and run the application. """
        self.view_manager.set_view(view.MainMenuView, root=self)
        self.running = True
        
        self._mainloop()
    
    
    def request_view_change(self, view: type[view.View]) -> None:
        """ Make a queued request of changing the current view. """
        if type(self.view_manager.get_current_view()) != view:
            request = partial(self.view_manager.set_view, view=view, root=self)
            self.request_queue.add(request)
            
            
    def set_background_visibility(self, state: bool) -> None:
        """ Make a queued request of setting the visibility of an animated view background. """
        self.view_manager._background["visible"] = state
    
    
    def request_transition_play(self, transition_name: Literal["out", "in"], duration: int) -> None:
        """ Make a queued request of playing a view transition for `duration` miliseconds.
        
            request_transition_play implicitly freezes inpit handling for the duration of 
            the transition being played.
        """
        transmap = {
            "out": self.view_manager.transition_out,
            "in":  self.view_manager.transition_in,
        }
        
        request = partial(transmap[transition_name], duration)
        self.request_queue.add_blocking(request, timeout=duration)
        
        
    def request_map_play(self, map_path: str) -> None:
        pass
        
        
    def request_song_play(self, song_path: str) -> None:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        
    def request_sound_play(self, sound_name: str) -> None:
        pygame.mixer.Sound(sound_name).play()
        
        
    def request_quit(self) -> None:
        """ Make a queued request of shutting down the application. """
        def request():
            self.running = False
            
        self.request_queue.add(request)
    
    
    def _mainloop(self) -> None:
        while self.running:
            dt = self.clock.tick()
            
            event_list = self.input_manager.poll_events()
            self.view_manager.handle_events(event_list)
            
            self.request_queue.process(dt)
            self.input_manager.update(dt)
            self.view_manager.update(dt)
            
            self.view_manager.render(self.display_surface)
            
            pygame.display.flip()
            pygame.display.set_caption(f"SoundMania | FPS: {round(self.clock.get_fps())}")
            
        self._shutdown()
        
        
    def _get_display(self) -> pygame.surface.Surface:        
        win_flags = pygame.RESIZABLE
        surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), win_flags)
        return surface
        
        
    def _shutdown(self) -> None:
        pygame.quit()
        