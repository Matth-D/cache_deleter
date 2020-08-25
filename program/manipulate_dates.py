#!/usr/bin/python3.8


import time
import datetime
import os

# Get today's date

today = datetime.date.today()

# We get a modified date from file

# path = "/home/matthieu/Documents/bb.txt"
# m_time = os.path.getmtime(path)
# date_file = datetime.datetime.fromtimestamp(m_time).date()
# date_file_display = date_file.strftime("%d/%m/%Y")
#
## We also get a time delta
#
# time_delta = 14
#
## We need to compare dates to today minus delta
#
## 1st step substract today and delta
#
# time_delta_format = datetime.timedelta(time_delta)
#
# limit_date = today - time_delta_format
#
#
# file = "/home/matthieu/GIT/cache_deleter/program/TEST_FILE_DATE.txt"
#
# t_delta = datetime.timedelta(8)
# date_dt = today - t_delta
# mod_time = time.mktime(date_dt.timetuple())
# os.utime(file, (mod_time, mod_time))
#

file1 = "/home/matthieu/GIT/cache_deleter/program/ui.py"
folder1 = "/home/matthieu/GIT"


m_time_1 = os.path.getmtime(file1)
date_file = datetime.datetime.fromtimestamp(m_time_1).date()
m_time_2 = os.path.getmtime(folder1)
date_folder = datetime.datetime.fromtimestamp(m_time_2).date()


print(date_file, date_folder)
