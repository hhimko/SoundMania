from __future__ import annotations

import pygame
import pygment

from core.input import SMEvent
import view


class MainMenuView(view.View):
    def __init__(self, root):
        super().__init__(root)

        # view layout
        menu = pygment.component.Frame("menu", ("60sw", 0, "40sw", "100sh"))
        menu.style.color = (0,0,0,128)
        
        menu_buttons = pygment.component.Frame("menu_buttons", ("50pw", "50ph", "100pw", "50ph"))
        menu_buttons.style.centered = True
        menu_buttons.join(menu)
        
        btn_style = {"color": (8,8,8), "border_radius": 20, "border_color": (160, 0, 0)}
        btn_play = pygment.component.Button("button_play", ("10pw", "10ph", "80pw", "20ph"), style=btn_style)
        btn_play.add(pygment.component.Label("button_play_label", ("50pw", "50ph", "80pw", "80ph"), text="play", align_center=True, centered=True))
        btn_play.on_mouse_enter = lambda btn: self._change_selected_button(btn)
        btn_play.on_mouse_click = self._button_play_callback
        btn_play.join(menu_buttons)
        
        btn_settings = pygment.component.Button("button_settings", ("10pw", "40ph", "80pw", "20ph"), style=btn_style)
        btn_settings.add(pygment.component.Label("button_settings_label", ("50pw", "50ph", "80pw", "80ph"), text="settings", align_center=True, centered=True))
        btn_settings.on_mouse_enter = lambda btn: self._change_selected_button(btn)
        btn_settings.on_mouse_click = self._button_settings_callback
        btn_settings.join(menu_buttons)
        
        btn_quit = pygment.component.Button("button_quit", ("10pw", "70ph", "80pw", "20ph"), style=btn_style)
        btn_quit.add(pygment.component.Label("button_quit_label", ("50pw", "50ph", "80pw", "80ph"), text="quit", align_center=True, centered=True))
        btn_quit.on_mouse_enter = lambda btn: self._change_selected_button(btn)
        btn_quit.on_mouse_click = self._button_quit_callback
        btn_quit.join(menu_buttons)
        
        layout = (menu,)
        self.viewrenderer = pygment.ViewRenderer((0,0), layout)
        
        self._buttons = (btn_play, btn_settings, btn_quit)
        self._selected_button = btn_play
        self._selected_button.style.border_thickness = 6
        self._selected_button_idx = self._buttons.index(self._selected_button)
        self._change_selected_button(btn_play)


    def handle_input(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.QUIT:
                self.root.request_quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._selected_button_idx = (self._selected_button_idx - 1) % len(self._buttons)
                    self._change_selected_button(self._buttons[self._selected_button_idx])

                elif event.key == pygame.K_RETURN:
                    self._selected_button.on_mouse_click()
                    
                elif event.key == pygame.K_DOWN:
                    self._selected_button_idx = (self._selected_button_idx + 1) % len(self._buttons)
                    self._change_selected_button(self._buttons[self._selected_button_idx])
                    
                elif event.key == pygame.K_p:
                    self._button_play_callback()
                    
                elif event.key == pygame.K_s:
                    self._button_settings_callback()
                    
                elif event.key == pygame.K_q:
                    self._button_quit_callback()
                    
            elif event.type == SMEvent.CON_KNOB_CW:
                self._selected_button_idx = (self._selected_button_idx + 1) % len(self._buttons)
                self._change_selected_button(self._buttons[self._selected_button_idx])       
                
            elif event.type == SMEvent.CON_KNOB_CCW:
                self._selected_button_idx = (self._selected_button_idx - 1) % len(self._buttons)
                self._change_selected_button(self._buttons[self._selected_button_idx])    
                        
                    
    def prepare(self) -> None:
        self.root.set_background_visibility(True)
        self.viewrenderer.size = self.root.display_surface.get_size()
          
            
    def update(self, dt: int) -> None:
        self.viewrenderer.update(dt)
    
    
    def render(self, surface: pygame.surface.Surface) -> None:
        self.viewrenderer.render(surface, (0,0))
        
        
    def on_window_resize(self) -> None:
        self.viewrenderer.size = self.root.display_surface.get_size()
        
        
    def _button_play_callback(self, *args) -> None:
        self.root.request_sound_play("SoundMania\\src\\menu_select.ogg")
        self.root.request_view_change(view.MapIndexView)
        
    
    def _button_settings_callback(self, *args) -> None:
        self.root.request_sound_play("SoundMania\\src\\menu_select.ogg")
        self.root.request_transition_play("out", 150)
        self.root.request_view_change(view.UserSettingsView)
        self.root.request_transition_play("in", 150)
        
        
    def _button_quit_callback(self, *args) -> None:
        self.root.request_sound_play("SoundMania\\src\\menu_select.ogg")
        self.root.request_transition_play("out", 1250)
        self.root.request_quit()
    
    
    def _change_selected_button(self, button: pygment.component.Button) -> None:
        if button != self._selected_button:
            self._selected_button.style.border_thickness = 0
            
            self._selected_button = button 
            self._selected_button.style.border_thickness = 6
            
            self._selected_button_idx = self._buttons.index(button)
            self.root.request_sound_play("SoundMania\\src\\menu_tick.ogg")
        