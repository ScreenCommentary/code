from moviepy.editor import *

# 음성 삽입 기능 구현
# 예 - 영상 4초에 2초짜리 음성 삽입하기
num_worker = 0
## AudioSegment
# 1. 음성 파일 가져오기
len = 10
TTS_audio = []
for i in range(2, len + 2):
    TTS_audio.append(AudioFileClip("../TTS/kor" + str(i) + ".wav")) # for sample
# print(TTS_audio) # for check

# 2. 음성 삽입 위치 정하기
'''
pNum : 삽입 위치 순서대로 지정
p1_dur : tts 음성 시간, 
p1_dur - pNum 길이만큼 기존 음성을 분리해 하나의 음성으로 합친 후 다시 연결하기
'''
'''
tts - [] 리스트 형태로 관리
구간을 선택하면 리스트에 .push() 형태로 값 넣기
값 빼는건 어떻게 할건지 ?
넣을 데이터 : () tuple 형태로 
(ex) (1, 3) : 00:00:01 시점에 3초 길이의 음성
########
tts = [(1, 3), (2, 4)]
'''
#tts = [(2, 4), (7, 5), (13, 5), (27, 5), (41, 1), (44, 4), (52, 4), (1, 13, 4), (77, 1), (90, 10)]
tts = [2, 7, 13, 27, 41, 44, 52, (1, 13), (1, 17), (1, 30)]

# 3. 영상 가져오기
# 경로지정 필요
videoclip = VideoFileClip("../prototype.mp4")
audioclip = videoclip.audio
print("video download success")

# 4. 영상의 소리와 tts 합치기
# 선택한 시점을 기준으로 영상 소리 분리
####### audio_TTS.set_start(p1) # tts 시작 시간 지정
for i in range(len):
    audioclip = CompositeAudioClip([TTS_audio[i].set_start(tts[i]), audioclip]) # 오디오 합성하기 - 여러 개일 경우 반복문 등으로 수정 필요

# 5. 영상의 소리로 넣고 새로운 비디오 파일 생성
videoclip.audio = audioclip

'''
tts 리스트에 있는 값 넣기
audioclip 계속 반복하는 문제 --> 더 간단하게 수정할 수 있는 방법 찾아보기
#########
for i in range (len(tts)):
    ## TTS 파일 가져오기 (숫자 번호로 이름 붙이기)
    audio_TTS = AudioFileClip("video/" + str(i) + ".mp3") 
    mod_audioclip = CompositeAudioClip([audio_TTS.set_start(tts[i][0]), audioclip]) 

# 마지막에 음성 합치기
videoclip.audio = mod_audioclip

'''

videoclip.write_videofile("Prototype_RESULT.mp4")
print("Video production succeeded")
