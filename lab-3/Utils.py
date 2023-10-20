from tkinter import filedialog
import datetime
import sys

def generateMMSSms():
    time = datetime.datetime.now()
    minutes = time.minute
    seconds = time.second
    milliseconds = time.microsecond // 1000  # Convert microseconds to milliseconds
    return f"{minutes}{seconds}{milliseconds}"

def promptForCTI(maxDuration: float):
    cti = maxDuration + 1
    while float(cti) > maxDuration:
        cti = input('> Enter CTI position in seconds (max: {0}): '.format(maxDuration))
    return float(cti)

def selectFile():
    filePath = filedialog.askopenfilename(filetypes=[('Audio file', '*.wav')])
    if not filePath:
        print("No file selected. Aborting.")
        sys.exit(1)
    return filePath