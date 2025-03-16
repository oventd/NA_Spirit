from shotgun_api3 import Shotgun
import os

class FlowUtils:


    SERVER_PATH = 'https://hi.shotgrid.autodesk.com'
    SCRIPT_NAME = 'nayeon_key'
    API_KEY = 'syeswcrleslhjbh4bd!poRvde'

    sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)

    @classmethod
    def find_asset_in_shot(cls, shot_id):



        used_asset_list =[]
        assets = cls.sg.find(
                "Asset",
                [["shots", "is",{"type":"Shot", "id":shot_id}]],
                ["id","code","sg_asset_type"]
            )
        for asset in assets:

            used_asset_list.append(asset["code"])
        return used_asset_list



    @classmethod
    def get_cut_in_out(cls,SHOT_ID): 
        current_steps = cls.sg.find(
                "Shot",
                [["id", "is",SHOT_ID]],
                ["sg_cut_in", "sg_cut_out"]
            )
        return current_steps


    @classmethod
    def get_upstream_tasks(cls, current_id, current_format):
        """
        특정 Task ID와 파일 확장자에 맞는 PublishedFile의 경로를 반환하는 함수
        """

        current_steps = cls.sg.find(
            "PublishedFile",
            [["task", "is", {"type": "Task", "id": current_id}]], 
            ["id", "path"]
        )

        if not current_steps:
            print(f"No Published File Found for Task ID: {current_id}")
            return None


        for current_step in current_steps:
            path_data = current_step.get("path", {})
            if not path_data:
                print(f"No path data found for Task ID: {current_id}")


            local_path = path_data.get("local_path")
            if not local_path:
                print(f"No local path found for Task ID: {current_id}")
                continue 

            _, file_extension = os.path.splitext(local_path)

            if file_extension == current_format:
                return local_path

        
        print(f"No {current_format} file found for Task ID: {current_id}")
        return None


    def update_published_file(cls,PUBLISHED_FILE_ID,published_file_data):
        updated_published_file = cls.sg.update(
            "PublishedFile", 
            PUBLISHED_FILE_ID, published_file_data,  # 연결된 엔티티
            
        )

        return updated_published_file



