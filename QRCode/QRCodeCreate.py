#Author: Johnson Chan
#Date: 2018/3/14

from PyQt5 import QtCore, QtWidgets, QtGui
import qrcode
import os

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=20,
    border=1,
)

class Ui_Form(object):

    def __init__(self):
        self.OkImage = os.getcwd() + '\\qrcode.png'


    def setupUi(self, Form):
        self.form = Form
        Form.setObjectName("Form")
        Form.setWindowTitle('二维码生成')
        Form.setFixedSize(420, 460)
        Form.setStyleSheet('QWidget{border-radius:5px;background-color:rgb(64,224,208);}')
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 60, 30))
        self.label.setObjectName("label")
        self.label.setStyleSheet('QLabel{background-color:rgba(155,255,193,90);font-size:15pt;font-weight:bold;border: 2px groove gray;}')
        self.label.setText('Text:')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.sourceEdit = QtWidgets.QTextEdit(Form)
        self.sourceEdit.setGeometry(QtCore.QRect(80, 10, 260, 30))
        self.sourceEdit.setStyleSheet('QTextEdit{background-color:rgba(155,255,193,90);font-size:15pt;border: 2px groove gray;}')

        self.picLab = QtWidgets.QLabel(Form)
        self.picLab.setGeometry(QtCore.QRect(5, 45, 410, 410))
        self.picLab.setObjectName("picLab")
        self.picLab.setText('QRCode')
        self.picLab.setAlignment(QtCore.Qt.AlignCenter)

        self.genButton = QtWidgets.QPushButton(Form)
        self.genButton.setGeometry(QtCore.QRect(350, 10, 60, 30))
        self.genButton.setText('生成')
        self.genButton.setStyleSheet('QPushButton{background-color:rgb(85, 170, 255);color:white;border-radius:8px;border: 2px groove gray; \
                         border-style: outset;font-family:Arial;font-size:20px;} QPushButton:pressed{background-color:rgb(85, 170, 255);border-style:inset;}')

        # 生成图片按钮绑定的自定义槽函数
        self.genButton.clicked.connect(self.generateImg)


    def generateImg(self):
        # print(self.sourceEdit.toPlainText())
        qr.add_data(self.sourceEdit.toPlainText())
        qr.make(fit=True)
        # 生成二维码图片
        img = qr.make_image()
        # 需要注意的是，有序自身机制，使用png形式图片会相当方便，其他的格式在生成QPixmap形式时候会报null
        img.save('qrcode.png')
        # 将已经生成的图片加载成为QPixmap格式
        qpic = QtGui.QPixmap(self.OkImage).scaled(self.picLab.width(), self.picLab.height())
        self.picLab.setPixmap(qpic)
        # 将已经生成的图片删除，不占用空间
        # os.remove(self.OkImage)

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

