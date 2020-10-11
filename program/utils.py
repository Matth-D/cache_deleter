"""Utils module for Cache Deleter"""

import os
import re
import pathlib
import glob
import shutil


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
        if (1024 ** i) <= byte_size < (1024 ** (i + 1)):
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
    file_size = os.path.getsize(path)
    if os.path.isdir(path):
        file_size = get_dir_size(path)
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
    basename = os.path.basename(path)
    match = re.findall(r"[.]\d*[.]", basename)
    if match:
        match = match[-1]
    return match


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


def get_suffix(path):
    """Return the input path file extension.

    Args:
        path (str): path to file.

    Returns:
        str: file suffix
    """
    suffixes = pathlib.Path(path).suffixes
    if is_sequence(path):
        suffixes = suffixes[1:]
    suffix = "".join(suffixes)
    return suffix


def delete_file(input_path):
    """Delete the provided path, or sequence of paths.

    Args:
        input_path (str): path to the file.
    """
    if os.path.isdir(input_path):
        shutil.rmtree(input_path)
        return
    if re.findall(r"\s[|]\s", os.path.basename(input_path)):
        hasht = re.findall(r"[.]#*[.]", input_path)[0]
        hasht = re.sub(r"#", "*", hasht)
        path = input_path.split("|")[0].strip()
        path = re.sub(r"[.]#*[.]", hasht, path)
        glob_file = glob.glob(path)
        [os.remove(path) for path in glob_file]
    else:
        os.remove(input_path)


# TODO Finish move function
def move_file(current_path, destination_dir):
    """Move input file to destination directory

    Args:
        current_path (str): Path to the input file.
        destination_dir (str): Path the the destination directory.
    """
    basename = os.path.basename(current_path)

    if re.findall(r"\s[|]\s", os.path.basename(input_path)):
        path = input_path.split("|")[0].strip()
        path = re.sub(r"[.]#*[.]", hasht, path)
        glob_file = glob.glob(path)
