from __future__ import annotations

import pygame

from ui import Button#, Slider
from ui.core import UIContainer
import view


class UserSettingsView(view.View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.menu_options = UIContainer("menu_container", (0, 0, "60vw", "100vh"),
            # Slider("slider_music_vol", (0, 0, "100pw", 50), color=(0, 0, 125)),
            centered=True                                
        )
        
        self.button_return = Button("button_return", (0, "45vh", "60vw", "10vh"), text="RETURN", text_color=(255,255,255), centered=True)
        self.button_return.on_mouse_click = self._button_return_callback


    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._button_return_callback()
                    
                    
    def prepare(self) -> None:
        self.root.set_background_visibility(True)
                
            
    def update(self, dt: int) -> None:
        self.menu_options.update(dt)
        self.button_return.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        self.menu_options.render(surface)
        self.button_return.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.button_return._on_window_resize()
        
        
    def _button_return_callback(self, *args) -> None:
        self.root.request_sound_play("SoundMania\\src\\menu_select.ogg")
        self.root.request_transition_play("out", 150)
        self.root.request_view_change(view.MainMenuView)
        self.root.request_transition_play("in", 150)
    