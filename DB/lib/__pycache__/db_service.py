from lib.db_crud import get_assets, get_asset_by_id

class AssetService:
    @staticmethod
    def fetch_assets(filter_conditions, sort_by=None, limit=20):
        return get_assets(filter_conditions, sort_by, limit)

    @staticmethod
    def fetch_asset_details(asset_id):
        return get_asset_by_id(asset_id)