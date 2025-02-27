import maya.mel as mel
import maya.cmds as cmds
import os
import uuid


class MayaLoader:
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
            for path in paths:
                if not os.path.exists(path):
                    cmds.warning(f"USD file not found: {path}")
                    continue

                cmds.file(path, reference=True, type = "USD Import") # 아무리생각해도 이쌔끼 때문임 

                path = path.replace("\\", "/")

                stage_nodes = cmds.ls(type = "mayaUsdProxyShape")
                if not stage_nodes:
                    print (" No stage nodes found")
                    mel.eval('mayaUsdCreateStageWithNewLayer;')
                    stage_nodes = cmds.ls(type = "mayaUsdProxyShape")
                else: 
                    print(f"{stage_nodes} already exist")
                    return False
                
                stage_name = stage_nodes[0]
                print(f"stage name is {stage_name}")

                cmds.mayaUsdLayerEditorWindow()

                root_layer = cmds.getAttr(f"{stage_name}")

                if not root_layer:
                    cmds.warning("Root layer not found")
                    return False

                print(f"root layer is {root_layer}")

                unique_layer_name = f"anon_{uuid.uuid4().hex[:8]}"
                # mel.eval(f'mayaUsdLayerEditor -edit -addAnonymous "{root_layer}" "{path}" ;')
                mel.eval(f'mayaUsdLayerEditor -edit -insertSubPath "{[root_layer]}" "{stage_name}" ;')

                print(f"Successfully added {paths} as sublayer in {stage_name}")
                    
        except Exception as e:
            cmds.warning(f"Failed to add sublayer: {str(e)}")
            return False
        return True


loader = MayaLoader()
paths = ["/home/rapa/3D_usd/Kitchen_set/assets/IronBoard/IronBoard.usd"]

result = loader.stage_file(paths)


# usd 데이터는 생성되었으나 editor layer에 추가되지 않는 문제 발생 