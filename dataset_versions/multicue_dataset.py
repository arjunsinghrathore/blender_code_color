import random
import math

from utils import pass_constants


def texture_only(p):
    p['model'] = {
        'grip_flag' : True,
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': True,
            'scale_range': (1, 1),
            'scale_uniform': True,
        },
    }
    p['material'] = {
        'type': 'principled',  # ,original,image,color
        'principled_parameters': {
            'base': 'image',
            'image_parameters': {
                'directory': 'textures_sorted',
            },
            'subsurface': 0,
            'metallic': (0.1, 0.9),
            'specular': (.2, .8),
            'specular_tint': (0.0, 1),
            'roughness': (0.2, 0.5),
            'anisotropic': 0.0,
            'anisotropic_rotation': 0.0,
            'sheen': 0.0,
            'sheen_tint': 0.0,
            'clearcoat': 0.0,
            'clearcoat_roughness': 0.0,
            'ior': 1.1,
            'transmission': 0.0,
            'transmission_roughness': 0.0,
        },
    }
    p['background'] = {
        'type': 'hdr',
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': 0.5,
            'hide_background': False
        }
    }
    p['camera'] = {
        'azimuth_range': [-2*math.pi,2*math.pi],
        'altitude_range': [-math.pi,math.pi],
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['lights'] = {
        'list': [
            {
                'color_type': 'rgb',
                'color': {
                    'r': 1,
                    'g': 1,
                    'b': 1
                },
                'azimuth_range': [-2*math.pi,2*math.pi],
                'altitude_range': [-math.pi,math.pi],
                'radius_factor': 2,
                'size_factor': 1.5,
                'intensity': 750
            },
            {
                'color_type': 'rgb',
                'color': {
                    'r': 1,
                    'g': 1,
                    'b': 1
                },
                'azimuth_range': [-2*math.pi,2*math.pi],
                'altitude_range': [-math.pi,math.pi],
                'radius_factor': 1.5,
                'size_factor': 2,
                'intensity': 250
            },
        ]

    }
    p['output'] = {
        'file_types': ['png'], #,'blend'
        'passes': ['color'],
        'output_filename': [['index']],
        'resolution': {
            'x': 224,
            'y': 224
        }
    }


############################################################################


def texture_CC(p):
    p['model'] = {
        'grip_flag' : False,
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': True,
            'scale_range': (1, 1.2),
            'scale_uniform': True,
        },
    }
    p['material'] = {
        'type': 'principled',  # ,original,image,color
        'principled_parameters': {
            'base': 'image',
            'image_parameters': {
                'directory': 'textures_sorted',
            },
            'subsurface': 0,
            'metallic': (0.1, 0.9),
            'specular': (.2, .8),
            'specular_tint': (0.0, 1),
            'roughness': (0.2, 0.5),
            'anisotropic': 0.0,
            'anisotropic_rotation': 0.0,
            'sheen': 0.0,
            'sheen_tint': 0.0,
            'clearcoat': 0.0,
            'clearcoat_roughness': 0.0,
            'ior': 1.1,
            'transmission': 0.0,
            'transmission_roughness': 0.0,
        },
    }
    p['background'] = {
        'type': 'hdr',
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': 0, # 0.5
            'hide_background': True
        }
    }
    p['camera'] = {
        'azimuth_range': [0.0,0.0],#[-2*math.pi,2*math.pi],
        'altitude_range': [0.0,0.0],#[-math.pi,math.pi],
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['lights'] = {
        'list': [
            {
                'color_type': 'rgb',
                'color': {
                    # 'r': 0.4,
                    # 'g': 1,
                    # 'b': 0.5
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'azimuth_range': [-math.pi/3,math.pi/3],
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {
                'color_type': 'rgb',
                'color': {
                    # 'r': 1,
                    # 'g': 0.1,
                    # 'b': 0.6
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'azimuth_range': [-math.pi/3,math.pi/3],
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            # {
            #     'color_type': 'rgb',
            #     'color': {
            #         # 'r': 0.1,
            #         # 'g': 0.7,
            #         # 'b': 0.6
            #         'r': (0.3, 0.8),
            #         'g': (0.3, 0.8),
            #         'b': (0.3, 0.8)
            #     },
            #     'azimuth_range': [-2*math.pi,2*math.pi],
            #     'altitude_range': [-math.pi,math.pi],
            #     'radius_factor': (1.5,4.5),
            #     'size_factor': 2,
            #     'intensity': (200,1000) #500
            # },
        ]
    }
    p['output'] = {
        'file_types': ['png'], #,'blend'
        'passes': pass_constants.special_passes, #['color'], special_passes useful_passes
        'output_filename': [['index']],
        'resolution': {
            'x': 256,
            'y': 256
        }
    }