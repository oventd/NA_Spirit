import json
from pxr import Usd, UsdShade
import sys
sys.path.append("/home/rapa/NA_Spirit/utils")
print(sys.path) 
from usd_utils import UsdUtils
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import sys

class SimpleWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 윈도우 제목 및 크기 설정
        self.setWindowTitle("버튼 예제")
        self.setGeometry(100, 100, 300, 100)

        # 레이아웃 설정
        self.layout = QVBoxLayout()

        # 버튼 생성
        self.button = QPushButton("클릭해주세요")
        self.button.clicked.connect(self.on_button_click)  # 버튼 클릭 시 실행될 함수 연결
        self.layout.addWidget(self.button)

        # 레이블 추가 (메시지 표시용)
        self.label = QLabel("버튼을 클릭하세요")
        self.layout.addWidget(self.label)

        # 레이아웃 설정
        self.setLayout(self.layout)

    def on_button_click(self):
        """버튼 클릭 시 실행될 함수"""
        self.label.setText("버튼이 클릭되었습니다!")  # 레이블 텍스트 변경


    def process_assets(json_path):
        """JSON 파일을 읽고, 각 에셋에 대해 작업을 처리하는 함수"""
        
        # JSON 파일 열기
        with open(json_path, 'r', encoding='utf-8') as f:
            final_data = json.load(f)  # JSON 파일을 Python 객체로 변환

    def bind_material(prim, material_path):
        stage = prim.GetStage()
        material = UsdShade.Material.Get(stage, material_path)
        UsdShade.MaterialBindingAPI(prim).Bind(material)
        stage.GetRootLayer().Save()
        
    # 추가 코드 작성

    def process_usd_and_bind():
        root_stage = UsdUtils.get_stage("/home/rapa/NA_Spirit/root.usd")
        root_prim = UsdUtils.get_prim(root_stage, "/Root")
        root_dict = UsdUtils.usd_to_dict(root_prim)

        geo_paths = UsdUtils.find_prim_paths_by_type(root_dict, "Mesh")
        mat_paths = UsdUtils.find_prim_paths_by_type(root_dict, "Material")

        # 매테리얼과 지오메트리 바인딩
        for geo_path, mat_path in zip(geo_paths, mat_paths):
            geo_prim = UsdUtils.get_prim(root_stage, geo_path)
            UsdUtils.bind_material(geo_prim, mat_path)


# 애플리케이션 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())
# 실행 예시

    process_usd_and_bind()
    process_assets("/nas/spirit/Char_ref/final_shader_data.json")  # JSON 파일 경로
