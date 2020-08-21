#!/usr/bin/python3.8

import datetime
import os

# Get today's date

today = datetime.date.today()

# We get a modified date from file

path = "/home/matthieu/Documents/bb.txt"
m_time = os.path.getmtime(path)
date_file = datetime.datetime.fromtimestamp(m_time).date()


# We also get a time delta

time_delta = 14

# We need to compare dates to today minus delta

# 1st step substract today and delta

time_delta_format = datetime.timedelta(time_delta)

limit_date = today - time_delta_format
