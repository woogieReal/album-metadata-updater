import os
import sys

from app import AlbumTagApp

if __name__ == "__main__":
    app = AlbumTagApp()
    app.run()
    if app.restart_requested:
        os.execv(sys.executable, [sys.executable] + sys.argv)
