from scipy import pi
from utils import pass_constants


def constancymodels1(p):
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


def constancy_distance_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'import_everything': True,
        }
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': (.75, 2),
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'z', 'normal', 'disparity', 'object_index', 'shallow_z'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('camera', 'radius_factor'): 20
    }


def constancy_lightcolor_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'import_everything': True,
        }
    }
    p['lights'] = {
        'shared_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0.0, 1.0),
                's': 1,
                'l': .5
            },
            'intensity': 400
        },
        'list': [
            {
                'azimuth': -pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': -pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }
        ]

    }
    p['background'] = {
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 0,
                'g': 0,
                'b': 0
            },
        }
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('lights', 'shared_parameters', 'color', 'h'): 20
    }


def constancy_lightcolor_bg_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'import_everything': True,
        }
    }
    p['lights'] = {
        'shared_parameters': {
            'color_type': 'hsl',
            'color': {
                'h': (0.0, 1.0),
                's': 1,
                'l': .5
            },
            'intensity': 400
        },
        'list': [
            {
                'azimuth': -pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': -pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }
        ]

    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('lights', 'shared_parameters', 'color', 'h'): 20
    }


def constancy_lightintensity_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'import_everything': True,
        }
    }
    p['lights'] = {
        'shared_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'intensity': (25, 800)
        },
        'list': [
            {
                'azimuth': -pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': -pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }
        ]

    }
    p['background'] = {
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 0,
                'g': 0,
                'b': 0
            },
        }
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('lights', 'shared_parameters', 'intensity'): 20
    }


def constancy_lightintensity_bg_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'import_everything': True,
        }
    }
    p['lights'] = {
        'shared_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'intensity': (25, 800)
        },
        'list': [
            {
                'azimuth': -pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': -pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': -pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }, {
                'azimuth': pi / 2,
                'altitude': pi / 2,
                'radius_factor': 1,
                'size_factor': 4,
            }
        ]
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('lights', 'shared_parameters', 'intensity'): 20
    }


def constancy_lightcolor_scene_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
            'overrides': {
                'light_color': {
                    'color_type': 'hsl',
                    'color': {
                        'h': (0.0, 1.0),
                        's': 1,
                        'l': .75
                    }
                }
            }
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'samples': 1000,
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth',
                   'combined_xyz'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20,
        ('background', 'scene_parameters', 'overrides', 'light_color', 'color', 'h'): 20
    }


def constancy_lightcolor_scene_gt_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]]
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['png', 'h5'],
        'passes': ['color', 'combined', 'object_index', 'diffuse_color', 'glossy_color', 'color_ground_truth',
                   'combined_xyz'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20
    }


def constancy_lightcolor_scene_2(p):
    constancy_lightcolor_scene_1(p)
    p['output']['file_types'] = ['h5', 'pkl']
    p['output']['passes'] = pass_constants.color_passes + ['combined', 'object_index']


def constancy_lightcolor_scene_gt_2(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
            'overrides': {
                'light_color': {
                    'color_type': 'rgb',
                    'color': {
                        'r': 1,
                        'g': 1,
                        'b': 1
                    }
                }
            }
        }
    }
    p['material'] = {
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': 0.0,
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['h5', 'pkl'],
        'passes': pass_constants.color_passes + ['combined', 'object_index'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20
    }


def constancy_lightsat_scene_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
            'overrides': {
                'light_color': {
                    'color_type': 'hsv',  # TODO remove this redundancy with set matching
                    'color': {
                        'h': 1,
                        's': (0.0, 1.0),
                        'v': 1,
                    }
                }
            }
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['h5', 'pkl'],
        'samples': 800,
        'passes': pass_constants.color_passes + ['combined', 'object_index'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('background', 'scene_parameters', 'overrides', 'light_color', 'color', 's'): 20,
        ('model', 'blend_parameters', 'directory'): 20,
    }


def constancy_lightsat_scene_white_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
            'overrides': {
                'light_color': {
                    'color_type': 'hsv',  # TODO remove this redundancy with set matching
                    'color': {
                        'h': 1,
                        's': (0.0, 1.0),
                        'v': 1,
                    }
                }
            }
        }
    }

    p['material'] = {  # TODO better version management
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': 0.0,
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['h5', 'pkl'],
        'samples': 800,
        'passes': pass_constants.color_passes + ['combined', 'object_index'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('background', 'scene_parameters', 'overrides', 'light_color', 'color', 's'): 20,
        ('model', 'blend_parameters', 'directory'): 20,
    }


def constancy_lightcolor_scene_white_1(p):
    constancy_lightcolor_scene_1(p)
    p['material'] = {
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': 0.0,
        }
    }
    p['output']['file_types'] = ['h5', 'pkl']
    p['output']['passes'] = pass_constants.color_passes + ['combined', 'object_index']


def constancy_lightcolor_scene_gt_white_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
            'overrides': {
                'light_color': {
                    'color_type': 'rgb',
                    'color': {
                        'r': 1,
                        'g': 1,
                        'b': 1
                    }
                }
            }
        }
    }
    p['material'] = {
        'type': 'color',
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': 0.0,
        }
    }

    p['camera'] = {
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'radius_factor': 1,
        'view_angle': pi / 2,
        'max_deviation_angle': 0,
    }
    p['output'] = {
        'file_types': ['h5', 'pkl', 'png'],
        'passes': pass_constants.color_passes + ['combined', 'object_index'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'blend_parameters', 'directory'): 20
    }


def constancy_distance_scene_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'blend',  # shape, blend, obj
        'blend_parameters': {
            'directory': '../images_constancymodels1',
            'scale_range': (.3, .3),
            'scale_uniform': True
        },
    }
    p['camera'] = {
        'radius_factor': (.75, 2),
        'azimuth': -pi / 5,
        'altitude': pi / 5,
        'view_angle': pi / 2,
        'max_deviation_angle': 0
    }
    p['background'] = {
        'type': 'scene',
        'scene_parameters': {
            'files': ['scenes/scene_1/Country-Kitchen.blend'],
            'model_position': [[0, 0, 1.5]],
        }
    }
    p['output'] = {
        'file_types': ['png', 'h5', 'pkl'],
        'samples': 1000,
        'passes': ['color', 'combined', 'z', 'normal', 'disparity', 'object_index', 'shallow_z'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('camera', 'radius_factor'): 20,
        ('model', 'blend_parameters', 'directory'): 20
    }
