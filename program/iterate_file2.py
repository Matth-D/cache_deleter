import datetime
import os
import utils
from PySide2 import QtWidgets, QtGui, QtCore


def iterate_file(current_dir, current_item):
    today = datetime.date.today()
    files = os.listdir(current_dir)
    paths = [os.path.join(current_dir, file) for file in files]
    dir_paths = [path for path in paths if os.path.isdir(path)]
    file_paths = [path for path in paths if os.path.isfile(path)]

    for path in dir_paths:
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

        dir_item = QtWidgets.QTreeWidgetItem(current_item)
        dir_item.setText(0, file)
        dir_item.setText(1, file_size)
        progress = self.setItemWidget(dir_item, 2, RootPercentageBar(root_prct))
        dir_item.setText(3, m_date_display)

        iterate_file(path, dir_item)

    for path in file_paths:
        QtWidgets
