# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrjylHjYX.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(984, 641)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Image_Import_Button = QPushButton(self.centralwidget)
        self.Image_Import_Button.setObjectName(u"Image_Import_Button")
        self.Image_Import_Button.setGeometry(QRect(50, 410, 151, 51))
        self.Set_Ok = QPushButton(self.centralwidget)
        self.Set_Ok.setObjectName(u"Set_Ok")
        self.Set_Ok.setGeometry(QRect(250, 410, 151, 51))
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(530, 30, 391, 471))
        self.lineEdit.setStyleSheet(u"background-color: rgb(217, 255, 217);")
        self.lineEdit.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.path = QLabel(self.centralwidget)
        self.path.setObjectName(u"path")
        self.path.setGeometry(QRect(80, 480, 291, 31))
        self.path.setLayoutDirection(Qt.LeftToRight)
        self.path.setStyleSheet(u"background-color:rgb(176, 237, 255);")
        self.path.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 40, 401, 351))
        self.label.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 984, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Image_Import_Button.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc9c4 \uc5c5\ub85c\ub4dc", None))
        self.Set_Ok.setText(QCoreApplication.translate("MainWindow", u"\ud310\ubcc4 \uc2dc\uc791", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\ud310\ubcc4 input text \ucc3d", None))
#if QT_CONFIG(tooltip)
        self.path.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.path.setText(QCoreApplication.translate("MainWindow", u"\ud574\ub2f9 \uc774\ubbf8\uc9c0 \ud3f4\ub354", None))
        self.label.setText("")
    # retranslateUi

