import maya.mel as mel
import maya.cmds as cmds
import os

import sys 
sys.path.append('/home/rapa/NA_Spirit/load/loader')
import Loader

#파일이름.클래스선언

class MayaLoader(Loader.Loader):
    def import_file(self, paths):
        
        for path in paths: 
            if not os.path.exists(path):
                cmds.warning(f"USD file not found: {path}")
                continue
            
            try: 
                cmds.file(path, i=True, type = "USD Import")
            except Exception as e:
                cmds.warning(f"Failed to import USD file{path}: {str(e)}")
                return False
        return True
    

    def reference_file(self, paths):
        try:
            cmds.file(new=True, force=True)

            for path in paths:
                if not os.path.exists(path):
                    cmds.file(path, reference = True) 
                    continue
                cmds.file(path, reference = True)
        except Exception as e:
            cmds.warning(f"Failed to reference USD file{path}: {str(e)}")
            print("hidfsa")
        return True
    

    def stage_file(self, paths):
        try:
            stages = cmds.ls(type="USD")
            if not stages:
                cmds.warning("No USD stages found in the scene.")
                return False
            

            current_stage = stages[0]
            print(current_stage)


            for path in paths:
                if not os.path.exists(path):
                    cmds.warning(f"USD file not found: {path}")
                    continue

                # cmds.file(path, reference=True, type = "USD Import")
                
                path = path.replace("\\", "/")

                cmds.mayaUsdLayerEditorWindow()

                base_name = os.path.splitext(os.path.basename(path))[0]
                stage_layer_name = f"Layer_{base_name}"
                ref_layer_name = paths[0]

                # if not mel.eval(f"mayaUsdLayerEditor -edit {layer_name};"):
                #     mel.eval(f"mayaUsdLayerEditor -new {layer_name};")

                # mel.eval('mayaUsdCreateStageWithNewLayer;') # 만약 잇으면 서브에 추가, 없으면 새스테이지 생성 함수 하기 
                mel.eval(f'mayaUsdLayerEditor -edit -addAnonymous "{stage_layer_name}" ;')
                mel.eval(f'mayaUsdLayerEditor -edit -insertSubPath 0 "{current_stage}" "{ref_layer_name}";')
                # mel.eval(f'mayaUsdLayerEditor -edit -addSubLayer "{stage_layer_name}" "{ref_layer_name}";')
                
                print(f"Successfully added {path} as sublayer in {current_stage}")
                    
        except Exception as e:
            cmds.warning(f"Failed to add sublayer: {str(e)}")
            return False
        return True


loader = MayaLoader()
paths = ["/home/rapa/3D_usd/Kitchen_set/assets/Refridgerator/Refridgerator.usd"]

result = loader.stage_file(paths)


# usd 데이터는 생성되었으나 editor layer에 추가되지 않는 문제 발생 