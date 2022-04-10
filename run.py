from sys import path
path.append("app")

from app import SoundMania


if __name__ == "__main__":
    app = SoundMania()
    app.run()