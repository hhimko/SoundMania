import logging
logging.basicConfig(level="INFO", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")

import pygame
pygame.init()

from arduino_controller import ArduinoController
from view import MainMenuView


class SoundMania:
    WINDOW_WIDTH: int  = 800
    WINDOW_HEIGHT: int = 600
    
    def __init__(self):
        self._pygame_init()
        
        self.controller = ArduinoController()
        self.view = MainMenuView(root=self)
        
    
    def run(self) -> None:
        self._running = True
        self.mainloop()
    
    
    def mainloop(self) -> None:
        while self._running:
            dt = self.clock.tick()

            self._handle_events()
            self.view.update(dt)
            self.view.render(self.screen_surface)
            
            pygame.display.flip()
            pygame.display.set_caption(f"SoundMania | FPS: {round(self.clock.get_fps())}")
            
        self._shutdown()
        
        
    def quit(self) -> None:
        self._running = False
        
        
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