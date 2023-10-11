import librosa
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf

from lib.Bitmap import Bitmap
from lib.Piano import Piano
from lib.Utils import Utils

class Audio:
  def __init__(self, image: Bitmap, piano: Piano, sample_rate = 44100, pixel_duration = 0.25, num_channels = 1):
    self.image = image
    self.num_channels = num_channels
    self.piano = piano
    self.pixel_duration = pixel_duration
    self.sample_rate = sample_rate

  def apply_envelop(self, sample, fade_in_percentage, fade_out_percentage):
    if fade_in_percentage > 0:
      fade_in_length = int(len(sample) * fade_in_percentage)
      for i in range(fade_in_length):
          sample[i] *= np.sin((i / fade_in_length) * (np.pi / 2))

    if fade_out_percentage > 0:
      fade_out_length = int(len(sample) * fade_out_percentage)
      for i in range(fade_out_length):
        sample[len(sample) - i - 1] *= np.sin((i / fade_out_length) * (np.pi / 2))

    return sample
  
  def process(self, num_pixels = 0):
    self.frequencies, self.samples = self.__init(num_pixels)

  def get_duration(self):
    return len(self.samples) / self.sample_rate

  def get_frequencies(self):
    return self.frequencies
  
  def get_notes(self):
    return [librosa.hz_to_note(frequency) for frequency in self.frequencies]
  
  def play(self):
    sd.play(self.samples, self.sample_rate)
    sd.wait()

  def plot(self):
    time_axis = np.linspace(0, self.get_duration(), len(self.samples))

    for channel_index in range(self.num_channels):
      plt.subplot(self.num_channels, 1, channel_index + 1)

      samples = self.samples
      if not isinstance(samples[0], float):
        samples = self.samples[:, channel_index]

      plt.grid(True)
      plt.plot(time_axis, samples)
      plt.title(f'{self.image.name} (channel {channel_index + 1})')
      plt.xlabel('Time (s)')
      plt.ylabel('Amplitude')

    plt.tight_layout()
    plt.show()

  def save(self):
    file_name = self.image.name + ".wav"
    sf.write(file_name, self.samples, self.sample_rate)
    
  def to_stereo(self, samples):
    if len(samples) % 2 == 1:
      samples = np.append(samples, samples[-1])

    half_length = len(samples) // 2
    left = samples[:half_length]
    right = samples[half_length:]

    return np.column_stack((left, right))

  def toString(self):
    return (
      f"Num samples: {len(self.samples)}\n"
      f"Sample rate: {self.sample_rate}\n"
      f"Duration: {self.get_duration()} s\n"
      f"Notes: {self.get_notes()[0:10]} ...\n"
      f"Frequencies: {self.get_frequencies()[0:10]} ...\n"
    )
    
  def __init(self, num_pixels):
    pixels = Utils.normalize(self.image.get_pixels())

    if not num_pixels:
      num_pixels = len(pixels)

    frequencies = []
    samples = []
    index_offset = 0

    for index in range(num_pixels):
      pixel = pixels[index - index_offset]
      next_pixel = pixels[index + 1] if index < num_pixels - 1 else None
      
      if pixel == next_pixel:
        index_offset += 1
      else:
        amplitude = Utils.linear_map(pixel, 0, 1, 0.1, 1)
        frequency = self.piano.value_to_frequency(pixel)
        frequencies.append(frequency)

        duration = self.pixel_duration * (index_offset + 1)
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)

        sample = amplitude * np.sin(2 * np.pi * frequency * t)
        sample = self.apply_envelop(sample, 0.01, 0.01)
        samples.extend(sample)
        
        index_offset = 0

    if self.num_channels == 2:
      samples = self.to_stereo(samples)

    return frequencies, samples
