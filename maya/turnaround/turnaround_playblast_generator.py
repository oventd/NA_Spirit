import maya.cmds as cmds
import maya.mel as mel
import sys
import playblast_generator

class TurnAroundPlayblastGenerator(playblast_generator.PlayblastGenerator):
    """
    playblast generator 클래스를 상속받아
    카메라를 생성하고, 턴어라운드 플레이블라스트를 생성하는 클래스
    """
    def __init__(self):
        super().__init__()
        self.__turnaround_cam = "publish_turnaround_cam#" # 턴어라운드 카메라 이름
        self.__turnaround_cam_group = "publish_turnaround_cam_group"   # 턴어라운드 카메라 그룹 이름
        self.user_cammera_name = "" # 유저가 사용하고 있는 기존 persp 뷰의 카메라 이름
        self.__offset_pos = {
            # 턴어라운드 카메라의 초기 위치
            "translateX" : 0,
            "translateY" : 12,
            "translateZ" : 70,
            "rotateX" : 0,
            "rotateY" : 0,
            "rotateZ" : 0
            }
        # 기본 프레임레인지 : 1 ~ 120
        self.set_frame_range(1, 120)
        self._path = ""

    def get_offset_pos(self):
        # 턴어라운드 카메라의 초기 위치를 가져오는 메서드
        return self.__offset_pos
        
    def set_offset_pos(self, tx=None, ty=None, tz=None, rx=None, ry=None, rz=None):
        """
        턴어라운드 카메라의 초기 위치를 설정하는 메서드
        """
        # 입력을 안한 입력변수는 기존 값을 사용
        tx = self.__offset_pos["translateX"] if tx is None else tx
        ty = self.__offset_pos["translateY"] if ty is None else ty
        tz = self.__offset_pos["translateZ"] if tz is None else tz
        rx = self.__offset_pos["rotateX"] if rx is None else rx
        ry = self.__offset_pos["rotateY"] if ry is None else ry
        rz = self.__offset_pos["rotateZ"] if rz is None else rz

        # 턴어라운드 카메라의 초기 위치를 설정
        self.__offset_pos = {
            "translateX": tx,
            "translateY": ty,
            "translateZ": tz,
            "rotateX": rx,
            "rotateY": ry,
            "rotateZ": rz
        }

    def create_turnaround_camera(self):
        """
        턴어라운드 카메라를 생성하는 메서드
        """
        # 카메라 생성
        self.__turnaround_cam = cmds.camera(name=self.__turnaround_cam)[0]

        # 카메라 위치 설정
        for key, value in self.__offset_pos.items():
            cmds.setAttr(f"{self.__turnaround_cam}.{key}", value)

        # 카메라 오프셋 그룹 생성
        cmds.select(cl=True)
        self.__turnaround_cam_group = cmds.group(name=self.__turnaround_cam_group,em=True)
        cmds.parent(self.__turnaround_cam,self.__turnaround_cam_group)

        # 카메라 그룹에 에니메이션 설정
        cmds.setKeyframe(self.__turnaround_cam_group, attribute="rotateY", value=0, time=1)
        cmds.setKeyframe(self.__turnaround_cam_group, attribute="rotateY", value=360, time=120)
        cmds.selectKey(self.__turnaround_cam_group, time=(1, 120), attribute="rotateY")
        cmds.keyTangent(inTangentType="linear", outTangentType="linear")

    def delete_camera(self):
        """
        만든 턴어라운드 카메라를 삭제하는 메서드
        """
        # 카메라 삭제
        wildcard = f"{self.__turnaround_cam}*"
        if cmds.objExists(wildcard):
            cmds.delete(wildcard)

        # 카메라 그룹 삭제
        wildcard = f"{self.__turnaround_cam_group}*"
        if cmds.objExists(wildcard):
            cmds.delete(wildcard)

    def create_turnaround_playblast(self, path=None,start_frame=None,end_frame=None):
        """
        턴어라운드 카메라 playblast 생성하는 메서드
        return: 생성된 mov 파일의 path
        """
        # path 설정
        if path:
            self.set_path(path)
        # 프레임레인지 설정
        if start_frame:
            self._playblast_options['startTime'] = start_frame
        if end_frame:
            self._playblast_options['endTime'] = end_frame
        
        # 유저가 사용하고 있는 persp 뷰의 카메라를 찾아아 저장함
        self.user_cammera_name = self.get_persp_camera()
        
        # 턴어라운드 카메라 생성
        self.create_turnaround_camera()

        # 턴어라운드 카메라를 persp 뷰에 설정
        self.set_persp_camera(self.__turnaround_cam)

        self.run()

    def run(self):

        # 프레임레인지 설정
        first_frame = self._playblast_options['startTime']
        last_frame = self._playblast_options['endTime']-1

        # Playblast 생성
        self.playblast(self._path, first_frame, last_frame)

        # 턴어라운드 카메라 삭제
        self.delete_camera()

        return self._path


if __name__ == "__main__":
    import sys
    path = '/home/rapa/NA_Spirit/maya/turnaround'
    sys.path.append(path)
    

    import turnaround_playblast_generator
    import imp
    imp.reload(turnaround_playblast_generator)
    tap = turnaround_playblast_generator.TurnAroundPlayblastGenerator()
    
    path = "/home/rapa/비디오/test.mov"
    tap.create_turnaround_playblast(path=path)
    tap.run()