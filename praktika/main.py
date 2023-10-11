from lib.Audio import Audio
from lib.Bitmap import Bitmap
from lib.Piano import Piano
from lib.Tempo import Tempo

image_path = "images/moonlight.tif"
image = Bitmap(path=image_path)
print(image.toString())

piano = Piano(note_start='f1', note_end='E6')
audio = Audio(image, piano,
          pixel_duration = Tempo("presto").get_note_duration(1/16),
          num_channels = 2
        )

audio.process()
print(audio.toString())

audio.save()
audio.play()
audio.plot()