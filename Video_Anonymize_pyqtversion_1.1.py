import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QSlider, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# packages used: deface, PyQt6 (and various core functions)

class DefaceRun(QThread):
    progress_signal = pyqtSignal(int, str)
    completion_signal = pyqtSignal()

    def __init__(self, filenames, outputpath, threshold, mask_scale):
        super().__init__()
        self.filenames = filenames
        self.outputpath = outputpath 
        self.threshold = threshold
        self.mask_scale = mask_scale

    
    def run(self):
        total_files = len(self.filenames)
        for i, file in enumerate(self.filenames):
            filename = os.path.basename(file)
            outputfilename = os.path.join(self.outputpath, filename.replace('_unblur','blur'))

            fps_value = 30

            status = filename

            self.progress_signal.emit(int(((i + 1) / total_files) * 100), status)
            # following commands need to be verbatim onto console for both restricting framerate and
            # running deface 

            ffmpeg_config = f'"{{\\"fps\\": {fps_value}}}"'
            command = f"deface {file} -t {self.threshold} --ffmpeg-config {ffmpeg_config} --mask-scale {self.mask_scale} -o {outputfilename}"
            
            process = os.system(command) # send to console 
            
            if process != 0:
                status = f"Error processing: {file}"
            
            
        
        self.completion_signal.emit()

class VideoAnonymizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    
    def initUI(self):
        self.setWindowTitle("Video Anonymizing Tool")
        self.setGeometry(100,100,600,400)

        layout = QVBoxLayout()

        self.label = QLabel("Select your Video Files and Output Directory") # instruction 
        layout.addWidget(self.label)

        self.filelabel = QLabel("") # empty label to be filled with file selection 
        layout.addWidget(self.filelabel)

        self.outputlabel = QLabel("")
        layout.addWidget(self.outputlabel)

        self.select_files_button = QPushButton("Select your files")
        self.select_files_button.clicked.connect(self.select_files) # needs to be a func for this 
        # self.select_files_button.clicked.connect(self.print_filenames)
        layout.addWidget(self.select_files_button)

        self.select_output_path = QPushButton("Select your output directory")
        self.select_output_path.clicked.connect(self.select_output_dir)
        layout.addWidget(self.select_output_path)

        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setMinimum(1) # set thresholds for detection strength
        self.threshold_slider.setMaximum(99)
        self.threshold_slider.setValue(20)
        self.threshold_slider.valueChanged.connect(self.update_threshold_label) #func name 
        layout.addWidget(QLabel("Adjust Detection Threshold: "))
        layout.addWidget(self.threshold_slider)

        self.threshold_label = QLabel("Current threshold: 0.20")
        layout.addWidget(self.threshold_label)

        self.mask_slider = QSlider(Qt.Orientation.Horizontal)
        self.mask_slider.setMinimum(0)
        self.mask_slider.setMaximum(200)
        self.mask_slider.setValue(130)
        self.mask_slider.valueChanged.connect(self.update_mask_label) # func name 
        layout.addWidget(QLabel("Adjust Mask Scale:"))
        layout.addWidget(self.mask_slider)
        
        self.mask_label = QLabel("Current Mask Scale: 1.30")
        layout.addWidget(self.mask_label)

        self.run_btn = QPushButton("Run Deface on All Files")
        self.run_btn.clicked.connect(self.run_deface)
        layout.addWidget(self.run_btn)
        
        self.progress_label = QLabel("Processing:")
        layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.filenames = []
        self.outputpath = ""


    def select_files(self):
        self.filenames, _ = QFileDialog.getOpenFileNames(self, "Select Video Files")
        self.filelabel.setText("Selected Files: \n" + "\n".join(self.filenames))
        # if self.filenames:
        #     self.filelabel.setText("Selected Files:\n" + "\n".join(self.filenames))
    
    def select_output_dir(self):
        self.outpath = QFileDialog.getExistingDirectory(self,"Select Output Directory")
        self.outputlabel.setText("Your output path is: "+ self.outpath)
        
    def update_threshold_label(self):
        self.threshold_label.setText(f"Current Threshold: {self.threshold_slider.value() / 100:.2f}")
    
    def update_mask_label(self):
        self.mask_label.setText(f"Current Mask Scale: {self.mask_slider.value() / 100:.2f}")

    def run_deface(self):
        # if not self.filenames or not self.outputpath:
        #     self.progress_label.setText("Please select files and output directory first.")
        #     return
        
        # self.progress_label.setText(f"Processing first file...")
        

        self.worker = DefaceRun(
            self.filenames, self.outputpath,
            self.threshold_slider.value() / 100,
            self.mask_slider.value() / 100
        )

        self.worker.progress_signal.connect(self.update_progress)
        self.worker.completion_signal.connect(self.processing_complete)
        self.worker.start()
        
    def update_progress(self, progress, status):
        self.progress_label.setText(f"Currently processing: {status}")
        self.progress_bar.setValue(progress-1)
    
    def processing_complete(self):
        self.progress_label.setText("All files processed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoAnonymizer()
    window.show()
    sys.exit(app.exec())