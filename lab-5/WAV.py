from playsound import playsound

import matplotlib.pyplot as plt
import numpy as np
import os
import wave

import Utils

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

        self.frameDuration = 25 # in milliseconds

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

    def getEnergy(self):
        return self.getFrameFeatures(self.signalToEnergy)
    
    def getFileSizeComputed(self) -> float:
        return self.numSamples * self.numChannels * self.bitsPerSample / 8
    
    def getFrameFeatures(self, feature_extractor):
        window_size, hop_size = self.parseFrameDuration()

        samples = self.normalize(self.toMono())
    
        features = []
        for i in range(0, len(samples) - window_size + 1, hop_size):
            signal = samples[i:i + window_size]
            result = feature_extractor(signal)
            features.append(result)

        return self.normalize(np.array(features))
    
    def getSamplesForChannel(self, channelIndex):
        return self.samples[channelIndex::self.numChannels]
    
    def getSamplesInTimeRange(self, start_time, end_time):
        start_index = int(self.sampleRate * start_time)
        end_index = int(self.sampleRate * end_time)
        return self.samples[start_index:end_index]
    
    def getSegments(self, data, threshold):
        window_size, hop_size = self.parseFrameDuration()

        segments = []
        segment_start = None
        step = (window_size - hop_size) / self.sampleRate
        for i, e in enumerate(data):
            if e > threshold:
                if segment_start is None:
                    segment_start = i * step
            elif segment_start is not None:
                segment_end = i * step
                segments.append((segment_start, segment_end))
                segment_start = None
        
        return segments
    
    def getZCR(self):
        return self.getFrameFeatures(self.signalToZCR)
    
    def normalize(self, np_array):
        return np_array / np_array.max()
    
    def parseFrameDuration(self):
        window_size = int(self.frameDuration * self.sampleRate / 1000)
        hop_size = window_size // 2

        return window_size, hop_size
    
    def play(self):
        playsound(self.filePath)

    def plot(self, data, start_time=0, end_time=None, label = "", title = "", segments=[]):
        if end_time is None:
            end_time = self.getDuration()

        time_axis = np.linspace(start_time, end_time, len(data))

        plt.figure(figsize=(10, 4))
        plt.title(title)
        plt.plot(time_axis, data, linewidth=1)
        plt.xlabel('Time (s)')
        plt.ylabel(label)
        plt.grid()
        for start, end in segments:
            plt.axvspan(start, end, color='red', alpha=0.5)
        plt.show()

    def plotSelf(self, cti: float = -1, segments = []):
        timeAxis = np.linspace(0, self.getDuration(), self.numSamples)
        
        plt.figure(figsize=(10, 4))

        for channelIndex in range(self.numChannels):
            plt.subplot(self.numChannels, 1, channelIndex + 1)
            
            plt.grid(True)
            plt.plot(timeAxis, self.getSamplesForChannel(channelIndex))
            plt.title(f'{self.name} (channel {channelIndex + 1})')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            # plt.ylim(self.getChannelWidthMin(), self.getChannelWidthMax())

            if cti > -1:
                plt.axvline(x=cti, color='r')

            for start, end in segments:
                plt.axvspan(start, end, color='red', alpha=0.5)

        plt.tight_layout()
        plt.show()

    def save(self, name=None):
        if name is None:
            name = self.name + "-" + Utils.generateMMSSms()

        file = wave.open(name, 'wb')
        file.setnchannels(self.numChannels)
        file.setsampwidth(int(self.bitsPerSample / 8))
        file.setframerate(self.sampleRate)
        file.setnframes(int(self.numSamples))
        file.writeframes(self.samples.tobytes())
        file.close()

        return name
    
    def setFrameDuration(self, frameDuration):
        self.frameDuration = frameDuration

    def signalToEnergy(self, signal):
        return np.sum(np.square(signal))
    
    def signalToZCR(self, signal):
        return np.sum(np.abs(np.diff(np.sign(signal)))) / (2 * len(signal))
    
    def toMono(self):
        samples = self.samples
        if self.numChannels == 2:
            left = self.getSamplesForChannel(0)
            right = self.getSamplesForChannel(1)
            samples = (left + right) // 2
            
        return samples
    
    def toStereo(self, offset_in_ms: int = 10):
        if self.numChannels != 1:
            print("Cannot convert non-mono track into stereo")
            exit(1)

        offset_in_frames = int(self.sampleRate * offset_in_ms / 1000)
        
        print(self.samples.dtype)
        self.numChannels = 2
        interleaved = np.empty(self.numSamples * self.numChannels, dtype=np.int16)
        interleaved[0::2] = self.samples
        interleaved[1::2] = np.roll(self.samples, offset_in_frames)
        self.samples = interleaved
        
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
