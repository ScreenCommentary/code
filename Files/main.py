from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPalette, QMovie
from PyQt5.uic import loadUi
from PyQt5 import uic
from media import CMultiMedia
import os
import sys
import datetime
import pandas as pd
from PyQt5.QtWidgets import  QTableWidgetItem, QTableWidget, QPushButton
from gtts import gTTS
from openpyxl.reader.excel import load_workbook
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

#from EditAudio import *
class CWidget(QWidget):
    file_sender = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.progressBar.setValue(0)
        # Multimedia Object
        self.mp = CMultiMedia(self, self.view)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # video background color
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.black)
        self.view.setAutoFillBackground(True)
        self.view.setPalette(pal)
        self.df_list=[]

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
        self.btn_push.clicked.connect(self.ToTTS)
        self.btn_push.setEnabled(False)
        #self.btn_push.clicked.connect(self)
        #self.btn_pull.clicked.connect(self)

        #self.section_list.itemDoubleClicked.connect(self)
        self.list.itemDoubleClicked.connect(self.dbClickList)
        self.vol.valueChanged.connect(self.volumeChanged)
        self.bar.sliderMoved.connect(self.barChanged)
        # tts list
        self.tts_list.itemDoubleClicked.connect(self.playTTS)

        #쓰레드 설정
        self.thread= ThreadClass(parent=self)
        self.file_sender.connect(self.thread.ToTTS2)
    def clickAdd(self):
        files, ext = QFileDialog.getOpenFileNames(self, "Open Movie", QDir.homePath())

        if files != '':
            self.mp.addMedia(files)
    def clickAddExcel(self):
        file_path, ext = QFileDialog.getOpenFileName(self, '파일 열기', os.getcwd(), 'excel file (*.xls *.xlsx)')
        if file_path:
            self.df_list = self.loadData(file_path)
            for i in self.df_list:
                self.cmb.addItem(i.name)
            file = file_path
            self.btn_push.setEnabled(True)  ## 엑셀파일 들어오면 버튼 클릭가능
            self.ToTTS(file)
            self.initTableWidget(0)
        else:
            self.btn_push.setEnabled(False)  ##엑셀파일 읽히기전에는 버튼클릭 불가능

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

    def loadData(self, file_name):###
        df_list = []
        with pd.ExcelFile(file_name) as wb:
            for i, sn in enumerate(wb.sheet_names):
                try:
                    df = pd.read_excel(wb, sheet_name=sn)
                except Exception as e:
                    print('File read error:', e)
                else:
                    df = df.fillna(0)
                    df.name = sn
                    df_list.append(df)
        return df_list

    def initTableWidget(self, id):###
        # 테이블 위젯 값 쓰기
        self.list.clear()
        # select dataframe
        df = self.df_list[id];
        # table write
        col = len(df.keys())
        self.list.setColumnCount(col)
        self.list.setHorizontalHeaderLabels(df.keys())

        row = len(df.index)
        self.list.setRowCount(row)
        self.writeTableWidget(id, df, row, col)

    def writeTableWidget(self, id, df, row, col): ###
        for r in range(row):
            for c in range(col):
                item = QTableWidgetItem(str(df.iloc[r][c]))
                self.list.setItem(r, c, item)
        self.list.resizeColumnsToContents()


    def ToTTS(self, file): #tts 변환 부분
        load_wb = load_workbook(file, data_only=True)
        # 시트 이름으로 불러오기
        load_ws = load_wb['Sheet1']
        maxrow = load_ws.max_row
        self.progressBar.setMaximum(maxrow-1)

        self.thread.countChanged.connect(self.onCountChanged)
        self.thread.start()
        self.file_sender.emit(file)
    def onCountChanged(self, value):
        self.progressBar.setValue(value)
    def playTTS(self):
        print('a')

class ThreadClass(QThread,QWidget):
    file_receive = pyqtSignal(object)
    countChanged = pyqtSignal(int)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._mutex = QMutex()


    @pyqtSlot(object)
    def ToTTS2(self,file):
        self._mutex.lock()
        count = 0
        self.countChanged.emit(count)
        if file is None:
            self.btn_push.setEnabled(False)
        else:
            load_wb = load_workbook(file, data_only=True)
            # 시트 이름으로 불러오기
            load_ws = load_wb['Sheet1']
            maxrow = load_ws.max_row

            # 셀 주소로 값 출력
            for i in range(2, maxrow + 1):
                count+=1
                a = load_ws['A' + str(i)].value
                eng_wav = gTTS(a, lang='ko')
                eng_wav.save('../TTS/kor' + str(i) + '.wav')
                self.countChanged.emit(count)


        self._mutex.unlock()

    def run(self):
        self._mutex.lock()
        self._mutex.unlock()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    w.show()
    sys.exit(app.exec_())