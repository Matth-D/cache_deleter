"""Cache Deleter"""

import sys
import os
import datetime
import platform
import glob
import utils
from PySide2 import QtWidgets, QtGui, QtCore

# Set constants
PLATFORM_NAME = platform.system().lower()
if PLATFORM_NAME == "windows":
    HOME = os.environ.get("USERPROFILE")
else:
    HOME = os.path.expanduser("~")



class RootPercentageBar(QtWidgets.QProgressBar):
    def __init__(self, value):
        super(RootPercentageBar, self).__init__()
        self.setValue(value)
        self.setAlignment(QtCore.Qt.AlignCenter)

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
        self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        main_layout.addWidget(warning_label)
        main_layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(self.confirm_button)
        horizontal_layout.addWidget(self.cancel_button)

        self.cancel_button.clicked.connect(self.close_window)

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
        self.extensions_list = kwargs.pop("extensions", None)
        self.root_path = None
        self.root_size = None
        self.time_delta = None
        self.extensions = None
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setHeaderLabels(["Name", "File Size", "root %", "Date Modified"])
        self.pop_up = PopUpNoPath()
        self.item_path = None
        self.top_level_item = None

    def get_root_value(self):
        self.root_path = self.root_path_button.text()
        if not os.path.exists(self.root_path):
            print("File: {0} doesn't exist, check again".format(self.root_path))
            return
        self.root_size = utils.get_size(self.root_path)
    
    def get_top_level_item(self):
        self.top_level_item = QtWidgets.QTreeWidget.topLevelItem(self, 0)

    def get_time_threshold(self):
        self.time_delta = int(self.time_threshold_button.text())

    def get_extensions_list(self):
        self.extensions = self.extensions_list.text().split(',')

    def item_single(self, path, current_item):

        suffix = utils.get_suffix(path)
        if os.path.isfile(path) and suffix not in self.extensions:
            return

        today = datetime.date.today()
        item_name = os.path.basename(path)
        if path == self.root_path:
            item_name = self.root_path
        byte_size = utils.get_size(path)
        file_size = utils.byte_size_to_display(byte_size)

        root_prct = 0
        if byte_size != 0:
            root_prct = round((byte_size / self.root_size) * 100)

        m_time = os.path.getmtime(path)
        m_date = datetime.datetime.fromtimestamp(m_time).date()
        datetime_delta = datetime.timedelta(self.time_delta)
        limit_date = today - datetime_delta
        m_date_display = m_date.strftime("%d/%m/%Y")

        item = QtWidgets.QTreeWidgetItem(current_item)
        item.setText(0, item_name)
        item.setText(1, file_size)
        self.setItemWidget(item, 2, RootPercentageBar(root_prct))
        item.setText(3, m_date_display)
        if m_date < limit_date:
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
            item.setForeground(1, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
            item.setForeground(3, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
        return item
    
    def item_sequence(self, path_prefix, current_item):

        file_glob = glob.glob(path_prefix + "*")
        file_sample = file_glob[0]
        suffix = utils.get_suffix(file_sample)
        if suffix not in self.extensions:
            return
        today = datetime.date.today()
        basename = os.path.basename(path_prefix)
        min_frame = utils.get_frame(
            min(file_glob, key=lambda x: utils.get_frame(x))
        )
        max_frame = utils.get_frame(
            max(file_glob, key=lambda x: utils.get_frame(x))
        )
        padding = "#" * len(str(max_frame))
        item_name = "{0}.{1}{2} | ({3}-{4})".format(
            basename, padding, suffix, min_frame, max_frame
        )
        #creer function pour recuperer size d'une sequence a partir de file_glob
        byte_size = utils.get_size(file_sample)
        file_size = utils.byte_size_to_display(byte_size)

        root_prct = 0
        if byte_size != 0:
            root_prct = round((byte_size / self.root_size) * 100)

        m_time = os.path.getmtime(file_sample)
        m_date = datetime.datetime.fromtimestamp(m_time).date()
        datetime_delta = datetime.timedelta(self.time_delta)
        limit_date = today - datetime_delta
        m_date_display = m_date.strftime("%d/%m/%Y")

        item = QtWidgets.QTreeWidgetItem(current_item)
        item.setText(0, item_name)
        item.setText(1, file_size)
        self.setItemWidget(item, 2, RootPercentageBar(root_prct))
        item.setText(3, m_date_display)
        if m_date < limit_date:
            item.setForeground(0, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
            item.setForeground(1, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
            item.setForeground(3, QtGui.QBrush(QtGui.QColor(255, 15, 15)))
        return item

    def fill_tree(self):

        if self.top_level_item is not None:
            return
        if self.root_path is None:
            self.pop_up.exec_()
            return

        def iterate_file(current_dir, current_item):
            files = os.listdir(current_dir)
            paths = [os.path.join(current_dir, file) for file in files]
            dir_paths = [path for path in paths if os.path.isdir(path)]
            for path in dir_paths:
                dir_item = self.item_single(path, current_item)
                iterate_file(path, dir_item)

            file_paths = [path for path in paths if os.path.isfile(path)]
            file_s_paths = [path for path in file_paths if not utils.is_sequence(path)]
            file_sq_path = []

            #  create list with file prefixes to collapse into a sequence
            for path in file_paths:
                if not utils.is_sequence(path):
                    break
                sq_prefix = path.split(".")[0]
                if sq_prefix not in file_sq_path:
                    file_sq_path.append(sq_prefix)

            #add non sequence paths to tree
            for path in file_s_paths:
                self.item_single(path, current_item)

            for path in file_sq_path:
                self.item_sequence(path, current_item)

        root_item = self.item_single(self.root_path, self)
        self.expandItem(root_item)
        iterate_file(self.root_path, root_item)
        # iterate_file(self.root_path, self)

    def get_item_path(self, item):

        path_names = []

        def iterate_item(item, path):
            item_name = item.text(0)
            path.insert(0, item_name)
            parent_item = item.parent()
            if parent_item is not None:
                iterate_item(parent_item, path)
            else:
                return

        iterate_item(item, path_names)
        path_names.insert(0, self.top_level_item.text(0))
        # path_names.insert(0, self.root_path)
        self.item_path = os.path.join(*path_names)


class CacheDeleter(QtWidgets.QDialog):
    def __init__(self):
        super(CacheDeleter, self).__init__()
        self.root_path = None
        self.pop_up_confirmation = PopUpConfirmation()
        self.init_ui()
        self.setGeometry(300, 300, self.app_size[0], self.app_size[1])
        self.setWindowTitle("Cache Deleter")
        self.center_window()
        self.time_threshold = None
        self.list_item_selected = None
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stylesheets.css")

        with open(path, "r") as stream:
            css = stream.read()
        self.setStyleSheet(css)

    def init_ui(self):
        """Init UI Layout."""
        self.screen_size = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        self.app_size = (
            round(self.screen_size.width() * 0.6),
            round(self.screen_size.height() * 0.8),
        )
        # Layout management
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.layout_h1 = QtWidgets.QHBoxLayout()
        self.root_path_button = QtWidgets.QLineEdit(self)
        self.browse_button = QtWidgets.QPushButton("Browse...", self)
        self.browse_button.setObjectName("browse_button")
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
            self, root=self.root_path_button,
            time=self.time_threshold_button,
            extensions=self.extensions_list
        )
        self.layout_filetree.addWidget(self.file_tree)

        self.layout_h3 = QtWidgets.QHBoxLayout()
        self.add_list = QtWidgets.QPushButton("", self)
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
        self.reset_list_button = QtWidgets.QPushButton("Reset List", self)
        self.reset_all_button = QtWidgets.QPushButton("Reset All", self)
        self.delete_button.setMinimumHeight(50)
        self.reset_list_button.setMinimumHeight(50)
        self.reset_all_button.setMinimumHeight(50)
        self.vertical_spacer_1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.layout_v2.addWidget(self.delete_button)
        self.layout_v2.addWidget(self.reset_list_button)
        self.layout_v2.addWidget(self.reset_all_button)
        self.layout_v2.addItem(self.vertical_spacer_1)

        self.main_layout.addLayout(self.layout_h1)
        self.main_layout.addLayout(self.layout_h2)
        self.main_layout.addLayout(self.layout_filetree)
        self.main_layout.addLayout(self.layout_h3)
        self.main_layout.addLayout(self.layout_h4)

        self.main_layout.setStretch(2, 5)
        self.main_layout.setStretch(4, 1)

        # Signals and connect
        self.browse_button.clicked.connect(self.select_file)
        self.root_path_button.textChanged.connect(self.file_tree.get_root_value)
        self.time_threshold_button.textChanged.connect(
            self.file_tree.get_time_threshold
        )
        self.extensions_list.textChanged.connect(self.file_tree.get_extensions_list)
        self.scan_button.clicked.connect(self.file_tree.fill_tree)
        self.scan_button.clicked.connect(self.file_tree.get_top_level_item)
        self.time_threshold_button.setText("14")
        self.extensions_list.setText(".bgeo.sc,.vdb,.abc,.hip")
        self.file_tree.itemClicked.connect(self.file_tree.get_item_path)
        self.add_list.clicked.connect(self.add_item_list)
        self.remove_list.clicked.connect(self.remove_item_list)
        self.list_view.itemClicked.connect(self.get_list_item_path)
        self.reset_list_button.clicked.connect(self.reset_list)
        self.reset_all_button.clicked.connect(self.reset_all)
        self.delete_button.clicked.connect(self.exec_pop_up)
        self.pop_up_confirmation.confirm_button.clicked.connect(self.delete_file_list)

        # Appearance
        # self.add_list.setObjectName("add_list")
        iconpath = os.path.abspath("./icons/icon_test.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconpath))
        self.add_list.setIcon(icon)
        self.remove_list.setObjectName("remove_list")

    def select_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setDirectory(HOME)
        folder_path = file_dialog.getExistingDirectory()
        self.root_path_button.setText(folder_path)

    def add_item_list(self):
        item = self.file_tree.item_path
        # list_items = []
        check_list = self.list_view.findItems(item, QtCore.Qt.MatchExactly)
        check_list = [item.text() for item in check_list]
        if item in check_list:
            return
        self.list_view.addItem(item)

    def exec_pop_up(self):
        self.pop_up_confirmation.exec()

    def delete_file_list(self):
        for item_number in range(self.list_view.count()):
            item_path = self.list_view.item(item_number).text()
            if not os.path.exists(item_path):
                print('{0} not found or already deleted.'.format(os.path.basename(item_path)))
                continue
            utils.delete_file(item_path)
        self.pop_up_confirmation.close_window()
        self.list_view.clear()
        self.file_tree.clear()
        self.file_tree.fill_tree()

    def remove_item_list(self):
        row = self.list_view.row(self.list_item_selected)
        self.list_view.takeItem(row)

    def get_list_item_path(self, item):
        self.list_item_selected = item

    def reset_list(self):
        self.list_view.clear()

    def reset_all(self):
        self.root_path_button.setText("")
        self.file_tree.clear()
        self.list_view.clear()

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
    app.setStyle('Fusion')
    cache_deleter = CacheDeleter()
    cache_deleter.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
