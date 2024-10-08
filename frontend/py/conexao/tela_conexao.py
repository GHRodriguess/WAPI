# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/ui/conexao/conecta_whatsapp.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tela_Conexao(object):
    def setupUi(self, Tela_Conexao):
        Tela_Conexao.setObjectName("Tela_Conexao")
        Tela_Conexao.setWindowModality(QtCore.Qt.NonModal)
        Tela_Conexao.setEnabled(True)        
        Tela_Conexao.setMouseTracking(False)
        Tela_Conexao.setFocusPolicy(QtCore.Qt.NoFocus)
        Tela_Conexao.setStyleSheet("QMainWindow{\n"
"background-color: rgb(50,50,50);\n"
"}")
        Tela_Conexao.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        Tela_Conexao.setDocumentMode(False)
        Tela_Conexao.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(Tela_Conexao)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 75))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 75))
        self.frame.setStyleSheet("QFrame {\n"
"background-color: rgb(70,70,70);\n"
"border-radius: 20px;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.botao_home = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.botao_home.sizePolicy().hasHeightForWidth())
        self.botao_home.setSizePolicy(sizePolicy)
        self.botao_home.setStyleSheet("QPushButton{\n"
"icon: url(:/icons/home.svg);\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"icon: url(:/icons/home_hover.svg);\n"
"background-color: transparent;\n"
"}")
        self.botao_home.setText("")
        self.botao_home.setIconSize(QtCore.QSize(40, 40))
        self.botao_home.setObjectName("botao_home")
        self.horizontalLayout.addWidget(self.botao_home)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.botao_contatos = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.botao_contatos.sizePolicy().hasHeightForWidth())
        self.botao_contatos.setSizePolicy(sizePolicy)
        self.botao_contatos.setStyleSheet("QPushButton{\n"
"icon: url(:/icons/contatos.svg);\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"icon: url(:/icons/contatos_hover.svg);\n"
"background-color: transparent;\n"
"}")
        self.botao_contatos.setText("")
        self.botao_contatos.setIconSize(QtCore.QSize(40, 40))
        self.botao_contatos.setObjectName("botao_contatos")
        self.horizontalLayout.addWidget(self.botao_contatos)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_2 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(15)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem3 = QtWidgets.QSpacerItem(583, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.botao_conexao = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.botao_conexao.sizePolicy().hasHeightForWidth())
        self.botao_conexao.setSizePolicy(sizePolicy)
        self.botao_conexao.setMinimumSize(QtCore.QSize(40, 40))
        self.botao_conexao.setStyleSheet("QPushButton{\n"
"icon: url(:/icons/nao_conectado.svg);\n"
"background-color: transparent;\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"icon: url(:/icons/nao_conectado_hover.svg);\n"
"background-color: transparent;\n"
"}")
        self.botao_conexao.setText("")
        self.botao_conexao.setIconSize(QtCore.QSize(35, 35))
        self.botao_conexao.setObjectName("botao_conexao")
        self.horizontalLayout.addWidget(self.botao_conexao)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 500))
        self.frame_2.setStyleSheet("QFrame {\n"
"background-color: rgb(70,70,70);\n"
"border-radius: 20px;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMaximumSize(QtCore.QSize(16777215, 75))
        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.qrcode = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Garamond")
        font.setPointSize(20)
        font.setBold(True)
        self.qrcode.setFont(font)
        self.qrcode.setStyleSheet("QLabel{\n"
"color: rgb(255,255,255);\n"
"}")
        self.qrcode.setAlignment(QtCore.Qt.AlignCenter)
        self.qrcode.setObjectName("qrcode")
        self.verticalLayout_2.addWidget(self.qrcode)
        self.verticalLayout.addWidget(self.frame_2)
        Tela_Conexao.setCentralWidget(self.centralwidget)

        self.retranslateUi(Tela_Conexao)
        QtCore.QMetaObject.connectSlotsByName(Tela_Conexao)

    def retranslateUi(self, Tela_Conexao):
        _translate = QtCore.QCoreApplication.translate
        Tela_Conexao.setWindowTitle(_translate("Tela_Conexao", "API WhatsApp"))
        self.label_2.setText(_translate("Tela_Conexao", "<html><head/><body><p><span style=\" color:#ffffff;\">CONEXÃO</span></p></body></html>"))
        self.label.setText(_translate("Tela_Conexao", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">ESCANEIE O QR CODE</span></p></body></html>"))
        self.qrcode.setText(_translate("Tela_Conexao", "<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\"><br/></span></p></body></html>"))
import frontend.ui.conexao.icons_rc as icons_rc
