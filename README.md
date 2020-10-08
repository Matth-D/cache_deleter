### REQUIREMENTS

Python 3+ 
PySide2 --> `pip3 install PySide2` in a terminal

### HOW TO USE 

In a terminal execute the cache_deleter.py scripts included at the package root with python.

`python3 cache_deleter.py`

Pick a root path either by typing it in the top bar or browsing through the file system clicking the Browse button.
Possibility to enter file extensions that will not be ignored in the tree view. Defaults to common Houdini extensions of scenes
and caches but works with any file type.
The time threshold parameter defaults to 14 and will display in red the files modified before the amount of days the parameter displays.

Hitting the Scan button will fill the Tree widget with the folder structure starting from the root_path parameter.
For each folder or file it displays the name, the weight, the percentage weight relative to the root path and the last modified date of the file.
Use the up or down buttons to add or remove items to the deleting list.
Items added to that list are selected to be further deleted.

Once the list is filled, you can click the Delete button that will ask you again if you want to delete the selected files.
Careful, all the files in the list and all elements of added sequences will be permanently deleted.
The two remaining button clear either the delete list or all fields in the UI.