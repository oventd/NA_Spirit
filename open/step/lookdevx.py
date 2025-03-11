import maya.cmds as cmds

# 모든 Mesh를 선택 제외하고 Shader만 선택
all_objects = cmds.ls(dag=True, long=True)  # 모든 DAG 노드 가져오기
mesh_objects = cmds.ls(type="mesh", long=True)  # 모든 Mesh 노드 가져오기

# Shape 노드가 아닌 Transform 노드를 찾기
mesh_transforms = cmds.listRelatives(mesh_objects, parent=True, fullPath=True) or []

# 전체 목록에서 Mesh Transform을 제외하고 선택
selection_excluding_mesh = list(set(all_objects) - set(mesh_transforms))

# 선택 변경
cmds.select(selection_excluding_mesh, replace=True)
print("Selected non-mesh objects:", selection_excluding_mesh)
