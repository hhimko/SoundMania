import pygame

from ui import Button, MapIndex
from ui.core.units import vw, vh
from view.baseview import View
import view


class MapIndexView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.button_return = Button("button_return", (0,vh(90),vw(100),vh(10)), text="RETURN", text_color=(255,255,255))
        self.button_return.on_mouse_click = self._button_return_callback
        
        self.map_index = MapIndex(root, "map_index", (0, vh(-5), vw(60), vh(90)), centered=True)
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.map_index.select_previous()

                elif event.key == pygame.K_RETURN:
                    print(self.map_index._map_paths[self.map_index._selected_index])
                    # self.options_menu.select_enter()
                    
                elif event.key == pygame.K_DOWN:
                    self.map_index.select_next()
                
            
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
        
        
    def _button_return_callback(self, obj: Button) -> None:
        self.root.request_transition_play('')
        self.root.request_view_change(view.MainMenuView)
    