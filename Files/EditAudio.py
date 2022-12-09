from moviepy.editor import *


class EditAudio:
    def __init__(self, videoName, times):
        self.videoName = videoName
        self.timestamp = times
        try:
            self.video = VideoFileClip(videoName)
        except Exception:
            print("Not detection")

    '''
    function name : getOriginalAudio
    do : get audio part from the input video
    param : VideoFileClip object
    '''
    def getOriginalAudio(self, videoclip):
        return videoclip.audio

    '''
    function name : getTTS
    do : make a list to save TTS file names, list length is count of TTS files
    param :
        len - TTS file list count
    '''
    def getTTS(self, items):
        TTS_audio = []
        for item in items:
            # TTS_audio.append(AudioFileClip("../TTS/kor_FAST" + str(i+1) + ".wav"))
            TTS_audio.append(AudioFileClip(item))
        return TTS_audio

    '''
    function name : getTimestamp
    do : return timestamp list to insert TTS file
    param : 
        timeestamp
    '''
    def getTimestamp(self, timestamp):
        return self.timestamp

    '''
    function name : setAudio
    do : edit audio file with TTS list
    param :
        audio - original audio file
        tts - tts file list (getTTS())
        timestamp - time list to insert TTS (getTimestamp())
    '''
    def setAudio(self, audio, tts):
        for i in range(len(self.timestamp)):
            # result = CompositeAudioClip([audio.set_start(i), tts]) # 오디오 합성하기
            audio = CompositeAudioClip([tts[i].set_start(self.timestamp[i]), audio])  # 오디오 합성하기
        return audio

    # setAudio(getOriginalAudio(), getTTS(), getTimestamp())

    '''
    function name : setVideo
    do : make final video with edited audio
    param :
        name - video name for making
        audio - edited audio file (setAudio())
        video - original video to composite
    '''
    def setVideo(self, name, audio, video):
        video.audio = audio
        # result name?
        video.write_videofile("result.mp4")
        print("Video production succeeded")
        return video
    # setVideo(name, setAudio(), getVideo())
