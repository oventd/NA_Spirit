import os
import sgtk
import sys
import shutil

sys.path.append('/home/rapa/NA_Spirit/utils')


from sg_path_utils import SgPathUtils
from flow_utils import FlowUtils
# from db_crud import AssetDb


class ShotGridAssetManager:
    def __init__(self):
        """
        ShotGrid 프로젝트의 정보를 가져오고, 에셋 관련 작업을 수행하는 클래스.
        """
        self.engine = sgtk.platform.current_engine()  # ShotGrid Toolkit 엔진 가져오기
        self.context = self.engine.context  # 컨텍스트 가져오기

        self.project_dir = self.get_project_directory()
        self.db_thub_path = "/nas/spirit/DB/thum/3d_assets"
        self.thumbnail_url = None  # 썸네일 URL을 저장할 변수 초기화

    def get_project_directory(self) -> str:
        """
        현재 ShotGrid Toolkit 프로젝트의 루트 디렉토리를 반환.

        :return: 프로젝트 디렉토리 경로 (str)
        """
        if not self.context or not self.context.project:
            raise ValueError("현재 ShotGrid 프로젝트 컨텍스트를 찾을 수 없습니다.")

        # 프로젝트의 루트 디렉토리 가져오기
        tk = self.engine.sgtk
        return tk.project_path

    def get_asset_info(self, source_path: str) -> dict:
        """
        주어진 경로에서 에셋 정보를 추출하여 딕셔너리로 반환.

        :param source_path: 에셋의 원본 경로
        :return: 에셋 정보가 담긴 딕셔너리
        """
        asset_name = os.path.basename(source_path)
        split = source_path.split("/")
        category = split[-2] if len(split) > 1 else ""

        self.destination_path = f"/nas/spirit/DB/source/{asset_name}"

        asset_info = {
            "name": asset_name,
            "description": "",
            "asset_type": "3D Model",
            "category": category,
            "style": "realistic",
            "resolution": "",
            "file_format": "",
            "size": "",
            "license_type": "",
            "creator_id": self.context.user["id"],
            "creator_name": self.context.user["name"],
            "downloads": "",
            "created_at": "",
            "updated_at": "",
            "preview_url": self.thumbnail_url if self.thumbnail_url else "",  # 썸네일 URL 추가
            "image_url": "",
            "source_url": self.destination_path,
            "video_url": "",
            "project_name": self.context.project["name"]
        }

        return asset_info

    def find_asset_path(self, asset_name: str) -> str:
        """
        프로젝트 디렉토리의 assets 폴더에서 depth 2의 하위 폴더를 검색하여
        asset_name과 일치하는 폴더의 전체 경로를 반환.

        :param asset_name: 찾고자 하는 폴더명
        :return: 해당 폴더의 전체 경로 (없으면 빈 문자열 반환)
        """
        assets_directory = os.path.join(self.project_dir, "assets")

        if not os.path.exists(assets_directory):
            raise FileNotFoundError(f"경로가 존재하지 않습니다: {assets_directory}")

        for folder in os.listdir(assets_directory):
            folder_path = os.path.join(assets_directory, folder)

            if os.path.isdir(folder_path):
                sub_dirs = [
                    name for name in os.listdir(folder_path)
                    if os.path.isdir(os.path.join(folder_path, name))
                ]
                if asset_name in sub_dirs:
                    return os.path.join(folder_path, asset_name)

        return ""  # 해당 폴더를 찾지 못한 경우 빈 문자열 반환

    def copy_folder(self, source_folder: str, destination_folder: str):
        """
        특정 폴더를 대상 경로로 복사하는 메서드.

        :param source_folder: 원본 폴더 경로
        :param destination_folder: 복사할 대상 폴더 경로
        """
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"원본 폴더가 존재하지 않습니다: {source_folder}")

        if os.path.exists(destination_folder):
            shutil.rmtree(destination_folder)  # 기존 폴더 삭제

        try:
            shutil.copytree(source_folder, destination_folder)
            print(f"폴더 복사가 완료되었습니다: {source_folder} -> {destination_folder}")
        except Exception as e:
            print(f"폴더 복사 중 오류 발생: {e}")

    def get_thumbnail_url(self, asset_name: str , thumbnail_url):
        """
        특정 에셋의 썸네일 URL을 가져오는 메서드.
        """
        try:
            asset_id = FlowUtils.get_asset_id(self.context.project["name"], asset_name)
           
            # FlowUtils에서 썸네일 다운로드
            FlowUtils.get_thumnail(asset_id, thumbnail_url)

        except Exception as e:
            print(f"썸네일 가져오기 실패: {e}")
            self.thumbnail_url = ""  # 에러 발생 시 빈 값 반환

    def process_asset(self, asset_name: str):
        """
        특정 에셋을 찾아 정보를 출력하는 메서드.

        :param asset_name: 찾을 에셋 이름
        """
        asset_dir = self.find_asset_path(asset_name)
        if not asset_dir:
            print(f"에셋 '{asset_name}'을 찾을 수 없습니다.")
            return
        self.thumbnail_url = os.path.join(self.db_thub_path, f"{asset_name}.png")
        temp_path = "/home/rapa/temp.png"
        self.get_thumbnail_url(asset_name, temp_path)
        asset_info = self.get_asset_info(asset_dir)

        self.copy_folder(asset_dir, self.destination_path)

        # try:
        #     # AssetDb().upsert_data(asset_info)
        #     print(f"에셋 정보:\n{asset_info}")
        # except Exception as e:
        #     print(f"데이터베이스 업로드 실패: {e}")


# 사용 예시
if __name__ == "__main__":
    manager = ShotGridAssetManager()
    asset_name = "wood"  # 찾고자 하는 에셋 이름
    manager.process_asset(asset_name)
