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
    def getTTS():
        TTS_audio = []
        for i in range(2, len + 2):
            TTS_audio.append(AudioFileClip("../TTS/kor" + str(i) + ".wav"))
        return TTS_audio
    
    def getTimestamp(timestamp):
        return timestamp

    ## param : original audio file,  tts audio file list, time list to insert TTS,
    def setAudio(audio, tts, timestamp):
        for i, j in [timestamp, len(timestamp)]:
            #result = CompositeAudioClip([audio.set_start(i), tts]) # 오디오 합성하기
            audioclip = CompositeAudioClip([tts[j].set_start(i), audioclip]) # 오디오 합성하기 
        return audioclip
   #setAudio(getOriginalAudio(), getTTS(), getTimestamp())

    def setVideo(name, audio, video):
        video.audio = audio
        video.write_videofile(name + ".mp4")
        print("Video production succeeded")
        return video
    #setVideo(name, setAudio(), getVideo())
    