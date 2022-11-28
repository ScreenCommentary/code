# import
import librosa # librosa==0.9.1
import webrtcvad # webrtcvad==2.0.10
import numpy as np

from os import path
from pydub import AudioSegment

# files
src = "prototype.mp4"
dst = "prototype_test.wav"

# convert mp4 to wav
sound = AudioSegment.from_file(src,format="mp4")
sound.export(dst, format="wav")

# load data
file_path = "prototype.wav"

# load wav file (librosa)
y, sr = librosa.load(file_path, sr=16000)
# convert the file to int if it is in float (Py-WebRTC requirement)
if y.dtype.kind == 'f':
    # convert to int16
    y = np.array([ int(s*32768) for s in y])
    # bound
    y[y > 32767] = 32767
    y[y < -32768] = -32768

# define webrtcvad VAD
vad = webrtcvad.Vad(3) # set aggressiveness from 0 to 3

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
frames = frame_generator(frame_duration_ms, y, sr)
not_speech_index = []
for i, frame in enumerate(frames):
    if not vad.is_speech(frame.bytes, sr):
        # non_speech라고 인식된 인덱스 출력 및 그 프레임의 timestamp 출력
        # 소수점이 너무 길어져서 소수점 둘째자리에서 올림
        print(i, end=' ')
        print(round(frame.timestamp,2)*2)
        # 따로 not_speech_index에 저장해놓음
        not_speech_index.append(i)

# queue 사용해서 연속된 (따로 길이를 지정하지는 않음) 
# non_speech_index에서 연속이 시작하는 인덱스를 저장함
queue = not_speech_index
packet = []
tmp = []
v = queue.pop(0)
tmp.append(v)
# print(v)

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

#10개이상 연속된 non_speech_index (0.1초)
end=[]
for i, con in enumerate(packet):
    if(len(packet[i])>9):
        end.append(packet[i])
for i, con in enumerate(end):
    print(con,len(con)*0.02)
start=[]
start_len=[]
for i in enumerate(end):
        start.append(i[1][0])
        start_len.append(len(i[1]))
print(start)

# # 연속된 인덱스의 timestamp를 가져옴
for i, times in enumerate(start):
    # 1분짜리 영상이 30까지 있는걸로 봐서 2배를 해줘서 시간을 맞춤
    print("non_speech_section start timestamp:",round((frames[times].timestamp*2),3))
    print("length:",round(start_len[i]*0.01,10))
