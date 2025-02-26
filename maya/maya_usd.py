import maya.cmds as cmds
import os
 


class Maya: 
    """ 클래스 초기화 및 경로 설정 """
    def __init__(self, work_path, publish_path, file_format='ma'):
        # 정보를 조회 a및 파일 열기 
        self.scene_name = cmds.file(q=True, sn=True) 
        self.work_path = work_path
        self.publish_path = publish_path
        self.file_format = file_format if file_format in ['ma', 'mb'] else 'ma' 


    def reference(self, usd_paths):   
        """ USD 파일 Maya 씬에 레퍼런스로 추가 """
        # 충동 방지를 위한 새로운 씬 강제 생성
        cmds.file(new=True, force=True)

        # 전달받은 모든 USD 파일 경로에 대해 반복, 각 파일을 레퍼런스 형태로 추가
        for usd_path in usd_paths:
            if not os.path.exists(usd_path):
                cmds.file(usd_path, reference=True, type = "USD") 
                continue
            cmds.file(usd_path, reference=True, type = "USD")

        # 작업 및 퍼블리시 파일 저장 
        self.save_work_file()
        self.save_publish_file()

        return True

    def import_usd (self, usd_paths):
        """USD 파일을 Maya로 직접 임포트하는 함수"""
    
        for usd_path in usd_paths: 
            if not os.path.exists(usd_path):
                cmds.warning(f"USD file not found: {usd_path}")
                continue
            cmds.mayaUSDImport(file=usd_path, primPath="/") #maya usd 임포트
        
        # 작업 및 퍼블리시 파일 저장 
        self.save_work_file()
        self.save_publish_file()

        return True

    def open_usd_layer_editor(self, usd_paths): 
        """ USD 레이어 에디터 창 열기"""
        for usd_path in usd_paths:
            # 레이어 에디터 창을 여는데 실패했을 경우를 고려 
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
        
        # 'ma'/ 'mb' 선택저장.(추후 usd형식 추가할지 상의)
        save_type = 'mayaAscii' if self.file_format == 'ma' else 'mayaBinary'
        work_dir = os.path.dirname(self.work_path)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        cmds.file(rename=self.work_path)
        cmds.file(save=True, type=save_type)
    
    def save_publish_file(self):
        """ 퍼블리시 파일을 저장하는 파일"""
        if not self.publish_path:
            cmds.warning("Publish path is not specified.")
            return
        publish_dir = os.path.dirname(self.publish_path)
        if not os.path.exists(publish_dir):
            os.makedirs(publish_dir)
        assets = cmds.ls(assemblies=True)
        cmds.mayaUSDExport(file=self.publish_path, exportRoots=assets)

