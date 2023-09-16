from WAV import WAV
import Utils


if __name__ == "__main__":
    wav = WAV(Utils.selectFile())
    print(wav.toString())

    cti = Utils.promptForCTI(wav.getDuration())
    wav.plot(cti)
