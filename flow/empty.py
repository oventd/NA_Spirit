task_id = 1234

# 필터 설정: 특정 작업 ID에 해당하는 작업을 찾습니다
filters = [['id', 'is', task_id]]

# 반환받을 필드 설정: 'upstream_tasks' 필드를 포함합니다
fields = ['upstream_tasks']

# 작업 정보 조회
task = sg.find_one('Task', filters, fields)

# 상위 종속성 작업 목록 추출
upstream_tasks = task.get('upstream_tasks', [])

# 상위 종속성 작업 출력
for upstream_task in upstream_tasks:
    print(f"Task ID: {upstream_task['id']}, Name: {upstream_task['name']}")

