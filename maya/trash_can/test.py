from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox,
    QComboBox, QLabel, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
import re

class ReferenceManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reference Version Manager")
        self.setGeometry(100, 100, 400, 600)

        # 메인 레이아웃
        self.main_layout = QVBoxLayout()

        # 업데이트 버튼
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_versions)
        self.main_layout.addWidget(self.update_button)

        # 스크롤 영역 추가
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # 내부 위젯을 스크롤 가능하게 설정
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        # 데이터 로드
        self.load_references()

    def load_references(self):
        """
        레퍼런스 파일들의 버전을 읽어와 UI를 동적으로 생성
        """
        # 20개의 테스트 데이터 생성
        references = [f"scene.v{str(i).zfill(3)}.ma" for i in range(1, 21)]

        # 정렬하여 최신 버전 찾기
        versions = sorted(references, key=self.extract_version)
        latest_version = self.clean_version(versions[-1]) if versions else None

        self.items = []  # UI 요소들을 저장할 리스트

        for i, file_name in enumerate(versions):
            current_version = self.clean_version(file_name)  # 현재 버전

            # 개별 아이템 레이아웃
            item_layout = QHBoxLayout()
            item_layout.setSpacing(0)  # 체크박스와 이름 간격을 없앰

            # 체크박스 추가 (완전히 붙임)
            checkbox = QCheckBox()
            item_layout.addWidget(checkbox)

            # 자산명 (완전히 체크박스에 붙임)
            asset_label = QLabel(f"Asset_{i+1}")
            asset_label.setFixedWidth(60)  # 고정 너비
            item_layout.addWidget(asset_label)

            # 현재 버전 콤보박스
            combo = QComboBox()
            for ver in versions:
                combo.addItem(self.clean_version(ver))
            combo.setCurrentText(current_version)
            combo.setFixedWidth(60)
            item_layout.addWidget(combo)

            # 최신 버전 라벨
            latest_label = QLabel(latest_version)
            latest_label.setAlignment(Qt.AlignCenter)
            latest_label.setFixedWidth(40)
            item_layout.addWidget(latest_label)

            # 최신 버전과 현재 버전 비교하여 색상 이모지 추가
            emoji_label = QLabel("🟢" if current_version == latest_version else "🟡")
            emoji_label.setAlignment(Qt.AlignCenter)
            emoji_label.setFixedWidth(20)
            item_layout.addWidget(emoji_label)

            # 개별 항목의 간격을 일정하게 유지하기 위해 프레임 추가
            item_frame = QFrame()
            item_frame.setLayout(item_layout)
            item_frame.setFixedHeight(30)  # 고정된 높이 적용
            self.scroll_layout.addWidget(item_frame)

            # UI 요소 저장
            self.items.append((checkbox, combo, latest_label, emoji_label))

        # 마지막 빈 공간 추가 (스크롤 뷰가 깔끔하게 보이도록)
        self.scroll_layout.addStretch()

    def clean_version(self, filename):
        """
        파일명에서 'scene.'과 '.ma'를 제거하고 'v001' 형식만 반환.
        """
        return filename.replace("scene.", "").replace(".ma", "")

    def extract_version(self, filename):
        """
        파일명에서 버전 번호 추출하여 정렬을 위한 숫자로 변환
        """
        match = re.search(r"v(\d{3})", filename)
        return int(match.group(1)) if match else 0

    def update_versions(self):
        """
        체크된 항목들의 current 버전을 latest로 변경하고 체크박스 해제
        """
        for checkbox, combo, latest_label, emoji_label in self.items:
            if checkbox.isChecked():
                latest_version = latest_label.text()
                combo.setCurrentText(latest_version)

                # 이모지 변경 (최신 버전과 동일해졌으므로 초록색)
                emoji_label.setText("🟢")

                # 체크 해제
                checkbox.setChecked(False)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ReferenceManager()
    window.show()
    sys.exit(app.exec())
