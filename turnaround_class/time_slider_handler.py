import maya.cmds as cmds
import maya.mel as mel

class TimeSliderHandler:
    """
    maya의 아래에 있는 타임슬라이더와 플레이백을 조정하는 클래스
    """
    def get_current_playback_range(self):
        """
        현재 사용자가 설정한 playback 즉, 안쪽 프레임 레인지를 정보를 가져오는 메서드
        """
        return cmds.playbackOptions(q=True, min=True), \
                cmds.playbackOptions(q=True, max=True)
       
    def get_current_timeslider_range(self):
        """
        현재 사용자가 설정한 timeslider 즉, 바깥쪽 프레임 레인지를 정보를 가져오는 메서드
        """
        return cmds.playbackOptions(query=True, animationStartTime=True), \
                cmds.playbackOptions(query=True, animationEndTime=True)

    def set_timeslider(self,playback_start, playback_end,timeslider_start=None,timeslider_end=None):
        """
        timeslider와 playback을 설정하는 메서드
        """
        if  timeslider_start or timeslider_end:
            cmds.playbackOptions(animationStartTime=timeslider_start, \
                                animationEndTime=timeslider_end)
            cmds.playbackOptions(minTime=playback_start, maxTime=playback_end)
        