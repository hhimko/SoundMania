from typing import Any, Callable

import pygame

from core.input.smcontroller import SMController
from core.input import SMEvent


class InputManager:
    """ Manager class responsible for generating events. """
    def __init__(self):
        self.controller = self._controller_init()
        self._last_knob_read = {"L": 0, "R": 0}
        
        self._controller_conversions = {
            "OL": pygame.K_RETURN,
            "IL": pygame.K_RETURN,
            "IR": pygame.K_ESCAPE,
            "OR": pygame.K_ESCAPE
        }
        
        
    def poll_events(self) -> list[pygame.event.Event]:
        event_list = pygame.event.get()
        
        # for event in event_list:
        #     pass # TODO: generate custom mouse wheel events
        
        return event_list
    
    
    def update(self, dt: int) -> None:
        self.controller.update(dt)
        
        
    def _controller_init(self) -> SMController:
        con = SMController()
        
        con.on_ol_button_state_changed = self._con_button_handler("OL")
        con.on_il_button_state_changed = self._con_button_handler("IL")
        con.on_ir_button_state_changed = self._con_button_handler("IR")
        con.on_or_button_state_changed = self._con_button_handler("OR")
        
        con.on_l_knob_state_changed = self._con_knob_handler("L")
        con.on_r_knob_state_changed = self._con_knob_handler("R")
        
        return con
    
    
    def _con_button_handler(self, button_label: str) -> Callable[[Any, Any], None]:
        
        def _handler(obj: Any, new_state: bool) -> None:
            smevent_type = SMEvent.CON_BUTTON_DOWN if new_state else SMEvent.CON_BUTTON_UP
            pygame.event.post(pygame.event.Event(smevent_type, button=button_label))
            
            converted_key = self._controller_conversions.get(button_label)
            if converted_key:
                pgevent_type = pygame.KEYDOWN if new_state else pygame.KEYUP
                pygame.event.post(pygame.event.Event(pgevent_type, key=converted_key))
            
        return _handler
    
    
    def _con_knob_handler(self, knob_label: str) -> Callable[[Any, Any], None]:
    
        def _handler(obj: Any, new_state: int) -> None:
            change = new_state - self._last_knob_read[knob_label]
            if abs(change) >= 4:
                self._last_knob_read[knob_label] = new_state
                smevent_type = SMEvent.CON_KNOB_CW if change > 0 else SMEvent.CON_KNOB_CCW
                pygame.event.post(pygame.event.Event(smevent_type, knob=knob_label))
            
        return _handler
        