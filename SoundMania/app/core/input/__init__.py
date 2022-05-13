from enum import IntEnum

import pygame


class SMEvent(IntEnum):
    CON_BUTTON_DOWN = pygame.event.custom_type()
    CON_BUTTON_UP   = pygame.event.custom_type()
    