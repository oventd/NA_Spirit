from shotgun_api3 import Shotgun

# ShotGrid 서버 정보 입력
SERVER_PATH = "https://hi.shotgrid.autodesk.com"  # 실제 ShotGrid 서버 주소
SCRIPT_NAME = "nayeon_key"  # ShotGrid 관리자에게 받은 스크립트 이름
API_KEY = "syeswcrleslhjbh4bd!poRvde"  # ShotGrid 관리자에게 받은 API 키

# ShotGrid API 연결
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, API_KEY)
PROJECT_ID = 124  # 실제 프로젝트 ID로 변경하세요



# Step의 code 값만 리스트로 저장
TASK_ID =121  #모델링

steps = sg.find("Step", [], ["id", "code", "short_name"])
print(steps)
tasks= sg.find("Task", [], ["id", "code", "short_name"])
print(tasks)
# task = sg.find_one("Step", [["id", "is", PROJECT_ID]], ["id", "content", "task_dependencies"])  # 애니메이션
# print(task)

# 프로젝트 ID 설정 (비어 있는 프로젝트의 ID 확인 필요)


# for step in steps:
#     print(f"현재 project의 Step Code: {step['code']}, Step Name: {step['short_name']}")

# existing_step = sg.find_one("Step", [["code", "is", "Design"]], ["id", "code"])
# print(existing_step)   # step 코드를 find_one
# step_id=existing_step["id"]

# tasks = sg.find("Task", [["step", "is", {"type": "Step", "id": step_id}]], ["id", "content", "entity"])


# print(tasks)

#desktop sg를 통해 파일을 열때 속해져있는 step의 값을 알아낼수 있다고함