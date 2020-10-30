### REQUIREMENTS

Python 3+ 
PySide2 --> `pip3 install PySide2` in a terminal

### PURPOSE

This is a tool developed to clean disks during or after a project that generated a lot of data to optimize space.
It was made with a use in the VFX industry in mind but could be useful for any type of case.

### INSTALL

First off you'll need to run the install.py script located at the package root.
That script will set a location for the deleting folder. That folder is where data will be sent if the Hard Delete checkbox is ticked off.
Caches will be stored in a subfolder based on the date of deletion.
It will also ask you for an amount of days. This will be used in the scan_delete.py script that will delete any folder in the deleting folder older
than the date minus the amount of days. 
After clicking the Install button those informations will be stored in a settings.json file in the config folder and used accross the tool.

### HOW TO USE 

In a terminal execute the cache_deleter.py scripts included at the package root with python.

`python3 cache_deleter.py`

Pick a root path either by typing it in the top bar or browsing through the file system clicking the Browse button.
Possibility to enter file extensions that will be displayed in the tree view. Defaults to common Houdini extensions of scenes
and caches but works with any file type.
The time threshold parameter defaults to 14 and will display in red the files last modified after the amount of days the parameter displays.

Hitting the Scan button will fill the File Tree window with the folder structure starting from the root_path parameter.
For each folder or file it displays the name, the file size, the percentage size relative to the root path and the last modified date of the file.
Use the up or down buttons to add or remove items to the deleting list.
Items added to that list are selected to be further deleted.

Once the list is filled, you can click the Delete button that will ask you again if you want to delete the selected files.
Careful, if the Hard Delete Checkbox is ticked on all the files in the list and all elements of added sequences will be permanently deleted.
If not they will be sent to the deleting folder and be further deleted with the scan_delete.py script.
Ideally the scan_delete.py script would be set as a recurring task so it would scan the deleting folder and clean old caches every day.
The two remaining button clear either the delete list or all fields in the UI.