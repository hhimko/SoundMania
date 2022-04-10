from serial.tools.list_ports import comports
from serial import Serial, SerialException

import logging
logger = logging.getLogger("SerialDevice")


class SerialDevice:
    """
    Simplified wrapper for `pyserial.Serial` objects.
    """
    def __init__(self, device_name: str = "Arduino"):
        self.port = Serial(baudrate=115200, timeout=None)
        self.device_name = device_name


    @property
    def connected(self) -> bool:
        """
        Check whether the port is active.
        
        Returns:
            True if the device's port was successfully located and is currently opened, otherwise False
        """
        if not self.port.is_open:
            return False
        
        try:
            self.port.in_waiting # try pinging the device to see if the port connection is still open 
        except SerialException:
            logger.info(f"Connection to device `{self.device_name}` was unexpectedly lost")
            self.port.close()
            return False
        else:
            return True
    
    
    def read(self) -> list[int]:
        """
        Retrieve recieved bytes from the serial port buffer.
        
        Returns:
            list of recieved bytes converted to integer values
        """
        recv = self.port.read_all()
        return list(recv) if recv else []
    
    
    def disconnect(self):
        """
        Close the serial connection.
        """
        if not self.connected: 
            return
        
        self.port.close()
        logger.info(f"Device `{self.device_name}` was successfully disconnected")
        
    
    def connect(self) -> bool:
        """
        Make a single attempt of connecting to a port with a desired name given by `self.device_name`.
        
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