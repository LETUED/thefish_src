import os
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.optim import lr_scheduler
from torchvision import datasets, transforms, models

# 데이터 경로, 배치 크기, 에폭 수, 모델 이름, 학습률, 스케줄러 설정을 위한 변수 선언
DATA_DIR = "data"  # 데이터 경로를 상대 경로로 변경
BATCH_SIZE = 32
NUM_EPOCHS = 25
MODEL_NAME = "resnet50"
LEARNING_RATE = 0.001
STEP_SIZE = 7
GAMMA = 0.1

# 데이터 전처리를 위한 변환 작업 정의
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),  # 무작위 크기 및 비율로 이미지 자르기 및 크기 조정
        transforms.RandomHorizontalFlip(),  # 무작위로 이미지 좌우 반전
        transforms.ToTensor(),  # 이미지를 텐서로 변환
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 정규화
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),  # 이미지 크기 조정
        transforms.CenterCrop(224),  # 중앙에서 이미지 자르기
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

# 이미지 데이터셋 로딩 및 데이터 로더 생성
image_datasets = {x: datasets.ImageFolder(os.path.join(DATA_DIR, x), data_transforms[x]) for x in ['train', 'val']}
dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=BATCH_SIZE, shuffle=True, num_workers=4) for x in ['train', 'val']}
dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 모델 훈련을 위한 클래스
class ModelTrainer:
    def __init__(self, model_name, num_classes):
        # 모델 초기화 및 최종 레이어 설정
        self.model_name = model_name
        if model_name == "resnet50":
            self.model = models.resnet50(pretrained=True)
            num_ftrs = self.model.fc.in_features
            self.model.fc = torch.nn.Linear(num_ftrs, num_classes)  # 마지막 fully connected 레이어 변경
        elif model_name == "vgg16":
            self.model = models.vgg16(pretrained=True)
            num_ftrs = self.model.classifier[6].in_features
            self.model.classifier[6] = torch.nn.Linear(num_ftrs, num_classes)  # VGG16의 분류기 변경
        else:
            raise ValueError("Unknown model name")

        # 멀티 GPU 설정
        if torch.cuda.device_count() > 1:
            print("Using", torch.cuda.device_count(), "GPUs!")
            self.model = torch.nn.DataParallel(self.model)

        # 모델을 GPU로 이동
        self.model = self.model.to(device)
        self.criterion = torch.nn.CrossEntropyLoss()  # 손실 함수 설정
        self.optimizer = optim.SGD(self.model.parameters(), lr=LEARNING_RATE, momentum=0.9)  # 최적화 기법 설정
        self.scheduler = lr_scheduler.StepLR(self.optimizer, step_size=STEP_SIZE, gamma=GAMMA)  # 학습률 감소 스케줄러 설정

        # 조기 종료를 위한 변수 설정
        self.early_stop_count = 0
        self.best_loss = float('inf')

    def train(self, num_epochs=NUM_EPOCHS):
        train_losses = []
        val_losses = []

        for epoch in range(num_epochs):
            # 에폭별 훈련 및 검증 시작
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)

            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train()  # 모델을 훈련 모드로 설정
                else:
                    self.model.eval()  # 모델을 평가 모드로 설정

                running_loss = 0.0
                running_corrects = 0

                # 데이터 로더에서 배치별로 데이터를 가져옴
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    self.optimizer.zero_grad()  # 기울기 초기화

                    # 순전파; 훈련 때만 기울기 계산
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = self.model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = self.criterion(outputs, labels)

                        # 역전파 + 최적화; 훈련 단계에서만
                        if phase == 'train':
                            loss.backward()
                            self.optimizer.step()

                    # 통계 계산
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss / dataset_sizes[phase]  # 에폭별 손실 계산
                epoch_acc = running_corrects.double() / dataset_sizes[phase]  # 에폭별 정확도 계산
                print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

                # 손실 기록
                if phase == 'train':
                    train_losses.append(epoch_loss)
                    self.scheduler.step()  # 학습률 감소
                else:
                    val_losses.append(epoch_loss)

                # 검증 단계에서 모델 저장 및 조기 종료 확인
                if phase == 'val':
                    if epoch_loss < self.best_loss:
                        self.best_loss = epoch_loss
                        self.early_stop_count = 0
                        self.save_model()  # 모델 저장
                    else:
                        self.early_stop_count += 1
                        if self.early_stop_count > 5:
                            print("Early stopping triggered.")
                            return  # 조기 종료

    def save_model(self):
        # 모델 저장 경로 설정 및 모델 저장
        model_save_path = os.path.join("/content/drive/MyDrive/thefish/results/models", f"{self.model_name}_checkpoint.pth")
        torch.save(self.model.state_dict(), model_save_path)
        print(f"Model saved at {model_save_path}")

# 모델 트레이너 인스턴스 생성 및 훈련 시작
trainer = ModelTrainer(MODEL_NAME, len(image_datasets['train'].classes))
trainer.train()
