# folder1
#    file1 bgeo sequence before 14 days
#       folder4 deeper hierarchy to check path reconstruction
#           test_file not important
# folder 2
#    file2 vdb sequence after 14 days
# folder 3
#   file 3 not bgeo abc or vdb


import os
import datetime
import time

today = datetime.date.today()

path_root = "/Users/matthieu/GIT/cache_deleter/program/"

name_folder = "test_folder"
root_folder = os.path.join(path_root, name_folder)

folder1 = os.path.join(root_folder, "folder1")
folder2 = os.path.join(root_folder, "folder2")
folder3 = os.path.join(root_folder, "folder3")
folder4 = os.path.join(folder1, "folder4")
folder_deep = os.path.join(folder4, "folder_deep")

os.mkdir(root_folder)
os.mkdir(folder1)
os.mkdir(folder2)
os.mkdir(folder3)
os.mkdir(folder4)
os.mkdir(folder_deep)

for i in range(150):
    f1_name = "bgeo_sequence.{}.bgeo.sc".format(i)
    f1_path = os.path.join(folder1, f1_name)
    f1 = open(f1_path, "w")
    t_delta = datetime.timedelta(7)
    date_dt = today - t_delta
    mod_time = time.mktime(date_dt.timetuple())
    os.utime(f1_path, (mod_time, mod_time))
os.utime(folder1, (mod_time, mod_time))

for i in range(150):
    f1_name = "bgeo_sequence_number2.{}.bgeo.sc".format(i)
    f1_path = os.path.join(folder1, f1_name)
    f1 = open(f1_path, "w")
    t_delta = datetime.timedelta(21)
    date_dt = today - t_delta
    mod_time = time.mktime(date_dt.timetuple())
    os.utime(f1_path, (mod_time, mod_time))
os.utime(folder1, (mod_time, mod_time))

for i in range(200):
    f2_name = "vdb_sequence.{}.vdb".format(i)
    f2_path = os.path.join(folder2, f2_name)
    f2 = open(f2_path, "w")
    t_delta = datetime.timedelta(16)
    date_dt = today - t_delta
    mod_time = time.mktime(date_dt.timetuple())
    os.utime(f2_path, (mod_time, mod_time))
os.utime(folder2, (mod_time, mod_time))

for i in range(75):
    f3_name = "other_sequence.{}.txt".format(i)
    f3_path = os.path.join(folder3, f3_name)
    f3 = open(f3_path, "w")
    t_delta = datetime.timedelta(16)
    date_dt = today - t_delta
    mod_time = time.mktime(date_dt.timetuple())
    os.utime(f2_path, (mod_time, mod_time))
os.utime(folder3, (mod_time, mod_time))

for i in range(50):
    f4_name = "test_deep_file.{}.jpg".format(i)
    f4_path = os.path.join(folder4, f4_name)
    f4 = open(f4_path, "w")
f4_name_single = "test_singlefile.1.jpg"
f4_path_single = os.path.join(folder4, f4_name_single)
f4_single = open(f4_path_single, "w")
