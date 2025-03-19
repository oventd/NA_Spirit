import json
import os

class DictManager:
    JSON_FILE_PATH = "/home/rapa/NA_Spirit/maya/asset_version_data.json"

    @staticmethod
    def save_dict_to_json(data):
        """✅ JSON 데이터를 특정 경로에 강제 저장"""
        try:
            with open(DictManager.JSON_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"✅ JSON 데이터 저장 완료: {DictManager.JSON_FILE_PATH}")  # 🚀 경로 확인!
        except Exception as e:
            print(f"⚠️ JSON 저장 실패: {e}")

    @staticmethod
    def load_dict_from_json():
        """🔹 JSON 파일에서 데이터를 불러옴. 없으면 자동 생성"""
        if not os.path.exists(DictManager.JSON_FILE_PATH):
            print("⚠️ JSON 파일이 존재하지 않습니다. 새 파일을 생성합니다.")
            # ✅ 빈 JSON 파일 생성
            DictManager.save_dict_to_json({})
            return {}

        try:
            with open(DictManager.JSON_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"✅ JSON 데이터가 로드되었습니다: {DictManager.JSON_FILE_PATH}")
            return data
        except Exception as e:
            print(f"⚠️ JSON 로드 실패: {e}")
            return {}
