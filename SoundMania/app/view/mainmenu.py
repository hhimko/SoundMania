from __future__ import annotations

import pygame

from core.input import SMEvent
from ui import Button, MenuItemList
from ui.core.units import pw, vw, vh
import view


class MainMenuView(view.View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        self.menu_items = MenuItemList("menu_container", (vw(15), 0, vh(70), vh(50)),
            Button("button_play", (0, vh(-15), pw(80), vh(10)), 
                centered=True, text="PLAY", color=(255,255,255)
            ),
            Button("button_settings", (0, 0, pw(80), vh(10)),
                centered=True, text="SETTINGS", color=(255,255,255)
            ),
            Button("button_quit", (0, vh(15), pw(80), vh(10)),
                centered=True, text="QUIT", color=(255,255,255)
            ),
            centered = True
        )

        self.menu_items.button_play.on_mouse_click = self._button_play_callback
        self.menu_items.button_settings.on_mouse_click = self._button_settings_callback
        self.menu_items.button_quit.on_mouse_click = self._button_quit_callback
        

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
                    
                elif event.key == pygame.K_p:
                    self._button_play_callback()
                    
                elif event.key == pygame.K_s:
                    self._button_settings_callback()
                    
                elif event.key == pygame.K_q:
                    self._button_quit_callback()
                    
                    
    def prepare(self) -> None:
        self.root.set_background_visibility(True)
                
            
    def update(self, dt: int) -> None:
        self.menu_items.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        self.menu_items.render(surface)
        
        
    def on_window_resize(self) -> None:
        self.menu_items._on_window_resize()
        
        
    def _button_play_callback(self, *args) -> None:
        self.root.request_view_change(view.MapIndexView)
        
    
    def _button_settings_callback(self, *args) -> None:
        self.root.request_transition_play("out", 200)
        self.root.request_view_change(view.UserSettingsView)
        self.root.request_transition_play("in", 200)
        
        
    def _button_quit_callback(self, *args) -> None:
        self.root.request_transition_play("out", 750)
        self.root.request_quit()
    