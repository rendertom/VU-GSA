import numpy as np
import os
from PIL import Image

from lib.Utils import Utils

class Bitmap:
  def __init__(self, path):
    self.image = Image.open(path)
    self.name = os.path.basename(path)
    self.path = path

  def get_normalized(self):
    self.image.path
    return Utils.normalize(self.get_pixels())
  
  def get_pixels(self):
    return np.array(self.image.convert("L")).flatten()

  def toString(self):
    return (
      f"Image size: {self.image.width}x{self.image.height}\n"
      f"Num pixels: {self.image.width * self.image.height}\n"
    )
