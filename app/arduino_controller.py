from serialdevice import SerialDevice

import logging
logger = logging.getLogger("ArduinoController")


class ArduinoController:
    CONNECTION_TIMEOUT = 5000 # timeout between device connection attempts in ms
    
    def __init__(self):
        self._dev = SerialDevice(device_name="Arduino")
        
        self._knobs = (0,0)
        self.btn1_down = False
        self.btn2_down = False
        self.state = []
        
        self._timeout = 0
        
        
    @property    
    def lknob(self) -> int:
        return self._knobs[0]
    
    
    @property    
    def rknob(self) -> int:
        return self._knobs[1]
    
    
    def update(self, dt: int):
        if not self._dev.connected:
            self._try_connect(dt)
            return
        
        for x in self._dev.read():
            self.btn1_down = bool(x & 0b00000001)
            self.btn2_down = bool(x & 0b00000010)
            
        print(self.btn1_down, self.btn2_down)
        
        
    def poll_event(self) -> list[int]:
        return self.state
    
    
    def _try_connect(self, dt: int):
        """
        Make a single attempt of connecting to the controller based on the timeout value.
        """
        if self._timeout > 0:
            self._timeout -= dt
            return
        
        if not self._dev.connect():
            self._timeout = self.CONNECTION_TIMEOUT
            logger.info(f"Could not connect to the controller, retrying in {self.CONNECTION_TIMEOUT}ms")