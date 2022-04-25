from __future__ import annotations
from functools import cache

import logging
logging.basicConfig(level="DEBUG", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")
logger = logging.getLogger("SoundMania")

import pygame
pygame.init()

from core.mapmanager import MapManager
import view  # import just the module name to avoid circular import


class SoundMania:
    WINDOW_WIDTH: int  = 1600
    WINDOW_HEIGHT: int = 900
    
    def __init__(self):
        self._pygame_init()
        
        self.map_manager = MapManager()
        
        self.view = self.get_view(view.MainMenuView)
        
    
    @cache
    def get_view(self, view: type[view.View]) -> view.View:
        """ Cached getter of view objects. """
        logger.debug(f"Initializing view {view.__name__}")
        return view(root=self)
    
    
    def request_view_change(self, view: type[view.View]) -> None:
        """ Make a request of changing the current view. """
        if view != type(self.view):
            self.view = self.get_view(view)
            self.view.prepare()
    
    
    def request_transition_play(self, transition: str) -> None:
        pass
        
        
    def request_quit(self) -> None:
        """ Make a request of shutting down the application. """
        self._running = False
        
        
    def run(self) -> None:
        self._running = True
        self._mainloop()
    
    
    def _mainloop(self) -> None:
        while self._running:
            dt = self.clock.tick()
            view = self.view

            self._handle_events()
            view.update(dt)
            view.render(self.screen_surface)
            
            pygame.display.flip()
            pygame.display.set_caption(f"SoundMania | FPS: {round(self.clock.get_fps())}")
            
        self._shutdown()
        
        
    def _handle_events(self) -> None:
        event_list = []
        
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.view.on_window_resize()
            else:
                # events unhandled here are passed in to the view event handler
                event_list.append(event)
                
        self.view.handle_input(event_list)
        
        
    def _pygame_init(self) -> None:        
        win_flags = pygame.RESIZABLE
        self.screen_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), win_flags)
        pygame.display.set_caption("SoundMania")

        self.clock = pygame.time.Clock()
        
        
    def _shutdown(self) -> None:
        pygame.quit()