import os

class SgPathUtils:
    """Shotgun과 관련된 경로 유틸리티 클래스."""

    @staticmethod
    def make_entity_file_path(
        root_path: str,
        entity_type: str,
        category: str,
        entity: str,
        step: str = None,
        version: str = None,
        dcc: str = None,
        file: str = None
    ) -> str:
        """
        파일 경로를 생성합니다.

        :param  root_path (str): 루트 경로.
        :param  entity_type (str): 엔티티 유형 (예: 'assets' 또는 'sequences').
        :param  category (str): 카테고리 (예: 캐릭터, 소품 등).
        :param  entity (str): 엔티티 이름.
        :param  step (str, optional): 작업 단계 (예: 'Model', 'Rig', 'Anim'). Defaults to None.
        :param  version (str, optional): 버전 정보 (예: 'v001'). Defaults to None.
        :param  dcc (str, optional): 사용 DCC (예: 'maya', 'houdini'). Defaults to None.
        :param  file (str, optional): 파일 이름. Defaults to None.

        :return: str 생성된 파일 경로.
        """
        path_parts = [entity_type, category, entity]
        
        if step is not None:
            path_parts.append(step)
        if version is not None:
            path_parts.append(version)
        if dcc is not None:
            path_parts.append(dcc)
        if file is not None:
            path_parts.append(file)

        return os.path.join(root_path, *path_parts)

    @staticmethod
    def get_entity_type(path: str) -> str:
        """
        경로에서 entity_type을 판별합니다.

        :param  path:(str) 파일 또는 폴더 경로.

        :return: (str) 'sequences' 또는 'assets' 중 하나. 일치하는 것이 없으면 None.
        """
        if 'sequences' in path:
            return 'sequences'
        elif 'assets' in path:
            return 'assets'
        return None
