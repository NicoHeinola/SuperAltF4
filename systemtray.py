from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QObject
import sys
import threading
import time


# Icons by: www.freepik.com

class SuperAltF4Tray(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon("./icons/active.png"))

        self.__activated = True

        menu = QtWidgets.QMenu()

        self.__toggle_app = menu.addAction("Disable")
        self.__toggle_app.triggered.connect(self.__toggleActivate)
        self.__toggle_app.setIcon(QtGui.QIcon("./icons/disable.png"))

        menu.addSeparator()

        self.__radio1 = menu.addAction("Kill Single Task")
        self.__radio1.setCheckable(True)
        self.__radio1.setChecked(True)
        self.__radio1.setIcon(QtGui.QIcon("./icons/radio_enabled.png"))
        self.__radio1.triggered.connect(lambda: self.__toggleMode(self.__radio1, 0))

        self.__radio2 = menu.addAction("Kill All Similar Tasks")
        self.__radio2.setCheckable(True)
        self.__radio2.triggered.connect(lambda: self.__toggleMode(self.__radio2, 1))
        self.__radio2.setIcon(QtGui.QIcon("./icons/radio_disabled.png"))
        self.__mode = 0

        menu.addSeparator()

        exit_app = menu.addAction("Exit")
        exit_app.triggered.connect(lambda: sys.exit())
        exit_app.setIcon(QtGui.QIcon("./icons/exit.png"))

        self.setContextMenu(menu)

        self.activated.connect(self.__onActivated)

    def __onActivated(self, reason):
        """
        Checks if double clicked
        :param reason: Event
        """
        if reason == self.DoubleClick:
            self.__toggleActivate()

    def getMode(self) -> int:
        """
        Returns the radio button state
        """
        return self.__mode

    def __toggleModeCompare(self, clicked: QtWidgets.QAction, to_compare: QtWidgets.QAction, mode: int) -> bool:
        """
        Toggles radio buttons between each other and updates 'mode'
        :param clicked: Radio button which was clicked
        :param to_compare: Other radio button
        :param mode: which radio button is active
        :return: Bool -> was the mode changed or not
        """
        if clicked != to_compare:
            if to_compare.isChecked():
                to_compare.setChecked(False)
                to_compare.setIcon(QtGui.QIcon("./icons/radio_disabled.png"))
                clicked.setIcon(QtGui.QIcon("./icons/radio_enabled.png"))
                self.__mode = mode
                return True
            else:
                clicked.setChecked(True)
                return False

    def __toggleMode(self, clicked: QtWidgets.QAction, mode: int):
        """
        Toggles between two radio buttons
        :param clicked: Clicked radio button
        :param mode: Radio button's mode
        """
        if not self.__toggleModeCompare(clicked, self.__radio1, mode):
            self.__toggleModeCompare(clicked, self.__radio2, mode)

    def isActivated(self) -> bool:
        """
        Checks whether or not the program is activated
        :return: True or False
        """
        return self.__activated

    def __toggleActivate(self):
        """
        Toggles the variable which determines if this program is active or not
        """
        if self.__activated:
            self.__activated = False
            self.__toggle_app.setText("Enable")
            self.__toggle_app.setIcon(QtGui.QIcon("./icons/enable.png"))
            self.setIcon(QtGui.QIcon("./icons/disabled.png"))
        else:
            self.__activated = True
            self.__toggle_app.setText("Disable")
            self.__toggle_app.setIcon(QtGui.QIcon("./icons/disable.png"))
            self.setIcon(QtGui.QIcon("./icons/active.png"))

    def show(self) -> None:
        super(SuperAltF4Tray, self).show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    tray_icon = SuperAltF4Tray()
    tray_icon.show()
    sys.exit(app.exec_())
