import json

def process_assets(json_path):
    """JSON 파일을 읽고 각 에셋을 처리하는 함수"""
    with open(json_path, 'r', encoding='utf-8') as f:
        final_data = json.load(f)

    for asset_name, asset_info in final_data.items():
        print(f"처리 중: {asset_name}")
        print(f"쉐이더 JSON 파일 경로: {asset_info['json']}")
        print(f"USD 파일들: {asset_info['usd']}")

        # 여기에 추가 작업을 할 수 있습니다
        # 예: 쉐이더 JSON 파일을 읽고, USD 파일을 처리하는 코드 등
        for usd_path in asset_info['usd']:
            print(f"USD 파일 경로: {usd_path}")
            # 예시: USD 파일 처리하는 작업 추가
            # stage = Usd.Stage.Open(usd_path)   # USD 파일 열기
            #  추가 작업을 할 수 있습니다

# 실행 예시 (이 부분을 나중에 `process_assets.py`에서 실행)
if __name__ == "__main__":
    process_assets("D:\\real\\char_ref\\final_shader_data.json")
