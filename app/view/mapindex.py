import pygame

from ui import Button, MenuItemList
from ui.core.units import vw, vh
from view.baseview import View
import view


class MapIndexView(View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.menu_items = MenuItemList("menu_container", (0, vh(70), vw(100), vh(30)),
            Button("button_return", (0, vh(20), vw(100), vh(10)),
                        text="- R E T U R N -", color=(255,255,255)
                    )
        )

        self.menu_items.button_return.on_mouse_click = self._button_return_callback
        

    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

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
        
        
    def _button_return_callback(self, obj: Button) -> None:
        self.root.request_transition_play('')
        self.root.request_view_change(view.MainMenuView)
    