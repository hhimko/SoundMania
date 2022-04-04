from serialdevice import SerialDevice
from time import sleep

import logging
logging.basicConfig(level="INFO", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")


if __name__ == "__main__":
    arduino = SerialDevice(device_name="Arduino")
    arduino._try_connect()
    sleep(3) # wait for the connection to settle

    while True:
        arduino.port.write(b'\x00')
        sleep(0.1)
        arduino.port.write(b'\xFF')
        sleep(0.1)
        