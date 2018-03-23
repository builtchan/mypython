#Author: Johnson Chan
#Date: 2018/3/15
#!/usr/bin/python
'''
    zxing   解析二维码或者条形码
'''

from zxing import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
import sys
import os

class Recog_UI(QtWidgets.QWidget):

    def __init__(self):
        super(Recog_UI, self).__init__()
        self.pwd = os.getcwd().replace('/', '\\')
        self.needdel = False    # 用于判断是否需要删除copy过来的图片，因为decode貌似不能加路径

        self.setStyleSheet('QWidget{border-radius:5px;background-color:rgb(224,255,255);}')
        self.setFixedSize(400, 400)
        self.selectBtn = QtWidgets.QPushButton(self)
        self.selectBtn.setGeometry(5, 5, 90, 30)
        self.selectBtn.setText('打开')
        self.selectBtn.clicked.connect(self.getfilepathslot)
        self.selectBtn.setStyleSheet('QPushButton{background-color:rgb(85, 170, 255);color:black;border-radius:8px;border: 2px groove gray; \
                         border-style: outset;font-family:Arial;font-size:20px;} QPushButton:pressed{background-color:rgb(85, 170, 255);border-style:inset;}')

        self.recognBtn = QtWidgets.QPushButton(self)
        self.recognBtn.setGeometry(107, 5, 90, 30)
        self.recognBtn.setText('识别')
        self.recognBtn.clicked.connect(self.recogniceslot)
        self.recognBtn.setStyleSheet('QPushButton{background-color:rgb(85, 170, 255);color:black;border-radius:8px;border: 2px groove gray; \
                         border-style: outset;font-family:Arial;font-size:20px;} QPushButton:pressed{background-color:rgb(85, 170, 255);border-style:inset;}')

        self.editText = QtWidgets.QTextEdit(self)
        self.editText.setGeometry(5, 40, 390, 40)
        self.editText.setStyleSheet('QTextEdit{background-color:rgba(155,255,193,90);font-size:15pt;border: 2px groove gray;}')

        self.showText = QtWidgets.QTextEdit(self)
        self.showText.setGeometry(5, 85, 390, 310)
        self.showText.setStyleSheet('QTextEdit{background-color:rgba(155,255,193,90);font-size:15pt;border: 2px groove gray;}')



    def getfilepathslot(self):
        self.filepath, fileType = QFileDialog.getOpenFileName(self, '选择要识别的文件', '.')
        self.filepath = self.filepath.replace('/', '\\')
        self.editText.setText(self.filepath)
        print('FilePath', self.filepath)

    def recogniceslot(self):
        self.filepath = self.editText.toPlainText()

        '''是否和当前路径一致'''
        print('path', self.filepath[:self.filepath.rfind('\\')])
        print(self.pwd)
        if self.pwd == self.filepath[:self.filepath.rfind('\\')]:
            if not os.path.exists(self.filepath):
                self.showText.append('请查看路径是否正确')
            self.needdel = False
        else:
            print('目录不一致')
            # 在子目录下，需要拷贝上了
            cmd = 'copy ' + self.filepath + ' ' + self.pwd + '\\temp > null'
            os.system(cmd)
            os.system('del null')
            self.needdel = True

        zx = BarCodeReader()
        if self.needdel:
            ret = zx.decode('temp')
            os.system('del temp')
        else:
            ret = zx.decode(self.filepath.split('\\')[-1])
        if ret:
            if None == ret.type:
                self.showText.append('请查看文件是否二维码图片')
                if self.needdel:
                    os.system('del temp')
            else:
                print(ret)
                self.showText.append('format: ' + ret.format)
                self.showText.append('type  : ' + ret.type)
                self.showText.append('raw   : ' + ret.raw)
        else:
            self.showText.append('请查看文件是否正确')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Recog_UI()
    ui.show()
    sys.exit(app.exec())


# path = 'qrcode.png'
#
# zx = BarCodeReader()
# ret = zx.decode(path)
#
# if ret:
#     print(ret)
#     print(ret.format)
#     print(ret.type)
#     print(ret.raw)
# else:
#     print('nothing')

