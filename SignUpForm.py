# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignUp-form.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 720)
        MainWindow.setMaximumSize(QtCore.QSize(1100, 730))
        MainWindow.setStyleSheet("background:white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(530, 0))
        self.frame.setStyleSheet("border:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/Images/Mobile-login-Cristina.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setIconSize(QtCore.QSize(500, 500))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_5.addWidget(self.pushButton_5, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.signUpBtn = QtWidgets.QPushButton(self.frame_2)
        self.signUpBtn.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.signUpBtn.setFont(font)
        self.signUpBtn.setStyleSheet("/* Normal state styling */\n"
"QPushButton#signUpBtn {\n"
"    color: white;\n"
"    background: #0BDABF;\n"
"    border: 2px solid #0BDABF;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"}\n"
"\n"
"/* Hover state styling */\n"
"QPushButton#signUpBtn:hover {\n"
"    background: #08A79D; /* Change the color for hover effect */\n"
"}\n"
"\n"
"/* Advanced styling */\n"
"QPushButton#signUpBtn:pressed {\n"
"    background: #067267; /* Change the color for pressed effect */\n"
"    border: 2px solid #067267;\n"
"}\n"
"\n"
"/* Add any other advanced styling here */\n"
"\n"
"")
        self.signUpBtn.setObjectName("signUpBtn")
        self.gridLayout_2.addWidget(self.signUpBtn, 14, 1, 1, 2)
        self.showPasswordBtn = QtWidgets.QCheckBox(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.showPasswordBtn.setFont(font)
        self.showPasswordBtn.setObjectName("showPasswordBtn")
        self.gridLayout_2.addWidget(self.showPasswordBtn, 12, 1, 1, 2)
        self.frame_12 = QtWidgets.QFrame(self.frame_2)
        self.frame_12.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.gridLayout_2.addWidget(self.frame_12, 10, 1, 2, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.userNameInput = QtWidgets.QLineEdit(self.frame_5)
        self.userNameInput.setGeometry(QtCore.QRect(0, 30, 489, 28))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.userNameInput.setFont(font)
        self.userNameInput.setStyleSheet("border:none;\n"
"border-bottom:2px solid black;")
        self.userNameInput.setText("")
        self.userNameInput.setObjectName("userNameInput")
        self.gridLayout_2.addWidget(self.frame_5, 2, 1, 1, 3)
        self.frame_8 = QtWidgets.QFrame(self.frame_2)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_8)
        self.frame_10.setMaximumSize(QtCore.QSize(35, 16777215))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout.addWidget(self.frame_10)
        self.gridLayout_2.addWidget(self.frame_8, 0, 1, 1, 2)
        self.frame_11 = QtWidgets.QFrame(self.frame_2)
        self.frame_11.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.gridLayout_2.addWidget(self.frame_11, 3, 1, 1, 3)
        self.frame_9 = QtWidgets.QFrame(self.frame_2)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2.addWidget(self.frame_9, 13, 1, 1, 2)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMinimumSize(QtCore.QSize(50, 0))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 600))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_2.addWidget(self.frame_4, 1, 4, 15, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setMinimumSize(QtCore.QSize(50, 0))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 12, 1)
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_6.setStyleSheet("border:none;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label = QtWidgets.QLabel(self.frame_6)
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.loginBtn = QtWidgets.QPushButton(self.frame_6)
        self.loginBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.loginBtn.setFont(font)
        self.loginBtn.setStyleSheet("color:#0BDABF;\n"
"border:none;\n"
"")
        self.loginBtn.setObjectName("loginBtn")
        self.gridLayout_4.addWidget(self.loginBtn, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.gridLayout_2.addWidget(self.frame_6, 1, 1, 1, 3)
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_2.addWidget(self.frame_7, 15, 1, 1, 3)
        self.frame_13 = QtWidgets.QFrame(self.frame_2)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.gridLayout_2.addWidget(self.frame_13, 6, 1, 1, 1)
        self.userEmailInput = QtWidgets.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.userEmailInput.setFont(font)
        self.userEmailInput.setStyleSheet("border:none;\n"
"border-bottom:2px solid black;")
        self.userEmailInput.setText("")
        self.userEmailInput.setObjectName("userEmailInput")
        self.gridLayout_2.addWidget(self.userEmailInput, 4, 1, 1, 1)
        self.userPasswordInput_2 = QtWidgets.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.userPasswordInput_2.setFont(font)
        self.userPasswordInput_2.setStyleSheet("border:none;\n"
"border-bottom:2px solid black;")
        self.userPasswordInput_2.setText("")
        self.userPasswordInput_2.setObjectName("userPasswordInput_2")
        self.gridLayout_2.addWidget(self.userPasswordInput_2, 9, 1, 1, 1)
        self.userPasswordInput = QtWidgets.QLineEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.userPasswordInput.setFont(font)
        self.userPasswordInput.setStyleSheet("border:none;\n"
"border-bottom:2px solid black;")
        self.userPasswordInput.setText("")
        self.userPasswordInput.setObjectName("userPasswordInput")
        self.gridLayout_2.addWidget(self.userPasswordInput, 7, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signUpBtn.setText(_translate("MainWindow", "Signup"))
        self.showPasswordBtn.setText(_translate("MainWindow", "Show Password"))
        self.label.setText(_translate("MainWindow", "Signup Now"))
        self.label_2.setText(_translate("MainWindow", "Already have an account?"))
        self.loginBtn.setText(_translate("MainWindow", "Login Here"))
import resource_rc
