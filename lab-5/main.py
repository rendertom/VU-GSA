from FFT import FFT
from WAV import WAV

import Utils

if __name__ == "__main__":
    wav = WAV("../sounds/Sinus_125Hz.wav")

    # Draw waveform so the user can select time
    wav.plotSelf()

    start_time = Utils.promptForCTI(wav.getDuration())
    end_time = start_time + Utils.promptForDuration(200)

    # Draw waveform with highlighted user range
    wav.plotSelf(segments=[(start_time, end_time)])

    fft = FFT(
        wav.sampleRate,
        wav.normalize(wav.getSamplesInTimeRange(start_time, end_time)),
        wav.name + ', time: {0} - {1}'.format(start_time, end_time)
    )

    # Draw samples that were fed into FFT
    wav.plot(fft.samples, start_time, end_time)

    # Plot FFT before adding new frequencies
    fft.plot()

    # Add some frequencies
    fft.transform(125)

    # Plot final FFT
    fft.plot()

    # Plot restored signal
    wav.plot(wav.normalize(fft.restore()), start_time, end_time)
   
    # Save signal to file
    wav.samples = fft.restoreSamples()
    wav.save("restored_audio.wav")
