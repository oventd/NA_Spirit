import maya.cmds as cmds
import sys
path = '/nas/sam/git'
sys.path.append(path)

import turnaround_playblast_generator

tap = turnaround_playblast_generator.TurnAroundPlayblastGenerator()
path = "/home/rapa/비디오/test.mov"
tap.create_turnaround_playblast(path=path)