import matplotlib.pyplot as plt
import numpy as np
import os
import wave


class WAV:
    def __init__(self, filePath):
        file = wave.open(filePath, 'rb')

        self.bitsPerSample = file.getsampwidth() * 8
        self.compressionName = file.getcompname()
        self.compressionType = file.getcomptype()
        self.filePath = filePath
        self.name = os.path.basename(filePath)
        self.numChannels = file.getnchannels()
        self.numSamples = file.getnframes()
        self.sampleRate = file.getframerate()
        self.samples = np.frombuffer(
            file.readframes(file.getnframes()),
            np.int16
        )

        file.close()

    def getAmplitudeMax(self) -> float:
        return self.samples.max()

    def getAmplitudeMin(self) -> float:
        return self.samples.min()

    def getBitrate(self) -> float:
        return self.sampleRate * self.numChannels * self.bitsPerSample

    def getChannelWidth(self) -> float:
        return 2 ** self.bitsPerSample

    def getChannelWidthMax(self) -> float:
        return self.getChannelWidth() / 2 - 1

    def getChannelWidthMin(self) -> float:
        return - self.getChannelWidth() / 2

    def getDuration(self) -> float:
        return self.numSamples / self.sampleRate

    def getFileSizeComputed(self) -> float:
        return self.numSamples * self.numChannels * self.bitsPerSample / 8

    def getSamplesForChannel(self, channelIndex):
        return self.samples[channelIndex::self.numChannels]

    def plot(self, cti: float = 0):
        timeAxis = np.linspace(0, self.getDuration(), self.numSamples)

        for channelIndex in range(self.numChannels):
            plt.subplot(self.numChannels, 1, channelIndex + 1)

            plt.grid(True)
            plt.plot(timeAxis, self.getSamplesForChannel(channelIndex))
            plt.title(f'{self.name} (channel {channelIndex + 1})')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.ylim(self.getChannelWidthMin(), self.getChannelWidthMax())

            plt.axvline(x=cti, color='r')

        plt.tight_layout()
        plt.show()

    def toString(self) -> str:
        return (
            f"bitRate: {self.getBitrate()} bits per second\n"
            f"bitsPerSample: {self.bitsPerSample} bits\n"
            f"compressionName: {self.compressionName}\n"
            f"compressionType: {self.compressionType}\n"
            f"duration: {self.getDuration()} seconds\n"
            f"filePath: {self.filePath}\n"
            f"fileSizeComputed: {self.getFileSizeComputed()} bytes\n"
            f"name: {self.name}\n"
            f"numChannels: {self.numChannels}\n"
            f"numSamples: {self.numSamples}\n"
            f"sampleRate: {self.sampleRate} Hz\n"
            f"samples: {self.samples}"
        )
