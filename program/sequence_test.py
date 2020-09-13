import os
import glob
import pathlib
import re
import utils

# 1- create function to check if file is part of sequence
#
#  file_s = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/folder4/test_singlefile.1.jpg"
#  #  file_sq = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/folder4/test_deep_file.0.jpg"
#
#  file_s_split = file_s.split(".")
#  file_s_id = file_s_split[0]
#
#  file_sq_split = file_sq.split(".")
#  file_sq_id = file_sq_split[0]
#
#  globsq = glob.glob(file_sq_id + "*")
#  globs = glob.glob(file_s_id + "*")
#

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
file_sample = file_glob[5]
suffix = pathlib.Path(file_sample).suffixes[1:]
suffix = "".join(suffix)
name = os.path.basename(input_f)
frame = str(pathlib.Path(file_sample).suffixes[:1])
frame = re.sub("[^0-9]", "", frame)
#  max_frame = max(file_glob
