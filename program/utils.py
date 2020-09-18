"""Utils module for Cache Deleter"""

import os
import glob
import re
import pathlib


def byte_size_to_display(byte_size):
    """Return size in display formate from byte.

    Args:
        byte_size (int): file size in byte

    Returns:
        str: file size in display format dd/mm/yyyy
    """

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
    """Return path size either file or directory.

    Args:
        path (str): path to directory or file.

    Returns:
        int: directory or file size in bytes.
    """

    if path == "":
        return
    file_size = get_dir_size(path)
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
    return file_size


def get_dir_size(path):
    """Return dir size in bytes by scanning content.

    Args:
        path (str): path to directory

    Returns:
        int: dir size in bytes
    """

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
    """Return if path is part of an image sequence or not.

    Args:
        path (str): path to file.

    Returns:
        bool: True or False if path is part of an image sequence.
    """
    #Simplifier cette fonction avec regex et trouver en fonction du pattern prefix . padding . autre chose
    path_split = path.split(".")
    glob_id = path_split[0] + "*"
    glob_list = glob.glob(glob_id)
    if len(glob_list) > 1:
        return True
    else:
        return False


def get_frame(path):
    """Return frame number from path.

    Args:
        path (str): path to file.

    Returns:
        int: frame number
    """
    frame = str(pathlib.Path(path).suffixes[:1])
    frame = re.sub("[^0-9]", "", frame)
    return int(frame)


# input_f = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/bgeo_sequence"
# file_glob = glob.glob(input_f + "*")
# file_sample = file_glob[0]
# suffix = pathlib.Path(file_sample).suffixes[1:]
# suffix = "".join(suffix)
# name = os.path.basename(input_f)
# min_frame = get_frame(min(file_glob, key=lambda x: get_frame(x)))
# max_frame = get_frame(max(file_glob, key=lambda x: get_frame(x)))
# padding = "#" * len(str(max_frame))
# input_f2 = "{0}.{1}{2} | ({3}-{4})".format(
#     input_f, padding, suffix, min_frame, max_frame
# )
file = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/bgeo_sequence.24.bgeo.sc"
basename = os.path.basename(file)