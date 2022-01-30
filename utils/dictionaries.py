import collections
from operator import getitem
from functools import *

"""
utils for manipulating dictionaries, 
specifically nested dictionaries 
"""


def dict_merge(main_dict, merge_dict):
    """ Recursive dict merge.
    from https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    merges merge_dict onto main_dict recursively
    """
    for k, v in merge_dict.iteritems():
        if (k in main_dict and isinstance(main_dict[k], dict)
            and isinstance(merge_dict[k], collections.Mapping)):
            dict_merge(main_dict[k], merge_dict[k])
        else:
            main_dict[k] = merge_dict[k]


def get_from_nested_dict(dictionary, keys):
    """ Get a value from nested dictionaries by iterating through a list of keys """
    try:
        value = reduce(getitem, keys, dictionary)
    except KeyError:
        value = None
    return value


def set_in_nested_dict(dictionary, keys, value):
    """ Set a value in nested dictionaries by iterating through a list of keys"""
    get_from_nested_dict(dictionary, keys[:-1])[keys[-1]] = value


def replace_in_nested_dict(dictionary, keys, function):
    """
    Replace a value in nested dictionaries with a modified version of itself,
    note function must take in one argument and return one value
    """
    value = get_from_nested_dict(dictionary, keys)
    if value is not None:
        set_in_nested_dict(dictionary, keys, function(value))
