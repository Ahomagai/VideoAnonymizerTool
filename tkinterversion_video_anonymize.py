import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import os
from ttkthemes import ThemedTk
import threading

# deface installed via: pip install deface

root = ThemedTk()
root.title("Video Anonymizer Tool")
root.tk.call('tk', 'scaling', 1.5)
root.geometry('900x500')

# Create an instance of ttk Style
style = ttk.Style(root)
style.theme_use('breeze')

# Adding a label
label = ttk.Label(root, text="Select your video file and output directory to anonymize your video:")
label.pack()

## Multiple file selection 
def vidselectors():
    global filenames
    filenames = filedialog.askopenfilenames()
    
    ttk.Label(root, text="Your files are:").pack()
    
    # Display each filename on a separate line
    for file in filenames:
        ttk.Label(root, text=file).pack()

## Button for multiple file selection 
FileSelectors = ttk.Button(root, text="Select your video files", command=vidselectors)
FileSelectors.pack()

def outputdir():
    global outputpath
    outputpath = filedialog.askdirectory()
    ttk.Label(root, text="Your output path is:").pack()
    outputlabel = ttk.Label(root, text=outputpath)
    outputlabel.pack()
    return outputpath

OutputButton = ttk.Button(root, text="Select your output directory", command=outputdir)
OutputButton.pack()

# Create a slider for the threshold
threshold_label = ttk.Label(root, text="Adjust threshold:")
threshold_label.pack()

threshold = tk.DoubleVar()  # Variable to store the threshold value
threshold_slider = ttk.Scale(root, from_=0.0, to=0.99, orient="horizontal", variable=threshold)
threshold_slider.set(0.2)  # Set a default value for the threshold
threshold_slider.pack()

# Label to display the current value of the slider
threshold_value_label = ttk.Label(root, text=f"Current threshold: {threshold.get():.2f}")
threshold_value_label.pack()

threshold_warning = tk.Label(root, text="Lower threshold values results in 'stronger' face detection, may result in more false positives (i.e. blurred hands)." + 
                             "\n Default value for threshold is 0.2." + 
                             "\n Adjust this value as necessary")
threshold_warning.pack()

# Function to update the threshold value label when slider is moved :: maybe pivot to input field instead of slider
def update_threshold_label(event):

    threshold_value_label.config(text=f"Current threshold:: {threshold.get():.2f}")

# Bind the slider to update the label when the value changes
threshold_slider.bind("<Motion>", update_threshold_label)

# Button to run deface on all files
RunMultipleDeface = ttk.Button(root, text='Run deface on all files', command=lambda: threading.Thread(target=run_multiple_deface).start())
RunMultipleDeface.pack()

# Create a label to show which file is being processed
current_file_label = ttk.Label(root, text="")
current_file_label.pack(pady=10, side="bottom")

# Create a progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20, side="bottom")

def run_multiple_deface():
    total_files = len(filenames)
    progress["maximum"] = total_files  # Set the max value of the progress bar

    for i, file in enumerate(filenames):
        current_file_label.config(text=f"Processing: {os.path.basename(file)}")
        root.update_idletasks()  # Update the label immediately

        outputfilename = os.path.join(outputpath, os.path.basename(file).replace('.mp4', '_blurred.mp4'))
        current_threshold = threshold.get()  # Get the current value of the threshold from the slider; maybe not the best tool here but it'll work
        command = ["deface", file, "-t", str(current_threshold), "-o", outputfilename]

        # Run the command in the background and wait for it to finish
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            ttk.Label(root, text=f"Successfully processed: {file}").pack()
        else:
            ttk.Label(root, text=f"Error processing: {file}").pack()
            ttk.Label(root, text=stderr.decode("utf-8")).pack()

        # Update the progress bar
        progress['value'] = i + 1
        root.update_idletasks()

    current_file_label.config(text="All files processed!")

# Start the application
root.mainloop()