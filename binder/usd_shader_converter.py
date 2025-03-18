import os
import json

# 기본 JSON 저장 경로 설정
BASE_DIR = "D:\\real\\char_ref"  # 모든 JSON 파일이 저장된 디렉토리
FINAL_JSON = os.path.join(BASE_DIR, "final_shader_data.json")

class USDShaderFinalizer:
    """USD Preview Surface JSON을 모두 수집하고 하나의 JSON으로 통합하는 클래스"""

    def __init__(self):
        self.master_data = {}

    def collect_json_files(self):
        """모든 JSON 파일을 수집하여 경로를 저장"""
        json_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.json') and f != "final_shader_data.json"]

        for json_file in json_files:
            asset_name = os.path.splitext(json_file)[0]  # 파일명(확장자 제거)이 에셋명
            json_path = os.path.join(BASE_DIR, json_file)  # 파일 경로
            self.master_data[asset_name] = json_path  # 에셋명 → JSON 파일 경로 매핑

    def merge_all_json(self):
        """마스터 JSON을 읽고 모든 JSON을 하나로 병합"""
        combined_data = {}

        for asset, json_path in self.master_data.items():
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                    combined_data.update(json_data)  # 모든 데이터를 하나의 딕셔너리로 통합

        return combined_data

    def save_final_json(self):
        """하나의 JSON 파일로 최종 저장"""
        self.collect_json_files()  # 모든 JSON 파일 수집
        final_data = self.merge_all_json()  # JSON 병합

        with open(FINAL_JSON, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

        print(f"모든 JSON 파일이 하나로 병합되었습니다: {FINAL_JSON}")

# 실행 예제
if __name__ == "__main__":
    finalizer = USDShaderFinalizer()

    # 모든 JSON 파일을 수집하여 하나의 JSON으로 저장
    finalizer.save_final_json()