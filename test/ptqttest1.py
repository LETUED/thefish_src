import sys
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QFrame, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image
import json


class FishClassifier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_model()
        # self.load_class_names()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("물고기 정보 프로그램")
        self.setFixedSize(900, 650)

        self.create_labels()
        self.create_buttons()
        self.create_central_line()
        self.create_info_window()  # info_window를 생성

        # info_window 위치 설정 코드 추가
        padding = 20
        central_line_x = self.width() // 2
        img_label_y = (self.height() - self.img_label.height()) // 2
        self.info_window.move(central_line_x + padding, img_label_y)

    def load_model(self):
        """모델 로드"""
        self.model = resnet50()
        num_features = self.model.fc.in_features
        self.model.fc = torch.nn.Linear(num_features, 40)
        checkpoint = torch.load('../models/resnet50_checkpoint.pth',
                                map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint)
        self.model.eval()

    def create_labels(self):
        """라벨 생성 및 스타일 설정"""
        self.img_label = QLabel(self)
        self.img_label.setFixedSize(400, 400)
        self.img_label.setStyleSheet("background-color: gray;")
        self.img_label.setAlignment(Qt.AlignCenter)

    def create_info_window(self):
        """info_window 라벨 생성 및 스타일 설정"""
        self.info_window = QLabel(self)
        self.info_window.setGeometry(50, 50, 350, 450)  # 라벨의 위치와 크기 지정
        self.info_window.setStyleSheet("background-color: white; border: 1px solid black; color: black;")
        self.info_window.setAlignment(Qt.AlignCenter)
        self.info_window.setText("-----------------------INFO-----------------------")
        self.info_window.show()  # 라벨을 화면에 표시
        self.info_window.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.info_window.setWordWrap(True)

        padding = 20
        central_line_x = self.width() // 2
        img_label_y = (self.height() - self.img_label.height()) // 2
        self.info_window.move(central_line_x + padding, img_label_y)
        self.info_window.raise_()  # 라벨을 최상위로 이동

    def create_buttons(self):
        """버튼 생성 및 위치 설정"""
        self.upload_btn = QPushButton("이미지 업로드", self)
        self.upload_btn.setFixedSize(150, 50)
        self.upload_btn.clicked.connect(self.upload_image)

    def create_central_line(self):
        """중앙선 생성 및 위치 설정"""
        self.central_line = QFrame(self)
        self.central_line.setFrameShape(QFrame.VLine)
        self.central_line.setFrameShadow(QFrame.Sunken)
        central_line_x = self.width() // 2
        self.central_line.setGeometry(central_line_x, 50, 2, 500)

        padding = 20
        img_label_x = central_line_x - padding - self.img_label.width()
        img_label_y = (self.height() - self.img_label.height()) // 2
        self.img_label.move(img_label_x, img_label_y)

        btn_x = img_label_x + (self.img_label.width() - self.upload_btn.width()) // 2
        btn_y = img_label_y + self.img_label.height() + padding
        self.upload_btn.move(btn_x, btn_y)

        # self.info_window.move(central_line_x + padding, img_label_y)

    def upload_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.', "Image files (*.jpg *.png)")
        if fname[0]:
            pixmap = QPixmap(fname[0])
            pixmap = pixmap.scaled(self.img_label.width(), self.img_label.height(), Qt.KeepAspectRatio)
            self.img_label.setPixmap(pixmap)
            self.classify_image(fname[0])

    def classify_image(self, path):
        """이미지 분류 및 결과 표시"""
        image = self.process_image(path)
        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = outputs.max(1)
            self.display_info(predicted.item())

    @staticmethod
    def process_image(path):
        """이미지 전처리"""
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img = Image.open(path).convert("RGB")
        return transform(img).unsqueeze(0)

    def get_fish_info(self, class_id):
        """물고기 ID를 기반으로 데이터베이스에서 정보를 검색하고 문자열로 반환"""

        # 데이터베이스에 연결
        conn = sqlite3.connect('FishDicDB.db')
        cursor = conn.cursor()

        # 물고기 정보 검색
        cursor.execute(f"SELECT 한글이름, 영어이름, 학명, 형태, 분포, 몸길이, 서식지 FROM COSDB WHERE ROWID={class_id + 1}")
        row = cursor.fetchone()

        # 연결 종료
        conn.close()

        if row:
            korname = row[0] if row[0] is not None else "정보 없음"
            engname = row[1] if row[1] is not None else "정보 없음"
            scientific_name = row[2] if row[2] is not None else "정보 없음"
            shape = row[3] if row[3] is not None else "정보 없음"
            distribution = row[4] if row[4] is not None else "정보 없음"
            body_length = row[5] if row[5] is not None else "정보 없음"
            habitat = row[6] if row[6] is not None else "정보 없음"

            return (f"한글이름 : {korname}\n\n"
                    f"영어이름 : {engname}\n\n"
                    f"학명 : {scientific_name}\n\n"
                    f"형태 : {shape}\n\n"
                    f"분포 : {distribution}\n\n"
                    f"몸길이 : {body_length}\n\n"
                    f"서식지 : {habitat}")
        else:
            return "해당하는 물고기 정보가 없습니다."

    # def load_class_names(self, file_path='/Users/jeondonghwan/Desktop/thefish_src/test/mapping.json'):
    #     """클래스 이름 로드"""
    #     try:
    #         with open(file_path, 'r') as file:
    #             self.class_names = json.load(file)
    #     except FileNotFoundError:
    #         print(f"파일 {file_path}를 찾을 수 없습니다.")
    #     except json.JSONDecodeError:
    #         print(f"파일 {file_path}의 JSON 형식에 오류가 있습니다.")

    def display_info(self, class_id):
        """분류된 정보를 라벨에 표시"""
        self.create_info_window()  # info_window를 새로 생성

        # DB에서 물고기 정보 조회
        fish_info = self.get_fish_info(class_id)

        if fish_info:
            info = f"--Info--\n\n물고기 ID: {class_id}\n\n{fish_info}"
            print("Info  --  ", info)
            self.info_window.setText(info)
        else:
            print(f"{class_id}에 해당하는 물고기 정보를 찾을 수 없습니다.")
            self.info_window.setText("해당하는 물고기 정보가 없습니다.")


# TODO: 창크기조절 라벨위치 조절

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FishClassifier()
    ex.show()
    sys.exit(app.exec_())