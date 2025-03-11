from shotgun_api3 import Shotgun
import os
from shotgrid_client_config import get_shotgrid_client

sg = get_shotgrid_client()


def find_asset_in_shot(shot_id):
    used_asset_list =[]
    assets = sg.find(
            "Asset",
            [["shots", "is",{"type":"Shot", "id":1182}]],
            ["id","code","sg_asset_type"]
        )
    for asset in assets:

        used_asset_list.append(asset["code"])
    return used_asset_list

find_asset_in_shot(1182)

