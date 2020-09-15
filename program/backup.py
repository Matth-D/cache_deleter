#old way of adding to the tree, now function based
dir_name = os.path.basename(path)
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

dir_item = QtWidgets.QTreeWidgetItem(current_item)
dir_item.setText(0, dir_name)
dir_item.setText(1, file_size)
progress = self.setItemWidget(dir_item, 2, RootPercentageBar(root_prct))
dir_item.setText(3, m_date_display)
if m_date < limit_date:
   dir_item.setText(3, "after")
else:
   dir_item.setText(3, "before")