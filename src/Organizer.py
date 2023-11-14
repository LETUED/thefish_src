import os
import shutil
from PIL import Image
from sklearn.model_selection import train_test_split


def split_data_into_train_val_test(src_directory, dest_directory, train_ratio=0.7, val_ratio=0.15):
    """
    데이터를 학습, 검증, 테스트로 분할하고, 목표 디렉터리에 복사합니다.

    Args:
    - src_directory (str): 원본 데이터 폴더 경로
    - dest_directory (str): 데이터 분할 후 저장할 폴더 경로
    - train_ratio (float): 학습 데이터의 비율
    - val_ratio (float): 검증 데이터의 비율
    """
    class_dirs = [d for d in os.listdir(src_directory) if os.path.isdir(os.path.join(src_directory, d))]

    for set_name in ['train', 'val', 'test']:
        set_path = os.path.join(dest_directory, set_name)
        os.makedirs(set_path, exist_ok=True)
        for class_dir in class_dirs:
            os.makedirs(os.path.join(set_path, class_dir), exist_ok=True)

    for class_dir in class_dirs:
        src_class_dir = os.path.join(src_directory, class_dir)
        all_files = [f for f in os.listdir(src_class_dir) if os.path.isfile(os.path.join(src_class_dir, f))]

        train_files, temp_files = train_test_split(all_files, train_size=train_ratio, random_state=42)
        val_files, test_files = train_test_split(temp_files, train_size=val_ratio / (1 - train_ratio), random_state=42)

        for file in train_files:
            shutil.copy(os.path.join(src_class_dir, file), os.path.join(dest_directory, 'train', class_dir, file))
        for file in val_files:
            shutil.copy(os.path.join(src_class_dir, file), os.path.join(dest_directory, 'val', class_dir, file))
        for file in test_files:
            shutil.copy(os.path.join(src_class_dir, file), os.path.join(dest_directory, 'test', class_dir, file))


class ImageOrganizer:
    """
    주어진 디렉터리의 이미지 파일을 정리하는 클래스
    """
    SUPPORTED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".ppm", ".bmp", ".pgm", ".tif", ".tiff", ".webp"]

    def __init__(self, root_dir="img_data"):
        self.root_dir = root_dir

    def _is_supported_file(self, file_path):
        _, extension = os.path.splitext(file_path)
        return extension.lower() in self.SUPPORTED_EXTENSIONS

    def _convert_image(self, img_path, target_extension=".jpg"):
        """
        이미지의 확장자를 대상 확장자로 변경함.
        """
        if not img_path.endswith(target_extension):
            try:
                img = Image.open(img_path)
                if img.mode in ["RGBA", "P"]:
                    img = img.convert("RGB")
                new_path = os.path.splitext(img_path)[0] + target_extension
                img.save(new_path)
                os.remove(img_path)
                return new_path
            except Exception as e:
                print(f"Error converting {img_path}: {e}")
        return img_path

    def _rename_images(self, dir_path):
        """
        디렉터리 내의 이미지 파일의 이름을 일련 번호로 변경함.
        """
        images = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and self._is_supported_file(f)]
        for idx, img_name in enumerate(sorted(images), 1):
            extension = os.path.splitext(img_name)[-1]
            new_name = f"{os.path.basename(dir_path)}_{idx}{extension}"
            os.rename(os.path.join(dir_path, img_name), os.path.join(dir_path, new_name))

    def organize(self, target_extension=".jpg"):
        """
        이미지를 정리하고
        필요한 경우 이미지의 확장자를 변경하고 이름을 일련 번호로 변경함.
        """
        if not os.path.exists(self.root_dir):
            print(f"Directory {self.root_dir} does not exist!")
            return

        for class_dir in os.listdir(self.root_dir):
            full_class_dir = os.path.join(self.root_dir, class_dir)
            if os.path.isdir(full_class_dir):
                for img_name in os.listdir(full_class_dir):
                    img_path = os.path.join(full_class_dir, img_name)
                    if self._is_supported_file(img_path):
                        self._convert_image(img_path, target_extension)
                self._rename_images(full_class_dir)


if __name__ == "__main__":
    # 이미지 정리
    ROOT_DIR = "" # 정리할 이미지가 있는 폴더 경로
    organizer = ImageOrganizer(ROOT_DIR)
    organizer.organize()
