import OpenEXR
import math
import Imath
import h5py
import numpy as np
from scipy.misc import imread, imsave
from copy import deepcopy
from . import transformations
from utils import pass_constants, colors
import pickle

"""
utils for:
managing render data from blender
retrieving it from render files and, and saving it to files
"""


def get_passes_from_exr(exr_filename, passes_list):
    """get blender generated EXR file and make dictionary of arrays of data"""
    pass_dict = pass_constants.pass_dict
    pass_mods = pass_constants.pass_mods
    pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)

    exr_file = OpenEXR.InputFile(exr_filename)
    dims = exr_file.header()['dataWindow']
    width, height = (dims.max.x - dims.min.x + 1, dims.max.y - dims.min.y + 1)
    base_layer = 'RenderLayer.'

    passes = {}

    for render_pass in passes_list:
        if render_pass.endswith(pass_mods):
            pass_channels = []
        else:
            pass_channels = pass_dict[render_pass]
            # TODO cleanup logic
        num_channels = len(pass_channels)
        if num_channels >= 1:
            image = np.zeros((height, width, num_channels), dtype='f')
            for index, channel_name in enumerate(pass_channels):
                data_string = exr_file.channel(base_layer + channel_name, pixel_type)
                data_array = np.fromstring(data_string, dtype='float32')
                data_array.shape = (height, width)
                image[:, :, index] = data_array
            passes[render_pass] = np.squeeze(image)
    return passes


def add_png_pass(passes, png_filename, side=''):
    """
    Import the png color render as a pass
    if stereo, side will be passed in as '_R or '_L'
    """
    key = 'color' + side
    passes[key] = imread(png_filename)[:, :, :3]


def add_contour_z_pass(passes, passes_list):
    """use depth pass to make a contour pass"""
    if 'z' in passes:
        shallow_depth = shallow_mod(passes['z'], 1000, 1 / 3)
        gradient = np.gradient(shallow_depth)
        norm_gradient = np.linalg.norm(gradient, axis=0)

        contour_range = np.max(norm_gradient) - np.min(norm_gradient)
        shallow_contour = shallow_mod(norm_gradient, contour_range / 2, 1 / 6)
        # TODO fix contour so less extreme contours show up better
        if 'contour' in passes_list:
            passes['contour'] = norm_gradient
        if 'shallow_contour' in passes_list:
            passes['shallow_contour'] = shallow_contour
        if 'shallow_z' in passes_list:
            passes['shallow_z'] = shallow_depth
    else:
        raise ValueError('Need to render with z pass to get contour')


def add_color_ground_truth_pass(passes, passes_list):
    """combine reflection free color passes"""
    if 'diffuse_color' in passes and 'glossy_color' in passes:
        passes['color_ground_truth'] = passes['glossy_color'] + passes['diffuse_color']
    else:
        raise ValueError('Need to render with diffuse color and glossy color to get color ground truth')


# TODO add lighting gt?

def add_slant_tilt_pass(passes, passes_list, camera_rotation):
    """add slant and/or tilt passes to pass dictionary"""
    if 'z' in passes_list and 'normal' in passes_list:
        slant_pass, tilt_pass = get_slant_and_tilt(passes['z'], passes['normal'], camera_rotation)
        if 'slant' in passes_list:
            passes['slant'] = slant_pass
        if 'tilt' in passes_list:
            passes['tilt'] = tilt_pass
    else:
        raise Exception('Must render with z and normal pass to use slant and tilt')


def black_background_mod(pass_name, passes):
    mask = passes['object_index']
    original = deepcopy(passes[pass_name.replace('_black', '')])
    original[mask == 0] = 0
    passes[pass_name] = original


def invert_mod(pass_name, passes):
    original = passes[pass_name.replace('_inv', '')]
    passes[pass_name] = np.max(original) - original


# TODO make real mod in code logic
def shallow_mod(image, background_threshold=1000, background_ratio=1 / 3):
    depth = deepcopy(image)
    back_indices = depth >= background_threshold
    min_depth = np.min(depth)
    # get max depth that isn't from background
    depth[back_indices] = -1000
    max_depth = np.max(depth)
    # set background to reasonable distance from scene
    depth[back_indices] = max_depth + (max_depth - min_depth) * background_ratio
    return depth


def add_disparity_pass(passes, passes_list):
    # TODO figure out disparity
    raise NotImplementedError


def add_xyz_dkl_pass(passes, passes_list):
    if 'combined' in passes_list:
        if 'combined_xyz' in passes_list:
            passes['combined_xyz'] = colors.RGB_to_XYZ(passes['combined'])
        if 'combined_dkl' in passes_list:
            # passes['combined_dkl'] = colors.RGB_to_DKL(passes['combined'])
            # TODO figure out DKL transform
            raise NotImplementedError
    else:
        raise Exception('Must render with combined pass to get xyz or dkl')


def get_slant_and_tilt(depth, normal, camera_rotation):
    """use depth and normal to get slant and tilt"""
    # create target images
    cam_dir = transformations.quaternion_matrix(camera_rotation)[0:3, 0:3]

    # Convert to camera space
    cam_normal = np.tensordot(normal, cam_dir.transpose(), axes=(2, 1))

    # Slant
    slant = 1 - cam_normal[:, :, 2]

    # Tilt
    tilt = (np.arctan2(cam_normal[:, :, 1], cam_normal[:, :, 0]) + math.pi) / (2 * math.pi + 0.0001)

    # Return calculated images
    return slant, tilt


def h5_from_passes(file_name, passes):
    """Make an HDF5 file of the pass dictionary"""
    h5_file = h5py.File(file_name + '.h5', 'w')
    for render_pass, data in passes.iteritems():
        h5_file[render_pass] = passes[render_pass]
        h5_file.flush()
    h5_file.close()


def png_from_each_pass(file_name, passes, to_save=None):
    """Save a PNG of each render pass"""
    if to_save:
        iter = [(render_pass, passes[render_pass]) for render_pass in to_save]
    else:
        iter = passes.iteritems()
    for render_pass, data in iter:
        pass_name = file_name + '.' + render_pass + '.png'
        imsave(pass_name, data)


def pickle_render(file_name, render):
    with open(file_name + '.pkl', 'wb') as f:
        pickle.dump(render, f, pickle.HIGHEST_PROTOCOL)
