from FFT import FFT
from WAV import WAV

import Utils

if __name__ == "__main__":
    wav = WAV(Utils.selectFile())

    # Draw waveform so the user can select time
    wav.plotSelf()

    start_time = Utils.promptForCTI(wav.getDuration())
    end_time = start_time + Utils.promptForDuration()

    # Draw waveform with highlighted user range
    wav.plotSelf(segments=[(start_time, end_time)])

    fft = FFT(
        wav.sampleRate,
        wav.normalize(wav.getSamplesInTimeRange(start_time, end_time)),
        wav.name + ', time: {0} - {1}'.format(start_time, end_time)
    )

    # Draw samples that were fed into FFT
    wav.plot(fft.samples, start_time, end_time)

    # Draw final FFT data
    fft.plot()
