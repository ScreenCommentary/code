# # python code 사용해서 mp4를 wav로 바꾼 파일은 계속 오류남
# # Error message: Error while processing frame

# # Python code to convert video to audio
# import moviepy.editor as mp
# # Insert Local Video File Path
# clip = mp.VideoFileClip("mp4.mp4")
# # Insert Local Audio File Path
# clip.audio.write_audiofile("wav.wav",codec='pcm_s16le')

from scipy.io import wavfile

filename = 'wav.wav'
sample_rate, samples = wavfile.read(filename)
print('sample rate : {}, samples.shape : {}'.format(sample_rate, samples.shape))

from scipy import signal
import numpy as np

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
not_speech_index = []
for i, frame in enumerate(frames):
    if not vad.is_speech(frame.bytes, sample_rate):
        # non_speech라고 인식된 인덱스 출력 및 그 프레임의 timestamp 출력
        # 소수점이 너무 길어져서 소수점 둘째자리에서 올림
        print(i, end=' ')
        print(round(frame.timestamp,2))
        # 따로 not_speech_index에 저장해놓음
        not_speech_index.append(i)

# queue 사용해서 연속된 (따로 길이를 지정하지는 않음) 
# non_speech_index에서 연속이 시작하는 인덱스를 저장함
queue = not_speech_index
packet = []
tmp = []
v = queue.pop(0)
tmp.append(v)
print(v)

while(len(queue)>0):
	vv = queue.pop(0)
	print(vv)
	if v+1 == vv:
		tmp.append(vv)
		v = vv
	else:
		packet.append(tmp)
		tmp = []
		tmp.append(vv)
		v = vv

packet.append(tmp)
start=[]
for i in enumerate(packet):
        start.append(i[1][0])
print(start)

# 연속된 인덱스의 timestamp를 가져옴
for i, times in enumerate(start):
    # 1분짜리 영상이 30까지 있는걸로 봐서 2배를 해줘서 시간을 맞춤
    print(round(frames[times].timestamp*2,2))
