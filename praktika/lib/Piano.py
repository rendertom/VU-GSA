import math
import numpy as np

class Piano:
  def __init__(self, note_start = 'C4', note_end = 'C5'):
    self.note_end = note_end
    self.note_names = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B']
    self.note_start = note_start
    self.notes = self.__init()

    self.frequencies = list(self.notes.values())
    self.thresholds = [i * (1 / len(self.notes)) for i in range(1, len(self.notes) + 1)]
  
  def get(self, note_name):
    return self.notes.get(note_name)

  def get_frequency_end(self):
    return self.get(self.note_end)
    
  def get_frequency_start(self):
    return self.get(self.note_start)
  
  def offset_frequency(self, base_freq, step):
    return base_freq * math.pow(2, step / len(self.note_names))

  def value_to_frequency(self, value):
    for i in range(len(self.notes) - 1):
      if self.thresholds[i] <= value <= self.thresholds[i + 1]:
        return self.frequencies[i + 1]

    return self.frequencies[0]
  
  def __init(self):
    numOctaves = 9
    keyNames = np.array([
      noteName + str(octaveIndex) for octaveIndex in range(0, numOctaves) for noteName in self.note_names
    ])

    note_index_start = np.where(keyNames == self.note_start)[0][0]
    note_index_end = np.where(keyNames == self.note_end)[0][0]
    
    base_freq = 440 #Frequency of Note A4
    base_index = np.where(keyNames == "A4")[0][0]
    base_freq_offset = base_index - note_index_start + 1

    keyNames = keyNames[note_index_start : note_index_end + 1]

    notes = {}
    for keyIndex in range(len(keyNames)):
      frequency = self.offset_frequency(base_freq, keyIndex + 1 - base_freq_offset)
      notes[keyNames[keyIndex]] = frequency

    return notes