
import sys
import os

# 현재 파일(ui.py)의 절대 경로
current_file_path = os.path.abspath(__file__)

# 'NA_Spirit' 폴더의 최상위 경로 찾기
na_spirit_dir = os.path.abspath(os.path.join(current_file_path, "../../"))

# 모든 하위 폴더를 sys.path에 추가
for root, dirs, files in os.walk(na_spirit_dir):
    if '__pycache__' not in root:  # __pycache__ 폴더는 제외
        sys.path.append(root)

from constant import *
from logger import *
from like_state import LikeState
from popup_manager import DownloadPopup


class DownloadManager:
    logger = create_logger(UX_DOWNLOAD_LOGGER_NAME, UX_DOWNLOAD_LOGGER_DIR)
    ui = None  # UI 저장용 클래스 변수 추가

    @classmethod
    def set_ui(cls, ui):
        cls.ui = ui  # UI 인스턴스 저장

    @classmethod
    def download_likged_assets_all(cls):
        if cls.ui is None:
            print("UI가 설정되지 않았습니다.")
            return
        
        download_list = LikeState().like_asset_list
        print(f"전체 다운로드 버튼이 눌렸어요 {download_list}")
        cls.ui.show()  # UI 전체를 보이게 설정
        cls.ui.stackedWidget.show()
        cls.ui.stackedWidget.setCurrentIndex(1)
        cls.logger.info(f"유저가 관심 에셋 전체를 다운받았어요")

    @classmethod
    def download_assets_one(cls):
        print("단일 에셋의 다운로드 버튼이 눌렸어요")
        cls.logger.info(f"유저가 단일 에셋을 다운받았어요")
