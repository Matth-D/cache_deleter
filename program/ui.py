# usr/bin/python3.8

"""Cache Deleter"""


import sys
import os
import time
import platform
import utils
import datetime
from PySide2 import QtWidgets, QtGui, QtCore


# 1- Browse for path in machine - DONE
# 2- Select file or folder to be QTree root - DONE
# 3- Hit Scan button to deploy fill QTree widget - Need to cancel Scan if tree already filled - DONE
# 4- Use add or remove buttons to add items to delete list
# 5- Reset all or Delete all
# 6- When Delete button is pressed, prompt warning and ask for confirmation.


# Set constants
PLATFORM_NAME = platform.system().lower()
if PLATFORM_NAME == "windows":
    HOME = os.environ.get("USERPROFILE")
else:
    HOME = "~"


class RootPercentageBar(QtWidgets.QProgressBar):
    def __init__(self, value):
        super(RootPercentageBar, self).__init__()
        self.setValue(value)


class PopUpConfirmation(QtWidgets.QDialog):
    def __init__(self):
        super(PopUpConfirmation, self).__init__()
        self.init_ui()
        self.setGeometry(150, 140, 100, 100)
        self.center_window()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        horizontal_layout = QtWidgets.QHBoxLayout()
        warning_label = QtWidgets.QLabel(
            "All files selected will be permmanently lost. Continue ?"
        )
        confirm_button = QtWidgets.QPushButton("Confirm", self)
        cancel_button = QtWidgets.QPushButton("Cancel", self)

        main_layout.addWidget(warning_label)
        main_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(confirm_button)
        horizontal_layout.addWidget(cancel_button)

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())

    def close(self):
        self.close()


class PopUpNoPath(QtWidgets.QDialog):
    def __init__(self):
        super(PopUpNoPath, self).__init__()
        self.init_ui()
        self.setGeometry(150, 140, 100, 100)
        self.center_window()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        warning_label = QtWidgets.QLabel("Please enter a root path before scanning")
        ok_button = QtWidgets.QPushButton("OK", self)

        main_layout.addWidget(warning_label)
        main_layout.addWidget(ok_button)

        ok_button.clicked.connect(self.close_window)

    def center_window(self):
        """Centers window on screen."""
        app_geo = self.frameGeometry()
        center_point = (
            QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        )
        app_geo.moveCenter(center_point)
        self.move(app_geo.topLeft())

    def close_window(self):
        self.close()


class FileTree(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(FileTree, self).__init__()
        self.root_path_button = kwargs.pop("root", HOME)
        self.time_threshold_button = kwargs.pop("time", None)
        self.root_path = None
        self.root_size = None
        self.time_delta = None
        self.setHeaderLabels(["Name", "File Size", "root %", "Date Modified"])
        self.pop_up = PopUpNoPath()

    def get_root_value(self):
        self.root_path = self.root_path_button.text()
        self.root_size = utils.get_size(self.root_path)

    def get_time_threshold(self):
        self.time_delta = int(self.time_threshold_button.text())

    def fill_tree(self):
        top_level_item = QtWidgets.QTreeWidget.topLevelItem(self, 0)

        if top_level_item is not None:
            return
        if self.root_path is None:
            self.pop_up.exec_()
            return

        def iterate_file(current_dir, current_item):

            today = datetime.date.today()

            for file in os.listdir(current_dir):
                path = os.path.join(current_dir, file)
                byte_size = utils.get_size(path)
                file_size = utils.byte_size_to_display(byte_size)
                if byte_size == 0:
                    root_prct = 0
                else:
                    root_prct = round((byte_size / self.root_size) * 100)
                m_time = os.path.getmtime(path)
                m_date = datetime.datetime.fromtimestamp(m_time).date()
                datetime_delta = datetime.timedelta(self.time_delta)
                limit_date = today - datetime_delta
                m_date_display = m_date.strftime("%d/%m/%Y")

                if os.path.isdir(path):
                    dir_item = QtWidgets.QTreeWidgetItem(current_item)
                    dir_item.setText(0, file)
                    dir_item.setText(1, file_size)
                    progress = self.setItemWidget(
                        dir_item, 2, RootPercentageBar(root_prct)
                    )
                    dir_item.setText(3, m_date_display)
                    # if m_date < limit_date:
                    #    dir_item.setText(3, "after")
                    # else:
                    #    dir_item.setText(3, "before")
                    iterate_file(path, dir_item)

                else:
                    file_item = QtWidgets.QTreeWidgetItem(current_item)
                    file_item.setText(0, file)
                    file_item.setText(1, file_size)
                    progress = self.setItemWidget(
                        file_item, 2, RootPercentageBar(root_prct)
                    )
                    file_item.setText(3, m_date_display)
                    # if m_date < limit_date:
                    #    file_item.setText(3, "after")
                    # else:
                    #    file_item.setText(3, "before")

        iterate_file(self.root_path, self)


class CacheDeleter(QtWidgets.QDialog):
    def __init__(self):
        super(CacheDeleter, self).__init__()
        self.root_path = None
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Cache Deleter")
        self.center_window()
        self.time_threshold = None

    def init_ui(self):
        """Init UI Layout."""
        self.screen_size = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.app_size = (
            round(self.screen_size.width() * 0.4),
            round(self.screen_size.height() * 0.8),
        )
        # Layout management
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.layout_h1 = QtWidgets.QHBoxLayout()
        self.root_path_button = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse...", self)
        self.layout_h1.addWidget(self.root_path_button)
        self.layout_h1.addWidget(self.browse_button)

        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.extensions_list = QtWidgets.QLineEdit(self)
        self.extensions_label = QtWidgets.QLabel("File extensions")
        self.time_threshold_button = QtWidgets.QLineEdit(self)
        self.time_threshold_button.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
            )
        )
        self.time_threshold_button.setInputMask("999")
        self.time_threshold_button.setMaximumWidth(60)
        self.time_threshold_label = QtWidgets.QLabel("Limit Date")
        self.scan_button = QtWidgets.QPushButton("Scan", self)
        self.layout_h2.addWidget(self.extensions_list)
        self.layout_h2.addWidget(self.extensions_label)
        self.layout_h2.addWidget(self.time_threshold_button)
        self.layout_h2.addWidget(self.time_threshold_label)
        self.layout_h2.addWidget(self.scan_button)

        self.layout_filetree = QtWidgets.QVBoxLayout()
        self.file_tree = FileTree(
            self, root=self.root_path_button, time=self.time_threshold_button
        )
        self.layout_filetree.addWidget(self.file_tree)

        self.layout_h3 = QtWidgets.QHBoxLayout()
        self.add_list = QtWidgets.QPushButton("Add", self)
        self.remove_list = QtWidgets.QPushButton("Remove", self)
        self.horizontal_spacer_1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.layout_h3.addWidget(self.add_list)
        self.layout_h3.addWidget(self.remove_list)
        self.layout_h3.addItem(self.horizontal_spacer_1)
        self.layout_h3.setSpacing(50)

        self.layout_h4 = QtWidgets.QHBoxLayout()
        self.list_view = QtWidgets.QListWidget()
        self.layout_h4.addWidget(self.list_view)

        self.layout_v2 = QtWidgets.QVBoxLayout()
        self.layout_h4.addLayout(self.layout_v2)
        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.reset_all_button = QtWidgets.QPushButton("Reset All", self)
        self.delete_button.setMinimumHeight(80)
        self.reset_all_button.setMinimumHeight(80)
        self.vertical_spacer_1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.layout_v2.addWidget(self.delete_button)
        self.layout_v2.addWidget(self.reset_all_button)
        self.layout_v2.addItem(self.vertical_spacer_1)

        self.main_layout.addLayout(self.layout_h1)
        self.main_layout.addLayout(self.layout_h2)
        self.main_layout.addLayout(self.layout_filetree)
        self.main_layout.addLayout(self.layout_h3)
        self.main_layout.addLayout(self.layout_h4)

        # Signals and connect
        self.extensions_list.setText("bgeo.sc,vdb,abc")
        self.browse_button.clicked.connect(self.select_file)
        self.root_path_button.textChanged.connect(self.file_tree.get_root_value)
        self.time_threshold_button.textChanged.connect(
            self.file_tree.get_time_threshold
        )
        self.scan_button.clicked.connect(self.file_tree.fill_tree)
        self.time_threshold_button.setText("14")
        self.root_path_button.setText(
            "/home/matthieu/GIT/cache_deleter/program/test_folder"
        )

    def select_file(self):
        self.file_dialog = QtWidgets.QFileDialog()
        self.file_dialog.setDirectory(HOME)
        self.folder_path = self.file_dialog.getExistingDirectory()
        self.root_path_button.setText(self.folder_path)

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
    cache_deleter = CacheDeleter()
    cache_deleter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
