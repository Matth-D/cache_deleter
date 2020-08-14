#!/usr/bin/python3.8

"""Utils module for Cache Deleter"""


def get_file_size(byte_size):
    byte_size *= 1.0
    byte_type = ["B", "KB", "MB", "GB", "TB"]
    for i, each in enumerate(byte_type):
        if byte_size >= 1024 ** i and byte_size < 1024 ** (i + 1):
            byte_size /= 1024 ** i
            byte_size = "{:.2f}".format(byte_size)
            byte_size = byte_size + " " + each
    return byte_size


test_size = 12485544294
print(get_file_size(test_size))
