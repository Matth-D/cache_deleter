"""Test file to create folder hierarchy to test out Cache deleter with single files and sequences of various file types"""


import os
import datetime
import time


def create_test_folder_delete():

    path_root = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "deleting_folder"
    )
    root_folder = path_root

    today = datetime.date.today()
    today_format = today.strftime("%d-%m-%Y")

    if not os.path.exists(root_folder):
        os.mkdir(root_folder)

    folder1 = os.path.join(root_folder, "folder1")
    folder2 = os.path.join(root_folder, "folder2")
    folder3 = os.path.join(root_folder, "folder3")
    folder4 = os.path.join(root_folder, "folder4")
    folder5 = os.path.join(root_folder, "folder5")

    for i in range(150):
        t_delta = datetime.timedelta(7)
        date_dt = today - t_delta
        date_dt_format = date_dt.strftime("%d-%m-%Y")
        folder1 = os.path.join(root_folder, date_dt_format)

        if not os.path.exists(folder1):
            os.mkdir(folder1)
        f1_name = "bgeo_sequence.{}.bgeo.sc".format(i)
        f1_path = os.path.join(folder1, f1_name)
        f1 = open(f1_path, "w")

        mod_time = time.mktime(date_dt.timetuple())
        os.utime(f1_path, (mod_time, mod_time))
    os.utime(folder1, (mod_time, mod_time))

    for i in range(250):
        t_delta = datetime.timedelta(14)
        date_dt = today - t_delta
        date_dt_format = date_dt.strftime("%d-%m-%Y")
        folder2 = os.path.join(root_folder, date_dt_format)

        if not os.path.exists(folder2):
            os.mkdir(folder2)
        f2_name = "bgeo_sequence.{}.bgeo.sc".format(i)
        f2_path = os.path.join(folder2, f2_name)
        f2 = open(f2_path, "w")

        mod_time = time.mktime(date_dt.timetuple())
        os.utime(f2_path, (mod_time, mod_time))
    os.utime(folder2, (mod_time, mod_time))

    for i in range(250):
        t_delta = datetime.timedelta(37)
        date_dt = today - t_delta
        date_dt_format = date_dt.strftime("%d-%m-%Y")
        folder3 = os.path.join(root_folder, date_dt_format)

        if not os.path.exists(folder3):
            os.mkdir(folder3)
        f3_name = "bgeo_sequence.{}.bgeo.sc".format(i)
        f3_path = os.path.join(folder3, f3_name)
        f3 = open(f3_path, "w")

        mod_time = time.mktime(date_dt.timetuple())
        os.utime(f3_path, (mod_time, mod_time))
    os.utime(folder3, (mod_time, mod_time))

    for i in range(250):
        t_delta = datetime.timedelta(55)
        date_dt = today - t_delta
        date_dt_format = date_dt.strftime("%d-%m-%Y")
        folder4 = os.path.join(root_folder, date_dt_format)

        if not os.path.exists(folder4):
            os.mkdir(folder4)
        f4_name = "bgeo_sequence.{}.bgeo.sc".format(i)
        f4_path = os.path.join(folder4, f4_name)
        f4 = open(f4_path, "w")

        mod_time = time.mktime(date_dt.timetuple())
        os.utime(f4_path, (mod_time, mod_time))
    os.utime(folder4, (mod_time, mod_time))

    for i in range(250):
        t_delta = datetime.timedelta(2)
        date_dt = today - t_delta
        date_dt_format = date_dt.strftime("%d-%m-%Y")
        folder5 = os.path.join(root_folder, date_dt_format)

        if not os.path.exists(folder5):
            os.mkdir(folder5)
        f5_name = "bgeo_sequence.{}.bgeo.sc".format(i)
        f5_path = os.path.join(folder5, f5_name)
        f5 = open(f5_path, "w")

        mod_time = time.mktime(date_dt.timetuple())
        os.utime(f5_path, (mod_time, mod_time))
    os.utime(folder5, (mod_time, mod_time))


create_test_folder_delete()