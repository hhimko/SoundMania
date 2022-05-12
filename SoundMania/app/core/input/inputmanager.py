from core.input.arduinocontroller import ArduinoController
from core.input import InputEvent

import pygame


class InputManager:
    def __init__(self):
        self.controller = ArduinoController()
        
        
    def poll_events(self) -> list[InputEvent]:
        return []