from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton

class ConfirmDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("확인")
        self.setModal(True)  # 모달 창 설정 (메인 윈도우 조작 불가)
        self.setGeometry(200, 200, 200, 100)

        layout = QVBoxLayout()

        # 안내 문구
        self.label = QLabel("정말로 실행하시겠습니까?")
        layout.addWidget(self.label)

        # 버튼 추가
        self.button_yes = QPushButton("Yes")
        self.button_no = QPushButton("No")
        layout.addWidget(self.button_yes)
        layout.addWidget(self.button_no)

        self.setLayout(layout)

        # 버튼 클릭 시 다이얼로그 결과 설정
        self.button_yes.clicked.connect(self.accept)  # Yes 선택 시 QDialog.accept() 호출
        self.button_no.clicked.connect(self.reject)  # No 선택 시 QDialog.reject() 호출

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("메인 윈도우")
        self.setGeometry(100, 100, 400, 300)

        # 버튼 추가
        self.button = QPushButton("팝업 열기", self)
        self.button.setGeometry(150, 130, 100, 40)
        self.button.clicked.connect(self.show_popup)

    def show_popup(self):
        dialog = ConfirmDialog()  # 팝업 창 생성
        result = dialog.exec()  # 팝업 실행 및 결과 반환

        if result == QDialog.Accepted:
            print("사용자가 'Yes'를 선택했습니다.")
        else:
            print("사용자가 'No'를 선택했습니다.")

# 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
