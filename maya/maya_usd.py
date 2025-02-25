"""
- 짜야할 일
    
    1. 사용자가 USD 파일의 경로를 입력하면 Maya에서 레퍼런스로 불러오는 기능
    
    2. 사용자가 USD 파일의 경로를 입력하면 Maya로 직접 임포트하는 기능
    
    3. USD Layer Editor에서 해당 파일을 열어볼 수 있는 기능
"""

"""
usd 메인 스크립트
    UI관련 코드

    USD Asset 기능

    Maya API로 USD 로드 후 씬에 추가 ->usd layer editor에서 확인 가능 

    실행 
       
    


"""




import maya.cmds as cmds
import os
 


class USD_UI: 
    """ 클래스 초기화 및 경로 설정 """
    def __init__(self, work_path, publish_path, file_format='ma'):
        # 쿼리 모드 활성화 하여 정보를 조회, 파일을 엶
        self.scene_name = cmds.file(q=True, sn=True) 
        self.work_path = work_path
        self.publish_path = publish_path
        self.file_format = file_format if file_format in ['ma', 'mb'] else 'ma' 


    def reference_usd(self, usd_paths):   
        """ USD 파일 Maya 씬에 레퍼런스로 추가 """
        # 충동 방지를 위한 새로운 씬 강제 생성
        cmds.file(new=True, force=True)

        # 전달받은 모든 USD 파일 경로에 대해 반복, 각 파일을 레퍼런스 형태로 추가
        for usd_path in usd_paths:
            if not os.path.exists(usd_path):
                cmds.file(usd_path, reference=True, type = "USD") 
                continue
            cmds.file(usd_path, reference=True, type = "USD")
        self.save_work_file()
        self.save_publish_file()

        return True

    def import_usd(self, usd_paths):
        """USD 파일을 Maya로 직접 임포트하는 함수"""
        for usd_path in usd_paths: 
            if not os.path.exists(usd_path):
                cmds.warning(f"USD file not found: {usd_path}")
                continue
            cmds.mayaUSDImport(file=usd_path, primPath="/") #maya usd 임포트
        self.save_work_file()
        self.save_publish_file()

        return True

    def open_usd_layer_editor(self, usd_paths): 
        """ USD 레이어 에디터 창 열기"""
        for usd_path in usd_paths:
            if not os.path.exists(usd_path):
                cmds.warning(f"USD file not found: {usd_path}")
                continue
            cmds.file(usd_path, reference=True, type = "USD")
            cmds.mayaUsdLayerEditorWindow()

    def save_work_file(self):
        """ 작업 파일을 저장하는 함수"""
        if not self.work_path:
            cmds.warning("Work path is not specified.")
            return
        
        # 파일 형식 지정
        save_type = 'mayaAscii' if self.file_format == 'ma' else 'mayaBinary'
        work_dir = os.path.dirname(self.work_path)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        cmds.file(rename=self.work_path)
        cmds.file(save=True, type=save_type)
    
    def save_publish_file(self):
        if not self.publish_path:
            cmds.warning("Publish path is not specified.")
            return
        publish_dir = os.path.dirname(self.publish_path)
        if not os.path.exists(publish_dir):
            os.makedirs(publish_dir)
        assets = cmds.ls(assemblies=True)
        cmds.mayaUSDExport(file=self.publish_path, exportRoots=assets)
