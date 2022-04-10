import logging
logging.basicConfig(level="INFO", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")

import pygame

from arduino_controller import ArduinoController


class SoundMania:
    def __init__(self):
        self.controller = ArduinoController()
        self.running = False
        
        self.clock = pygame.time.Clock()
        
        
    def handle_input(self):
        for event in self.controller.poll_event():
            pass
        
        
    def update(self):
        dt = self.clock.tick(60)
        self.controller.update(dt)
        
        
    def render(self):
        pass
    
    
    def run(self):
        pygame.init()
        
        self.running = True
        self.mainloop()
    
    
    def mainloop(self):
        while self.running:
            self.handle_input()
            self.update()
            self.render()