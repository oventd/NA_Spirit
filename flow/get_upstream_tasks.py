from shotgun_api3 import Shotgun
import os
from shotgrid_client_config import get_shotgrid_client

sg = get_shotgrid_client()

PROJECT_ID = 124  # 실제 프로젝트 ID로 변경하세유

        
current_id =5911 
current_fomat =".abc"



# task_id = 1234

# # 필터 설정: 특정 작업 ID에 해당하는 작업을 찾습니다
# filters = [['id', 'is', task_id]]

# # 반환받을 필드 설정: 'upstream_tasks' 필드를 포함합니다
# fields = ['upstream_tasks']

# # 작업 정보 조회
# task = sg.find_one('Task', filters, fields)

# # 상위 종속성 작업 목록 추출
# upstream_tasks = task.get('upstream_tasks', [])

# # 상위 종속성 작업 출력
# for upstream_task in upstream_tasks:
#     print(f"Task ID: {upstream_task['id']}, Name: {upstream_task['name']}")


# 포멧은 신영지정 >> 지정이 없으면 업스트림 정보가 담긴 모든 포멧을 리턴
# 지정이 있다면 해당 포멧만 리턴

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



file_path = find_published_file(5911, ".abc")

print(f"Found File: {file_path}")

      

      






