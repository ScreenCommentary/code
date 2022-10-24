from moviepy.editor import *

class EditAudio:
    videoName = ""
    timestamp = []

    def __init__(self, videoName, times) :
        self.videoName = videoName
        self.timestamp = times

    def getVideo(videoName) :
        #videoclip = VideoFileClip(videoName)
        ##### location exception needed
        return VideoFileClip(videoName)
    
    def getOriginalAudio(videoclip) :
        return videoclip.audio

    ##  언제 불러야 하는지?
    def getTTS(filename):
        #result = AudioFileClip(filename)
        return AudioFileClip(filename)

    ## param : original audio file, time list to insert TTS, tts audio file list
    def setAudio(audio, timestamp):
        for i, j in [timestamp, len(timestamp)]:
            fileName = "kor" + j + ".wav"
            print(fileName)
            tts = AudioFileClip(fileName) # ineffective?
            result = CompositeAudioClip([audio.set_start(i), tts]) # 오디오 합성하기 
        return result

        

    
# 음성 삽입 기능 구현

## AudioSegment
# 1. 음성 파일 가져오기
TTS_audio = AudioFileClip("video/sampleBgm2.mp3") # for sample

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
p1 = 4 # sample insert point 
p1_dur = 2 # sample TTS duration


## 음성 구간 잘라내기 기능
#audio_TTS = TTS_audio[p1 * 1000 : p1 + dur_seconds] 
audio_TTS = TTS_audio.subclip(p1, p1 + p1_dur) # 2초짜리 TTS -> TTS 파일 삽입할 때는 필요 없는 구문


# 3. 영상 가져오기
# 경로지정 필요
videoclip = VideoFileClip("video/new video.mp4")
audioclip = videoclip.audio

# 4. 영상의 소리와 tts 합치기
# 선택한 시점을 기준으로 영상 소리 분리
####### audio_TTS.set_start(p1) # tts 시작 시간 지정
new_audioclip = CompositeAudioClip([audio_TTS.set_start(p1), audioclip]) # 오디오 합성하기 - 여러 개일 경우 반복문 등으로 수정 필요

# 5. 영상의 소리로 넣고 새로운 비디오 파일 생성
videoclip.audio = new_audioclip

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

videoclip.write_videofile("new video2.mp4")
print("Video production succeeded")
