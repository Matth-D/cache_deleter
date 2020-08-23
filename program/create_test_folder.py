#!usr/bin/python3.8

# folder1
#    file1 bgeo sequence before 14 days
# folder 2
#    file2 vdb sequence after 14 days
# folder 3
# folder 4
#   file 3 not bgeo abc or vdb


import os
import datetime


path_root = "/home/matthieu/GIT/cache_deleter/program/"

name_folder = "test_folder"
root_folder = os.path.join(path_root, name_folder)

folder1 = os.path.join(root_folder, "folder1")
folder2 = os.path.join(root_folder, "folder2")
folder3 = os.path.join(root_folder, "folder3")

os.mkdir(root_folder)
os.mkdir(folder1)
os.mkdir(folder2)
os.mkdir(folder3)

for i in range(150):
    f1_name = "bgeo_sequence.{}.bgeo.sc".format(i)
    f1_path = os.path.join(folder1, f1_name)
    f1 = open(f1_path, "w")

for i in range(200):
    f2_name = "vdb_sequence.{}.vdb".format(i)
    f2_path = os.path.join(folder2, f2_name)
    f2 = open(f2_path, "w")

for i in range(75):
    f3_name = "other_sequence.{}.txt".format(i)
    f3_path = os.path.join(folder3, f3_name)
    f3 = open(f3_path, "w")
