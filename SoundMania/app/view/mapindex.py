import pygame

from ui import Button, MapIndex
from view.baseview import View
import view


class MapIndexView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.button_return = Button("button_return", (0, "90vh", "100vw", "10vh"), text="RETURN", text_color=(255,255,255))
        self.button_return.on_mouse_click = lambda obj: self.root.request_view_change(view.MainMenuView)
        
        self.map_index = MapIndex(root, "map_index", (0, "-5vh", "60vw", "90vh"), centered=True)
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.map_index.select_previous()

                elif event.key == pygame.K_RETURN:
                    self.map_index.select_enter()
                    
                elif event.key == pygame.K_DOWN:
                    self.map_index.select_next()
                    
                elif event.key == pygame.K_ESCAPE:
                    self.root.request_view_change(view.MainMenuView)
                    
                elif event.key == pygame.K_z:
                     print(abs((pygame.mixer.music.get_pos() / (1000 / (140/60))) % 1 - 0.5) * 100)
                     
                     
    def prepare(self) -> None:
        self.root.set_background_visibility(False)
                
            
    def update(self, dt: int) -> None:
        self.map_index.update(dt)
        self.button_return.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.map_index.render(surface)
        self.button_return.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.button_return._on_window_resize()
        self.map_index._on_window_resize()
        