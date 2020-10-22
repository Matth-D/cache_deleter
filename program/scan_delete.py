"""Script that will scan the deleting folder once every day and delete files older than time threshold"""

import os
import datetime
import shutil
import json


parent = os.path.dirname(__file__)
project_root = os.path.dirname(parent)

config_folder = os.path.join(project_root, "config")
settings = os.path.join(config_folder, "settings.json")

DELETING_FOLDER = os.path.join(project_root, "deleting_folder")
if os.path.exists(settings):
    with open(settings, "r") as f:
        settings_dict = json.load(f)
        DELETING_FOLDER = settings_dict["DELETE_FOLDER"]
        DAY_DELTA = settings_dict["DAY_DELTA"]

# Replace DELETING FOLDER CONSTANT BY LOCATION OF DELETING FOLDER


def recycle_delete(deleting_folder_path):
    """Delete folder older than DAY_DELTA days.

    Args:
        deleting_folder_path (str): path to the deleting folder.
    """

    today = datetime.date.today()

    for item in os.scandir(deleting_folder_path):
        if item.is_file():
            return
        if item.is_dir():
            m_time = os.path.getmtime(item.path)
            m_date = datetime.datetime.fromtimestamp(m_time).date()
            time_delta = datetime.timedelta(DAY_DELTA)
            limit_date = today - time_delta
            if m_date < limit_date:
                shutil.rmtree(item.path)


# recycle_delete(DELETING_FOLDER)