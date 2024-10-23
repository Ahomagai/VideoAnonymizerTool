This is a simple UI wrapper that uses the deface package in python to anonymize videos automatically. 

Required packages: https://pypi.org/project/deface/

Install:  -m pip install deface

Required package: ttkbootstrap

Install: -m pip install ttkbootstrap

Packages used:
deface, tkinter, subprocess, threading, ttkbootstrap (for theme and UI elements)


Important to know:
deface runs from the command line, meaning running it as a function at the script level does not work. We need to run it through the terminal or shell level.
This UI tool helps give the input and output arguments for the deface function which is passed into the command line.


Usage:
Install required packages. Download the script and run it (double click the .py file OR run it from any python IDE) from any location. 
The UI elements contains buttons to select video file(s), select output folder, select desired threshold of face detection, and finally the 'RUN' button to start anonymization of faces.

Select your videos of interest, adjust threshold as necessary (lower threshold == stronger face detection, but may result in false positives).

Make sure to double check your videos as they output to ensure proper detection of faces. 

Once you hit the 'RUN' button, it should show the current file that it is processing, and the update bar progresses as each video is completed. 

Here is what the program looks like:
![alt text](https://github.com/Ahomagai/VideoAnonymizerTool/blob/main/UserInterface.png "Video Anonymizer Tool")
