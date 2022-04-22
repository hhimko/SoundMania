import pygame

from ui.core.units import vw, vh
from view.baseview import View
from ui import Button, MenuItemList


class MainMenuView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.menu_items = MenuItemList("menu_container", (0,0,vw(70),vh(50)),
            Button("button_play", (0,vh(-10),vw(50),vh(10)), centered=True, text="PLAY", color=(255,255,255)),
            Button("button_quit", (0,vh( 10),vw(50),vh(10)), centered=True, text="QUIT", color=(255,255,255)),
            centered = True
        )

        self.menu_items.button_play.on_mouse_click = lambda obj: print("PLAY")
        self.menu_items.button_quit.on_mouse_click = lambda obj: print("QUIT")
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu_items.select_previous()

                elif event.key == pygame.K_RETURN:
                    self.menu_items.select_enter()
                    
                elif event.key == pygame.K_DOWN:
                    self.menu_items.select_next()
                
            
    def update(self, dt: int) -> None:
        self.menu_items.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.menu_items.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.menu_items._on_window_resize()