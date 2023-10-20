from WAV import WAV

if __name__ == "__main__":
    wav = WAV("../sounds/Angry_german.wav")
    print(wav.toString())
    wav.play()
    wav.plotSelf()
    wav.toStereo(50)

    wav2 = WAV(wav.save())
    print(wav2.toString())
    wav2.play()
    wav2.plotSelf()