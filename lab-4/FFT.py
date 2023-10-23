import matplotlib.pyplot as plt
import numpy as np

class FFT:
    def __init__(self, sampleRate, samples, title):
        self.sampleRate = sampleRate
        self.samples = samples
        self.title = title
        self.fft = self._process()

    def plot(self):
      time_axis = np.linspace(0, self.sampleRate / 2, len(self.fft))

      plt.figure(figsize=(10, 4))
      plt.plot(time_axis, self.fft)
      plt.grid()
      plt.title(self.title)
      plt.xlabel('Frequency')
      plt.show()

    def _process(self):
        count = len(self.samples)
        samples = self.samples * np.hanning(count)

        fft = np.fft.fft(samples)
        fft = np.abs(fft)

        return fft[0:round(count / 2)]