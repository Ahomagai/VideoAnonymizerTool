import tkinter as tk
from tkinter import ttk, filedialog, Canvas
import os
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import *
import json

## TODO: Implement a mean 'score' for id faces, makes it easier to know which video files to analyze again for 
# accuracy & precision of deface protocol

## TODO: Give a test folder option instead, deface can handle full folders and nested folder paths

# Root window 
root = ttk.Window(themename="flatly")
root.title("Video Anonymizer Tool")
root.geometry("1300x900")

# Create the canvas
canvas = Canvas(root)
canvas.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)

# Scrollbar for canvas 
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
content_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Configure frame to be modular with canvas size
content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Add widgets to the content frame instead of root
label = ttk.Label(content_frame, text="Select your video file and output directory to anonymize your video:", style="")
label.pack()

## Multiple file selection
def vidselectors():
    global filenames
    filenames = filedialog.askopenfilenames()
    ttk.Label(content_frame, text="Your video files are: \n ", style='').pack()

    # Display each filename on a separate line
    for file in filenames:
        ttk.Label(content_frame, text=file).pack()

# Button for multiple file selection
FileSelectors = ttk.Button(content_frame, text="Select your video files", style='', command=vidselectors)
FileSelectors.pack()

def outputdir():
    global outputpath
    outputpath = filedialog.askdirectory()
    ttk.Label(content_frame, text="\n Your output path is: \n ", style="").pack()
    outputlabel = ttk.Label(content_frame, text=outputpath)
    outputlabel.pack()
    return outputpath

ttk.Label(content_frame, text="").pack(pady=1)

OutputButton = ttk.Button(content_frame, text="Select your output directory", style='', command=outputdir)
OutputButton.pack()

ttk.Label(content_frame, text="").pack(pady=1) # just for space 


######## Label for the threshold slider and slider itself #####################
# Create a slider for the threshold
threshold_label = ttk.Label(content_frame, text="Adjust detection threshold:")
threshold_label.pack()

threshold = tk.DoubleVar()  # Variable to store the threshold value
threshold_slider = ttk.Scale(content_frame, from_=0.01, to=0.99, length=500,orient="horizontal", variable=threshold)
threshold_slider.set(0.2)  # Set a default value for the threshold
threshold_slider.pack()

# Label to display the current value of the slider
threshold_value_label = ttk.Label(content_frame, text=f"Current threshold: {threshold.get():.2f}")
threshold_value_label.pack()

threshold_warning = tk.Label(content_frame, text="Lower threshold values result in stronger face detection \n may result in more false positives (i.e., blurred hands).\n Default value for threshold is 0.2, adjust as necessary")
threshold_warning.pack()


# Update threshold label when slider is moved
def update_threshold_label(event):
    threshold_value_label.config(text=f"Current threshold: {threshold.get():.2f}")

threshold_slider.bind("<Motion>", update_threshold_label)

ttk.Label(content_frame, text="").pack(pady=10)


################## Mask scale slider #############################
### Mask scale slider, defaults to 1.3 
mask_slider_label = ttk.Label(content_frame, text="Adjust mask scale:")
mask_slider_label.pack()

mask_scale = tk.DoubleVar()  # Variable to store the mask scale value
mask_slider = ttk.Scale(content_frame, from_=0.0, to=2.0, length=500, orient="horizontal", variable=mask_scale)
mask_slider.set(1.3)  # Set a default value for the mask scale
mask_slider.pack()

# Label to display the current value of the mask scale slider
mask_scale_value_label = ttk.Label(content_frame, text=f"Current mask scale: {mask_scale.get():.2f}")
mask_scale_value_label.pack()

mask_scale_warning = tk.Label(content_frame, text="\n Mask scale adjusts how much of the face is covered by the blur masking. \n Default value for mask scale is 1.3, larger value = more of the face blurred.")
mask_scale_warning.pack()

# Update mask scale value label when slider is moved
def update_mask_scale_label(event):
    mask_scale_value_label.config(text=f"Current mask scale: {mask_scale.get():.2f}")

mask_slider.bind("<Motion>", update_mask_scale_label)


ttk.Label(content_frame, text="").pack(pady=10)

### 
# Button to run deface on all files
RunMultipleDeface = ttk.Button(content_frame, text='Run deface on all files', style='success.TButton' , command=lambda: threading.Thread(target=run_multiple_deface).start())
RunMultipleDeface.pack()

# Label for the current file being processed
current_file_label = ttk.Label(content_frame, text="", style="success.TLabel")
current_file_label.pack(pady=10)

# Progress bar
progress = ttk.Progressbar(content_frame, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

# Function to run deface on all files
def run_multiple_deface():
    total_files = len(filenames)
    progress["maximum"] = total_files  # Set the max value of the progress bar

    ttk.Label(content_frame, text="Output::", style="").pack(pady=10)

    for i, file in enumerate(filenames):
        current_file_label.config(text=f"Processing: {os.path.basename(file)}")
        root.update_idletasks()

        outputfilename = os.path.join(outputpath, os.path.basename(file).replace('_unblur', '_blur'))
        current_threshold = threshold.get()
        mask_scale_value = mask_scale.get()

        

        # Assuming 30 fps for all videos
        fps_value = 30
        ffmpeg_config = '"{\\"fps\\": ' + str(fps_value) + '}"' # Properly formatted JSON string for ffmpeg_config line 

        command = [
            "deface",
            file,
            "-t",
            str(current_threshold),
            "--ffmpeg-config",
            ffmpeg_config,
            "--mask-scale",
            str(mask_scale_value),
            "-o",
            outputfilename
        ]
        command = " ".join(command)

        # needed command structure as verbatim: deface --ffmpeg-config "{\"fps\": 20}" --keep-audio -o outputfilename

        #ttk.Label(content_frame, text=f"Processing: {command}", style="").pack()
        print(command) # send the command onto the console for debugging purposes instead of the UI, reduces clutter 

        process = os.system(command)

        if process == 0:
            ttk.Label(content_frame, text=f"Successfully processed: {file}", style = 'success.Inverse.TLabel').pack()
        else:
            ttk.Label(content_frame, text=f"Error processing: {file}").pack()

        progress['value'] = i + 1
        root.update_idletasks()

    current_file_label.config(text="All files processed!")

# Start the application
root.mainloop()
