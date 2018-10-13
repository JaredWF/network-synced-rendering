# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configurator.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Configurator(object):
    def setupUi(self, Configurator):
        Configurator.setObjectName("Configurator")
        Configurator.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Configurator)
        self.centralwidget.setObjectName("centralwidget")
        self.buttons = []
        for i in range(0, 5):
            sendButton = QtWidgets.QPushButton(self.centralwidget)
            sendButton.setGeometry(QtCore.QRect(10, i*120 + 10, 120, 60))
            font = QtGui.QFont()
            font.setFamily("Simplex")
            font.setPointSize(30)
            sendButton.setFont(font)
            sendButton.setObjectName("sendButton")
            sendButton.setText("Fire!")
            self.buttons.append(sendButton)
        Configurator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Configurator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        Configurator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Configurator)
        self.statusbar.setObjectName("statusbar")
        Configurator.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(Configurator)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Configurator = QtWidgets.QMainWindow()
    ui = Ui_Configurator()
    ui.setupUi(Configurator)
    Configurator.show()
    sys.exit(app.exec_())
