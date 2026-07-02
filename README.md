# TheFish — AI 해양생물 분류 및 백과사전

이미지를 업로드하면 ResNet50 전이학습 모델이 어종을 분류하고, SQLite 백과사전 DB에서 해당 어종 정보를 보여주는 데스크톱 앱.
2023년 ICT이노베이션스퀘어 동아리 프로젝트 (팀 "쌀과자가 좋아", 4인).

## 구성

| 경로 | 설명 |
|---|---|
| `test/ptqttest1.py` | 메인 앱 (PyQt5) — 이미지 분류(40클래스) + 어종 정보 출력 |
| `test/FishDicDB.db` | 어종 백과사전 SQLite DB |
| `models/resnet50_checkpoint.pth` | 학습된 ResNet50 체크포인트 (90MB) |
| `src/학습.py` | ResNet50 전이학습 스크립트 (ImageFolder 기반) |
| `src/Organizer.py` | 데이터셋 train/val/test 분할 도구 |
| `app.py`, `Prj.py` | PySide6 GUI 프로토타입 (백업에서 복원) |
| `test/ptqttest1.spec` | PyInstaller 배포 스펙 |

학습 이미지 데이터셋(웹 크롤링 수집)과 활동 보고서는 저장소에 포함하지 않고 로컬 `data/`, `archive/`에 보관한다.

## 실행

`requirements.txt`는 2023년 개발 당시(Python 3.11) 고정 버전이라 Python 3.13에서는 설치가 실패한다. 3.13에서는 최신 CPU 빌드로 설치한다:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install PyQt5 pillow
cd test
python ptqttest1.py
```

![데모](docs/demo.png)

2026-07 기준 Python 3.13 + torch 2.x(CPU)/PyQt5로 동작 확인 — 이미지 업로드 → ResNet50 분류 → SQLite 백과사전 표시까지 전체 플로우 정상. (torch를 PyQt5보다 먼저 import해야 DLL 충돌이 없다.)

## 히스토리

- 자체 CNN → 클래스 증가 시 정확도 저하 → ResNet50 전이학습으로 전환, 40+ 클래스 분류 달성
- 이미지 수집: [AutoCrawler](https://github.com/YoongiKim/AutoCrawler) 활용
- 2026-07: 구글드라이브 백업(E드라이브)에서 GUI 프로토타입·데이터셋 복원
