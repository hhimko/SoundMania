from typing import Any, Callable

import pygame

from core.input.smcontroller import SMController
from core.input import SMEvent


class InputManager:
    """ Manager class responsible for generating events. """
    def __init__(self):
        self.controller = self._controller_init()
        
        self._controller_conversions = {
            "OL": pygame.K_RETURN,
            "IL": pygame.K_RETURN,
            "IR": pygame.K_ESCAPE,
            "OR": pygame.K_ESCAPE
        }
        
        
    def poll_events(self) -> list[pygame.event.Event]:
        event_list = pygame.event.get()
        for event in event_list:
            pass
        return event_list
    
    
    def update(self, dt: int) -> None:
        self.controller.update(dt)
        
        
    def _controller_init(self) -> SMController:
        con = SMController()
        
        con.on_ol_button_state_changed = self._con_button_handler("OL")
        con.on_il_button_state_changed = self._con_button_handler("IL")
        con.on_ir_button_state_changed = self._con_button_handler("IR")
        con.on_or_button_state_changed = self._con_button_handler("OR")
        
        return con
    
    def _con_button_handler(self, button_label: Any) -> Callable[[Any, Any], None]:
        
        def _handler(obj: Any, new_state: Any) -> None:
            smevent_type = SMEvent.CON_BUTTON_DOWN if new_state else SMEvent.CON_BUTTON_UP
            pygame.event.post(pygame.event.Event(smevent_type, button=button_label))
            
            converted_key = self._controller_conversions.get(button_label)
            if converted_key:
                pgevent_type = pygame.KEYDOWN if new_state else pygame.KEYUP
                pygame.event.post(pygame.event.Event(pgevent_type, key=converted_key))
            
        return _handler
        