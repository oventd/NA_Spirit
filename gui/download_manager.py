
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
        print(f"✅ UI가 설정되었습니다: {cls.ui}")

    @classmethod
    def download_likged_assets_all(cls):
        if cls.ui is None:
            print("❌ UI가 설정되지 않았습니다. set_ui()를 호출했는지 확인하세요.")
            return
        
        print(f"✅ UI 객체 확인: {cls.ui}")
        print(f"✅ stackedWidget 객체 확인: {getattr(cls.ui, 'stackedWidget', 'stackedWidget 없음')}")

        if not hasattr(cls.ui, "stackedWidget"):
            print("❌ UI에 stackedWidget이 존재하지 않습니다.")
            return

        download_list = LikeState().like_asset_list
        print(f"🟢 전체 다운로드 버튼이 눌렸어요: {download_list}")

        try:
            cls.ui.stackedWidget.setCurrentIndex(1)  # ✅ 두 번째 화면으로 변경
            cls.ui.stackedWidget.show()  # ✅ stackedWidget 보이게 하기

            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()  # ✅ UI 강제 업데이트

            print("✅ UI 화면 전환 성공!")
        except AttributeError as e:
            print(f"❌ UI 화면 전환 실패: {e}")

        cls.logger.info(f"유저가 관심 에셋 전체를 다운받았어요")
