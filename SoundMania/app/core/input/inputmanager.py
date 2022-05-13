from core.input.smcontroller import SMController

import pygame


INPUT_EVENT = pygame.event.custom_type()

class InputManager:
    """ Manager class responsible for generating events. """
    def __init__(self):
        self.controller = SMController()
        
        self.controller.on_ol_button_state_changed = lambda _: print("OL")
        self.controller.on_il_button_state_changed = lambda _: print("IL")
        self.controller.on_ir_button_state_changed = lambda _: print("IR")
        self.controller.on_or_button_state_changed = lambda _: print("OR")
        
        
    def poll_events(self) -> list[pygame.event.Event]:
        event_list = pygame.event.get()
        for event in event_list:
            pass
        return event_list
    
    
    def update(self, dt: int) -> None:
        self.controller.update(dt)
        