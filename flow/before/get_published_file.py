from shotgun_api3 import Shotgun
import os
from shotgrid_client_config import get_shotgrid_client

sg = get_shotgrid_client()

PROJECT_ID = 124 
current_id =5911 
current_fomat =".abc"



def find_published_file(current_id, current_format):
    """
    특정 Task ID와 파일 확장자에 맞는 PublishedFile의 경로를 반환하는 함수
    """

    current_steps = sg.find(
        "PublishedFile",
        [["task", "is", {"type": "Task", "id": current_id}]], 
        ["id", "path"]
    )

    if not current_steps:
        print(f"No Published File Found for Task ID: {current_id}")
        return None


    for current_step in current_steps:
        path_data = current_step.get("path", {})


        local_path = path_data.get("local_path")
        if not local_path:
            continue 

        _, file_extension = os.path.splitext(local_path)

        if file_extension == current_format:
            return local_path

    
    print(f"No {current_format} file found for Task ID: {current_id}")
    return None



      

      






