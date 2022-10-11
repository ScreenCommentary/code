from scipy.io import wavfile

filename = '0a7c2a8d_nohash_0.wav'
sample_rate, samples = wavfile.read(filename)
print('sample rate : {}, samples.shape : {}'.format(sample_rate, samples.shape))

from scipy import signal
import numpy as np

def log_specgram(audio, sample_rate, window_size=20, step_size=10, eps=1e-10):
    # nperseg: Length of each segment
    # noverlap: Number of points to overlap between segments
    nperseg = int(round(window_size * sample_rate / 1e3))
    noverlap = int(round(step_size * sample_rate / 1e3))
    freqs, times, spec = signal.spectrogram(audio, fs=sample_rate,
                                            window='hann', nperseg=nperseg,
                                            noverlap=noverlap, detrend=False)
    return freqs, times, np.log(spec.T.astype(np.float32) + eps)

import matplotlib.pyplot as plt

freqs, times, spectrogram = log_specgram(samples, sample_rate)

fig = plt.figure(figsize=(14, 8))
ax1 = fig.add_subplot(211)
ax1.set_title('Raw wave of ' + filename)
ax1.set_ylabel('Amplitude')
ax1.plot(np.linspace(0, sample_rate/len(samples), sample_rate), samples)

ax2 = fig.add_subplot(212)
ax2.imshow(spectrogram.T, aspect='auto', origin='lower',
           extent=[times.min(), times.max(), freqs.min(), freqs.max()])
ax2.set_yticks(freqs[::16])
ax2.set_xticks(times[::16])
ax2.set_title('Spectrogram of ' + filename)
ax2.set_ylabel('Freqs in Hz')
ax2.set_xlabel('Seconds')

mean = np.mean(spectrogram, axis=0)
std = np.std(spectrogram, axis=0)
spectrogram = (spectrogram - mean) / std
spectrogram.shape

import IPython.display as ipd
ipd.Audio(samples, rate=sample_rate)

# 0.25 ~ 0.8125 * sample_rate(16000)
samples_cut = samples[4000:13000]
ipd.Audio(samples_cut, rate=sample_rate)

import webrtcvad
vad = webrtcvad.Vad()
# 1~3 까지 설정 가능, 높을수록 aggressive
vad.set_mode(3)

class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    frames = []
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        frames.append(Frame(audio[offset:offset + n], timestamp, duration))
        timestamp += duration
        offset += n
    
    return frames

# 10, 20, or 30
frame_duration_ms = 10 # ms
frames = frame_generator(frame_duration_ms, samples, sample_rate)
for i, frame in enumerate(frames):
    if not vad.is_speech(frame.bytes, sample_rate):
        print(i, end=' ')