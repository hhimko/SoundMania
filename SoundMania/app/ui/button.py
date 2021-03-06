import pygame

from core.core import callback_property
from ui.core import UIComponent


class Button(UIComponent):
    on_mouse_pressed = callback_property()
    on_mouse_click   = callback_property()
    on_mouse_over    = callback_property()
    on_mouse_down    = callback_property()
    on_mouse_up      = callback_property()

    def postinit(self) -> None:
        self.is_mouse_pressed = False
        self._was_mouse_pressed_on_enter = False
        self.is_mouse_over    = False


    def update(self, dt: int) -> None:
        mouse_pos = pygame.mouse.get_pos()
        
        mouse_over = self.get_rect().collidepoint(mouse_pos)
        if mouse_over:
            self.on_mouse_over()
            
            if not self.is_mouse_over:
                self._mouse_entering()
            
            lmb_down = pygame.mouse.get_pressed()[0]
            if lmb_down:
                self._mouse_pressing()
            else:
                if self.is_mouse_pressed:
                    self._mouse_releasing()
                
        else: # mouse not over
            if self.is_mouse_over:
                self._mouse_leaving()
        
        
    def _mouse_entering(self) -> None:
        """ Singly-triggered mouse event. 
            Played when mouse cursor enters the object boundary. 
        """
        self.is_mouse_over = True
        self._was_mouse_pressed_on_enter = pygame.mouse.get_pressed()[0]
        
        
    def _mouse_pressing(self) -> None:
        """ Continously-triggered mouse event. 
            Played when mouse button is pressed while cursor is over the object. 
        """
        if not self.is_mouse_pressed and not self._was_mouse_pressed_on_enter:
            self.on_mouse_down()
        
        self.is_mouse_pressed = True
        self.on_mouse_pressed()
        
        
    def _mouse_releasing(self) -> None:
        """ Singly-triggered mouse event. 
            Played when mouse button was released while cursor is over the object. 
        """
        self.is_mouse_pressed = False 
        if not self._was_mouse_pressed_on_enter:
            self.on_mouse_click()
            
        self._was_mouse_pressed_on_enter = False
        self.on_mouse_up()
        
        
    def _mouse_leaving(self) -> None:
        """ Singly-triggered mouse event. 
            Played when mouse cursor leaves the object boundary.
        """
        self.is_mouse_over = False
        self.is_mouse_pressed = False