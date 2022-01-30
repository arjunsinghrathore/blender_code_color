#!/usr/bin/env python

import os
import sys
import dataset_versions
from config import resources_path, output_path
from utils.selection import get_from_nested_dict, set_in_nested_dict
from utils.logging import announce


def initialize_parameters(version, batch_size, grid_index=0, gpu_index=0, force_continue=None, job_number=None):
    """
    Initialize parameters based on dataset version
    and render index
    """
    parameters = {}
    version_parameters(parameters, version)
    parameters['version'] = version
    parameters['resources_path'] = resources_path
    parameters['gpu_index'] = gpu_index
    parameters['output_path'] = output_path
    if job_number is not None:
        parameters['job_number'] = job_number
    if force_continue is not None:
        parameters['force_continue'] = force_continue
    total_render_count = grid_parameters(parameters)
    if batch_size:
        parameters['index'] = {
            'min': grid_index,
            'max': grid_index + batch_size,
            'batch_size': batch_size,
            'total': grid_index + batch_size
        }
    if not batch_size and total_render_count:
        parameters['index'] = {
            'min': grid_index,
            'max': grid_index + total_render_count,
            'batch_size': total_render_count
        }
    return parameters


def version_parameters(parameters, version):
    """
    If user specified version matches a function in testing.py call that function
    to apply version specific parameters
    """
    try:
        version_function = getattr(dataset_versions, version)
        version_function(parameters)
    except AttributeError:
        announce('Version {0} not found'.format(parameters['version']))
        raise


def grid_parameters(parameters):
    """
    Check if the version specific parameters specify any gridded parameters
    and convert their values to a grid-specification dictionary
    """
    try:
        stride = 1
        for keys, num in parameters['grid'].items():
            original = get_from_nested_dict(parameters, keys)
            value = {
                'value': original,
                'num': num,
                'stride': stride
            }
            set_in_nested_dict(parameters, keys, value)
            stride *= num
        if parameters['grid']:
            parameters['num_gridded_parameters'] = stride
            announce('Found {0} gridded parameters, yielding {1} renders'.format(len(parameters['grid']), stride))
        else:
            announce('{0} Renders'.format(parameters['index']['batch_size']))
        return stride
    except KeyError:
        return


def setup_output_directory(parameters):
    """
    If specified output path doesn't exist, make the folder
    """
    #Setup job number related output paths if neccesary
    images_path = os.path.join(parameters['output_path'], 'images_' + parameters['version'])
    announce("Rendering to folder: {0}".format(images_path))
    if not os.path.isdir(images_path):
        try:
            # os.mkdir(images_path)
            os.makedirs(images_path, exist_ok=True)
            announce("Output folder created successfully")
        except OSError:
            print ("Can't create folder: %s" % images_path)
            sys.exit(0)
    if 'job_number' in parameters:
        try:
            final_path = os.path.join(images_path, repr(parameters['job_number'])) 
            images_path = final_path
            # os.mkdir(final_path)
            os.makedirs(final_path, exist_ok=True)
            
            announce("Job folder successfully created")
        except OSError:
            print ("Cant create folder: %s" % images_path)
            sys.exit(0)
    parameters['output_path'] = images_path
