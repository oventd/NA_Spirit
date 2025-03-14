
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
    
    def __init__(self):
        pass
        
    @classmethod
    def download_likged_assets_all(cls):
        download_list=LikeState().like_asset_list
        print(f"전체 다운로드 버튼이 눌렸어요{download_list}")

        cls.logger.info(f"유저가 관심에셋 전체를 다운받았어요")
        widget = DownloadPopup()
        widget.value_changed.connect(download_list)  # 시그널을 메인 윈도우의 슬롯에 연결
        widget.show()

    @classmethod
    def download_assets_one(cls):
        print("단일 에셋의 다운로드 버튼이 눌렸어요")

        cls.logger.info(f"유저가 단일 에셋을 다운받았어요")
    
    