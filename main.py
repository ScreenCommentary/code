from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QUrl, QDir
from PyQt5.QtGui import QPalette
from PyQt5.uic import loadUi
from media import CMultiMedia
import os
import sys
import datetime

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)


class CWidget(QWidget):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        # Multimedia Object
        self.mp = CMultiMedia(self, self.view)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # video background color
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self.view.setAutoFillBackground(True);
        self.view.setPalette(pal)

        # volume, slider
        self.vol.setRange(0, 100)
        self.vol.setValue(50)

        # play time
        self.duration = ''

        # signal
        self.btn_video_add.clicked.connect(self.clickAdd)
        self.btn_script_add.clicked.connect(self.clickAddExcel)
        self.btn_play.clicked.connect(self.clickPlay)
        self.btn_stop.clicked.connect(self.clickStop)
        self.btn_pause.clicked.connect(self.clickPause)
        self.btn_forward.clicked.connect(self.clickForward)
        self.btn_prev.clicked.connect(self.clickPrev)
        #self.btn_push.clicked.connect(self)
        #self.btn_pull.clicked.connect(self)

        self.list.itemDoubleClicked.connect(self.dbClickList)
        self.vol.valueChanged.connect(self.volumeChanged)
        self.bar.sliderMoved.connect(self.barChanged)


    def clickAdd(self):
        files, ext = QFileDialog.getOpenFileNames(self, "Open Movie", QDir.homePath())

        if files != '':
            print('success')
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(files)))
    def clickAddExcel(self):
        file_path, ext = QFileDialog.getOpenFileName(self, '파일 열기', os.getcwd(), 'excel file (*.xls *.xlsx)')
        if file_path:
            self.df_list = self.loadData(file_path)

            # 콤보박스 워크시트 목록 추가
            for i in self.df_list:
                self.cmb.addItem(i.name)

            self.initTableWidget(0)

    def clickPlay(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def clickStop(self):
        self.mp.stopMedia()

    def clickPause(self):
        self.mp.pauseMedia()

    def clickForward(self):
        cnt = self.list.count()
        curr = self.list.currentRow()
        if curr < cnt - 1:
            self.list.setCurrentRow(curr + 1)
            self.mp.forwardMedia()
        else:
            self.list.setCurrentRow(0)
            self.mp.forwardMedia(end=True)

    def clickPrev(self):
        cnt = self.list.count()
        curr = self.list.currentRow()
        if curr == 0:
            self.list.setCurrentRow(cnt - 1)
            self.mp.prevMedia(begin=True)
        else:
            self.list.setCurrentRow(curr - 1)
            self.mp.prevMedia()

    def dbClickList(self, item):
        row = self.list.row(item)
        self.mp.playMedia(row)

    def volumeChanged(self, vol):
        self.mp.volumeMedia(vol)

    def barChanged(self, pos):
        print(pos)
        self.mp.posMoveMedia(pos)

    def updateState(self, msg):
        self.state.setText(msg)

    def updateBar(self, duration):
        self.bar.setRange(0, duration)
        self.bar.setSingleStep(int(duration / 10))
        self.bar.setPageStep(int(duration / 10))
        self.bar.setTickInterval(int(duration / 10))
        td = datetime.timedelta(milliseconds=duration)
        stime = str(td)
        idx = stime.rfind('.')
        self.duration = stime[:idx]

    def updatePos(self, pos):
        self.bar.setValue(pos)
        td = datetime.timedelta(milliseconds=pos)
        stime = str(td)
        idx = stime.rfind('.')
        stime = f'{stime[:idx]} / {self.duration}'
        self.playtime.setText(stime)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    w.show()
    sys.exit(app.exec_())