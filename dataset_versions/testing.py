#!/usr/bin/env python

"""
Defines version-specific rendering parameters
"""

from scipy import pi
from utils import pass_constants
from .constancy import *
from .other import *
from .ben import *


# TODO animations/movements/optical flow
# TODO write "modules" for whole param categories, ex. p['camera']=front_half_of_object(radius_factor=2)
# TODO documentation: any param of external files (hdrs, texture, imported blends)
# TODO ^^^can be 'directory':'directory_name' or 'files':['some/list.of','files.in','resources.directory']
# TODO better version management
# TODO TODO TODO check on azimuth altitude negative vals and altitude units
# TODO document scene model position must be list of lists
# TODO more scene overrides, lights on off, background, material

def test1(p):
    constancy_distance_scene_1(p)
    p['output']['file_types'] = ['png']
    p['grid'][('camera', 'radius_factor')] = 10


def test2(p):
    constancy_lightsat_scene_white_1(p)
    p['output']['file_types'] = ['png']
    p['grid'][('background', 'scene_parameters', 'overrides', 'light_color', 'color', 's')] = 10


def test3(p):
    constancy_lightcolor_scene_2(p)
    p['output']['file_types'] = ['png']
    p['grid'][('background', 'scene_parameters', 'overrides', 'light_color', 'color', 'h')] = 10


def test4(p):
    constancy_lightcolor_scene_white_1(p)
    p['output']['file_types'] = ['png']
    p['grid'][('background', 'scene_parameters', 'overrides', 'light_color', 'color', 'h')] = 10

#Test Procedural Rotation
def test5(p):
    ben_ccv_lambert_1(p)
    p['animate'] = {}
    p['animate']['model'] = {}
    p['animate']['frames'] = 480
    p['animate']['fps'] = 30
    p['animate']['model']['position_range'] = 0
    p['animate']['model']['rotation_range'] = 5
    p['animate']['model']['num_stages'] = 8
    p['animate']['model']['mode'] = 'range'
    p['output']['file_types'] = ['avi_raw']

#Test Keyframe Specified Rotation
def test6(p):
    ben_ccv_lambert_1(p)
    p['animate'] = {}
    p['animate']['model'] = {}
    p['animate']['frames'] = 60
    p['animate']['fps'] = 30
    p['animate']['model']['mode'] = 'keyframe'
    p['animate']['model']['keyframes'] = {
        '0' : {
            "position" : (0,0,0),
            "rotation" : (0,0,0)
        },
        '60' : {
            "position" : (0,0,0),
            "rotation" : (0,0,6)
        }
    }
    p['output']['file_types'] = ['avi_raw']

#Test Modification Script for Marking Grip Points
def test7(p):
    test5(p)
    p['model']['grip_flag'] = True
    p['background'] = {
        'type': 'hdr',
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': 1.5,
            'hide_background': False
        }
    }