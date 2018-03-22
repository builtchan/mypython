# Author: Johnson Chan
# Date: 2018/3/14
'''

    func:   用于生成中软AFC设备条屏显示模式配置文件

'''

from PyQt5 import QtCore, QtWidgets, QtGui
import sys


class UI_Form(object):
    def __init__(self):

        self.id1 = ''               # 计算ID1
        self.id2 = ''               # 计算ID2
        self.bitCheckBoxes = {}     # 是否有效
        self.bitRadioBtn = {}       # 不选择则 CheckBoxes 不加入计算

        self.choiceTopIndex = 26
        self.choiceLeftIndex = 10

        # 模式共4个字节
        self.choiceLabelHeight = 240
        self.choiceLabelWidth = 150

    def setFrom(self, form):
        form.setObjectName('form')
        form.setFixedWidth(self.choiceLabelWidth * 4 + self.choiceLeftIndex * 5)
        form.setFixedHeight(330)
        form.setWindowTitle('条屏状态模式生成器1.0 (RadioButton决定CheckBox是否参与计算)      by Johnson')

        # 模式共4个字节 background
        self.choiceLabel1 = QtWidgets.QLabel(form)
        self.choiceLabel1.setGeometry(self.choiceLeftIndex, self.choiceTopIndex, self.choiceLabelWidth, self.choiceLabelHeight)
        self.choiceLabel1.setText('维修模式:\n\n允许售票:\n\n允许充值:\n\n无打印模式:\n\n暂停服务:\n\n关闭服务:\n\n列车故障:\n\n紧急模式:')
        self.choiceLabel1.setStyleSheet("QLabel{background:rgb(155,205,193);border-radius:5px;font-size:13px;font-weight:bold;}")
        self.choiceLeftIndex = self.choiceLabelWidth + self.choiceLeftIndex + 10

        self.choiceLabel2 = QtWidgets.QLabel(form)
        self.choiceLabel2.setGeometry(self.choiceLeftIndex, self.choiceTopIndex, self.choiceLabelWidth, self.choiceLabelHeight)
        self.choiceLabel2.setText('允许纸币:\n\n允许硬币:\n\n储值卡:\n\n银行卡:\n\nNFC支付:\n\n手机扫码:\n\n代金券:\n\n二维码:')
        self.choiceLabel2.setStyleSheet("QLabel{background:rgb(155,205,193);border-radius:5px;font-size:13px;font-weight:bold;}")
        self.choiceLeftIndex = self.choiceLabelWidth + self.choiceLeftIndex + 10

        self.choiceLabel3 = QtWidgets.QLabel(form)
        self.choiceLabel3.setGeometry(self.choiceLeftIndex, self.choiceTopIndex, self.choiceLabelWidth, self.choiceLabelHeight)
        self.choiceLabel3.setText('正常找零:\n\n无找零模式:\n\n无部分币值:\n\n预留:\n\n允许查询:\n\n第三方支付:\n\n预留:\n\n预留:')
        self.choiceLabel3.setStyleSheet("QLabel{background:rgb(155,205,193);border-radius:5px;font-size:13px;font-weight:bold;}")
        self.choiceLeftIndex = self.choiceLabelWidth + self.choiceLeftIndex + 10
        self.choiceLabel4 = QtWidgets.QLabel(form)
        self.choiceLabel4.setGeometry(self.choiceLeftIndex, self.choiceTopIndex, self.choiceLabelWidth, self.choiceLabelHeight)
        self.choiceLabel4.setText('币值1:\n\n币值2:\n\n币值3:\n\n币值4:\n\n币值5:\n\n币值6:\n\n预留:\n\n预留:')
        self.choiceLabel4.setStyleSheet("QLabel{background:rgb(155,205,193);border-radius:5px;font-size:13px;font-weight:bold;}")
        self.choiceLeftIndex = self.choiceLabelWidth + self.choiceLeftIndex + 10

        # # 32个模式因子
        # self.mode1 =


        # 4字节 checkbox
        self.RaidoBtnGroup = QtWidgets.QButtonGroup(form)
        '''不互斥'''
        self.RaidoBtnGroup.setExclusive(False)
        for i in range(4):
            for j in range(8):
                self.bitCheckBoxes['bit' + str(i + 1) + str(j)] = QtWidgets.QCheckBox(form)
                self.bitCheckBoxes['bit' + str(i + 1) + str(j)].setGeometry((self.choiceLabelWidth + 10) * (i + 1) - 20,
                                                                        30 * (j + 1), 20, 20)
                self.bitRadioBtn['bit' + str(i + 1) + str(j)] = QtWidgets.QRadioButton(form)
                self.bitRadioBtn['bit' + str(i + 1) + str(j)].setGeometry((self.choiceLabelWidth + 10) * (i + 1) - 40,
                                                                        30 * (j + 1), 20, 20)
                self.RaidoBtnGroup.addButton(self.bitRadioBtn['bit' + str(i + 1) + str(j)])

        # 计算按钮
        self.addButton = QtWidgets.QPushButton(form)
        self.addButton.setText('计算mode')
        self.addButton.setGeometry(10, self.choiceLabelHeight + self.choiceTopIndex * 1.5, 120, 40)
        # self.addButton.setStyleSheet('QPushButton{font-size:22pt;font-weight:bold;background:rgb(82,139,139);}')
        self.addButton.setStyleSheet('QPushButton{background-color:rgb(85, 170, 255);color:white;border-radius:8px;border: 2px groove gray; \
                         border-style: outset;font-family:Arial;font-size:20px;} QPushButton:pressed{background-color:rgb(85, 170, 255);border-style:inset;}')
        self.addButton.clicked.connect(self.getModeSlot)

        font = QtGui.QFont()
        font.bold()
        font.setPixelSize(18)
        # id1
        self.id1Label = QtWidgets.QLabel(form)
        self.id1Label.setGeometry(200, self.choiceLabelHeight + self.choiceTopIndex * 1.5, 50, 40)
        self.id1Label.setText('ID1:')
        self.id1Label.setStyleSheet("QLabel{background:rgb(155,205,193);font-size:18pt;border-radius:10px;}")

        self.id1LineEdit = QtWidgets.QLineEdit(form)
        self.id1LineEdit.setGeometry(250, self.choiceLabelHeight + self.choiceTopIndex * 1.5, 120, 40)
        self.id1LineEdit.setFont(font)

        # id2
        self.id2Label = QtWidgets.QLabel(form)
        self.id2Label.setGeometry(420, self.choiceLabelHeight + self.choiceTopIndex * 1.5, 50, 40)
        self.id2Label.setText('ID2:')
        self.id2Label.setStyleSheet("QLabel{background:rgb(155,205,193);font-size:18pt;border-radius:10px;}")

        self.id2LineEdit = QtWidgets.QLineEdit(form)
        self.id2LineEdit.setGeometry(470, self.choiceLabelHeight + self.choiceTopIndex * 1.5, 120, 40)
        self.id2LineEdit.setFont(font)

        # 全选按钮
        self.choiceRadiogroup = QtWidgets.QButtonGroup(form)
        self.choiceRadiogroup.setExclusive(False)
        self.choiceCheckgroup = QtWidgets.QButtonGroup(form)
        self.choiceCheckgroup.setExclusive(False)
        self.allRadiaChoice1 = QtWidgets.QRadioButton(form)
        self.allRadiaChoice1.setObjectName('1')
        self.allRadiaChoice1.setGeometry((self.choiceLabelWidth + 10) - 40, 8, 20, 20)
        self.choiceRadiogroup.addButton(self.allRadiaChoice1)
        self.allCheckBoxChoice1 = QtWidgets.QCheckBox(form)
        self.allCheckBoxChoice1.setObjectName('1')
        self.allCheckBoxChoice1.setGeometry((self.choiceLabelWidth + 10) - 20, 8, 20, 20)
        self.choiceCheckgroup.addButton(self.allCheckBoxChoice1)

        self.allRadiaChoice2 = QtWidgets.QRadioButton(form)
        self.allRadiaChoice2.setGeometry((self.choiceLabelWidth + 10) * 2 - 40, 8, 20, 20)
        self.choiceRadiogroup.addButton(self.allRadiaChoice2)
        self.allRadiaChoice2.setObjectName('2')
        self.allCheckBoxChoice2 = QtWidgets.QCheckBox(form)
        self.allCheckBoxChoice2.setGeometry((self.choiceLabelWidth + 10) * 2 - 20, 8, 20, 20)
        self.choiceCheckgroup.addButton(self.allCheckBoxChoice2)
        self.allCheckBoxChoice2.setObjectName('2')

        self.allRadiaChoice3 = QtWidgets.QRadioButton(form)
        self.allRadiaChoice3.setGeometry((self.choiceLabelWidth + 10) * 3 - 40, 8, 20, 20)
        self.choiceRadiogroup.addButton(self.allRadiaChoice3)
        self.allRadiaChoice3.setObjectName('3')
        self.allCheckBoxChoice3 = QtWidgets.QCheckBox(form)
        self.allCheckBoxChoice3.setGeometry((self.choiceLabelWidth + 10) * 3 - 20, 8, 20, 20)
        self.choiceCheckgroup.addButton(self.allCheckBoxChoice3)
        self.allCheckBoxChoice3.setObjectName('3')

        self.allRadiaChoice4 = QtWidgets.QRadioButton(form)
        self.allRadiaChoice4.setGeometry((self.choiceLabelWidth + 10) * 4 - 40, 8, 20, 20)
        self.choiceRadiogroup.addButton(self.allRadiaChoice4)
        self.allRadiaChoice4.setObjectName('4')
        self.allCheckBoxChoice4 = QtWidgets.QCheckBox(form)
        self.allCheckBoxChoice4.setGeometry((self.choiceLabelWidth + 10) * 4 - 20, 8, 20, 20)
        self.choiceCheckgroup.addButton(self.allCheckBoxChoice4)
        self.allCheckBoxChoice4.setObjectName('4')

        '''connect'''
        self.choiceRadiogroup.buttonClicked.connect(self.setRadioCheckedSlot)
        self.choiceCheckgroup.buttonClicked.connect(self.setBoxCheckedSlot)

    def getModeSlot(self):
        self.id1 = ''
        self.id2 = ''
        for i in range(4):
            temp1 = 0
            temp2 = 0
            for j in range(8):
                if self.bitCheckBoxes['bit' + str(i + 1) + str(j)].isChecked() and self.bitRadioBtn['bit' + str(i + 1) + str(j)].isChecked():
                    temp1 += pow(2, j)
                elif self.bitRadioBtn['bit' + str(i + 1) + str(j)].isChecked():
                    temp2 += pow(2, j)
                # print(hex(temp1), hex(temp2))
            if temp1 < 15:
                self.id1 = '0' + str(hex(temp1).replace('0x', '')) + self.id1
            else:
                self.id1 = str(hex(temp1).replace('0x', '')) + self.id1
            if temp2 < 15:
                self.id2 = '0' + str(hex(temp2).replace('0x', '')) + self.id2
            else:
                self.id2 = str(hex(temp2).replace('0x', '')) + self.id2
        # print(self.id1)
        # print(self.id2)
        self.id1LineEdit.setText(self.id1)
        self.id2LineEdit.setText(self.id2)

    def setBoxCheckedSlot(self, CheckBox):
        for i in range(8):
            self.bitCheckBoxes['bit' + CheckBox.objectName() + str(i)].setChecked(CheckBox.isChecked())


    def setRadioCheckedSlot(self, RadioBtn):
        for i in range(8):
            self.bitRadioBtn['bit' + RadioBtn.objectName() + str(i)].setChecked(RadioBtn.isChecked())



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = UI_Form()
    ui.setFrom(widget)
    widget.show()
    sys.exit(app.exec())
