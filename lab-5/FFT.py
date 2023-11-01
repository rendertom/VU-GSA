import matplotlib.pyplot as plt
import numpy as np

class FFT:
    def __init__(self, sampleRate, samples, title):
        self.sampleRate = sampleRate
        self.samples = samples
        self.title = title
        self.fft = self._process()
        self.phase_spectrum = np.angle(self.fft)        

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
        # samples = self.samples * np.hamming(count)

        fft = np.fft.rfft(self.samples)
        fft = np.abs(fft)

        return fft
        
    def addFrequency(self, frequency, amp_multiplier=1):
        index = int(frequency * len(self.fft) * 2 / self.sampleRate)
        self.fft[index] = amp_multiplier * max(self.fft)

    def restore(self):
        return np.fft.irfft(self.fft * np.exp(1j * self.phase_spectrum), n=len(self.samples))

    def restoreSamples(self):
        return np.int16(self.restore() * self.sampleRate)

    def transform(self, base_freq):
        self.addFrequency(base_freq * 2, 0.8) #
        self.addFrequency(base_freq * 3, 0.25) 
        self.addFrequency(base_freq * 4, 0.5) #
        self.addFrequency(base_freq * 5, 0.25) 
        self.addFrequency(base_freq * 6, 0.25) 
        self.addFrequency(base_freq * 7, 0.25) 
        self.addFrequency(base_freq * 8, 0.5) #
