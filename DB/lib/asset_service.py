from lib.db_crud import Crud  # 수정된 db_crud에서 Asset 클래스를 import

class AssetService:
    """
    UI와 DB 사이의 중간 계층 역할을 수행하는 서비스 클래스.
    - UI에서는 직접 db_crud.py를 호출하지 않고, 이 클래스를 통해서만 데이터 요청을 함.
    """

    @staticmethod
    def get_all_assets(filter_conditions=None, sort_by=None, limit=10):
        """
        모든 자산 데이터를 MongoDB에서 가져옴.
        - db_crud.py의 get_all_assets() 호출
        - 데이터를 UI에서 쉽게 사용 가능하도록 리스트로 변환
        """
        asset_manager = Crud()  # Asset 클래스의 인스턴스를 생성
        return asset_manager.get_assets(filter_conditions=filter_conditions, sort_by=sort_by, limit=limit)

    @staticmethod
    def get_asset_by_id(asset_id):
        """
        특정 ID의 자산 데이터를 가져옴.
        - UI에서 사용자가 클릭한 자산의 ID를 전달받아 해당 데이터를 조회
        """
        asset_manager = Crud()  # Asset 클래스의 인스턴스를 생성
        return asset_manager.get_asset_by_id(asset_id)
