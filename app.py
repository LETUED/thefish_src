import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QWidget, QLineEdit
from Prj import Ui_MainWindow
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QImage

class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setupUi(self)
        self.Image_Import_Button.clicked.connect(self.uploadImages)
        self.Set_Ok.clicked.connect(self.setInputs)
        self.image_paths = []

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


    def uploadImages(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_paths, _ = QFileDialog.getOpenFileNames(self, "이미지 선택", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

        if file_paths:
            self.image_paths = file_paths
            folder_path = os.path.dirname(file_paths[0])
            self.path.setText(f"폴더 위치: {folder_path}")

    def setInputs(self):
        if self.image_paths:
            pixmap = QPixmap(self.image_paths[0])
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)
            self.lineEdit.setText("판별중..")
            self.startTimer()

    def startTimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.hideText)
        timer.start(10000)

    def hideText(self):
        self.lineEdit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    window.show()
    sys.exit(app.exec())
