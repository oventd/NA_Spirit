import os
import json

# JSON과 USD 파일이 저장된 폴더
BASE_DIR = "D:\\real\\char_ref"
FINAL_JSON_PATH = os.path.join(BASE_DIR, "final_shader_data.json")

class USDShaderFinalizer:
    """모든 에셋 데이터를 저장하는 프로그램"""

    def __init__(self, asset_name, json_path, usd_paths):
        self.asset_name = asset_name  # 에셋 이름 (예: "character_01")
        self.json_path = json_path  # JSON 파일 경로
        self.usd_paths = usd_paths  # USD 파일 리스트
        self.final_data = self.load_final_json()  # 기존 데이터 불러오기

    def load_final_json(self, path):
        """통합 JSON(`final_shader_data.json`)을 불러온다"""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}  # 기존 파일이 없으면 새로 만든다

    def update_final_json(self):
        """새로운 에셋 데이터를 통합 JSON에 추가"""
        self.final_data[self.asset_name] = {
            "json": self.json_path,
            "usd": self.usd_paths
        }

        # 통합 JSON 저장
        with open(FINAL_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.final_data, f, indent=4, ensure_ascii=False)

        print(f" {self.asset_name} 데이터가 통합 JSON에 저장됨: {FINAL_JSON_PATH}")
    

# 실행 예제
if __name__ == "__main__":
    # 모델러가 퍼블리시한 에셋 데이터
    asset_name = input(" 캐릭터 이름을 입력하세요: ")  # 예: "robot"

    # JSON 파일 경로 입력
    json_path = input(" 쉐이더 JSON 파일 경로를 입력하세요: ")  # 예: "D:\\real\\char_ref\\robot_shader.json"

    # USD 파일들 입력 (쉼표로 구분해서 여러 개 입력 가능)
    usd_paths_input = input(" USD 파일 경로들을 쉼표(,)로 구분하여 입력하세요: ")  # 예: "D:\\real\\char_ref\\robot_material_1.usd, D:\\real\\char_ref\\robot_material_2.usd"

    # 입력된 값을 리스트로 변환
    usd_paths = [path.strip() for path in usd_paths_input.split(",")]

    # 데이터 저장하기
    finalizer = USDShaderFinalizer(asset_name, json_path, usd_paths)
    finalizer.update_final_json()

    finalizer.load_final_json(FINAL_JSON_PATH)  # 최종 데이터 확인


