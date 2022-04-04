from serialdevice import SerialDevice

import logging
logging.basicConfig(level="INFO", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")


if __name__ == "__main__":
    arduino = SerialDevice(device_name="Arduino")

    print(arduino._try_connect())
    print(arduino.connected)