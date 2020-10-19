"""Cache Deleter Install"""


import sys
import json
import os
import platform
from PySide2 import QtWidgets, QtCore, QtGui

# Set constants
PLATFORM_NAME = platform.system().lower()
if PLATFORM_NAME == "windows":
    HOME = os.environ.get("USERPROFILE")
else:
    HOME = os.path.expanduser("~")


class Installer(QtWidgets.QDialog):
    """Cache Deleter Installer main class.

    Args:
        QtWidgets.QDialog (class): QtWidgets.QDialog inheritance.
    """

    def __init__(self):
        super(Installer, self).__init__()
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Install Cache Deleter")
        self.center_window()

    def init_ui(self):
        """Init UI Layout."""
        self.screen_size = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.app_size = (
            round(self.screen_size.width() * 0.3),
            round(self.screen_size.height() * 0.1),
        )
        # Layout management
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.vertical_spacer_1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.layout_h1 = QtWidgets.QHBoxLayout()
        self.delete_path_button = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse...", self)
        self.layout_h1.addWidget(self.delete_path_button)
        self.layout_h1.addWidget(self.browse_button)

        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.days_button = QtWidgets.QLineEdit(self)
        self.days_label = QtWidgets.QLabel("Days")
        self.horizontal_spacer_1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.layout_h2.addItem(self.horizontal_spacer_1)
        self.layout_h2.addWidget(self.days_button)
        self.layout_h2.addWidget(self.days_label)
        self.layout_h2.addItem(self.horizontal_spacer_1)

        self.layout_h3 = QtWidgets.QHBoxLayout()
        self.install_button = QtWidgets.QPushButton("Install", self)
        self.layout_h3.addWidget(self.install_button)

        self.main_layout.addLayout(self.layout_h1)
        self.main_layout.addLayout(self.layout_h2)
        self.main_layout.addLayout(self.layout_h3)
        self.main_layout.addItem(self.vertical_spacer_1)

        # Appearance
        self.days_button.setMaximumWidth(40)
        self.install_button.setMaximumWidth(150)

    def select_file(self):
        """Create File browser and set selected directory to delete file folder parameter."""

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDirectory(HOME)
        folder_path = file_dialog.getExistingDirectory()
        self.root_path_button.setText(folder_path)

    def center_window(self):
        """Centers window on screen."""

        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())


def main():
    """Set main program function."""

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    installer = Installer()
    installer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()