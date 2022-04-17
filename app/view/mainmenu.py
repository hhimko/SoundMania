import pygame

from view.baseview import View
from ui import Button, MenuItemList


class MainMenuView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.button_play = Button(100, 100, 50, 50)
        self.button_quit = Button(100, 200, 50, 50)

        self.button_play.on_mouse_down = lambda obj: print("play")
        self.button_quit.on_mouse_down = lambda obj: print("quit")


    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.quit()

    
    def update(self, dt: int) -> None:
        self.button_play.update(dt)
        self.button_quit.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.button_play.render(surface)
        self.button_quit.render(surface)
    