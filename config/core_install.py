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


class BaseDialog(QtWidgets.QDialog):
    """Base Dialog class for pop ups.

    Args:
        QtWidgets.QDialog (class): QDialog class inheritance.
    """

    def __init__(self):
        super(BaseDialog, self).__init__()
        self.init_ui()
        self.setGeometry(150, 140, 100, 100)
        self.center_window()
        # self.setStyleSheet(get_stylesheet())
        self.setObjectName("pop_up")

    def init_ui(self):
        """Init pop up UI."""
        pass

    def center_window(self):
        """Centers window on screen"""

        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())

    def close_window(self):
        """Close pop up window."""

        self.close()


class PopUpFields(BaseDialog):
    """Warning Pop Up if empty field.

    Args:
        BaseDialog (class): Base Dialog class inheritance.
    """

    def __init__(self):
        super(PopUpFields, self).__init__()

    def init_ui(self):
        """Init PopUpConfirmation UI."""

        main_layout = QtWidgets.QVBoxLayout(self)
        horizontal_layout = QtWidgets.QHBoxLayout()
        warning_label = QtWidgets.QLabel("Please enter a value in both fields.")
        self.confirm_button = QtWidgets.QPushButton("OK", self)
        main_layout.addWidget(warning_label)
        main_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.confirm_button)

        self.confirm_button.clicked.connect(self.close_window)


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
        self.pop_up_empty = PopUpFields()
        self.delete_install_path = None
        self.days_delta = None
        self.install_dict = {"DELETING_FOLDER": None, "DAYS_DELTA": None}

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
        tooltip1 = (
            "Pick the folder path where selected caches will be sent,"
            "filed and deleted according to their last modified"
            " dates. Best to create a new folder."
        )
        self.delete_path_button.setToolTip(tooltip1)
        self.browse_button.setToolTip(tooltip1)
        self.layout_h1.addWidget(self.delete_path_button)
        self.layout_h1.addWidget(self.browse_button)

        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.days_button = QtWidgets.QLineEdit(self)
        self.days_button.setInputMask("999")
        self.days_label = QtWidgets.QLabel("Days")
        tootltip2 = (
            "The time threshold after which the files stored in the "
            "folder specified above will be deleted"
        )
        self.days_button.setToolTip(tootltip2)
        self.days_label.setToolTip(tootltip2)
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

        # Connect
        self.browse_button.clicked.connect(self.select_file)
        self.install_button.clicked.connect(self.make_install)

        # Default, to delete
        # self.delete_path_button.setText(
        #     "/Users/matthieu/GIT/cache_deleter/deleting_folder"
        # )
        # self.days_button.setText("14")

    def get_delete_folder_path(self):
        self.delete_install_path = self.delete_path_button.text()
        if os.listdir(self.delete_install_path) or not os.path.exists(
            self.delete_install_path
        ):
            self.delete_install_path = os.path.join(
                self.delete_install_path, "deleting_folder"
            )

    def get_days_delta(self):
        self.days_delta = int(self.days_button.text())

    def fill_install_dict(self):
        self.install_dict["DELETING_FOLDER"] = self.delete_install_path
        self.install_dict["DAYS_DELTA"] = self.days_delta

    def select_file(self):
        """Create File browser and set selected directory to delete file folder parameter."""

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDirectory(HOME)
        folder_path = file_dialog.getExistingDirectory()
        self.delete_path_button.setText(folder_path)

    def make_install(self):
        self.get_delete_folder_path()
        self.get_days_delta()
        self.fill_install_dict()

        if not os.path.exists(self.delete_install_path):
            os.mkdir(self.delete_install_path)

        if not self.delete_install_path or not self.days_delta:
            self.pop_up_empty.exec_()
            return
        settings_json = os.path.join(os.path.dirname(__file__), "settings.json")

        with open(settings_json, "w") as out_json:
            json.dump(self.install_dict, out_json, indent=4)

        QtCore.QCoreApplication.instance().quit()

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