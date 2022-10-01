from moviepy.editor import *

# 음성 삽입 기능 구현
# 예 - 영상 4초에 2초짜리 음성 삽입하기

## AudioSegment
# 1. 음성 파일 가져오기
#TTS_audio = AudioSegment.from_mp3("video/sampleBgm2.mp3")
TTS_audio = AudioFileClip("video/sampleBgm2.mp3")

# 2. 음성 삽입 위치 정하기
'''
pNum : 삽입 위치 순서대로 지정
p1_dur : tts 음성 시간, 
p1_dur - pNum 길이만큼 기존 음성을 분리해 하나의 음성으로 합친 후 다시 연결하기
'''
p1 = 4 # sample insert point 
p1_dur = 2 # sample TTS duration

## 음성 구간 잘라내기 기능
#audio_TTS = TTS_audio[p1 * 1000 : p1 + dur_seconds] 
audio_TTS = TTS_audio.subclip(p1, p1 + p1_dur) # 2초짜리 TTS -> 변환한 음성으로 바꾸기 필요


# 3. 영상 가져오기
videoclip = VideoFileClip("video/new video.mp4")
audioclip = videoclip.audio


# 4. 영상의 소리와 tts 합치기
# 선택한 시점을 기준으로 영상 소리 분리

####### audio_TTS.set_start(p1) # tts 시작 시간 지정
new_audioclip = CompositeAudioClip([audio_TTS.set_start(p1), audioclip]) # 오디오 합성하기 - 여러 개일 경우 반복문 등으로 수정 필요

# 5. 영상의 소리로 넣기
videoclip.audio = new_audioclip

videoclip.write_videofile("new video2.mp4")

print("done") # check
