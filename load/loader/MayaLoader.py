import Loader
import maya.cmds as cmds
import os




class MayaLoader(Loader):
    def __init__(self, work_path, publish_path, file_format='ma'):
        # 정보를 조회 a및 파일 열기 
        self.scene_name = cmds.file(q=True, sn=True) 
        self.work_path = work_path
        self.publish_path = publish_path
        self.file_format = file_format if file_format in ['ma', 'mb'] else 'ma' 


    def import_file(self, paths):
        """ USD 파일을 Maya로 직접 임포트하는 함수 """
        # 전달받은 모든 USD 파일 경로에 대해 반복
        for path in paths: 
            if not os.path.exists(path):
                cmds.warning(f"USD file not found: {path}")
                continue
            # maya usd 임포트
            cmds.mayaUSDImport(file=path, primPath="/") 

        return True

    def reference_file(self, paths):
        """ USD 파일 Maya 씬에 레퍼런스로 추가 """
        # 충돌 방지를 위한 새로운 씬 강제 생성
        cmds.file(new=True, force=True)
    
        # 전달받은 모든 USD 파일 경로에 대해 반복, 각 파일을 레퍼런스 형태로 추가
        for path in paths:
            if not os.path.exists(path):
                cmds.file(path, reference = True) 
                continue
            cmds.file(path, reference = True)
        
        return True
    
    def stage_file(self, paths):
        anonymous_layer = "AnonymousLayer1"
        existing_layers = cmds.mayaUsdLayerEditor(query=True, listAnonymousLayers=True) or []
        for path in paths:
            if not os.path.exists(path):
                cmds.warning(f"USD file not found: {path}")
                continue
            
            cmds.file(path, reference=True, type = "USD")
            cmds.mayaUsdLayerEditorWindow(edit=True, addSubLayer=(anonymous_layer, path))


            print(f"Added {path} as sublayer to {anonymous_layer}")



    # def stage_file(self, paths):
    #     """ USD 레이어 에디터 창 열기 및 sublayer 자동 추가 """
    #     # Open the USD Layer Editor
    #     cmds.mayaUsdLayerEditor()

    #     # Create or use an existing anonymous layer
    #     anonymous_layer = "AnonymousLayer1"
    #     existing_layers = cmds.mayaUsdLayerEditor(query=True, listAnonymousLayers=True) or []

    #     if anonymous_layer not in existing_layers:
    #         # Create a new anonymous layer if it doesn't exist
    #         cmds.mayaUsdLayerEditor(edit=True, addAnonymous=anonymous_layer)
    #         print(f"Created new anonymous layer: {anonymous_layer}")
    #     else:
    #         print(f"Using existing anonymous layer: {anonymous_layer}")

    #     # Iterate through the provided paths
    #     for path in paths:
    #         if not os.path.exists(path):
    #             cmds.warning(f"USD file not found: {path}")
    #             continue

    #         # Reference the USD file into the scene
    #         cmds.file(path, reference=True, type="USD")
    #         print(f"Referenced USD file: {path}")

    #         # Add the referenced USD file as a sublayer to the anonymous layer
    #         cmds.mayaUsdLayerEditor(edit=True, addSubLayer=(anonymous_layer, path))
    #         print(f"Added {path} as sublayer to {anonymous_layer}")

    #     return True

    # def stage_file(self, paths):
    #         """ USD 레이어 에디터 창 열기 및 sublayer 자동 추가"""

    #         cmds.mayaUsdLayerEditor()
    #         for path in paths:
    #             if not os.path.exists(path):
    #                 cmds.warning(f"USD file not found: {path}")
    #                 continue
                    
    #             # USD 파일을 레퍼런스로 추가
    #             cmds.file(path, reference=True, type="USD")

    #             anonymous_layer = "AnonymousLayer1"
    #             existing_layers = cmds.mayaUsdLayerEditor(query=True, listAnonymousLayers=True) or []

    #             if anonymous_layer not in existing_layers:
    #                 cmds.mayaUsdLayerEditor(edit=True, addAnonymous=anonymous_layer)
        
           
    #             cmds.mayaUsdLayerEditor(edit=True, addSubLayer=(anonymous_layer, path))

    #             print(f"Added {path} as sublayer to {anonymous_layer}")





        