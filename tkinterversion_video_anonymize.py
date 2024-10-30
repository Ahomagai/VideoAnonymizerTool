import tkinter as tk
from tkinter import ttk, filedialog

from ttkthemes import ThemedTk

import subprocess
import os
import threading

# Initialize root window
root = ThemedTk(theme="arc")
root.title("Video Anonymizer Tool")
root.tk.call('tk', 'scaling', 2)
root.geometry('800x1000')

# Set up the main frame and scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# Configure the scrollbar
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add widgets to the scrollable_frame instead of root
label = ttk.Label(scrollable_frame, text="Select your video file and output directory to anonymize your video:")
label.pack()

## Multiple file selection
def vidselectors():
    global filenames
    filenames = filedialog.askopenfilenames()
    ttk.Label(scrollable_frame, text="Your files are:").pack()

    # Display each filename on a separate line
    for file in filenames:
        ttk.Label(scrollable_frame, text=file).pack()

# Button for multiple file selection
FileSelectors = ttk.Button(scrollable_frame, text="Select your video files", command=vidselectors)
FileSelectors.pack()

def outputdir():
    global outputpath
    outputpath = filedialog.askdirectory()
    ttk.Label(scrollable_frame, text="\n Your output path is:").pack()
    outputlabel = ttk.Label(scrollable_frame, text=outputpath)
    outputlabel.pack()
    return outputpath

ttk.Label(scrollable_frame, text="").pack(pady=1)

OutputButton = ttk.Button(scrollable_frame, text="Select your output directory", command=outputdir)
OutputButton.pack()

ttk.Label(scrollable_frame, text="").pack(pady=1)

# Create a slider for the threshold
threshold_label = ttk.Label(scrollable_frame, text="Adjust detection threshold:")
threshold_label.pack()

threshold = tk.DoubleVar()  # Variable to store the threshold value
threshold_slider = ttk.Scale(scrollable_frame, from_=0.01, to=0.99, orient="horizontal", variable=threshold)
threshold_slider.set(0.2)  # Set a default value for the threshold
threshold_slider.pack()

# Label to display the current value of the slider
threshold_value_label = ttk.Label(scrollable_frame, text=f"Current threshold: {threshold.get():.2f}")
threshold_value_label.pack()

threshold_warning = tk.Label(scrollable_frame, text="Lower threshold values result in stronger face detection \n may result in more false positives (i.e., blurred hands).\n Default value for threshold is 0.2, adjust as necessary")
threshold_warning.pack()

# Update threshold label when slider is moved
def update_threshold_label(event):
    threshold_value_label.config(text=f"Current threshold: {threshold.get():.2f}")

threshold_slider.bind("<Motion>", update_threshold_label)

ttk.Label(scrollable_frame, text="").pack(pady=20)

# Button to run deface on all files
RunMultipleDeface = ttk.Button(scrollable_frame, text='Run deface on all files', command=lambda: threading.Thread(target=run_multiple_deface).start())
RunMultipleDeface.pack()

# Label for the current file being processed
current_file_label = ttk.Label(scrollable_frame, text="")
current_file_label.pack(pady=10)

# Progress bar
progress = ttk.Progressbar(scrollable_frame, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

# Function to run deface on all files
def run_multiple_deface():
    total_files = len(filenames)
    progress["maximum"] = total_files  # Set the max value of the progress bar

    for i, file in enumerate(filenames):
        current_file_label.config(text=f"Processing: {os.path.basename(file)}")
        root.update_idletasks()

        outputfilename = os.path.join(outputpath, os.path.basename(file).replace('.mp4', '_blurred.mp4'))
        current_threshold = threshold.get()
        command = ["deface", file, "-t", str(current_threshold), "-o", outputfilename]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            ttk.Label(scrollable_frame, text=f"\n Successfully processed: {file}").pack()
        else:
            ttk.Label(scrollable_frame, text=f"Error processing: {file}").pack()
            ttk.Label(scrollable_frame, text=stderr.decode("utf-8")).pack()

        progress['value'] = i + 1
        root.update_idletasks()

    current_file_label.config(text="All files processed!")

# Start the application
root.mainloop()
