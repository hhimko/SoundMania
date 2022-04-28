from sys import path
path.append("SoundMania/app")

import logging
logging.basicConfig(level="DEBUG", 
                    format="[{levelname}][{asctime}] {name}: {message}", 
                    style='{', 
                    datefmt=f"%H:%M:%S")

from app import SoundMania


if __name__ == "__main__":
    app = SoundMania()
    app.run()
    