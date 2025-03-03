import json
import os

class JsonManager:
    def __init__(self, file_path: str):
        """
        :param file_path: 읽거나 쓸 JSON 파일의 경로
        """
        self.file_path = file_path

    def read_json(self) -> dict:
        """
        지정된 JSON 파일을 읽어 딕셔너리로 반환합니다.
        파일이 없으면 빈 딕셔너리를 반환합니다.
        """
        if not os.path.exists(self.file_path):
            print(f"JSON file not found: {self.file_path}")
            return {}
        try:
            with open(self.__path, "r") as file:
                if os.stat(self.__path).st_size == 0:
                    return {}
                return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"'{self.__path}' contains invalid JSON data.")

    def write_json(self, data: dict) -> None:
        """
        주어진 데이터를 JSON 형식으로 파일에 저장합니다.
        :param data: 저장할 딕셔너리 데이터
        """
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_json(self, updates: dict) -> None:
        """
        기존 JSON 파일의 데이터를 업데이트합니다.
        파일이 없으면 새로 생성합니다.
        :param updates: 업데이트할 딕셔너리 데이터 (기존 데이터와 병합)
        """
        data = self.read_json()
        data.update(updates)
        self.write_json(data)