import wave
import numpy as np
from tkinter import filedialog

# file_path = filedialog.askopenfilename(filetypes=[('Audio file', '*.wav')])
file_path = "/Users/tomas/Downloads/Sounds/Angry_german.wav"
print(file_path)

file = wave.open(file_path, 'rb')
numberOfFrames = file.getnframes()
frameRate = file.getframerate()
dataByteString = file.readframes(numberOfFrames)

data = np.frombuffer(dataByteString, np.int16)
duration = numberOfFrames / frameRate

print(
  "Num chanels:", file.getnchannels(),
  "\nsample width in bytes:", file.getsampwidth(),
  "\nsampling frequency:", frameRate,
  "\nnumber of audio frames:", numberOfFrames,
  "\ncompression type:", file.getcomptype(),
  "\ncompression name:", file.getcompname(),
  "\nduration (s):", duration
  )
file.close() 
