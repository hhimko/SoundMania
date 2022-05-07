from __future__ import annotations

import pygame

from ui import Button, MenuItemList
from ui.core.units import vw, vh
import view


class UserSettingsView(view.View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.button_return = Button("button_return", (0, vh(40), vw(60), vh(10)), text="RETURN", text_color=(255,255,255), centered=True)
        self.button_return.on_mouse_click = self._button_return_callback


    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._button_return_callback()
                
            
    def update(self, dt: int) -> None:
        self.button_return.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        surface.fill((255, 0, 0))
        self.button_return.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.button_return._on_window_resize()
        
        
    def _button_return_callback(self, *args) -> None:
        self.root.request_transition_play("out", 200)
        self.root.request_view_change(view.MainMenuView)
        self.root.request_transition_play("in", 200)
    