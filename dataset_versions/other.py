from scipy import pi
from utils import pass_constants


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


def bigrange1(p):
    p['model'] = {
        # TODO 'select_first':'model' or 'arrangement'
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
        'type': ['external', 'image', 'color'],  # ,original,image,color
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
        'type': ['hdr', 'hdr', 'hdr', 'hdr', 'color'],  # TODO maybe make any array weightable?
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': (.5, 2)
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
        'file_types': ['png', 'h5', 'pkl'],
        'passes': pass_constants.xyz_passes,
        'resolution': {
            'x': 256,
            'y': 256
        }
    }


def testrange1(p):
    p['model'] = {
        # TODO 'select_first':'model' or 'arrangement'
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
        'type': ['external', 'image', 'color'],  # ,original,image,color
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
        'type': ['hdr', 'hdr', 'hdr', 'hdr', 'color'],  # TODO maybe make any array weightable?
        'hdr_parameters': {
            'directory': 'hdr',
            'strength': (.5, 2)
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
        'passes': [],
        'resolution': {
            'x': 1920,
            'y': 1080
        }
    }


def testtext1(p):
    p['model'] = {
        'arrangement': 'single',  # single, cluster, grid or random_cube
        'type': 'text',  # shape, blend, obj, text
        'text_parameters': {
            'body_parameters': {
                # 'body': ['a','b','x','y','p','ab','ll','ts','er','po','q'],
                # 'directory':,
                'files': 'wordlist_clean.txt',
                'line_number': (0, 69885)  # for directory/files only
            },
            'font_parameters': {
                'directory': 'fonts_text'},
            'depth': (0, .5),
            'bevel_depth': (0, .04),
            'bevel_resolution': (0, 5),
            'scale_uniform': False,
            'scale_range': (.75, 1),
            'rotate': False
        }
    }
    p['material'] = {
        'type': 'principled',  # ,original,image,color
        'principled_parameters': {
            'base': ['color', 'image'],
            'color_type': 'hsl',
            'color': {
                'h': (0, 1),
                's': (0, 1),
                'l': (0, 1)
            },
            'image_parameters': {
                'directory': ['textures_sorted', 'mattes_textures'],  # TODO docs directory array not griddable
            },
            'subsurface': 0,
            'metallic': (0.0, 1),
            'specular': (0.0, 1),
            'specular_tint': (0.0, 1),
            'roughness': (0.0, 1),
            'anisotropic': (0.0, 1),
            'anisotropic_rotation': (0.0, 1),
            'sheen': (0.0, 1),
            'sheen_tint': (0.0, 1),
            'clearcoat': (0.0, 1),
            'clearcoat_roughness': (0.0, 1),
            'ior': (1.1, 2.6),
            'transmission': (0.0, 1),
            'transmission_roughness': (0.0, .5),
        },
    }

    # p['material'] = {
    #     'type': ['image', 'color'],  # ,original,image,color
    #     'external_parameters': {
    #         'files': 'materials/materials.blend'
    #     },
    #     'color_parameters': {
    #         'color_type': 'hsl',
    #         'color': {
    #             'h': (0, 1),
    #             's': (0, 1),
    #             'l': (0, 1)
    #         },
    #         'type': ['principled'],
    #         'roughness': (0, .1)
    #     },
    #     'image_parameters': {
    #         'directory': ['textures_sorted', 'mattes_textures'],  # TODO docs directory array not griddable
    #         'roughness': (0, .06),
    #         'glossiness': (.05, .7)
    #     }
    # }
    p['background'] = {
        'type': ['hdr', 'hdr', 'hdr', 'color'],  # TODO maybe make any array weightable?
        'hdr_parameters': {
            'directory': ['hdr', 'hdr_new', 'hdr_studio'],  # TODO doc that mult directory is merge
            'strength': (.5, 2)
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
                'radius_factor': (2, 8),
                'size_factor': (2, 8),
                'intensity': (100, 400)
            }, {
                'color_type': 'inv_temp',
                'color': (1.0 / 7000.0, 1.0 / 3000.0),
                'azimuth': (0, 2 * pi),
                'altitude': (0, 2 * pi),
                'radius_factor': (2, 8),
                'size_factor': (2, 8),
                'intensity': (100, 400)
            }
        ]

    }

    p['camera'] = {
        'azimuth': (-pi / 10, pi / 10),
        'altitude': (- pi / 10, pi / 10),
        # 'view_angle': (pi / 5, pi / 3),
        'radius_factor': (1.4, 1.6),
        # 'max_deviation_angle': (0, .1),
        'normalize_radius': True,
        'normalize_center': True
    }
    p['output'] = {
        'file_types': ['png'],
        'output_filename': [['index'],
                            ('model', 'text_parameters', 'body_parameters', 'body'),
                            ('model', 'text_parameters', 'font_parameters', 'font')],
        # TODO doc must be unique prop, and array of arrays, single item array needs []
        'passes': [],
        'samples': 20,
        'denoise': False, #set float
        'resolution': {
            # 'x': 1920,
            # 'y': 1080
            'x': 1280,
            'y': 720
        }
    }
    p['grid'] = {
        ('model', 'text_parameters', 'body_parameters', 'line_number'): 69885,
    }


def bigrange2(p):
    bigrange1(p)
