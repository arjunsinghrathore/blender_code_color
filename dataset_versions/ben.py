from scipy import pi
from utils import pass_constants

def mondrian_test(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'shape',  # shape, blend, obj, stl
        'shape_parameters': {
            'shapes': ['cube'],
            'shape_weights': [1],
            'edge_radius': (0, .5),
            'vertices': 6,
            'scale_uniform': False,
            'scale_range': (.25, 1),
            'rotate': False
        },
    }    
    p['material'] = {
        'type': 'image',  # principled,original,image,color
        'image_parameters': {
            'directory': 'base_mondrians',
            'color_type': 'hsl',
            'roughness': (0, .06),
            'glossiness': (.05, .7)
        },
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['png'],
        'passes': ['color'],
        'resolution': {
            'x': 256,
            'y': 256
        }
    }

def ben_render_test(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': False,
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
            'strength': 1.5,
            'hide_background': True
        }
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['png'],
        'output_filename': [('model', 'models', 0, 'filename'),
                            ['index']],
        'passes': ['color', 'z', 'shallow_z', 'normal', 'slant', 'shallow_z_inv', 'slant_black',
                   'object_index'],
        # 'passes': ['color', 'object_index','z','shallow_z','slant'],
        'png_passes': ['shallow_z', 'shallow_z_inv', 'slant', 'slant_black'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'stl_parameters', 'directory'): 20
    }


def ben_ccv_complex_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'kunsberg_shapes/set_1/test_stls_for_philip',
            'rotate': False,
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
            'strength': 1.5,
            'hide_background': True
        }
    }
    p['camera'] = {
        'azimuth': 10,
        'altitude': 10,
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['png'],
        'passes': ['color'],
        'output_filename': [('model', 'models', 0, 'filename'),
                            ['index'],
                            ['time']],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'stl_parameters', 'directory'): 5000
    }


def ben_ccv_lambert_1(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': False,
            'scale_range': (1, 1),
            'scale_uniform': True,
        },
    }
    p['material'] = {
        'type': 'color',  # ,original,image,color
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': .5
        },
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
        },
    }
    p['camera'] = {
        'azimuth': 1,
        'altitude': 1,
        'radius_factor': 3,
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
                'azimuth': 1,
                'altitude': 10,
                'radius_factor': 2,
                'size_factor': 1.5,
                'intensity': 500
            },
            {
                'color_type': 'rgb',
                'color': {
                    'r': 1,
                    'g': 1,
                    'b': 1
                },
                'azimuth': -pi / 4,
                'altitude': 1,
                'radius_factor': 1.5,
                'size_factor': 2,
                'intensity': 500
            },
        ]

    }
    p['output'] = {
        'file_types': ['png'],
        'output_filename': [('model', 'models', 0, 'filename'),
                            ['index']],
        'passes': ['color', 'z', 'shallow_z', 'normal', 'slant', 'shallow_z_inv', 'slant_black',
                   'object_index'],
        'png_passes': ['shallow_z_inv', 'slant_black'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'stl_parameters', 'directory'): 5000
    }


def ben_image_test(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': False,
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
            'strength': 1.5,
            'hide_background': True
        }
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
        'radius_factor': 1.5,
        'max_deviation_angle': 0
    }
    p['output'] = {
        'file_types': ['png'],
        'output_filename': [('model', 'models', 0, 'filename'),
                            ['index'],
                            ['time']],
        'passes': ['color'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'stl_parameters', 'directory'): 20
    }


def ben_lambert_test(p):
    p['model'] = {
        'arrangement': 'single',
        'type': 'stl',  # shape, blend, obj, stl
        'stl_parameters': {
            'directory': 'ben_blobs/test_stls',
            'rotate': False,
            'scale_range': (1, 1),
            'scale_uniform': True,
        },
    }
    p['material'] = {
        'type': 'color',  # ,original,image,color
        'color_parameters': {
            'color_type': 'rgb',
            'color': {
                'r': 1,
                'g': 1,
                'b': 1
            },
            'type': 'matte',
            'roughness': .5
        },
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
        },
    }
    p['camera'] = {
        'azimuth': 0,
        'altitude': 0,
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
                'azimuth': 0,
                'altitude': pi / 4,
                'radius_factor': 2,
                'size_factor': 1.5,
                'intensity': 500
            },
            {
                'color_type': 'rgb',
                'color': {
                    'r': 1,
                    'g': 1,
                    'b': 1
                },
                'azimuth': -pi / 4,
                'altitude': 0,
                'radius_factor': 1.5,
                'size_factor': 2,
                'intensity': 500
            },
        ]

    }
    p['output'] = {
        'file_types': ['png'],
        'passes': ['color'],
        'output_filename': [('model', 'models', 0, 'filename'),
                            ['index'],
                            'plain'],
        'resolution': {
            'x': 512,
            'y': 512
        }
    }
    p['grid'] = {
        ('model', 'stl_parameters', 'directory'): 20
    }
