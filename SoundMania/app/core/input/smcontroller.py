import logging
logger = logging.getLogger("SMController")

from core.core import callback_property, notify_property_changed
from core.input.serialdevice import SerialDevice


class SMController:
    """ Class responsible for maintaining connection with a custom SoundMania game controller. """
    PACKET_TYPE_MASK   = 0b10000000
    PACKET_TYPE_BUTTON = 0
    PACKET_TYPE_KNOB   = 1

    PACKET_OL_BTN_MASK = 0b00000001
    PACKET_IL_BTN_MASK = 0b00000010
    PACKET_IR_BTN_MASK = 0b00000100
    PACKET_OR_BTN_MASK = 0b00001000

    CONNECTION_TIMEOUT = 5000 # timeout between device connection attempts in ms
    
    on_ol_button_state_changed = callback_property()
    on_il_button_state_changed = callback_property()
    on_ir_button_state_changed = callback_property()
    on_or_button_state_changed = callback_property()
    on_l_knob_state_changed    = callback_property()
    on_r_knob_state_changed    = callback_property()
    
    def __init__(self):
        self._dev = SerialDevice(device_name="Arduino")
        
        self._knobs = [0, 0]
        self._buttons = [False, False, False, False]
        
        self._timeout = 0
        
        
    @notify_property_changed(on_ol_button_state_changed)
    def ol_button(self) -> bool:
        """ Return the current state of outer left button. """
        return self._buttons[0]
    
    
    @ol_button.setter
    def ol_button(self, value: bool) -> None:
        self._buttons[0] = value
        
    
    @notify_property_changed(on_il_button_state_changed)
    def il_button(self) -> bool:
        """ Return the current state of inner left button. """
        return self._buttons[1]
    
    
    @il_button.setter
    def il_button(self, value: bool) -> None:
        self._buttons[1] = value
    
    
    @notify_property_changed(on_ir_button_state_changed)
    def ir_button(self) -> bool:
        """ Return the current state of inner right button. """
        return self._buttons[2]
    
    
    @ir_button.setter
    def ir_button(self, value: bool) -> None:
        self._buttons[2] = value
    
    
    @notify_property_changed(on_or_button_state_changed)
    def or_button(self) -> bool:
        """ Return the current state of outer right button. """
        return self._buttons[3]
    
    
    @or_button.setter
    def or_button(self, value: bool) -> None:
        self._buttons[3] = value
    
    
    @notify_property_changed(on_l_knob_state_changed)
    def l_knob(self) -> int:
        """ Return the current state of left knob. """
        return self._knobs[0]
    
    
    @l_knob.setter
    def l_knob(self, value: int) -> None:
        self._knobs[0] = value
    
    
    @notify_property_changed(on_r_knob_state_changed)    
    def r_knob(self) -> int:
        """ Return the current state of right knob. """
        return self._knobs[1]
    
    
    @r_knob.setter
    def r_knob(self, value: int) -> None:
        self._knobs[1] = value
    
    
    def update(self, dt: int):
        """ Update the controller state by reading the devices serial port buffer.
        
            This method is additionally responsible for maintaining the connection
            with the controller. It periodically attempts to open the connection and
            pings the serial port to check its current state. 
            
            Args:
                dt: elapsed time since the last frame. 
        """
        if not self._dev.connected:
            self._try_connect(dt)
            return
        
        for packet in self._dev.read():
            self._read_packet(packet)
        
        
    def _read_packet(self, packet: int) -> None:
        if packet & self.PACKET_TYPE_MASK == self.PACKET_TYPE_BUTTON:
            self._decode_button_packet(packet)
        else:
            self._decode_knob_packet(packet)
        
                    
    def _decode_button_packet(self, packet: int) -> None:
        self.ol_button = bool(packet & self.PACKET_OL_BTN_MASK)
        self.il_button = bool(packet & self.PACKET_IL_BTN_MASK)
        self.ir_button = bool(packet & self.PACKET_IR_BTN_MASK)
        self.or_button = bool(packet & self.PACKET_OR_BTN_MASK)
        
        
    def _decode_knob_packet(self, packet: int) -> None:
        knob_idx = (packet >> 6) & 0b1
        negative = (packet >> 5) & 0b1
        change = (packet & 0b11111)
        if negative:
            change = -change
        
        if knob_idx:
            self.l_knob += change
        else:
            self.r_knob += change

    
    def _try_connect(self, dt: int) -> None:
        if self._timeout > 0:
            self._timeout -= dt
            return
        
        if not self._dev.connect():
            self._timeout = self.CONNECTION_TIMEOUT
            logger.info(f"Could not connect to the controller, retrying in {self.CONNECTION_TIMEOUT}ms")
            