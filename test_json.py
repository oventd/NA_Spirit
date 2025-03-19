import sys
import os

# 🔹 DictManager가 있는 폴더 경로 추가
custom_script_path = "/home/rapa/NA_Spirit/maya/"
if custom_script_path not in sys.path:
    sys.path.append(custom_script_path)

# 🔹 DictManager 불러오기
from json_manager import DictManager

# 🔹 JSON 저장 & 불러오기 테스트
data = {
    "character": {
        "path": "/home/rapa/NA_Spirit/maya/character_v002.mb",
        "objects": ["character_ctrl", "character_mesh"]
    },
    "prop": {
        "path": "/home/rapa/NA_Spirit/maya/prop_v003.mb",
        "objects": ["prop_ctrl", "prop_mesh"]
    }
}

# 🔹 JSON 저장 테스트
DictManager.save_dict_to_json(data)

# 🔹 JSON 불러오기 테스트
loaded_data = DictManager.load_dict_from_json()
print("✅ 불러온 데이터:", loaded_data)
