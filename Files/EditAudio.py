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

    '''
    function name : getTTS
    do : make a list to save TTS file names, list length is count of TTS files
    param :
        len - TTS file list coun
    '''
    def getTTS():
        TTS_audio = []
        for i in range(2, len + 2):
            TTS_audio.append(AudioFileClip("../TTS/kor" + str(i) + ".wav"))
        return TTS_audio
    
    def getTimestamp(timestamp):
        return timestamp

    '''
    function name : setAudio
    do : edit audio file with TTS list
    param :
        audio - original audio file
        tts - tts file list (getTTS())
        timestamp - time list to insert TTS (getTimestamp())
    * test needed
    '''
    def setAudio(audio, tts, timestamp):
        for i, j in [timestamp, len(timestamp)]:
            #result = CompositeAudioClip([audio.set_start(i), tts]) # 오디오 합성하기
            audio = CompositeAudioClip([tts[j].set_start(i), audio]) # 오디오 합성하기 
        return audio
   #setAudio(getOriginalAudio(), getTTS(), getTimestamp())
   
    '''
    function name : setVideo
    do : make final video with edited audio
    param :
        name - video name for making
        audio - edited audio file (setAudio())
        video - original video to composite
    '''
    def setVideo(name, audio, video):
        video.audio = audio
        video.write_videofile(name + ".mp4")
        print("Video production succeeded")
        return video
    #setVideo(name, setAudio(), getVideo())
    