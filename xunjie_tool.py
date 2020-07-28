import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import Ui_MainWindow
from utils.xunjie import audioToText
import platform


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        #浏览
        self.pushButton_5.clicked.connect(self.select_file)

        #解析
        self.audioToText_t = AudioToTextThread()
        self.pushButton_4.clicked.connect(self.audioToText)
        self.audioToText_t.signal_audioToText.connect(self.button_audioToText_callback)


    def select_file(self):
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self, filter='m4a Files(*.m4a);;mp3 Files(*.mp3);;aac Files(*.aac);;wav Files(*.wav);;flac Files(*.flac);;')
        if platform.system() == 'Windows':
            fileName = fileName.replace("/","\\")
        self.lineEdit_2.setText(fileName)


    def audioToText(self):

        fileName = self.lineEdit_2.text()
        if fileName is None or fileName == '':
            self.statusBar().showMessage("请选择音频文件")
            return

        self.statusBar().showMessage("转换中")
        self.textEdit.setText('')
        self.audioToText_t.audioToText(fileName)


    def button_audioToText_callback(self, text):

        self.statusBar().showMessage("转换成功")
        self.textEdit.setText(text)



class AudioToTextThread(QtCore.QThread):
    signal_audioToText = QtCore.pyqtSignal(str)  # 信号

    def __init__(self, parent=None):
        super(AudioToTextThread, self).__init__(parent)
        self.filePath = None

    def audioToText(self, fileName):
        self.fileName = fileName
        self.start()

    def run(self):

        text =audioToText(self.fileName)

        self.signal_audioToText.emit(text)  # 发送信号



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())