# # python code 사용해서 mp4를 wav로 바꾼 파일은 계속 오류남
# # Error message: Error while processing frame

# # Python code to convert video to audio
# import moviepy.editor as mp
# # Insert Local Video File Path
# clip = mp.VideoFileClip("mp4.mp4")
# # Insert Local Audio File Path
# clip.audio.write_audiofile("wav.wav",codec='pcm_s16le')

# import
import struct 
import librosa # librosa==0.9.1
import webrtcvad # webrtcvad==2.0.10
import numpy as np

# load data
file_path = 'prototype.wav'

# load wav file (librosa)
y, sr = librosa.load(file_path, sr=16000)
# convert the file to int if it is in float (Py-WebRTC requirement)
if y.dtype.kind == 'f':
    # convert to int16
    y = np.array([ int(s*32768) for s in y])
    # bound
    y[y > 32767] = 32767
    y[y < -32768] = -32768

# create raw sample in bit
raw_samples = struct.pack("%dh" % len(y), *y)

# define webrtcvad VAD
vad = webrtcvad.Vad(3) # set aggressiveness from 0 to 3
window_duration = 0.03 # duration in seconds
samples_per_window = int(window_duration * sr + 0.5)
bytes_per_sample = 2 # for int16

# Start classifying chunks of samples
# var to hold segment wise report
segments = []
# iterate over the audio samples
for i, start in enumerate(np.arange(0, len(y), samples_per_window)):
    stop = min(start + samples_per_window, len(y))
    loc_raw_sample = raw_samples[start * bytes_per_sample: stop * bytes_per_sample]
    try:
        if(not vad.is_speech(loc_raw_sample, sample_rate = sr)):
            is_speech = vad.is_speech(loc_raw_sample, 
                                sample_rate = sr)
            segments.append(dict(
                    start = start,
                    stop = stop,
                    is_speech = is_speech))
    except Exception as e:
        print(f"Failed for step {i}, reason: {e}")

print(segments)
# # queue 사용해서 연속된 (따로 길이를 지정하지는 않음) 
# # non_speech_index에서 연속이 시작하는 인덱스를 저장함
# queue = not_speech_index
# packet = []
# tmp = []
# v = queue.pop(0)
# tmp.append(v)
# print(v)

# while(len(queue)>0):
# 	vv = queue.pop(0)
# 	print(vv)
# 	if v+1 == vv:
# 		tmp.append(vv)
# 		v = vv
# 	else:
# 		packet.append(tmp)
# 		tmp = []
# 		tmp.append(vv)
# 		v = vv

# packet.append(tmp)
# start=[]
# for i in enumerate(packet):
#         start.append(i[1][0])
# print(start)

# # 연속된 인덱스의 timestamp를 가져옴
# for i, times in enumerate(start):
#     # 1분짜리 영상이 30까지 있는걸로 봐서 2배를 해줘서 시간을 맞춤
#     print(round(frames[times].timestamp*2,2))
