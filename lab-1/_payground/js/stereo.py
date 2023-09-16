import wave
import numpy as np
import matplotlib.pyplot as plt

def plot_waveform(wav_file):
    with wave.open(wav_file, 'rb') as wf:
        num_channels = wf.getnchannels()
        num_frames = wf.getnframes()
        sample_width = wf.getsampwidth()
        sample_rate = wf.getframerate()
        audio_data = wf.readframes(num_frames)

        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        time_axis = np.linspace(0, num_frames / sample_rate, num_frames)

        plt.figure(figsize=(10, 4 * num_channels))

        for channel in range(num_channels):
            plt.subplot(num_channels, 1, channel + 1)
            channel_data = audio_array[channel::num_channels]
            plt.plot(time_axis, channel_data, label=f'Channel {channel + 1}')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.title(f'Channel {channel + 1} Waveform')
            plt.grid(True)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    wav_file = "/Users/tomas/Downloads/Sounds/Stereo_music.wav"
    plot_waveform(wav_file)