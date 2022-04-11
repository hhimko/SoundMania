from serialdevice import SerialDevice

import logging
logger = logging.getLogger("ArduinoController")

PACKET_TYPE_MASK = 0b10000000

PACKET_BTN0_MASK = 0b00000001
PACKET_BTN1_MASK = 0b00000010
PACKET_BTN2_MASK = 0b00000100
PACKET_BTN3_MASK = 0b00001000


class ArduinoController:
    CONNECTION_TIMEOUT = 5000 # timeout between device connection attempts in ms
    
    def __init__(self):
        self._dev = SerialDevice(device_name="Arduino")
        
        self._knobs = (0,0)
        self._buttons = [False, False, False, False]
        self.state = []
        
        self._timeout = 0
        
        
    @property    
    def l_knob(self) -> int:
        """ Return the current state of left knob. """
        return self._knobs[0]
    
    
    @property    
    def r_knob(self) -> int:
        """ Return the current state of right knob. """
        return self._knobs[1]
    
    
    @property    
    def ol_button(self) -> bool:
        """ Return the current state of outer left button. """
        return self._buttons[0]
    
    
    @property    
    def il_button(self) -> bool:
        """ Return the current state of inner left button. """
        return self._buttons[1]
    
    
    @property    
    def ir_button(self) -> bool:
        """ Return the current state of inner right button. """
        return self._buttons[2]
    
    
    @property    
    def or_button(self) -> bool:
        """ Return the current state of outer right button. """
        return self._buttons[3]
    
    
    def update(self, dt: int):
        if not self._dev.connected:
            self._try_connect(dt)
            return
        
        for packet in self._dev.read():
            self._decode_packet(packet)
            
            print(list(map(int, self._buttons)))
        
        
    def poll_event(self) -> list[int]:
        return self.state
    
    
    def _decode_packet(self, packet: int):
        if packet & PACKET_TYPE_MASK: # knob-state packet recieved
            self._update_knobs_state()
            
        else: # button-state packet recieved
            b0 = bool(packet & PACKET_BTN0_MASK)
            b1 = bool(packet & PACKET_BTN1_MASK)
            b2 = bool(packet & PACKET_BTN2_MASK)
            b3 = bool(packet & PACKET_BTN3_MASK)
            
            self._update_buttons_state(b0, b1, b2, b3)
    
    def _update_knobs_state(self):
        pass
    
    
    def _update_buttons_state(self, btn0: bool, btn1: bool, btn2: bool, btn3: bool):
        self._buttons = [btn0, btn1, btn2, btn3]
    
    
    def _try_connect(self, dt: int):
        if self._timeout > 0:
            self._timeout -= dt
            return
        
        if not self._dev.connect():
            self._timeout = self.CONNECTION_TIMEOUT
            logger.info(f"Could not connect to the controller, retrying in {self.CONNECTION_TIMEOUT}ms")