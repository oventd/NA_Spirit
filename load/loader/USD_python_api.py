from pxr import Usd
import maya.mel as mel
import maya.cmds as cmds
import os
import sys

# 커스텀 로더 모듈 추가
sys.path.append('/home/rapa/NA_Spirit/load/loader')
import Loader

class MayaLoader(Loader.Loader):
    def import_file(self, paths):
        """USD 파일을 마야에 임포트"""
        for path in paths:
            if not os.path.exists(path):
                cmds.warning(f"USD file not found: {path}")
                continue
            
            try:
                cmds.file(path, i=True, type="USD Import")
            except Exception as e:
                cmds.warning(f"Failed to import USD file {path}: {str(e)}")
                return False
        return True

    def reference_file(self, paths):
        """USD 파일을 마야에 레퍼런스로 추가"""
        try:
            cmds.file(new=True, force=True)
            for path in paths:
                if os.path.exists(path):
                    cmds.file(path, reference=True)
                else:
                    cmds.warning(f"USD file not found: {path}")
        except Exception as e:
            cmds.warning(f"Failed to reference USD file {path}: {str(e)}")
        return True

    def create_usd_proxy_node(self, usd_file_path):
        """USD Proxy 노드를 생성하고 USD 파일을 로드"""
        if not os.path.exists(usd_file_path):
            cmds.warning(f"USD file not found: {usd_file_path}")
            return None

        # USD 프록시 노드 생성
        proxy_node = cmds.createNode("mayaUsdProxyShape", name="USD_Proxy")
        cmds.setAttr(f"{proxy_node}.filePath", usd_file_path, type="string")

        # 뷰포트 갱신을 위해 인뷰 메시지 출력
        cmds.inViewMessage(amg=f'<hl>USD Proxy Created:</hl> {usd_file_path}', pos='topCenter', fade=True)
        
        return proxy_node

    def stage_file(self, paths):
        """마야에서 USD 프록시를 생성하고 파일을 로드"""
        if not paths:
            cmds.warning("No USD files provided!")
            return False
        
        for path in paths:
            self.create_usd_proxy_node(path)
        
        return True

# 로더 실행
loader = MayaLoader()
paths = ["/home/rapa/3D_usd/Kitchen_set/assets/IronBoard/IronBoard.usd"]

result = loader.stage_file(paths)
