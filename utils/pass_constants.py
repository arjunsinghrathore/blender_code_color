"""
Datastructures for different render passes available from blender
and their corresponding names as rendered from blender
"""
# TODO pass modifiers, black, inv, shallow
RGB = ['R', 'G', 'B']
XYZ = ['X', 'Y', 'Z']
XYZW = ['X', 'Y', 'Z', 'W']
UVA = ['U', 'V', 'A']
pass_dict = {
    'z': ['Depth.Z'],
    'mist': ['Mist.Z'],
    'normal': ['Normal.' + c for c in XYZ],
    'vector': ['Vector.' + c for c in XYZW],
    'uv': ['UV.' + c for c in UVA],
    'object_index': ['IndexOB.X'],
    'material_index': ['IndexMA.X'],
    'shadow': ['Shadow.' + c for c in RGB],
    'ambient_occlusion': ['AO.' + c for c in RGB],
    'subsurface_indirect': ['SubsurfaceInd.' + c for c in RGB],
    'subsurface_direct': ['SubsurfaceDir.' + c for c in RGB],
    'subsurface_color': ['SubsurfaceCol.' + c for c in RGB],
    'diffuse_indirect': ['DiffInd.' + c for c in RGB],
    'diffuse_direct': ['DiffDir.' + c for c in RGB],
    'diffuse_color': ['DiffCol.' + c for c in RGB],
    'transmission_indirect': ['TransInd.' + c for c in RGB],
    'transmission_direct': ['TransDir.' + c for c in RGB],
    'transmission_color': ['TransCol.' + c for c in RGB],
    'glossy_indirect': ['GlossInd.' + c for c in RGB],
    'glossy_direct': ['GlossDir.' + c for c in RGB],
    'glossy_color': ['GlossCol.' + c for c in RGB],
    'emit': ['Emit.' + c for c in RGB],
    'environment': ['Env.' + c for c in RGB],
    'combined': ['Combined.' + c for c in RGB],
    'stereo': [],
    'slant': [],
    'contour': [],
    'color': [],
    'tilt': [],
    'shallow_z': [],
    'disparity': [],
    'color_ground_truth': [],
    'combined_xyz': [],
    'combined_dkl': []
}
pass_mods = ('_black', '_inv', '_Zshallow')
all_passes = ['combined', 'z', 'mist', 'normal', 'vector', 'uv', 'object_index', 'material_index', 'shadow',
              'ambient_occlusion', 'subsurface_direct', 'subsurface_indirect', 'subsurface_color',
              'diffuse_indirect', 'diffuse_direct', 'diffuse_color', 'transmission_indirect',
              'transmission_direct', 'transmission_color', 'glossy_direct', 'glossy_indirect', 'glossy_color',
              'emit', 'environment', 'stereo', 'slant', 'tilt']

# NOTE 'combined' is the rendered image
all_normal_passes = ['combined', 'z', 'mist', 'normal', 'vector', 'uv', 'object_index', 'material_index', 'shadow',
                     'ambient_occlusion', 'subsurface_direct', 'subsurface_indirect', 'subsurface_color',
                     'diffuse_indirect', 'diffuse_direct', 'diffuse_color', 'transmission_indirect',
                     'transmission_direct', 'transmission_color', 'glossy_direct', 'glossy_indirect', 'glossy_color',
                     'emit', 'environment', 'slant', 'tilt', 'contour']

useful_passes_long = ['combined', 'z', 'normal', 'vector', 'object_index', 'material_index', 'shadow', 'diffuse_color',
                      'glossy_direct', 'slant', 'tilt', 'shallow_z', 'contour', 'shallow_contour']

useful_passes = ['combined', 'z', 'normal', 'object_index', 'diffuse_color', 'glossy_color', 'slant', 'tilt',
                 'shallow_z', 'contour', 'shallow_contour']

xyz_passes = ['combined', 'combined_xyz', 'object_index', 'color']

special_passes = ['color', 'stereo', 'contour', 'object_index']

all_color_passes = ['diffuse_direct', 'diffuse_indirect', 'diffuse_color', 'transmission_direct',
                    'transmission_indirect', 'transmission_color', 'subsurface_direct', 'subsurface_indirect',
                    'subsurface_color', 'glossy_direct', 'glossy_indirect', 'glossy_color', 'emit', 'environment']
color_passes = ['diffuse_color', 'transmission_color', 'glossy_color', 'emit', 'environment']
