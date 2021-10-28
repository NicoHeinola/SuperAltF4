import os

from window import Window
import time
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QObject
import sys
import threading
import time
from systemtray import SuperAltF4Tray
import keyboard
from pygame import time as pg_time
import setproctitle


class Main:
    def __init__(self):
        super(Main, self).__init__()

        # Tray icon
        self.tray_icon = SuperAltF4Tray()
        self.tray_icon.show()

        # Options
        self.fps = 12
        self.wait_period = 1
        self.key = "ctrl+alt+f4"

    def keyLoop(self):
        if self.tray_icon.isActivated():
            keys = keyboard.get_hotkey_name()
            if keys == self.key:
                if self.tray_icon.getMode() == 0:
                    Window.killWindow()
                else:
                    Window.killSimilarWindows()
                time.sleep(self.wait_period)

    def start(self):
        clock = pg_time.Clock()
        while clock.tick(self.fps):
            self.keyLoop()


if __name__ == '__main__':
    setproctitle.setproctitle("Test 1234 :DD")
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    threading.Thread(target=main.start, daemon=True).start()
    sys.exit(app.exec_())
