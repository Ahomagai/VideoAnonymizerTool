## New UI Version of VidAnon Tool
Instead of using the .exe, you can instead install the PyQt6 package in Python using ```pip install PyQt6``` from your terminal
Then you only have to run the **Video_Anonymize_pyqtversion_1.1** file from the .zip to get started with the program.


Required packages: **Deface** (https://pypi.org/project/deface/), **PyQt6** (https://pypi.org/project/PyQt6/)


Currently working on an exe and deployment version of this similar to the TKinter version but for now running the .py file should work




## Older method (still works):
This is a simple UI wrapper that uses the deface package in python to anonymize videos automatically. 

Required packages: https://pypi.org/project/deface/

Install:  ```-m pip install deface```

Required package: ttkbootstrap

Install: ```-m pip install ttkbootstrap```

Packages used:
deface, tkinter, subprocess, threading, ttkbootstrap (for theme and UI elements)

Installation video for python, deface, and ttkbootstrap:
https://youtu.be/iLCpJ5LhSTU




## Important to know:
deface runs from the command line, meaning running it as a function at the script level does not work. We need to run it through the terminal or shell level.
This UI tool helps give the input and output arguments for the deface function which is passed into the command line.



## USAGE: 

Download the file as a .zip and extract to any directory. Run the tkinterversion_video_anonymize.exe file to use the program. Again, this requires the ttkbootstrap and deface packages to be installed prior.

## Alternate usage: 
Download the file as a .zip and extract to any directory. Run the **Video_Anonymize_pyqtversion_1.1** file. This requires the deface package and the PyQt6 package.
