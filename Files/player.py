from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt, QUrl


class CPlayer:

    def __init__(self, parent):
        # 윈도우 객체
        self.parent = parent

        self.player = QMediaPlayer()
        self.player.currentMediaChanged.connect(self.mediaChanged)
        # self.player.durationChanged.connect(self.durationChanged)
        # self.player.positionChanged.connect(self.positionChanged)

        self.playlist = QMediaPlaylist()

    def play(self, playlists, startRow=0, option=QMediaPlaylist.Sequential):
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
        else:
            self.createPlaylist(playlists, startRow, option)
            self.player.setPlaylist(self.playlist)
            self.playlist.setCurrentIndex(startRow)
            self.player.play()

    def createPlaylist(self, playlists, startRow=0, option=QMediaPlaylist.Sequential):
        self.playlist.clear()
        for path in playlists:
            url = QUrl.fromLocalFile('../TTS' + path)
            self.playlist.addMedia(QMediaContent(url))
        self.playlist.setPlaybackMode(option)

    def updatePlayMode(self, option):
        self.playlist.setPlaybackMode(option)

    def upateVolume(self, vol):
        self.player.setVolume(vol)

    def mediaChanged(self, e):
        self.parent.updateMediaChanged(self.playlist.currentIndex())

