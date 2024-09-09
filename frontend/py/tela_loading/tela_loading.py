# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend\ui\tela_loading\tela_loading.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tela_Loading(object):
    def setupUi(self, Tela_Loading):
        Tela_Loading.setObjectName("Tela_Loading")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Tela_Loading.sizePolicy().hasHeightForWidth())
        Tela_Loading.setSizePolicy(sizePolicy)
        Tela_Loading.setMinimumSize(QtCore.QSize(0, 0))
        Tela_Loading.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Tela_Loading.setStyleSheet("QMainWindow{\n"
"background-color: rgb(50,50,50);\n"
"\n"
"}")
        self.centralwidget = QtWidgets.QWidget(Tela_Loading)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 370))
        self.frame.setStyleSheet("QFrame{\n"
"image: url(:/icons/ampulheta.svg);\n"
"\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2.addWidget(self.frame)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMinimumSize(QtCore.QSize(0, 50))
        self.label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
"color: white\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame_2)
        Tela_Loading.setCentralWidget(self.centralwidget)

        self.retranslateUi(Tela_Loading)
        QtCore.QMetaObject.connectSlotsByName(Tela_Loading)

    def retranslateUi(self, Tela_Loading):
        _translate = QtCore.QCoreApplication.translate
        Tela_Loading.setWindowTitle(_translate("Tela_Loading", "Iniciando WAPI"))
        self.label.setText(_translate("Tela_Loading", "INICIANDO WAPI"))
import frontend.ui.tela_loading.icons_rc as icons_rc