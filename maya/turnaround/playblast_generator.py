import maya.cmds as cmds
import maya.mel as mel

class PlayblastGenerator:
    """
    플레이블라스트를 만드는 클래스
    """

    def __init__(self):
        self._playblast_options = {
            'startTime':0,
            'endTime':0,
            'format': 'qt',
            'filename': "",
            'forceOverwrite': True,
            'sequenceTime': 0,
            'clearCache': True,
            'viewer': False,
            'showOrnaments': False,
            'offScreen': True,
            'fp': 4,  # Frame padding
            'percent': 100,
            'compression': 'none',
            'quality': 100,
            'widthHeight': (1280, 720),
        }        
    
    def get_path(self):
        # playblast path 가져오기
        return self._playblast_options['filename'] 
    
    def set_path(self, path):
        # playblast path 설정
        self._playblast_options['filename'] = path

    def get_options(self):
        # playblast options 가져오기
        return self._playblast_options
        
    def set_options(self, options):
        # playblast options 설정
        self._playblast_options = options

    def get_resolution(self):
        # playblast 해상도 가져오기
        return self._playblast_options['widthHeight']

    def set_resolution(self, width, height):
        # playblast 해상도 설정
        self._playblast_options['widthHeight'] = (width, height)
    
    def get_frame_range(self):
        # 프레임레인지 가져오기
        return self._playblast_options['startTime'], self._playblast_options['endTime']

    def set_frame_range(self, first_frame, last_frame):
        # 프레임레인지 설정
        self._playblast_options['startTime'] = first_frame
        self._playblast_options['endTime'] = last_frame
    
    def get_persp_camera(self):
        """
        maya의 viewport의 persp view에 현재 사용중인 카메라를 찾아오는 함수
        """
        try:
            camera = cmds.modelPanel('modelPanel4', query=True, camera=True)
            return camera
        except:
            print('AnimCam not found')
            return None

    def set_persp_camera(self, camera):
        """
        maya의 viewport의 persp view에 camera를 설정하는 함수
        camera: persp view에 설정하고 싶은 카메라 이름 str
        """
        try:
            mel.eval('setNamedPanelLayout "Single Perspective View"')
            cmds.lookThru(camera, "modelPanel4") 
        except:
            print('AnimCam not found')
            return

    def playblast(self, path=None,first_frame=None,last_frame=None):
        """
        playblast를 path에 만들어주는 함수
        """
        if first_frame:
            self._playblast_options['startTime'] = first_frame
        if last_frame:
            self._playblast_options['endTime'] = last_frame
        if path:
            self._playblast_options['filename'] = path
        # 현재 프레임 가져오기
        current_frame = cmds.currentTime(query=True)
        # playblast 생성
        cmds.playblast(**self._playblast_options)
        # 기존 프레임으로 바꾸기
        cmds.currentTime(current_frame)
        print(f'playblast completed {current_frame}')
