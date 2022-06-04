from __future__ import annotations

import pygame
import pygment

import view


class UserSettingsView(view.View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        settings = pygment.component.Frame("settings_frame", ("20sw", 0, "60sw", "100sh"))
        settings.style.color = (0,0,0,128)
        
        button_return = pygment.component.Button("button_return", ("10pw", "90ph", "80pw", "10ph"))
        button_return.style = {"color": (8,8,8), "border_radius": 20, "border_thickness": 5, "border_color": (0,0,0)}
        button_return.add(pygment.component.Label("button_return_label", ("50pw", "50ph", "80pw", "80ph"), text="return", centered=True))
        button_return.on_mouse_click = self._button_return_callback
        button_return.join(settings)
        
        layout = (settings, )
        self.viewrenderer = pygment.ViewRenderer((0,0), layout)


    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._button_return_callback()
                    
                    
    def prepare(self) -> None:
        self.root.set_background_visibility(True)
        self.viewrenderer.size = self.root.display_surface.get_size()
                
            
    def update(self, dt: int) -> None:
        self.viewrenderer.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        self.viewrenderer.render(surface, (0,0))
        
        
    def on_window_resize(self) -> None:
        self.viewrenderer.size = self.root.display_surface.get_size()
        
        
    def _button_return_callback(self, *args) -> None:
        self.root.request_sound_play("SoundMania\\src\\menu_select.ogg")
        self.root.request_transition_play("out", 150)
        self.root.request_view_change(view.MainMenuView)
        self.root.request_transition_play("in", 150)
    