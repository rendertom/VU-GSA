class Tempo:
  def __init__(self, tempo):
    self.tempo = tempo

  def get_bpm(self, tempo):
    tempo_to_bpm = {
      "adagio": (66, 76),
      "allegro": (120, 168),
      "andante": (76, 108),
      "andantino": (80, 108),
      "grave": (25, 45),
      "largo": (40, 60),
      "moderato": (108, 120),
      "presto": (168, 200),
      "vivace": (168, 176),
    }

    return tempo_to_bpm.get(tempo.lower())
  
  def get_note_duration(self, note_duration, measures = 4):
    bpm_range = self.get_bpm(self.tempo)
    bpm_average = (bpm_range[0] + bpm_range[1]) / 2

    return 60 * measures * note_duration / bpm_average
      