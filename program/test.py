import os
import utils

file1 = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/bgeo_sequence_number2.2.bgeo.sc"
file2 = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/bgeo_sequence.30.bgeo.sc"
file3 = "/Users/matthieu/GIT/cache_deleter/program/test_folder/folder1/test_single_sequence38.png"

print(utils.is_sequence(file1))
print(utils.is_sequence(file2))
if utils.is_sequence(file3):
    print("prout")
