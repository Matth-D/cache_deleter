#!/usr/bin/python3.8

"""Cache Deleter"""
import sys
from PySide2 import QtWidgets, QtGui, QtCore


class CacheDeleter(QtWidgets.QDialog):
    def __init__(self):
        super(CacheDeleter, self).__init__()
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Cache Deleter")
        self.center_window()

    def init_ui(self):
        """Init UI Layout."""
        desktop = QtWidgets.QDesktopWidget()
        self.screen_size = desktop.availableGeometry(desktop.primaryScreen())
        self.app_size = (
            round(self.screen_size.width() * 0.4),
            round(self.screen_size.height() * 0.8),
        )

        self.main_layout = QtWidgets.QVBoxLayout(self)

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())


def main():
    """Set main program function."""
    app = QtWidgets.QApplication(sys.argv)
    cache_deleter = CacheDeleter()
    cache_deleter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
