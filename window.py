import time

import win32gui
import win32process
import psutil
import os


class Window:
    @staticmethod
    def __killProcess(pid):
        try:
            os.system("TASKKILL /PID " + str(pid) + " /F")
        except Exception as e:
            print(e)

    @staticmethod
    def killWindow():
        """
        Kills the foreground or selected window
        """
        foreground_window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(foreground_window)[1]
        if Window.__checkBlacklist(pid):
            Window.__killProcess(pid)

    @staticmethod
    def __checkBlacklist(window_pid):
        for process in psutil.process_iter():
            name = process.name()
            pid = process.pid
            if window_pid == pid and name == "explorer.exe":
                return False
        return True

    @staticmethod
    def killSimilarWindows():
        """
        Kills all windows that have the same process name
        """

        fg_window = win32gui.GetForegroundWindow()
        fg_pid = win32process.GetWindowThreadProcessId(fg_window)[1]
        process_name = psutil.Process(fg_pid).name()

        for process in psutil.process_iter():
            name = process.name()
            pid = process.pid
            if name == process_name:
                # pids.append(pid)
                Window.__killProcess(pid)
