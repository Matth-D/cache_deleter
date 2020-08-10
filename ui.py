##!/usr/bin/python3.8

"""Cache Deleter"""
import sys
import os
from PySide2 import QtWidgets, QtGui, QtCore


# 1- Browse for path in machine
# 2- Select file or folder to be QTree root
# 3- Hit Scan button to deploy fill QTree widget
# 4- Use add or remove buttons to add items to delete list
# 5- Reset all or Delete all
# 6- When Delete button is pressed, prompt warning and ask for confirmation.

HOME = "~"


class FileTree(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(FileTree, self).__init__()
        self.root_dir = kwargs.pop("root", HOME)
        self.setHeaderLabels(["Name", "File Size", "root %", "Date Modified"])
        # self.item_test = QtWidgets.QTreeWidgetItem(self, ["prout", "2k","21%","21/12/2019"])
        # for i in range(4):
        #     subitm = QtWidgets.QTreeWidgetItem(self.item_test, ["prout", "2k","21%","21/12/2019"])

    def fill_tree(self):
        def iterate(current_dir, current_item):
            for file in os.listdir(current_dir):
                path = os.path.join(current_dir, file)
                if os.path.isdir(path):
                    dir_item = QtWidgets.QTreeWidgetItem(current_item)
                    dir_item.setText(0, file)
                    iterate(path, dir_item)
                else:
                    file_item = QtWidgets.QTreeWidgetItem(current_item)
                    file_item.setText(0, file)

        iterate(self.root_dir, self)


class CacheDeleter(QtWidgets.QDialog):
    def __init__(self):
        super(CacheDeleter, self).__init__()
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Cache Deleter")
        self.center_window()

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
        self.root_path = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.select_file)
        self.layout_h1.addWidget(self.root_path)
        self.layout_h1.addWidget(self.browse_button)

        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.extensions_list = QtWidgets.QLineEdit(self)
        self.extensions_label = QtWidgets.QLabel("File extensions")
        self.time_threshold = QtWidgets.QLineEdit(self)
        self.time_threshold_label = QtWidgets.QLabel("Limit Date")
        self.scan_button = QtWidgets.QPushButton("Scan", self)
        self.layout_h2.addWidget(self.extensions_list)
        self.layout_h2.addWidget(self.extensions_label)
        self.layout_h2.addWidget(self.time_threshold)
        self.layout_h2.addWidget(self.time_threshold_label)
        self.layout_h2.addWidget(self.scan_button)

        self.layout_filetree = QtWidgets.QVBoxLayout()
        self.file_tree = FileTree(self, root=self.root_path.text())
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
            20, 40, QtWidgets.QSizePolicy.Minimum
        )
        self.layout_v2.addWidget(self.delete_button)
        self.layout_v2.addWidget(self.reset_all_button)
        self.layout_v2.addItem(self.vertical_spacer_1)

        self.main_layout.addLayout(self.layout_h1)
        self.main_layout.addLayout(self.layout_h2)
        self.main_layout.addLayout(self.layout_filetree)
        self.main_layout.addLayout(self.layout_h3)
        self.main_layout.addLayout(self.layout_h4)

        # Default Values
        self.extensions_list.setText("bgeo.sc,vdb,abc")
        self.root_path.setText("/")

        self.file_tree.fill_tree()

    def select_file(self):
        self.file_dialog = QtWidgets.QFileDialog()
        self.file_qurl = self.file_dialog.getOpenFileUrl(self)
        self.file_path = self.file_qurl[0].toLocalFile()
        self.root_path.setText(self.file_path)

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
