from tkinter import filedialog
import sys

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