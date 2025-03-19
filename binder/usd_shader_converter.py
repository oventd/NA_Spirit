import os
import json

# 기본 경로 설정
BASE_DIR = "/nas/spirit/Char_ref"
USD_SHADER_JSON = os.path.join(BASE_DIR, "usd_preview_surface_assignments.json")
FINAL_JSON_PATH = os.path.join(BASE_DIR, "final_shader_data.json")

class USDShaderIntegrator:
    """쉐이더 JSON에서 에셋을 기준으로 통합 JSON을 생성하는 클래스"""

    def __init__(self):
        self.asset_data = {}

    def load_shader_json(self):
        """USD Preview Surface JSON 파일을 읽고, 에셋별 쉐이더 정보를 매핑"""
        if not os.path.exists(USD_SHADER_JSON):
            print(f"파일을 찾을 수 없습니다: {USD_SHADER_JSON}")
            return

        with open(USD_SHADER_JSON, 'r', encoding='utf-8') as f:
            shader_data = json.load(f)

        # 쉐이더별로 연결된 에셋을 가져와서 asset_data에 저장
        for shader, assets in shader_data.items():
            for asset in assets:
                if asset not in self.asset_data:
                    self.asset_data[asset] = {
                        "shader": shader,
                        "shader_json": USD_SHADER_JSON
                    }

    def link_usd_files(self):
        """에셋에 해당하는 USD 파일 연결"""
        usd_files = [f for f in os.listdir(BASE_DIR) if f.endswith('.usda') or f.endswith('.usd')]

        for usd_file in usd_files:
            asset_name = os.path.splitext(usd_file)[0]
            usd_path = os.path.join(BASE_DIR, usd_file)

            if asset_name in self.asset_data:
                self.asset_data[asset_name]["usd_file"] = usd_path

    def save_final_json(self):
        """에셋을 기준으로 한 최종 JSON 저장"""
        self.load_shader_json()  # 쉐이더 JSON 불러오기
        self.link_usd_files()  # USD 파일 연결

        with open(FINAL_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.asset_data, f, indent=4, ensure_ascii=False)

        print(f"통합 JSON이 저장되었습니다: {FINAL_JSON_PATH}")

# 실행 예제
if __name__ == "__main__":
    integrator = USDShaderIntegrator()
    integrator.save_final_json()
