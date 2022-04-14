import logging

logging.basicConfig(level="INFO", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")

import pygame

from arduino_controller import ArduinoController
from view.mainmenu import MainMenuView


class SoundMania:
    WINDOW_WIDTH: int  = 800
    WINDOW_HEIGHT: int = 600
    
    def __init__(self):
        # self.controller = ArduinoController()
        self.view = MainMenuView(root=self)
        
        self._pygame_init()
        
    
    def run(self) -> None:
        self._running = True
        self.mainloop()
    
    
    def mainloop(self) -> None:
        while self._running:
            dt = self.clock.tick(60)
            view = self.view
            
            event_list = pygame.event.get()
            view.handle_input(event_list)
            view.update(dt)
            view.render(self.screen_surface)
            
            pygame.display.flip()
            
        self._shutdown()
        
        
    def quit(self):
        self._running = False
        
        
    def _pygame_init(self) -> None:
        pygame.init()
        
        win_flags = pygame.RESIZABLE
        self.screen_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), win_flags)
        pygame.display.set_caption("SoundMania")

        self.clock = pygame.time.Clock()
        
        
    def _shutdown(self):
        pygame.quit()