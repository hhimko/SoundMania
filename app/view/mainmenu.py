import pygame
from pygame.surface import Surface
from pygame.event import Event

from view.baseview import View
from ui import Button 


class MainMenuView(View):
    def __init__(self, root):
        super().__init__(root)
        self.button = Button(20, 20, 100, 50)
    
    
    def handle_input(self, event_list: list[Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.quit()
        
    
    def update(self, dt: int) -> None:
        self.button.update(dt)
    
    
    def render(self, surface: Surface) -> None:
        surface.fill((255, 0, 0))
        self.button.render(surface)


    def play(self):
        print("xd")