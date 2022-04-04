from serial.tools.list_ports import comports
from serial import Serial, SerialException

import logging
logger = logging.getLogger("SerialDevice")


class SerialDevice:
    """
    Basic wrapper for `pyserial.Serial` objects.
    """
    def __init__(self, device_name: str = "Arduino"):
        self.port = Serial(baudrate=9600, timeout=None)
        self.device_name = device_name


    @property
    def connected(self) -> bool:
        """
        Returns:
            True if the device's port was successfully located and is currently opened, otherwise False
        """
        return self.port.is_open
    
    
    def disconnect(self):
        """
        Closes the serial connection.
        """
        self.port.close()
        logger.info(f"Device `{self.device_name}` was successfully disconnected")
        
    
    def _try_connect(self) -> bool:
        """
        Makes a single attempt of connecting to a port with a desired name given by `self.device_name`.
        
        Returns:
            True if a connection was established, otherwise False
        """
        dev_name = self.device_name.lower()
        for comport in comports():
            
            if dev_name in str(comport.description).lower():
                self.port.port = comport.name
                
                try:
                    self.port.open()
                except SerialException:
                    logger.exception(
                        f"Device `{self.device_name}` was found but the port could not be opened"
                    )
                    return False
                
                logger.info(f"Device `{self.device_name}` was successfully connected")
                return True
             
        return False
    
    
    def __del__(self):
        self.disconnect()