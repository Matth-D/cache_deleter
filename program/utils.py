#!/usr/bin/python3.8

"""Utils module for Cache Deleter"""

import os


def byte_size_to_display(byte_size):
    byte_size *= 1.0
    byte_type = ["B", "KB", "MB", "GB", "TB"]
    for i, each in enumerate(byte_type):
        if byte_size >= (1024 ** i) and byte_size < (1024 ** (i + 1)):
            byte_size /= 1024 ** i
            byte_size = "{:.2f}".format(byte_size)
            byte_size = byte_size + " " + each
            break
    return str(byte_size)


def get_size(path):
    if path == "":
        return
    if os.path.isdir(path) is False:
        file_size = os.path.getsize(path)
    else:
        file_size = get_dir_size(path)
    return file_size


def get_dir_size(path):
    if path == "":
        return
    byte_size_total = 0
    for item in os.scandir(path):
        item_path = os.path.join(path, item)
        if item.is_file():
            byte_size_total += os.path.getsize(item_path)
        elif item.is_dir():
            byte_size_total += get_dir_size(item_path)
        else:
            byte_size_total += 0
    return byte_size_total


# file sequence function
#
#
# input > folder files content to loop on
#
# example > filesequence.1244.bgeo.sc
#       > filesequence_other.012.jpg
#           >output : [
#               'filesequence.####.bgeo.sc (450-1321)',
#               'filesequence_other.###.jpg (0-54)'
#           ]
#
# first step > check if file is in a sequence
#
#
# output > list of files with number of element in the name
