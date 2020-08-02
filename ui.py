#!/usr/bin/python3.8

"""Cache Deleter"""
import sys
from PySide2 import QtWidgets, QtGui, QtCore


class FileTree(QtWidgets.QTreeWidget):
    def __init__(self):
        super(FileTree, self).__init__()


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
        self.setLayout(self.main_layout)

        self.layout_h1 = QtWidgets.QHBoxLayout()
        self.root_path = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse...", self)
        self.browse_button.clicked.connect(self.select_file)
        self.scan_button = QtWidgets.QPushButton("Scan", self)
        self.layout_h1.addWidget(self.root_path)
        self.layout_h1.addWidget(self.browse_button)
        self.layout_h1.addWidget(self.scan_button)

        self.layout_h2 = QtWidgets.QHBoxLayout()
        self.extensions_list = QtWidgets.QLineEdit(self)
        self.extensions_label = QtWidgets.QLabel("File extensions")
        self.time_threshold = QtWidgets.QLineEdit(self)
        self.time_threshold_label = QtWidgets.QLabel("Limit Date")
        self.layout_h2.addWidget(self.extensions_list)
        self.layout_h2.addWidget(self.extensions_label)
        self.layout_h2.addWidget(self.time_threshold)
        self.layout_h2.addWidget(self.time_threshold_label)

        self.file_tree = FileTree()

        self.layout_h3 = QtWidgets.QHBoxLayout()
        self.add_list = QtWidgets.QPushButton("Add", self)
        self.remove_list = QtWidgets.QPushButton("Remove", self)
        self.layout_h3.addWidget(self.add_list)
        self.layout_h3.addWidget(self.remove_list)

        self.placeholder = QtWidgets.QWidget()
        self.placeholder.setStyleSheet("background-color:grey")
        self.placeholder.setMinimumHeight(self.screen_size.height() * 0.2)

        self.main_layout.addLayout(self.layout_h1)
        self.main_layout.addLayout(self.layout_h2)
        self.main_layout.addWidget(self.file_tree)
        self.main_layout.addLayout(self.layout_h3)
        self.main_layout.addWidget(self.placeholder)

    def select_file(self):
        self.file_qurl = QtWidgets.QFileDialog().getOpenFileUrl(self)
        self.file_path = self.file_qurl[0].toLocalFile()
        self.root_path.setText(self.file_path)

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
