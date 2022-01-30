import random
import math

from utils import pass_constants

import os



def single_illuminant(p):
    # p['model'] = {
    #     'grip_flag' : False,
    #     'arrangement': 'single',
    #     'type': 'stl',  # shape, blend, obj, stl
    #     'stl_parameters': {
    #         'directory': 'ben_blobs/test_stls',   # darpa/3d_model?
    #         'rotate': True,
    #         'scale_range': (1, 1.2),
    #         'scale_uniform': True,
    #     },
    # }

    p['model'] = {
        'grip_flag' : False,
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',   # darpa/3d_model?
            'rotate': True,
            'scale_range': (0.35, 0.55),
            'scale_uniform': True,
            'position_range': (-2.5,2.5)
        },
    }

    # p['material'] = {
    #     'type': 'principled',  # ,original,image,color
    #     'principled_parameters': {
    #         'base': 'image',
    #         'image_parameters': {
    #             'directory': 'render_textures/temp_test',
    #         },
    #         # https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html
    #         'subsurface': (0, 0),                    
    #         'metallic': (0, 0),   # No reflections
    #         'specular': (.0, 0),
    #         'specular_tint': (0.0, 0),
    #         'roughness': (0, 1),
    #         'anisotropic': (0, 0),
    #         'anisotropic_rotation': 0.0,
    #         'sheen': (0, 0),
    #         'sheen_tint': (0, 0),
    #         'clearcoat': (0, 0),
    #         'clearcoat_roughness': (0, 0),
    #         'ior': (1.3, 1.3),
    #         'transmission': (0, 0),
    #         'transmission_roughness': (0, 0),
    #     },
    # }

    p['material'] = {
        'type': 'color',  # ,original,image,color
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': (0.1, 0.9),
                'g': (0.1, 0.9),
                'b': (0.1, 0.9)
            },
            'type': ['matte'],
            'roughness': (0, 1)
        }
    }

    # p['background'] = {
    #     'type': 'hdr',
    #     'hdr_parameters': {
    #         'directory': 'hdr',
    #         'strength': 0, # 0.5
    #         'hide_background': True
    #     }
    # }

    paths = ["AI_33", "AI_43", "AI_48", "AI_58"]
    # paths = ["AI_58"]

    blend_files = []

    for path in paths:
        path_c = "/users/aarjun1/scratch/train_data/scenes/" + path
        for root, dirs, files in os.walk(path_c):
            for file in files:
                if file.endswith(".blend") and file.startswith("AI"):
                    temp = "/".join(root.split('/')[-3:])
                    blend_files.append(os.path.join(temp,file))

    print(blend_files)
    print('blend_files len : ', len(blend_files))

    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            # 'files': ['scenes/scene_1/Country-Kitchen.blend', 'scenes/scene_16/Interior.blend', 'scenes/scene_15/gym.blend', \
            #           'scenes/scene_8/quarto01-cycles_2.63.blend', 'scenes/scene_11/main.blend', \
            #           'scenes/scene_12/salon-blanco.blend'], #'scenes/scene_14/perdeler.blend'],
            # 'files': ['scenes/AI_48/AI48_001/AI48_001.blend'], #'scenes/scene_14/perdeler.blend'],
            'files': blend_files,
            'model_position': [[0, 0, 0]],
            'overrides': {
                    'light_color': {
                    'color_type': 'rgb',
                    'color': {
                        'r': (0.1, 0.9),
                        'g': (0.1, 0.9),
                        'b': (0.1, 0.9)
                    },
		            'intensity': (0, 0),
                    'name': 'scene_light'
                }
            }
        }
    }

    p['camera'] = {
        'azimuth_range': [-math.pi,math.pi],#[-math.pi,math.pi],#[0.0,0]
        'altitude_range': [-math.pi,math.pi],#[0.0,0.0],#[-math.pi,math.pi],
        'radius_factor':(0.75,4.0),
        'max_deviation_angle': 0,
        'view_angle': math.pi/2  # (2*math.pi)/3
    }
    p['lights'] = {
        'list': [
            {
                'name': 'light',
                'color_type': 'rgb',
                'color': {
                    # 'r': 1,
                    # 'g': 0,
                    # 'b': 0
                    'r': (0.1, 0.9),
                    'g': (0.1, 0.9),
                    'b': (0.1, 0.9)
                },
                'azimuth_range': [-math.pi,math.pi],
                'altitude_range': [0,math.pi],
                'radius_factor': (0.75, 4.0),
                'size_factor': 1.5,
                'intensity': (100,200)
            },
        ]
    }
    # p['animate'] = {
    #     # TODO document: model only be animated if join:True or one object,
    #     # TODO document if lookat=true, deviation angle will go away, animate numbers are deltas
    #     # TODO 'lights':{},
    #     # TODO 'model': {'position_range': 0,'rotation_range': 0},
    #     # 'camera': {'azimuth': math.pi / 4,
    #     #            'altitude': 0,
    #     #            'radius_factor': -1
    #     #            },
    #     # TODO document can be seconds or frames, for now fps set in blender.py:
    #     # 'seconds': .5,
    #     'frames': 20,
    #     'fps': 15,
    #     #'model': {'mode': 'keyframe',
    #     #          ''
    #     #}

    # }
    p['output'] = {
        'file_types': ['png'],
        # 'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth',
        #            'combined_xyz'],
        'passes': pass_constants.all_passes, #['color'], special_passes useful_passes
        'output_filename': [['index']],
        'resolution': {
            'x': 256,
            'y': 256
        },
        'samples': 600,
        'denoise': True
    }





def single_illuminant_train(p):
    single_illuminant(p)
    p['material']['principled_parameters']['image_parameters']['directory'] = 'textures_train'
    p['background']['hdr_parameters']['directory'] = 'hdr_train'

def single_illuminant_val(p):
    single_illuminant(p)
    p['material']['principled_parameters']['image_parameters']['directory'] = 'textures_val'
    p['background']['hdr_parameters']['directory'] = 'hdr_val'




def multi_illuminant(p):
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
                'directory': 'textures_train',
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
        'number': (2, 5),
        'shared_parameters': {
            'name': 'light',
            'color_type': 'rgb',
            'color': {
                'r': (0.2, 0.8),
                'g': (0.2, 0.8),
                'b': (0.2, 0.8)
            },
            'azimuth_range': [-math.pi/2,math.pi/2],
            'altitude_range': [-math.pi/2,math.pi/2],
            'radius_factor': (1.5,2.0),
            'size_factor': 1.5,
            'intensity': (800,1000)
        },
        
        'list': [
            {    
                'name': 'light_1',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'altitude_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {   
                'name': 'light_2',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {    
                'name': 'light_3',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {    
                'name': 'light_4',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {    
                'name': 'light_5',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
            {    
                'name': 'light_6',
                'color_type': 'rgb',
                'azimuth_range': [-math.pi/3,math.pi/3],
                'color': {
                    'r': (0.2, 0.8),
                    'g': (0.2, 0.8),
                    'b': (0.2, 0.8)
                },
                'altitude_range': [-math.pi/3,math.pi/3],
                'radius_factor': (1.5,2.0),
                'size_factor': 1.5,
                'intensity': (800,1000)
            },
        ]
    }
    p['output'] = {
        'file_types': ['png'],
        'passes': pass_constants.special_passes, #['color'], special_passes useful_passes
        'output_filename': [['index']],
        'resolution': {
            'x': 256,
            'y': 256
        }
    }



def multi_illuminant_train(p):
    multi_illuminant(p)
    p['material']['principled_parameters']['image_parameters']['directory'] = 'textures_train'
    p['background']['hdr_parameters']['directory'] = 'hdr_train'

def multi_illuminant_val(p):
    multi_illuminant(p)
    p['material']['principled_parameters']['image_parameters']['directory'] = 'textures_val'
    p['background']['hdr_parameters']['directory'] = 'hdr_val'

