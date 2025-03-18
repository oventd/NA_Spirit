import os
from json_utils import JsonUtils  # JsonUtils 클래스 임포트

# LookdevX JSON 데이터 로드
def load_shader_json(json_path):
    """LookdevX 퍼블리시된 쉐이더 JSON 파일을 로드한다."""
    shader_json = JsonUtils.read_json(json_path)
    if shader_json is None:  # 파일이 없거나 JSON 파싱에 실패한 경우
        print(f" 에러: JSON 파일을 찾을 수 없거나 비어 있음 - {json_path}")
        return {}
    return shader_json

# 기존 데이터를 유지하면서 새로운 데이터를 추가 (업데이트)
def integrate_shader_data(json_path, output_path):
    """기존 JSON 데이터를 유지하면서 새로운 JSON 데이터를 추가한다."""
    
    # 기존 JSON 데이터 로드 (없으면 빈 딕셔너리 반환)
    existing_data = JsonUtils.read_json(output_path)

    # 새로운 JSON 데이터 로드
    new_shader_data = load_shader_json(json_path)

    # 기존 데이터에 새로운 데이터 추가 (덮어쓰지 말구 기존 데이터 유지)
    existing_data.update(new_shader_data)

    # 병합된 JSON 데이터 저장
    JsonUtils.write_json(output_path, existing_data)
    print(f" JSON 데이터가 {output_path} 파일에 성공적으로 병합되었습니다!")

# 메인 실행 함수
def main():
    """LookdevX 퍼블리시된 JSON을 불러와 기존이미 데이터에 병합하는 메인 함수"""
    LOCAL_PATH = r"home/rapa/char_ref"  # 로컬 경로
    JSON_FILE = os.path.join(LOCAL_PATH, "shader_data.json")  # LookdevX에서 퍼블리시된 JSON
    OUTPUT_JSON = os.path.join(LOCAL_PATH, "shader_data_integrated.json")  # 병합할 JSON 저장 경로

    integrate_shader_data(JSON_FILE, OUTPUT_JSON)

# 실행 부분
if __name__ == "__main__":
    main()
