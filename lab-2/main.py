from WAV import WAV
import Utils

if __name__ == "__main__":
    # wav = WAV(Utils.selectFile())
    wav = WAV("sounds/applause.wav")
    # wav = WAV("sounds/Opera-vocal_129bpm_F_minor.wav")

    print(wav.toString())
    wav.plotSelf()

    wav.setFrameDuration(25)

    # signalo energija
    wav.plot(wav.getEnergy(), "Energy (25ms)", wav.name)

    # NKS diagrama
    wav.plot(wav.getZCR(), "NKS (25ms)", wav.name)

    energyThrechold = 0.021 # 0.05
    wav.plotSelf(
        segments=wav.getSegments(wav.getEnergy(), energyThrechold)
    )
