#!/usr/bin/env python

import glob
import os
import numbers
import random
from .dictionaries import get_from_nested_dict, set_in_nested_dict
from six import string_types
from utils.logging import announce


"""
utils used for selecting specific render conditions 
from render parameters, which can take many formats
"""


def get_parameter_set_condition(parameter_dictionary, condition_dictionary, keys, cast_int=False):
    """
    Get the parameter (can be range, list or value) from the dictionary of render parameters
    Select a value and set it in the dictionary of a render condition
    Return the value
    """
    value = get_condition(get_from_nested_dict(parameter_dictionary, keys),
                          condition_dictionary['index'])
    if cast_int and isinstance(value, numbers.Number):
        value = int(value)
    set_in_nested_dict(condition_dictionary, keys, value)
    return value


def get_condition(parameter, index=None):
    """
    Rendering parameters can be a range of values, a list of values,
    a dictionary specifying gridded values or a single value
    Acts accordingly and return a single value
    """
    if is_gridded(parameter) and index is not None:
        return grid_condition(parameter, index)
    elif isinstance(parameter, list):
        return random_choice(parameter)
    elif isinstance(parameter, tuple) and len(parameter) == 2:
        return random_float(parameter)
    else:
        return parameter


def grid_condition(parameter, index):
    """
    Select a render condition value from a parameter that is gridded
    """
    stride = parameter['stride']
    num = parameter['num']
    value = parameter['value']
    grid_index = (index // stride) % num
    if isinstance(value, list):
        return value[grid_index]
    elif isinstance(value, tuple):
        return value[0] + (float(value[1]) - value[0]) * grid_index / max(num - 1, 1)
    else:
        return value


def is_gridded(parameter):
    """
    Gridded parameters are represented as dictionaries and have the keys: 'value', 'num', and 'stride'
    """
    return (isinstance(parameter, dict) and 'value' in parameter and 'num' in parameter and 'stride' in parameter)


def random_choice(data_set):
    """
    Select an item from a list of items
    """
    announce('This is lenn: {0}'.format(len(data_set)), '#')
    assert len(data_set)
    return random.choice(data_set)


def random_float(data_range, dim=1):
    """
    Generate a single random float or a list of them, according to dim
    """
    values = [random.uniform(data_range[0], data_range[1]) for _ in range(dim)]
    if dim == 1:
        values = values[0]
    return values


def get_resource_list(base_dir, sub_dir, extensions):
    """
    Get a list of files from a directory
    """
    files = []

    if isinstance(extensions, string_types):
        extensions = [extensions]
    if isinstance(sub_dir, string_types):
        sub_dir = [sub_dir]
    for dir in sub_dir:
        for ext in extensions:
            path = os.path.join(base_dir, dir, '*.' + ext)
            files += glob.glob(path)

    return files


def select_line_from_file(line_number, file_path):
    with open(file_path) as fp:
        for i, line in enumerate(fp):
            if i == line_number:
                return line
