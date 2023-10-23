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
        cti = input('> Enter start position in seconds (max: {0}): '.format(maxDuration))
    return float(cti)

def promptForDuration():
    default_duration = 30 / 1000
    user_input = input('> Enter duration in seconds (defaults to {0} ms): '.format(default_duration))

    try:
        duration = float(user_input)
    except ValueError:
        duration = default_duration

    return duration

def selectFile():
    filePath = filedialog.askopenfilename(filetypes=[('Audio file', '*.wav')])
    if not filePath:
        print("No file selected. Aborting.")
        sys.exit(1)
    return filePath