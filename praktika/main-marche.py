from lib.Audio import Audio
from lib.Bitmap import Bitmap
from lib.Piano import Piano
from lib.Tempo import Tempo

image_path = "images/marche.tif"
image = Bitmap(path=image_path)
print(image.toString())

piano = Piano(note_start='A2', note_end='C6')
audio = Audio(image, piano,
          pixel_duration = Tempo("allegretto").get_note_duration(1/16),
          num_channels = 2,
          low_note_is_pause = True
        )

audio.process()
print(audio.toString())

audio.save()
audio.play()
audio.plot()