import pygame

from view.baseview import View
from ui import Button, MenuItemList


class MainMenuView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.menu_items = MenuItemList("menu_container", (0,0,500,500),
            Button("button_play", (100,100,100,50), text="PLAY", color=(255,255,255)),
            Button("button_quit", (100,200,100,50), text="QUIT", color=(255,255,255)),
        )

        self.menu_items.button_play.on_mouse_over = lambda obj: print("play")
        self.menu_items.button_quit.on_mouse_over = lambda obj: print("quit")
    

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.quit()

            # if event.type == pygame.key

    
    def update(self, dt: int) -> None:
        self.menu_items.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.menu_items.render(surface)