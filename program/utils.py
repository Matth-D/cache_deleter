"""Utils module for Cache Deleter"""

import os
import glob
import re
import pathlib


def byte_size_to_display(byte_size):
    byte_size *= 1.0
    byte_type = ["B", "KB", "MB", "GB", "TB"]
    for i, each in enumerate(byte_type):
        if byte_size >= (1024 * i) and byte_size < (1024 * (i + 1)):
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


def is_sequence(path):
    path_split = path.split(".")
    glob_id = path_split[0] + "*"
    glob_list = glob.glob(glob_id)
    if len(glob_list) > 1:
        return True
    else:
        return False


def get_frame(path):
    frame = str(pathlib.Path(path).suffixes[:1])
    frame = re.sub("[^0-9]", "", frame)
    return int(frame)


#  input file name shortened
#  perform glob to get one actual file from the sequence to extract info from
#  isolate suffix
#  get padding from highest frame number
#  get smallest frame
#  get highest frame
#  replace frame by # * padding
#  join everything
#  perform date operation based on one file from sequence
#  output = file_hierarchy/file_name.####.suffix (fstart-fend)

input_f = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/bgeo_sequence"
file_glob = glob.glob(input_f + "*")
file_sample = file_glob[0]
suffix = pathlib.Path(file_sample).suffixes[1:]
suffix = "".join(suffix)
name = os.path.basename(input_f)
min_frame = get_frame(min(file_glob, key=lambda x: get_frame(x)))
max_frame = get_frame(max(file_glob, key=lambda x: get_frame(x)))
padding = "#" * len(str(max_frame))
input_f2 = "{0}.{1}{2} | ({3}-{4})".format(
    input_f, padding, suffix, min_frame, max_frame
)
