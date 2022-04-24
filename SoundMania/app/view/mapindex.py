import pygame

from ui import Button, MenuItemList, MapIndex
from ui.core.units import vw, vh
from view.baseview import View
import view


class MapIndexView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.button_return = Button("button_return", (0,0,200,50), text="RETURN", text_color=(255,255,255))
        self.button_return.on_mouse_click = self._button_return_callback
        
        self.map_index = MapIndex()
        
        self.options_menu = MenuItemList("options_menu_container", (0, vh(70), vw(100), vh(30)),
                Button("button_return", (0, vh(20), vw(100), vh(10)), text="RETURN", color=(255,255,255))
        )
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.options_menu.select_previous()

                elif event.key == pygame.K_RETURN:
                    self.options_menu.select_enter()
                    
                elif event.key == pygame.K_DOWN:
                    self.options_menu.select_next()
                
            
    def update(self, dt: int) -> None:
        self.button_return.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.button_return.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.button_return._on_window_resize()
        
        
    def _button_return_callback(self, obj: Button) -> None:
        self.root.request_transition_play('')
        self.root.request_view_change(view.MainMenuView)
    