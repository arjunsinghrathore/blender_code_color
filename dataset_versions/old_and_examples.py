#!/usr/bin/env python

"""
Defines version-specific rendering parameters
"""

from scipy import pi
from utils import pass_constants


# TODO animations/movements/optical flow
# TODO write "modules" for whole param categories, ex. p['camera']=front_half_of_object(radius_factor=2)
# TODO documentation: any param of external files (hdrs, texture, imported blends)
# TODO ^^^can be 'directory':'directory_name' or 'files':['some/list.of','files.in','resources.directory']
def test1(p):
#     p['model'] = {
#         'arrangement': 'single',
#         'type': 'obj',  # shape, blend, obj
#         'obj_parameters': {
#             'directory': 'shapenet/small_test',
#             'rotate': True,
#             'scale_range': (.25, 1),
#             'scale_uniform': False,
#         }
#     }
#     p['lights'] = {
#         'shared_parameters': {
#             'color_type': 'rgb',
#             'color': {
#                 'r': 1,
#                 'g': 1,
#                 'b': 1
#             },
#             'intensity': 400
#         },
#         'list': [
#             {
#                 'azimuth': -pi / 2,
#                 'altitude': -pi / 2,
#                 'radius_factor': 1,
#                 'size_factor': 4,
#             }, {
#                 'azimuth': pi / 2,
#                 'altitude': -pi / 2,
#                 'radius_factor': 1,
#                 'size_factor': 4,
#             }, {
#                 'azimuth': -pi / 2,
#                 'altitude': pi / 2,
#                 'radius_factor': 1,
#                 'size_factor': 4,
#             }, {
#                 'azimuth': pi / 2,
#                 'altitude': pi / 2,
#                 'radius_factor': 1,
#                 'size_factor': 4,
#             }
#         ]
#
#     }
#     p['camera'] = {
#         'azimuth': 0,
#         'altitude': 0,
#         'radius_factor': 2,
#         'max_deviation_angle': 0
#     }
#     p['background'] = {
#         'type': 'color',
#         'color_parameters': {
#             'color_type': 'rgb',
#             'color': {
#                 'r': 0,
#                 'g': 0,
#                 'b': 0
#             },
#         }
#     }
#     p['output'] = {
#         'file_types': ['png', 'h5'],
#         'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth'],
#         'resolution': {
#             'x': 512,
#             'y': 512
#         }
#     }
#     p['grid'] = {
#     }


def test1(p):
    p['model'] = {
        # TODO 'select_first':'model' or 'arrangement'
        'arrangement': ['cluster'],  # single, cluster, grid or random_cube
        'cluster_parameters': {
            'number_of_objects': (1, 7),
            'position_range': (-1, 1),
        },
        'grid_parameters': {
            'grid_dimensions': {
                'x': (2, 3),
                'y': (2, 3),
                'z': (2, 3)
            },
            'grid_spacing': 1,
            'position_range': (-.5, .5),
        },
        'type': 'shape',  # shape, blend, obj
        'shape_parameters': {
            'shapes': ['cube', 'torus', 'cylinder', 'cone', 'meta_cube', 'meta_ball', 'empty'],
            'shape_weights': [1, 1, 1, .5, 1, 2, 4],
            'edge_radius': (0, .5),
            'vertices': 150,
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': True
        }
    }
    p['material'] = {
        'type': ['external', 'image', 'image', 'image', 'color'],  # ,original,image,color
        'external_parameters': {
            'files': 'materials/materials.blend'
        },
        'color_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            'type': ['glossy', 'matte'],
            'roughness': (0, .1)
        },
        'image_parameters': {
            'directory': 'textures_sorted_100',
            'color_type': 'hsl',
            'roughness': (0, .06),
            'glossiness': (.05, .7)
        }
    }
    p['background'] = {
        'type': ['color'],  # TODO maybe make any array weightable?
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': (1, 2)
        },
        'color_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            # 'color_type': 'inv_temp',
            # 'color': (1.0 / 7000.0, 1.0 / 3000.0),
        }
    }
    p['lights'] = {
        'number': (1, 6),
        'list': [
            {
                'color_type': 'rgb',
                'color': {
                    'r': (0, 1),
                    'g': (0, 1),
                    'b': (0, 1)
                },
                'azimuth': (0, 2 * pi),
                'altitude': (0, 2 * pi),
                'radius_factor': (1, 3),
                'size_factor': (2, 20),
                'intensity': (100, 400)
            }, {
                'color_type': 'inv_temp',
                'color': (1.0 / 7000.0, 1.0 / 3000.0),
                'azimuth': (0, 2 * pi),
                'altitude': (0, 2 * pi),
                'radius_factor': (1, 3),
                'size_factor': (2, 20),
                'intensity': (100, 400)
            }
        ]

    }

    p['camera'] = {
        'azimuth': (0, 2 * pi),
        'altitude': (- pi / 3, pi / 3),
        # 'view_angle': (pi / 5, pi / 3),
        'radius_factor': (.75, 1.5),
        'max_deviation_angle': (0, .1)
    }
    p['output'] = {
        'file_types': ['png'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
def test1(p):
    p['model'] = {
        'type': 'generated',
        'parameters': {
            'type': 'cluster',
            'grid_dimensions': {
                'x': 3,
                'y': 3,
                'z': 3
            },
            'grid_spacing': 1,
            'number_of_objects': (3, 4),
            'shapes': ['cube', 'torus', 'meta_ball'],
            'shape_weights': [1, 1, 2],
            'edge_radius': (0, .5),
            'vertices': 150,
            # TODO : join shapes=false breaks gridding, breaks condition storing
            'join_shapes': True,
            # TODO : document params of the format {param}_range must be tuple for now, as they are calc'd on the blender side
            # TODO : calc param_range values on the blender_manager side
            'position_range': (-.5, .5),
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': True
        }
    }
    p['material'] = {
        'type': 'image',
        'parameters': {
            'directory': 'textures_sorted_100',
            'type': ['glossy'],
            'color': {
                'h': (0, 1),
                's': 1,
                'l': .5
            },
            'roughness': (0, .06),
            'glossiness': .25
        }
    }
    p['lights'] = [{
        'color_type': 'temp',
        'color': {
            'h': (0, 1),
            's': 1,
            'l': .5
        },
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': 3,
        'size_factor': 3,
        'intensity': 300
    }]
    p['background'] = {
        'type': 'hdr',
        'parameters': {
            'directory': 'hdr',
            'strength': (.5, 2)
        }
    }
    p['camera'] = {
        'azimuth': pi / 4,
        'altitude': (0, 2),
        'radius_factor': 2,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
        # 'type': 'stereo'
    }
    p['animate'] = {
        # TODO document: model only be animated if join:True or one object,
        # TODO document if lookat=true, deviation angle will go away, animate numbers are deltas
        # TODO 'lights':{},
        # TODO 'model': {'position_range': 0,'rotation_range': 0},
        'camera': {'azimuth': pi / 2,
                   'altitude': 0,
                   'radius_factor': -1
                   },
        # TODO document can be seconds or frames, for now fps set in blender.py:
        # 'seconds': .5,
        'frames': 5

    }
    p['output'] = {
        'file_types': ['blend', 'png', 'exr', 'h5'],  # TODO, 'h5' w anim broken,
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('material', 'parameters', 'directory'): 2,
        ('background', 'parameters', 'strength'): 3,
        ('camera', 'altitude'): 3
    }


def test2(p):
    p['model'] = {
        # TODO 'select_first':'model' or 'arrangement'
        'arrangement': 'random_cube',  # single, cluster, grid or random_cube
        'cluster_parameters': {
            'number_of_objects': (3, 4),
            'position_range': (-.5, .5),
        },
        'grid_parameters': {
            'grid_dimensions': {
                'x': 3,
                'y': 3,
                'z': 3
            },
            'grid_spacing': 1,
            'position_range': (-.5, .5),
        },
        'random_cube_parameters': {
            'cube_dimensions': {
                'x': (0, 3),
                'y': (0, 3),
                'z': (0, 3)
            },
            'number_of_objects': (3, 4),
        },
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': 'train',
            'rotate': True,
            'scale_range': (.25, 1),
            'scale_uniform': False,
        }
    }
    #
    # p['model'] = {
    #     'type': 'external',
    #     'parameters': {
    #         'directory': 'train',
    #         'rotate': True,
    #         # 'scale_range': (.25, 1)
    #         # 'position_range': (-.1,.1)
    #     }
    # }
    #
    # p['model'] = {
    #     'type': 'generated',
    #     'parameters': {
    #         'type': 'cluster',
    #         'grid_dimensions': {
    #             'x': 3,
    #             'y': 3,
    #             'z': 3
    #         },
    #         'grid_spacing': 1,
    #         'number_of_objects': (3, 4),
    #         'shapes': ['cube', 'torus', 'meta_ball'],
    #         'shape_weights': [1, 1, 2],
    #         'edge_radius': (0, .5),
    #         'vertices': 150,
    #         # TODO : join shapes=false breaks gridding, breaks condition storing
    #         'join_shapes': True,
    #         # TODO : document params of the format {param}_range must be tuple for now, as they are calc'd on the blender side
    #         # TODO : calc param_range values on the blender_manager side
    #         'position_range': (-.5, .5),
    #         'scale_uniform': False,
    #         'scale_range': (.25, 1),
    #         'rotate': True
    #     }
    # }
    p['material'] = {
        'type': 'external',  # (master_file),original,image,color
        'parameters': {
            'files': 'materials/materials.blend'
        }
        # 'parameters': {
        #     'color_type': 'hsl',
        #     'color': {
        #         'h': (0, 1),
        #         's': (0, 1),
        #         'l': .5
        #     },
        #     'type': 'glossy',
        #     'roughness': (0, .1)
        # }
    }
    p['background'] = {
        'type': 'hdr',
        'parameters': {
            'directory': 'hdr',
            'strength': (1, 2)
        }
    }
    p['lights'] = [
        # {
        #     'color_type': 'rgb',
        #     'color': {
        #         'r': 1,
        #         'g': 1,
        #         'b': 0
        #     },
        #     'azimuth': (0, 2 * pi),
        #     'altitude': (0, 2 * pi),
        #     'radius_factor': 1,
        #     'size_factor': 10,
        #     'intensity': (100, 400)
        # }, {
        #     'color_type': 'rgb',
        #     'color': {
        #         'r': 1,
        #         'g': 1,
        #         'b': 0
        #     },
        #     'azimuth': (0, 2 * pi),
        #     'altitude': (0, 2 * pi),
        #     'radius_factor': 1,
        #     'size_factor': 10,
        #     'intensity': (100, 400)
        # }
    ]
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 2,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['h5', 'blend', 'png'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 300
        }
    }


def test3(p):
    p['model'] = {
        'type': 'generated',
        'parameters': {
            # 'directory': 'train',
            'type': ['cluster', 'grid'],
            'grid_dimensions': {
                'x': 3,
                'y': 3,
                'z': 3
            },
            'grid_spacing': (.5, 2),
            'number_of_objects': (2, 5),
            'shapes': ['cube', 'torus', 'meta_ball', 'meta_capsule'],
            'shape_weights': [1, 1, 1, 1],
            'edge_radius': (0, .5),
            'vertices': 150,
            # TODO : document join shapes false breaks gridding, breaks condition storing
            'join_shapes': True,
            'position_range': (-.5, .5),
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': True
        }
    }
    p['material'] = {
        'type': ['image'],  # ,'color'],
        'parameters': {
            'directory': 'mattes_textures',
            'type': ['glossy'],
            'color': {
                'h': (0, 1),
                's': 1,
                'l': .5
            },
            'color_type': 'hsl',
            'roughness': (0, .06),
            'glossiness': (.05, .7)
        }
    }
    p['lights'] = [{
        'color_type': 'hsl',
        'color': {
            'h': (0, 1),
            's': 1,
            'l': .5
        },
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': 3,
        'size_factor': 3,
        'intensity': (0, 600)
    }, {
        'color_type': 'hsl',
        'color': {
            'h': (0, 1),
            's': 1,
            'l': .5
        },
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': 3,
        'size_factor': 3,
        'intensity': (0, 600)
    }, {
        'color_type': 'hsl',
        'color': {
            'h': (0, 1),
            's': 1,
            'l': .5
        },
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': 3,
        'size_factor': 3,
        'intensity': (0, 600)
    }, {
        'color_type': 'hsl',
        'color': {
            'h': (0, 1),
            's': 1,
            'l': .5
        },
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': 3,
        'size_factor': 3,
        'intensity': (0, 600)
    }]
    p['background'] = {
        # 'type': 'hdr',
        # 'parameters': {
        #     'directory': 'hdr',
        #     'strength': (.75, 1.75)
        # }
        'type': 'color',
        'parameters': {
            'color_type': 'hsl',
            'color': {
                'h': 0,
                's': 0,
                'l': .25
            },

        }
    }
    p['camera'] = {
        'azimuth': (0, 2 * pi),
        'altitude': (-1, 1),
        'radius_factor': (.6, 1.5),
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
        # 'type': 'stereo'
    }
    p['animate'] = {
        # 'camera': {'azimuth': pi / 2,
        #            'altitude': 0,
        #            'radius_factor': -1
        #            },
        # 'seconds': .5,
        # 'frames':24
    }
    p['output'] = {
        'file_types': ['png', 'blend'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 2880,
            'y': 1800
        }
    }
    p['grid'] = {
        # ('material', 'parameters', 'directory'): 2,
        # ('background', 'parameters', 'strength'): 3,
        # ('camera', 'altitude'): 3
    }


def model(p):
    p['model'] = {
        'type': 'generated',
        'parameters': {
            'type': 'cluster',
            'number_of_objects': (5, 9),
            'shapes': ['cube', 'torus', 'meta_ball', 'meta_cube', 'sphere'],
            'weights': [1, .5, 1.5, 1, .75],
            'edge_radius': (.05, .5),
            'vertices': 150,
            # TODO : document join shapes false breaks gridding, breaks condition storing
            'join_shapes': True,
            # Todo : document range must be tuple
            'position_range': (-1.5, 1.5),
            'scale_uniform': False,
            'scale_range': (.5, 1),
            'rotate': True
        }
    }
    p['output'] = {
        'file_types': ['blend'],
        'passes': pass_constants.useful_passes
    }


def demo(p):
    p['model'] = {
        'type': 'external',
        'parameters': {
            # 'files': 'demo_chimera/generated.time.1515095885.72.pid.5083.node.g12.blend',
            'directory': 'demo_chimera',
            'rotate': False,
            # 'scale_range': (.25, 1)
            # 'position_range': (-.1,.1)
        }
    }
    p['material'] = {
        # 'type': 'external',
        # 'parameters': {
        #     'files': 'materials/materials.blend'
        # }
        'type': 'color',
        'parameters': {
            'color_type': 'hsl',
            'color': {
                'h': .5,
                's': .95,
                'l': .5
            },
            'type': 'glossy',
            'roughness': .025
        }
        # 'parameters': {
        #     'color_type': 'hsl',
        #     'color': {
        #         'h': (0, 1),
        #         's': (0, 1),
        #         'l': .5
        #     },
        #     'type': 'glossy',
        #     'roughness': (0, .1)
        # }
    }
    p['lights'] = [
        #     {
        #     'color_type': 'inv_temp',
        #     'color': 1.0/4800.0,
        #     'azimuth': pi/4,
        #     'altitude': .5,
        #     'radius_factor': 3,
        #     'size_factor': 3,
        #     'intensity': 500
        # }
    ]
    p['background'] = {
        'type': 'hdr',
        'parameters': {
            'files': 'hdr/10-Shiodome_Stairs_3k.hdr',
            # 'directory': 'hdr',
            # 'strength': (0.1,3)
            'strength': 1
        }
        # 'type': 'color',
        # 'parameters': {
        #     'color_type': 'hsl',
        #     'color': {
        #         'h': 0,
        #         's': 0,
        #         'l': .25
        #     },
        #
        # }
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
        # 'type': 'stereo'
    }
    p['output'] = {
        'file_types': ['png', 'tfrecords'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        # ('material', 'parameters', 'directory'): 2,
        # ('background', 'parameters', 'strength'): 8,
        # ('camera', 'radius_factor'): 4
    }
def test1(p):
    p['model'] = {
        # TODO 'select_first':'model' or 'arrangement'
        'arrangement': 'cluster',  # single, cluster, grid or random_cube
        'cluster_parameters': {
            'number_of_objects': (2, 7),
            'position_range': (-1, 1),
        },
        'type': 'shape',  # shape, blend, obj
        'shape_parameters': {
            'shapes': ['cube', 'torus', 'cylinder', 'cone', 'meta_cube', 'meta_ball', 'empty'],
            'shape_weights': [1, 1, 1, .5, 1, 2, 4],
            'edge_radius': (0, .5),
            'vertices': 150,
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': True
        }
    }
    p['material'] = {
        'type': ['external', 'image', 'image', 'image', 'color'],  # ,original,image,color
        'external_parameters': {
            'files': 'materials/materials.blend'
        },
        'color_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            'type': ['glossy', 'matte'],
            'roughness': (0, .07)
        },
        'image_parameters': {
            'directory': 'textures_sorted',
            'color_type': 'hsl',
            'roughness': (0, .06),
            'glossiness': (.05, .7)
        }
    }
    p['background'] = {
        'type': 'hdr',  # TODO maybe make any array weightable?
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': (1, 2)
        }
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['blend', 'png'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 512
        }
    }

def bigrange1(p):
    p['model'] = {
        'arrangement': ['cluster', 'grid'],  # single, cluster, grid or random_cube
        'cluster_parameters': {
            'number_of_objects': (1, 7),
            'position_range': (-1, 1),
        },
        'grid_parameters': {
            'grid_dimensions': {
                'x': (2, 3),
                'y': (2, 3),
                'z': (2, 3)
            },
            'grid_spacing': 1,
            'position_range': (-.5, .5),
        },
        'type': 'shape',  # shape, blend, obj
        'shape_parameters': {
            'shapes': ['cube', 'torus', 'cylinder', 'cone', 'meta_cube', 'meta_ball', 'empty'],
            'shape_weights': [1, 1, 1, .5, 1, 2, 4],
            'edge_radius': (0, .5),
            'vertices': 150,
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': True
        }
    }
    p['material'] = {
        'type': ['external', 'image', 'image', 'image', 'color'],  # ,original,image,color
        'external_parameters': {
            'files': 'materials/materials.blend'
        },
        'color_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            'type': ['glossy', 'matte'],
            'roughness': (0, .1)
        },
        'image_parameters': {
            'directory': 'textures_sorted_100',
            'color_type': 'hsl',
            'roughness': (0, .06),
            'glossiness': (.05, .7)
        }
    }
    p['background'] = {
        'type': ['hdr', 'hdr', 'hdr', 'hdr', 'color'],  # todo maybe make any array weightable?
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': (1, 2)
        },
        'color_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            # 'color_type': 'inv_temp',
            # 'color': (1.0 / 7000.0, 1.0 / 3000.0),
        }
    }
    p['lights'] = {
        'number': (0, 6),
        'list': [
            {
                'color_type': 'rgb',
                'color': {
                    'r': (0, 1),
                    'g': (0, 1),
                    'b': (0, 1)
                },
                'azimuth': (0, 2 * pi),
                'altitude': (0, 2 * pi),
                'radius_factor': (1, 3),
                'size_factor': (2, 20),
                'intensity': (100, 400)
            }, {
                'color_type': 'inv_temp',
                'color': (1.0 / 7000.0, 1.0 / 3000.0),
                'azimuth': (0, 2 * pi),
                'altitude': (0, 2 * pi),
                'radius_factor': (1, 3),
                'size_factor': (2, 20),
                'intensity': (100, 400)
            }
        ]

    }

    p['camera'] = {
        'azimuth': (0, 2 * pi),
        'altitude': (- pi / 3, pi / 3),
        # 'view_angle': (pi / 5, pi / 3),
        'radius_factor': (.75, 1.5),
        'max_deviation_angle': (0, .1)
    }
    p['output'] = {
        'file_types': ['png'],
        'passes': pass_constants.useful_passes,
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
