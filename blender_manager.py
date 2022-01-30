#!/usr/bin/env python

import sys
import time
import os
import re
import numpy as np
import random
import pickle
from copy import deepcopy
from operator import add
from fauxton import BlenderModule
from fauxton._core import server
from utils.colors import HSL_to_RGBA, HSV_to_RGBA, kelvin_to_RGBA
from utils.coordinates import AAR_to_XYZ, look_at, generate_random_orientation
from utils.logging import announce
from utils.selection import get_from_nested_dict, get_parameter_set_condition, get_resource_list, is_gridded, \
    random_float, get_condition, set_in_nested_dict, select_line_from_file
from utils.transformations import quaternion_multiply
from six import string_types
from collections import OrderedDict
import cv2

# TODO re-add join models option
# TODO render from single condition
# TODO make conditions list, render from that
# TODO renderscripts, batch jobs, gpu queue from db
# TODO add logging to files, decide if logging is flag or version param
# TODO add force on error, decide if flag or param
# TODO selectrot selectpos selectscale --> selectvector
# TODO render list of indices
# TODO blender AO simplify
# TODO index linked to timeline frames
# TODO blender python string griddable
# TODO background black / invert passes
# TODO png pass select some as output
# TODO pass dependency graph
# TODO add freestyle
# todo (eventually) update 2.8 bindings

class RenderManager(object):
    def __init__(self, parameters):
        """
        A class that iteratively generates a render condition
        from the render parameters, sets up a blender file with
        these conditions and renders it
        """
        self.parameters = parameters
        self.render_condition = deepcopy(self.parameters)
        self.index = parameters['index']['min']

        if 'job_number' in self.parameters:
            self.dataset_file_name = str(self.parameters['job_number'])
        else:
            self.dataset_file_name = str(self.parameters['index']['min']) + '_' + str(self.parameters['index']['max'])
            
        self.database_illum = [] #OrderedDict()


    def __enter__(self):
        """
        Set up a fauxton BlenderModule when used in a 'with RenderManager as ____' statement
        """
        self.blender = BlenderModule(self.load_blender_script('blender.py'))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Destroy the BlenderModule server
        """
        server.remove_module(self.blender._id)
        del self.blender
        # Pass exception
        if exc_type is not None:
            return False
        return self

    def __iter__(self):
        return self

    def __next__(self):
        """
        Make a new blender file and render condition and render it,
        returns path to render/model files
        """
        if self.index >= self.parameters['index']['max'] or \
                (self.parameters.get('num_gridded_parameters') and
                 self.index >= self.parameters['num_gridded_parameters']):
            raise StopIteration
        if self.parameters.get('force_continue'):
            # TODO debug this force thing
            try:
                return self.do_render_steps()
            except Exception as e:
                announce('Error While Rendering:{0}'.format(sys.exc_info()), '~', force=True)
                announce('Continuing to next render', '~', force=True)
                self.index += 1
                return None
        else:
            return self.do_render_steps()

    def next(self):
        return self.__next__()

    def do_render_steps(self):

        self.model_data = {}
        self.camera_data = {}
        self.material_data = {}
        
        whole_count = 0
        while whole_count<20:
            self.render_condition['index'] = self.index
            announce('Rendering index {0}'.format(self.index), '~', force=True)
            self.blender.setup()
            
            self.light_colors = {}

            self.ill_locations = []

            # Dictionary Items
            self.scene_color = self.select_color(['background', 'scene_parameters', 'overrides', 'light_color'])
            self.scene_intensity = []
            self.camera_dist = []
            self.scene_name = []
            self.blob_color = []

            self.scale = 0
            
            whole_count += 1

            self.very_less_light = ["AI33_005_280.blend"]
            self.less_light = ["AI58_006.blend", "AI58_009.blend", "AI58_003.blend", "AI58_004.blend", "AI58_008.blend", \
                               "AI043_004.blend", "AI043_003.blend", "AI33_006_280.blend", "AI43_007.blend", "AI33_008_280.blend", \
                               "AI58_002.blend", "AI48_010.blend", "AI48_001.blend", "AI043_006_Blender.blend"]
            self.medium_high_light = ["AI48_004.blend", "AI043_005_Blender.blend", \
                                      "AI48_002.blend", "AI48_003.blend", "AI33_002_280.blend"]
            self.more_light = ["AI33_009_280.blend", "AI33_004_280.blend", "AI33_001_280.blend", "AI48_008.blend", "AI58_001.blend", \
                               "AI58_010.blend"]

            self.setup_background()

            self.bound_limits = self.blender.bound_limitss(self.scene_name)
            announce('vertices: {0}'.format(self.bound_limits[0]))
            announce('max_vol_name: {0}'.format(self.bound_limits[1]))
            # announce('vertices_list: {0}'.format(self.bound_limits[2]))
            announce('bounding_limits: {0}'.format(self.bound_limits[2]))
            # announce('union: {0}'.format(self.bound_limits[3]))
            announce('max_vol_name_list: {0}'.format(self.bound_limits[3]))

            # DEciding world light
            if self.scene_name in self.less_light:
                self.blender.env_light(self.scene_color, 10)
            elif self.scene_name in self.very_less_light:
                self.blender.env_light(self.scene_color, 2)
            elif self.scene_name in self.more_light:
                self.blender.env_light(self.scene_color, 160)
            elif self.scene_name in self.medium_high_light:
                self.blender.env_light(self.scene_color, 85)
            else:
                self.blender.env_light(self.scene_color, 45)

            # if self.scene_name in self.less_light:
            #     self.blender.env_light(self.scene_color, 5)
            # elif self.scene_name in self.very_less_light:
            #     self.blender.env_light(self.scene_color, 2)
            # elif self.scene_name in self.more_light:
            #     self.blender.env_light(self.scene_color, 70)
            # elif self.scene_name in self.medium_high_light:
            #     self.blender.env_light(self.scene_color, 35)
            # else:
            #     self.blender.env_light(self.scene_color, 20)

            self.setup_model()
            self.setup_camera()
            if self.bool_chi:
                continue
            self.setup_lights()
            if self.bool_chi:
                continue
            self.setup_material()
            self.setup_misc_scripts()
            # self.setup_animation()
            break

        announce('light_colors: {0}'.format(self.light_colors))
        announce('scene_intensity: {0}'.format(self.scene_intensity))

        self.info_dict = {'scene_color': self.scene_color, 'light_intensity': self.scene_intensity, 'camera_dist': self.camera_dist, \
                     'scene_name': self.scene_name, 'blob_color': self.blob_color}


        self.database_illum.append({'index':self.index,'illuminants':self.light_colors})

        if whole_count < 20:
            ################################################
            # manual adding of different conditions
            ################################################



            ####################
            # standard condition
            self.render(condition='')
            #####################
            # saving dict info
            announce('info_dict: {0}'.format(self.info_dict))
            with open(self.output_filee + '.pkl', 'wb') as f:
                pickle.dump(self.info_dict, f, protocol=-1)

            #########################
            # Saving color png file
            # scene_colorr = np.ones((256,256,3))
            # for c_i in range(3):
            #     scene_colorr[:,:,c_i] = scene_colorr[:,:,c_i]*int(self.blob_color[c_i]*255)

            # cv2.imwrite(self.output_filee + '_rgb.png', cv2.cvtColor(scene_colorr.astype('uint8'), cv2.COLOR_BGR2RGB))

            ####################
            # # Only Object segmentation BW
            # self.blender.only_object()
            
            self.render(condition='gt_sm', bool_ch = True)           # <----------------- # <-----------------

            #############################
            # Ground Truth black
            self.blender.only_object()
            # listi = self.blender.add_light('light', [1,1,1,1], 150, self.camera_data['rotation'], self.camera_data['location'], 1,\
            #                                      self.camera_data['model_center'], self.camera_data['radius'], \
            #                                      self.camera_data['az_r_l'], self.camera_data['az_r_u'], self.camera_data['al_r_l'], \
            #                                      self.camera_data['al_r_u'], self.camera_data['model_max_dimension'], self.camera_data['if_counter'])
            # self.blender.set_color_background([0,0,0,0])
            self.blender.env_light([1,1,1,1], 0.65)

            self.render(condition='gt_r')    # <----------------- # <-----------------


            #############################
            # For finding the illuminant
            self.blender.only_camera()
            self.blender.env_light(self.scene_color, 0.65)
            # self.blender.modify_principled_material_mask()

            self.render(condition='gt_ill')    # <----------------- # <-----------------


            ####################
            # ground truth reflectance condition
            
            # print(self.light_colors)
            # changing lights to white
            # materials = self.blender.modify_principled_material()
            # announce('materials: {0}'.format(materials))
            # for k, v in self.light_colors.items():
            #     self.blender.set_light_properties(k, 'color', [1.0,1.0,1.0,1.0])

            # self.render(condition='gt_r')             # <-----------------
            
            # # changing them back
            # for k, v in self.light_colors.items():
            #     self.blender.set_light_properties(k, 'color', v)

            
        # TODO simple plane scenes ground
        self.index += 1

        return self.render_condition

    def save_dataset(self):
        output_path = self.parameters['output_path']
        print('saving dataset')
        file_path = os.path.join(output_path, self.dataset_file_name+'.pickle')
        with open(file_path, 'wb') as f:
            pickle.dump(self.database_illum, f)
        
    def set_condition_value(self, keys, cast_int=False):
        """
        Wrapper for the get_parameter_set_condition function with first two args fixed
        """
        return get_parameter_set_condition(self.parameters, self.render_condition, keys, cast_int)

    def get_condition_value(self, keys, cast_int=False):
        """
        Wrapper similar to get_parameter_set_condition function but doesn't set value in condition dict
        """
        value = get_condition(get_from_nested_dict(self.parameters, keys), self.render_condition['index'])
        if cast_int:
            value = int(value)
        return value

    def select_resource(self, key_list, file_types, set_in_condition_dict=True):
        """
        select external resource file for blender model
        takes gridding, and file specification type into account
        file specification can either be a list of files to choose from or
        a local path to a directory of files
        """
        if set_in_condition_dict:
            value_function = self.set_condition_value
        else:
            value_function = self.get_condition_value

        sub_parameters = get_from_nested_dict(self.parameters, key_list)
        files_key_list = key_list + ['files']
        if 'files' in sub_parameters:
            file_path = value_function(files_key_list)
            if self.parameters['resources_path'] not in file_path:
                file_path = os.path.join(self.parameters['resources_path'], file_path)
        elif 'directory' in sub_parameters:  # convert directory param into files param
            sub_parameters['files'] = deepcopy(sub_parameters['directory'])
            if is_gridded(sub_parameters['directory']):
                directory = sub_parameters['directory']['value']
            else:
                directory = sub_parameters['directory']
            resources_list = get_resource_list(self.parameters['resources_path'], directory, file_types)
            if is_gridded(sub_parameters['directory']):
                sub_parameters['files']['value'] = resources_list
            else:
                sub_parameters['files'] = resources_list
            file_path = value_function(files_key_list)
        else:
            raise KeyError('No proper file input for resource')
        if set_in_condition_dict:
            set_in_nested_dict(self.render_condition, list(key_list) + ['full_path'], file_path)
        return file_path

    def select_color(self, key_list, set_in_condition_dict=True):
        """
        Select a color from the color parameter
        using the colors and values specified at the nested dictionary
        found using key_list
        """
        if set_in_condition_dict:
            value_function = self.set_condition_value
        else:
            value_function = self.get_condition_value

        color_parameters = get_from_nested_dict(self.parameters, key_list)
        color_type = color_parameters['color_type']
        if color_type == 'temp' or color_type == 'inv_temp':
            color = value_function(key_list + ['color'])
            if color_type == 'inv_temp':
                color = 1 / color
            color = kelvin_to_RGBA(color)
        elif color_type in ['rgb', 'hsl', 'hsv']:
            color = {}
            for channel in color_parameters['color']:
                color[channel] = value_function(key_list + ['color', channel])
            if color_type == 'hsl':
                color = HSL_to_RGBA(color['h'], color['s'], color['l'])
            elif color_type == 'hsv':
                color = HSV_to_RGBA(color['h'], color['s'], color['v'])
            else:
                color = [color['r'], color['g'], color['b'], 1]
        else:
            raise ValueError('No proper color type specified')
        if set_in_condition_dict:
            set_in_nested_dict(self.render_condition, list(key_list) + ['RGB'], color)
        return color

    def select_scale(self, sub_parameters):
        """
        generate a tuple of 3 scale values
        """
        scale = [1, 1, 1]

        scale_range = sub_parameters.get('scale_range')
        scale_uniform = sub_parameters.get('scale_uniform')
        if scale_range:
            if scale_uniform:
                scale = random_float(scale_range)
                scale = [scale] * 3
            else:
                scale = random_float(scale_range, 3)
        
        announce('Scale: {0}'.format(scale))

        return scale

    def select_rotation(self, sub_parameters):
        """
        generate a random euler rotation if specified
        """
        if sub_parameters.get('rotate'):
            rotation = random_float((-np.pi, np.pi), 3)
        else:
            rotation = (0, 0, 0)
        return rotation

    def select_mod_position(self):
        whole_mdim = self.bound_limits[2]

        position = []

        for i in range(3):
            if whole_mdim[i][0] < whole_mdim[i][1]:
                position.append(random.uniform(whole_mdim[i][0],whole_mdim[i][1]))
            else:
                position.append(random.uniform(whole_mdim[i][1],whole_mdim[i][0]))

        return position

    def select_position(self, sub_parameters):
        """
        generate a random XYZ tuple if specified
        """
        position = (0, 0, 0)
        announce('sub_parameters: {0}'.format(sub_parameters))
        if sub_parameters:
            position_range = sub_parameters.get('position_range')
            announce('position_range: {0}'.format(position_range))
            if position_range:
                position = self.select_mod_position()
                # position[-1] = abs(position[-1])
                announce('position: {0}'.format(position))
        self.set_condition_value(('background', 'scene_parameters', 'model_position'))
        position_shift = get_from_nested_dict(self.render_condition,
                                              ('background', 'scene_parameters', 'model_position'))
        if position_shift:
            position = map(add, position, position_shift)


        return tuple(position)

    def load_blender_script(self, filename):
        """
        load whole blender script file into memory
        """
        return open(os.path.join(os.path.dirname(__file__), filename)).read()

    # TODO restructure model parameters so user can have single, grid or cluster of shapes OR imported model
    def setup_model(self):
        model_arrangement = self.set_condition_value(('model', 'arrangement'))
        self.render_condition['model']['models'] = []
        announce('Model arrangement: {0}'.format(model_arrangement))
        models_list = self.render_condition['model']['models']
        if model_arrangement == 'single':
            self.setup_single_model(models_list)
        if model_arrangement == 'cluster':
            self.setup_cluster_model(models_list)
        if model_arrangement == 'grid':
            self.setup_grid_model(models_list)
        elif model_arrangement == 'random_cube':
            self.setup_random_cube_model(models_list)
        self.blender.convert_to_meshes()
        self.blender.finish_model()

    def setup_single_model(self, models_list):
        parameters = self.parameters['model']['stl_parameters']
        position = self.select_position(parameters)
        models_list.append({'position': position})
        self.select_and_place_model(models_list[0], False)

    def setup_cluster_model(self, models_list):
        model_parameters = self.parameters['model']['cluster_parameters']
        number_of_objects = self.set_condition_value(('model', 'cluster_parameters', 'number_of_objects'), True)
        announce('Number of objects: {0}'.format(number_of_objects))
        for i in range(number_of_objects):
            position = self.select_position(model_parameters)
            models_list.append({'position': position})
            if i == number_of_objects - 1 and not self.blender.mesh_count():
                can_be_empty = False
            else:
                can_be_empty = True
            self.select_and_place_model(models_list[-1], can_be_empty)

    def setup_grid_model(self, models_list):
        grid_parameters = self.parameters['model']['grid_parameters']
        grid_x = self.set_condition_value(('model', 'grid_parameters', 'grid_dimensions', 'x'), True)
        grid_y = self.set_condition_value(('model', 'grid_parameters', 'grid_dimensions', 'y'), True)
        grid_z = self.set_condition_value(('model', 'grid_parameters', 'grid_dimensions', 'z'), True)
        grid_spacing = self.set_condition_value(('model', 'grid_parameters', 'grid_spacing'))
        i = 0
        number_of_objects = grid_x * grid_y * grid_z
        for x in range(grid_x):
            x_pos = grid_spacing * (x - grid_x / 2.0)
            for y in range(grid_y):
                y_pos = grid_spacing * (y - grid_y / 2.0)
                for z in range(grid_z):
                    i += 1
                    z_pos = grid_spacing * (z - grid_z / 2.0)
                    position_shift = self.select_position(grid_parameters)
                    position = tuple(map(add, [x_pos, y_pos, z_pos], position_shift))
                    models_list.append({'position': position})
                    if i == number_of_objects - 1 and not self.blender.mesh_count():
                        can_be_empty = False
                    else:
                        can_be_empty = True
                    self.select_and_place_model(models_list[-1], can_be_empty)

    def setup_random_cube_model(self, models_list):
        number_of_objects = self.set_condition_value(('model', 'cube_parameters', 'number_of_objects'), True)

        for i in range(number_of_objects):
            cube_x = self.set_condition_value(('model', 'cube_parameters', 'cube_dimensions', 'x'))
            cube_y = self.set_condition_value(('model', 'cube_parameters', 'cube_dimensions', 'y'))
            cube_z = self.set_condition_value(('model', 'cube_parameters', 'cube_dimensions', 'z'))
            # while number_paced<number_of_objects:
            #   if try_place():
            #       number_placed+=1
            models_list.append({'position': [cube_x, cube_y, cube_z]})
            if i == number_of_objects - 1 and not self.blender.mesh_count():
                can_be_empty = False
            else:
                can_be_empty = True
            self.select_and_place_model(models_list[-1], can_be_empty)

    def select_and_place_model(self, model_dict, can_be_empty=True):
        model_type = self.set_condition_value(('model', 'type'))
        if model_type == 'shape':
            self.add_shape_model(model_dict, can_be_empty)
        if model_type == 'blend':
            self.add_blend_model(model_dict)
        if model_type == 'obj':
            self.add_obj_model(model_dict)
        if model_type == 'stl':
            self.add_stl_model(model_dict)
        if model_type == 'text':
            self.add_text_model(modify_principled_materialmodel_dict)

    def add_shape_model(self, model_dict, can_be_empty=True):
        edge_radius = self.set_condition_value(('model', 'shape_parameters', 'edge_radius'))
        shape_parameters = self.parameters['model']['shape_parameters']
        scale = self.select_scale(shape_parameters)
        rotation = self.select_rotation(shape_parameters)
        shapes = shape_parameters['shapes']
        shape_weights = shape_parameters.get('shape_weights')
        if not can_be_empty:  # for now, assuming empty only removed upon last shape placement
            try:
                empty_index = shapes.index('empty')
                shapes.remove('empty')
                if shape_weights:
                    shape_weights.pop(empty_index)
            except:
                pass
        shape = self.select_shape_from_list(shapes, shape_weights)
        announce('Model shape: {0}'.format(shape))
        if shape == 'empty':
            return
        vertices = shape_parameters.get('vertices', 150)
        model_dict.update({
            'type': 'shape',
            'shape': shape,
            'edge_radius': edge_radius,
            'vertices': vertices,
            'rotation': rotation,
            'scale': scale
        })
        self.blender.make_shape(shape, edge_radius, vertices, model_dict['position'], rotation, scale)

    def select_shape_from_list(self, shapes, weights):
        if weights:
            s = sum(weights)
            shape_weights = [float(p) / s for p in weights]
            choice = np.random.choice(len(shapes), p=shape_weights)
            shape = shapes[choice]
        else:
            shape = np.random.choice(shapes).tostring()
        return shape

    def add_blend_model(self, model_dict):
        blend_parameters = self.parameters['model']['blend_parameters']
        model_path = self.select_resource(['model', 'blend_parameters'], 'blend', False)
        announce('Importing model from {0}'.format(model_path.split('/')[-1]))
        import_everything = self.set_condition_value(('model', 'blend_parameters', 'import_everything'))
        if import_everything:
            self.blender.add_blend_file(model_path)
            model_dict.update({
                'type': 'blend',
                'file': model_path,
                'filename': model_path.split('/')[-1],
            })
            return
        # whole_mdim = min(self.blender.model_dimensions(True))
        # model_center = [0, 0, 0]
        # announce('model pos {0}'.format(model_dict['position']))
        # announce('scene whole_mdim {0}'.format(whole_mdim))
        # squared_dist = np.sum((np.array(model_dict['position'])-np.array(model_center))**2, axis=0)
        # dist = np.sqrt(squared_dist)
        # announce('dist   {0}'.format(dist))

        # constraint = whole_mdim/2 if whole_mdim/2 > 2 else 2

        # if dist > constraint:
        #     while True:
        #         model_dict['position'] = self.select_mod_position()
        #         model_dict['position'][-1] = abs(model_dict['position'][-1])
        #         squared_dist = np.sum((np.array(model_dict['position'])-np.array(model_center))**2, axis=0)
        #         dist = np.sqrt(squared_dist)
        #         if dist < constraint:
        #             break
        scale = self.select_scale(blend_parameters)
        rotation = self.select_rotation(blend_parameters)
        model_dict.update({
            'type': 'blend',
            'file': model_path,
            'filename': model_path.split('/')[-1],
            'rotation': rotation,
            'scale': scale
        })
        announce('model pos {0}'.format(model_dict['position']))
        animate = self.parameters.get('animate')
        self.blender.set_animation_parameters(self.parameters.get('animate'))
        counterr = self.blender.add_blend_model(model_path, tuple(model_dict['position']), rotation, scale, animate)
        announce('model counterr {0}'.format(counterr))

    def add_obj_model(self, model_dict):
        obj_parameters = self.parameters['model']['obj_parameters']
        model_path = self.select_resource(['model', 'obj_parameters'], 'obj', False)
        announce('Importing model from {0}'.format(model_path.split('/')[-1]))
        scale = self.select_scale(obj_parameters)
        rotation = self.select_rotation(obj_parameters)
        model_dict.update({
            'type': 'obj',
            'file': model_path,
            'filename': model_path.split('/')[-1],
            'rotation': rotation,
            'scale': scale
        })
        self.blender.add_obj_model(model_path, model_dict['position'], rotation, scale)

    def add_stl_model(self, model_dict):
        stl_parameters = self.parameters['model']['stl_parameters']
        model_path = self.select_resource(['model', 'stl_parameters'], 'stl', False)
        announce('Importing model from {0}'.format(model_path.split('/')[-1]))
        scale = self.select_scale(stl_parameters)
        rotation = self.select_rotation(stl_parameters)
        model_dict.update({
            'type': 'stl',
            'file': model_path,
            'filename': model_path.split('/')[-1],
            'rotation': rotation,
            'scale': scale
        })

        # whole_mdim = min(self.blender.model_dimensions(True))
        # model_center = [0, 0, 0]
        # announce('model pos {0}'.format(model_dict['position']))
        # announce('scene whole_mdim {0}'.format(whole_mdim))
        # squared_dist = np.sum((np.array(model_dict['position'])-np.array(model_center))**2, axis=0)
        # dist = np.sqrt(squared_dist)
        # announce('dist   {0}'.format(dist))

        # constraint = whole_mdim/2 if whole_mdim/2 < 4 else 4

        # if dist > constraint:
        #     while True:
        #         model_dict['position'] = self.select_mod_position()
        #         model_dict['position'][-1] = abs(model_dict['position'][-1])
        #         squared_dist = np.sum((np.array(model_dict['position'])-np.array(model_center))**2, axis=0)
        #         dist = np.sqrt(squared_dist)
        #         if dist < constraint:
        #             break
        
        announce('model pos {0}'.format(model_dict['position']))
        animate = self.parameters.get('animate')
        if animate:
            self.blender.set_animation_parameters(self.parameters.get('animate'))

        listi = self.blender.add_stl_model(model_path, model_dict['position'], rotation, scale, animate, self.bound_limits, self.ill_locations)
        counterr = listi[0]
        location = listi[1]
        distt = listi[2]
        self.model_data.update({
            'location': location,
            'model_path': model_path,
            'rotation': rotation,
            'scale': scale,
            'animate': animate,
        })
        announce('model counterr {0}'.format(counterr))
        # announce('model distt {0}'.format(distt))

    def add_text_model(self, model_dict):
        text_parameters = self.parameters['model']['text_parameters']
        try:
            body_path = self.select_resource(['model', 'text_parameters', 'body_parameters'], 'txt', False)
            line_number = self.set_condition_value(('model', 'text_parameters', 'body_parameters', 'line_number'), True)
            body = select_line_from_file(line_number, body_path)
            body = re.sub('\s+', '', body)
            set_in_nested_dict(self.render_condition, ('model', 'text_parameters', 'body_parameters', 'body'), body)
        except KeyError:
            body = self.set_condition_value(('model', 'text_parameters', 'body_parameters', 'body'))
        announce('Creating text model: {0}'.format(body))
        font_file = self.select_resource(['model', 'text_parameters', 'font_parameters'], ['otf', 'ttf'], False)
        set_in_nested_dict(self.render_condition, ('model', 'text_parameters', 'font_parameters', 'font'),
                           font_file.split('/')[-1].split('.')[0])
        announce('Using font: {0}'.format(font_file.split('/')[-1]))
        scale = self.select_scale(text_parameters)
        rotation = self.select_rotation(text_parameters)
        depth = self.set_condition_value(('model', 'text_parameters', 'depth'))
        bevel_depth = self.set_condition_value(('model', 'text_parameters', 'bevel_depth'))
        bevel_resolution = self.set_condition_value(('model', 'text_parameters', 'bevel_resolution'))
        model_dict.update({
            'type': 'text',
            'body': body,
            'rotation': rotation,
            'scale': scale,
            'depth': depth,
            'bevel_resolution': bevel_resolution,
            'bevel_depth': bevel_depth
        })
        self.blender.add_text_model(body, depth, bevel_depth, bevel_resolution, font_file, model_dict['position'],
                                    rotation, scale)

    def setup_material(self):
        if self.parameters.get('material'):
            material_type = self.set_condition_value(('material', 'type'))
            if material_type == 'external':
                self.setup_external_material()
                return
            elif material_type == 'original':
                return
            objects = self.blender.mesh_indices()
            len_ = -1
            for object_index in objects:
                announce('Done Material: {0}'.format(object_index))
                if material_type == 'image':
                    self.setup_image_material(object_index)
                elif material_type == 'color':
                    self.setup_color_material(object_index)
                elif material_type == 'principled':
                    len_ = self.setup_principled_material(object_index, len_)

    def setup_image_material(self, object_index):
        image_path = self.select_resource(['material', 'image_parameters'], 'png') #jpg
        announce('Image Material: {0}'.format(image_path.split('/')[-1]))
        roughness = self.set_condition_value(('material', 'image_parameters', 'roughness'))
        glossiness = self.set_condition_value(('material', 'image_parameters', 'glossiness'))
        self.blender.set_image_material(image_path, roughness, glossiness, object_index)

    def setup_color_material(self, object_index):
        color = self.select_color(['material', 'color_parameters'])
        self.blob_color = color
        announce('Color Material: {0}'.format(color))
        material = self.set_condition_value(('material', 'color_parameters', 'type'))
        roughness = self.set_condition_value(('material', 'color_parameters', 'roughness'))
        self.blender.set_color_material(color, material, roughness, object_index)

    def setup_principled_material(self, object_index, len_):
        base = self.set_condition_value(('material', 'principled_parameters', 'base'))
        if base == 'color':
            color = self.select_color(['material', 'principled_parameters'])
        elif base == 'image':
            ####################################################################################################################################################################################
            #### change file type ##############################################################################################################################################################
            ####################################################################################################################################################################################
            color = self.select_resource(['material', 'principled_parameters', 'image_parameters'], 'jpg')
            # color = self.select_resource(['material', 'principled_parameters', 'image_parameters'], 'png')
        else:
            raise Exception('Improper base type for principled material')
        announce('Principled Material: {0}'.format(color))
        subsurface = self.set_condition_value(('material', 'principled_parameters', 'subsurface'))
        metallic = self.set_condition_value(('material', 'principled_parameters', 'metallic'))
        specular = self.set_condition_value(('material', 'principled_parameters', 'specular'))
        specular_tint = self.set_condition_value(('material', 'principled_parameters', 'specular_tint'))
        roughness = self.set_condition_value(('material', 'principled_parameters', 'roughness'))
        anisotropic = self.set_condition_value(('material', 'principled_parameters', 'anisotropic'))
        anisotropic_rotation = self.set_condition_value(('material', 'principled_parameters', 'anisotropic_rotation'))
        sheen = self.set_condition_value(('material', 'principled_parameters', 'sheen'))
        sheen_tint = self.set_condition_value(('material', 'principled_parameters', 'sheen_tint'))
        clearcoat = self.set_condition_value(('material', 'principled_parameters', 'clearcoat'))
        clearcoat_roughness = self.set_condition_value(('material', 'principled_parameters', 'clearcoat_roughness'))
        ior = self.set_condition_value(('material', 'principled_parameters', 'ior'))
        transmission = self.set_condition_value(('material', 'principled_parameters', 'transmission'))
        transmission_roughness = self.set_condition_value(('material', 'principled_parameters', 'transmission_roughness'))
        # announce('Done Principled Material: {0}'.format(object_index))
        len_ = self.blender.set_principled_material(base, color, subsurface, metallic, specular, specular_tint,
                                             roughness, anisotropic, anisotropic_rotation, sheen, sheen_tint, clearcoat,
                                             clearcoat_roughness, ior, transmission, transmission_roughness,
                                             object_index, len_)
        self.material_data.update({
            'base': base,
            'color': color,
            'subsurface': subsurface,
            'metallic': metallic,
            'specular': specular,
            'specular_tint': specular_tint,
            'roughness': roughness,
            'anisotropic': anisotropic,
            'anisotropic_rotation': anisotropic_rotation,
            'sheen': sheen,
            'sheen_tint': sheen_tint,
            'clearcoat': clearcoat,
            'clearcoat_roughness': clearcoat_roughness,
            'ior': ior,
            'transmission': transmission,
            'transmission_roughness': transmission_roughness,
            'object_index': object_index,
            'len_': len_
        })

        return len_

    def setup_external_material(self):
        material_path = self.select_resource(['material', 'external_parameters'], 'blend')
        announce('External Material: {0}'.format(material_path))  # .split('/')[-1]))
        self.blender.add_external_materials(material_path)

    def setup_lights(self):
        lights = self.parameters.get('lights')
        if lights:

            number_of_lights = self.set_condition_value(('lights', 'number'), True)
            shared_parameters = lights.get('shared_parameters')
            if shared_parameters:
                shared_properties = self.get_light_properties(['lights', 'shared_parameters'])
                if 'name' not in shared_properties:
                    shared_properties['name'] = 'light'

            else:
                shared_properties = {}
            
            lights_list = lights.get('list')
            self.render_condition['lights']['list'] = []
            # print('lights_list', lights_list)
            
            # print('adding lights')

            if number_of_lights and lights_list:
            # if number_of_lights and shared_properties!={}:
                for i in range(number_of_lights):
                    # index = np.random.randint(len(lights_list))
                    shared_properties['name'] = shared_properties['name'] + str(i)
                    # self.add_light(index, shared_properties)
                    self.add_light(i, shared_properties)
            elif lights_list:
                for index, light in enumerate(lights_list):
                    self.add_light(index, shared_properties)

    def add_light(self, index, shared_properties):
        model_max_dimension = max(self.blender.model_dimensions())
        constraint_m = model_max_dimension*1.5 #if model_max_dimension*1.5 #> 0.75 else 0.75
        radius = random.uniform(constraint_m,constraint_m*2)
        # try:
        #     properties = self.get_light_properties(['lights', 'list', index])
        # except:
        #     properties = {}

        properties = self.get_light_properties(['lights', 'list', index])

        light_properties = deepcopy(shared_properties)
        # print(properties)
        light_properties.update(properties)
        name = light_properties['name']
        radius = radius #light_properties['radius_factor'] #* model_max_dimension
        size = light_properties['size_factor'] #* model_max_dimension
        azimuth = light_properties['azimuth']
        altitude = light_properties['altitude']
        whole_mdim = min(self.blender.model_dimensions(True))
        # radius = whole_mdim
        location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude,
                              radius=radius)
        az_r_l = light_properties['az_r_l']
        az_r_u = light_properties['az_r_u']
        al_r_l = light_properties['al_r_l']
        al_r_u = light_properties['al_r_u']

        model_center = self.blender.model_center()
        announce('before light location: {0}'.format(location))
        location = tuple(map(add, location, model_center))
        # squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
        # dist = np.sqrt(squared_dist)
        squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
        dist_m = np.sqrt(squared_dist_m)

        # constraint = whole_mdim/2 if whole_mdim/2 < 4 else 4
        if_counter = 0 

        if dist_m < constraint_m: # or dist > constraint:
            while True:
                if_counter += 1
                radius = random.uniform(constraint_m,constraint_m*2)# * model_max_dimension
                azimuth = random.uniform(az_r_l,az_r_u)
                altitude = random.uniform(al_r_l,al_r_u)
                location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude,
                              radius=radius)
                location = tuple(map(add, location, model_center))
                # squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
                # dist = np.sqrt(squared_dist)
                squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
                dist_m = np.sqrt(squared_dist_m)
                if dist_m > constraint_m: # and dist < constraint:
                    break
        
        # size = dist_m*size

        rotation = look_at(location, model_center)

        # light_properties['intensity'] = light_properties['intensity']*(whole_mdim/2)

        listi = self.blender.add_light(name, light_properties['color'], light_properties['intensity'], rotation, location, size, model_center,
                                            radius, az_r_l, az_r_u, al_r_l, al_r_u, model_max_dimension, if_counter)
        counterr = listi[0]
        self.bool_chi = listi[1]
        if_counter = listi[2]
        objects_list = listi[3]
        announce('counterr light: {0}'.format(counterr))
        announce('if_counter light: {0}'.format(if_counter))
        announce('light location: {0}'.format(location))
        announce('light bool_chi: {0}'.format(self.bool_chi))
        # announce('objects_list: {0}'.format(objects_list))
        # added for constancy
        self.light_colors[name] = light_properties['color']
        self.scene_intensity = light_properties['intensity']
        
        self.render_condition['lights']['list'].append({'color': light_properties['color'],
                                                        'intensity': light_properties['intensity'],
                                                        'rotation': rotation,
                                                        'location': location,
                                                        'size': size})
        

    def get_light_properties(self, keys):
        try:
            if self.scene_color:
                color = self.scene_color
                announce('Universal color works : {0}'.format(color))
            else:
                color = self.select_color(keys, False)
                self.scene_color = color
        except KeyError:
            color = None
        # try:
        #     color = self.select_color(keys, False)
        # except KeyError:
        #     color = None
        azimuth = self.get_condition_value(keys + ['azimuth'])
        altitude = self.get_condition_value(keys + ['altitude'])
        if not azimuth and not altitude:
            #Set azimth and altitude from a uniform range
            az_r_l = self.get_condition_value(keys + ['azimuth_range'] + [0])
            az_r_u = self.get_condition_value(keys + ['azimuth_range'] + [1])
            al_r_l = self.get_condition_value(keys + ['altitude_range'] + [0])
            al_r_u = self.get_condition_value(keys + ['altitude_range'] + [1])
            azimuth = random.uniform(az_r_l,az_r_u)
            altitude = random.uniform(al_r_l,al_r_u)
        whole_mdim = min(self.blender.model_dimensions(True))
        model_max_dimension = max(self.blender.model_dimensions())
        constraint_m = model_max_dimension*1.5
        radius_factor = random.uniform(constraint_m,constraint_m*2)
        size_factor = self.get_condition_value(keys + ['size_factor'])
        intensity = self.get_condition_value(keys + ['intensity'])
        
        name = self.get_condition_value(keys + ['name'])
        properties = {
            'name': name,
            'color': color,
            'azimuth': azimuth,
            'altitude': altitude,
            'radius_factor': radius_factor,
            'size_factor': size_factor,
            'intensity': intensity,
            'az_r_l': az_r_l,
            'az_r_u': az_r_u,
            'al_r_l': al_r_l,
            'al_r_u': al_r_u
        }
        return {prop: value for prop, value in properties.items() if value is not None}

    def setup_background(self):
        background = self.parameters.get('background')
        if background:
            background_type = self.set_condition_value(('background', 'type'))
            if background_type == 'hdr':
                self.setup_hdr_background()
            elif background_type == 'color':
                self.setup_color_background()
            elif background_type == 'scene':
                self.setup_scene_background()

    def setup_hdr_background(self):
        hdr_path = self.select_resource(['background', 'hdr_parameters'], 'hdr', False)
        announce('Background: {0}'.format(hdr_path.split('/')[-1]))
        strength = self.set_condition_value(('background', 'hdr_parameters', 'strength'))
        hide_background = self.set_condition_value(('background', 'hdr_parameters', 'hide_background'))
        self.blender.set_hdr_background(hdr_path, strength, hide_background)

    def setup_color_background(self):
        color = self.select_color(['background', 'color_parameters'])
        announce('Background color: {0}'.format(color))
        self.blender.set_color_background(color)

    def setup_scene_background(self):
        # TODO model bounds
        scene_path = self.select_resource(['background', 'scene_parameters'], 'blend')
        announce('Background: {0}'.format(scene_path.split('/')[-1]))
        self.scene_name = scene_path.split('/')[-1]
        # self.set_condition_value(('background', 'scene_parameters', 'model_position'))
        self.scale, pivot = self.blender.set_scene_background(scene_path, self.scene_name)

        announce('Background pivot: {0}'.format(pivot))

        # announce('Background list_hide_render: {0}'.format(list_hide_render))
        # announce('Background list_hide: {0}'.format(list_hide))

        name = self.get_condition_value(['background', 'scene_parameters', 'overrides', 'light_color'] + ['name'])

        overrides = get_from_nested_dict(self.render_condition, ('background', 'scene_parameters', 'overrides'))
        if overrides:
            if overrides.get('light_color'):
                if self.scene_color:
                    light_color = self.scene_color
                    announce('Universal color works22 : {0}'.format(light_color))
                else:
                    light_color = self.select_color(['background', 'scene_parameters', 'overrides', 'light_color'])
                    self.scene_color = light_color
                self.light_colors[name] = light_color
                intensity = self.get_condition_value(['background', 'scene_parameters', 'overrides', 'light_color', 'intensity'])
                # self.scene_intensity = intensity
                announce('Background intensity: {0}'.format(intensity))
                counts = self.blender.override_scene_lights(light_color, intensity)
                announce('mat_count : {0}'.format(counts[0]))
                announce('lamp_count: {0}'.format(counts[1]))
                # announce('lamp typess: {0}'.format(counts[2]))
                # announce('ill_locations: {0}'.format(counts[3]))
                self.ill_locations = counts[3]
            if overrides.get('material'):
                # TODO override scene material
                pass

    def setup_camera(self):
        if 'camera' in self.parameters:
            azimuth = self.set_condition_value(('camera', 'azimuth'))
            altitude = self.set_condition_value(('camera', 'altitude'))
            if not azimuth and not altitude:
                az_r_l = self.get_condition_value(['camera'] + ['azimuth_range'] + [0])
                az_r_u = self.get_condition_value(['camera'] + ['azimuth_range'] + [1])
                al_r_l = self.get_condition_value(['camera'] + ['altitude_range'] + [0])
                al_r_u = self.get_condition_value(['camera'] + ['altitude_range'] + [1])
                azimuth = random.uniform(az_r_l,az_r_u)
                altitude = random.uniform(al_r_l,al_r_u)
            view_angle = self.set_condition_value(('camera', 'view_angle'))
            if not view_angle:
                view_angle = np.pi / 4
                self.render_condition['camera']['view_angle'] = view_angle
            
            # radius_factor = self.set_condition_value(('camera', 'radius_factor'))

            whole_mdim = self.blender.model_dimensions(True)
            # announce('Scene whole_mdim: {0}'.format(whole_mdim))
            # whole_mdim = min(whole_mdim)
            # radius_factor = random.uniform(0.25,whole_mdim/3)
            # normalize_radius = self.set_condition_value(('camera', 'normalize_radius'))
            # if normalize_radius:
            #     if model_max_dimension == self.blender.model_dimensions()[0] or model_max_dimension == \
            #             self.blender.model_dimensions()[2]:
            #         model_max_dimension *= 2
            #     model_max_dimension = min(model_max_dimension, 10*10)

            # constraint = whole_mdim/2 if whole_mdim/2 < 4 else 4
            model_max_dimension = max(self.blender.model_dimensions())
            constraint_m = model_max_dimension*3 #if model_max_dimension*1.5 #> 0.75 else 0.75
            if_counter = 0

            multiplier = 1.5

            radius = random.uniform(constraint_m,constraint_m*multiplier) #radius_factor #* model_max_dimension
            self.render_condition['camera']['radius'] = radius
            max_deviation_angle = self.set_condition_value(('camera', 'max_deviation_angle'))
            location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude, radius=radius)
            announce('origin_location: {0}'.format(location))
            model_center = self.blender.model_center()

            # normalize_center = self.set_condition_value(('camera', 'normalize_center'))
            # if normalize_center:
            #     model_center = np.array(model_center)
            #     model_center[model_center > 1] = 0
            #     model_center = model_center.tolist()

            location = tuple(map(add, location, model_center))
            announce('Model center location: {0}'.format(model_center))

            model_cen = [0, 0, 0]

            # squared_dist_w = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
            # dist_w = np.sqrt(squared_dist_w)
            
            squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
            dist_m = np.sqrt(squared_dist_m)
            self.camera_dist = dist_m


            if (dist_m < constraint_m or dist_m > constraint_m*multiplier): # or dist_w > constraint:
                while True:
                    if_counter += 1
                    radius = random.uniform(constraint_m,constraint_m*multiplier) # * model_max_dimension
                    azimuth = random.uniform(az_r_l,az_r_u)
                    altitude = random.uniform(al_r_l,al_r_u)
                    location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude,
                                radius=radius)
                    location = tuple(map(add, location, model_center))
                    # squared_dist_w = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
                    # dist_w = np.sqrt(squared_dist_w)
                    squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
                    dist_m = np.sqrt(squared_dist_m)
                    if (dist_m > constraint_m and dist_m < constraint_m*multiplier): # and dist_w < constraint:
                        break

            rotation = look_at(location, model_center)
            if max_deviation_angle:
                deviation = generate_random_orientation(max_deviation_angle).tolist()
                rotation = quaternion_multiply(rotation, deviation).tolist()
                self.render_condition['camera']['deviation'] = deviation
            self.render_condition['camera']['location'] = location
            self.render_condition['camera']['rotation'] = rotation
            self.render_condition['camera']['azimuth'] = azimuth
            self.render_condition['camera']['altitude'] = altitude
            self.render_condition['camera']['radius'] = radius
            # self.render_condition['camera']['radius_factor'] = radius_factor
            stereo = self.set_condition_value(('camera', 'type')) == 'stereo'
            self.render_condition['output']['stereo'] = stereo
            # rotation = look_at(location, [0,50,50]) ###################################################
            announce('Camera location: {0}, rotation: {1}'.format(location, rotation))
            listi = self.blender.add_camera(rotation, location, view_angle, stereo, radius, model_center, az_r_l, az_r_u, al_r_l, al_r_u, if_counter,\
                                            model_max_dimension)
            counter = listi[0]
            self.bool_chi = listi[1]
            if_counter = listi[2]

            self.camera_data.update({
                'location': listi[5],
                'view_angle': view_angle,
                'rotation': listi[3],
                'stereo': stereo,
                'radius': listi[4],
                'model_center': model_center,
                'az_r_l': az_r_l,
                'az_r_u': az_r_u,
                'al_r_l': al_r_l,
                'al_r_u': al_r_u,
                'if_counter': 0,
                'model_max_dimension': model_max_dimension
            })

            announce('Camera counter: {0}'.format(counter))
            announce('Camera if_counter: {0}'.format(if_counter))
            announce('Camera bool_chi: {0}'.format(self.bool_chi))
            # return bool_chi

    def setup_misc_scripts(self):
        model_grip_flag = self.set_condition_value(('model','grip_flag'))
        if model_grip_flag:
            dist = self.blender.setup_model_grip_points()
            version = self.parameters['version']
            output_path = self.parameters['output_path'] + "/" + "data_log.pickle"
            if not os.path.exists(output_path):
                log_file = {}
            else:
                with open(output_path, 'rb') as log_file_input:
                    log_file = pickle.load(log_file_input)
            log_file[self.index] = {'diametric_distance':dist}
            with open(output_path, "wb") as log_file_output:
                pickle.dump(log_file,log_file_output,protocol=pickle.HIGHEST_PROTOCOL)

    def setup_animation(self):
        animate = self.parameters.get('animate')
        if animate:
            camera = animate.get('camera')
            model = animate.get('model')
            lights = animate.get('lights')
            seconds = self.set_condition_value(('animate', 'seconds'))
            frames = self.set_condition_value(('animate', 'frames'))
            if seconds:
                frames = int(float(seconds) * self.blender.frame_rate())
                self.render_condition['animate']['frames'] = frames
            # self.blender.set_animation_parameters(self.parameters.get('animate'))
            # self.blender.animate_model_curve()
            if camera:

                d_azimuth = self.set_condition_value(('animate', 'camera', 'azimuth'))
                if not d_azimuth:
                    d_azimuth = 0
                new_azimuth = self.render_condition['camera']['azimuth'] + d_azimuth

                d_altitude = self.set_condition_value(('animate', 'camera', 'altitude'))
                if not d_altitude:
                    d_altitude = 0
                new_altitude = self.render_condition['camera']['altitude'] + d_altitude

                d_radius_factor = self.set_condition_value(('animate', 'camera', 'radius_factor'))
                if not d_radius_factor:
                    d_radius_factor = 0
                model_max_dimension = max(self.blender.model_dimensions())
                new_radius_factor = self.render_condition['camera']['radius_factor'] + d_radius_factor
                radius = self.render_condition['camera']['radius']
                new_radius = new_radius_factor #* model_max_dimension
                new_location = AAR_to_XYZ(azimuth=new_azimuth, altitude=new_altitude, radius=new_radius)
                model_center = self.blender.model_center()
                new_rotation = look_at(new_location, model_center)
                deviation = self.render_condition['camera'].get('deviation')
                if deviation:
                    new_rotation = quaternion_multiply(new_rotation, deviation).tolist()
                else:
                    self.blender.track_model()
                self.render_condition['animate']['camera']['location'] = new_location
                self.render_condition['animate']['camera']['rotation'] = new_rotation
                announce('Animation new_location: {0}'.format(new_location))
                announce('Animation new_rotation: {0}'.format(new_rotation))
                self.blender.animate_camera(new_rotation, new_location, radius, new_radius, frames)
            if model:
                mode = self.set_condition_value(('animate','model','mode'))
                keyframes = {}
                if mode == "range":
                    stages = self.set_condition_value(('animate','model','num_stages'))
                    position_range = self.set_condition_value(('animate','model','position_range'))
                    rotation_range = self.set_condition_value(('animate','model','rotation_range'))
                    #Get the frame numbers for keyframes
                    frame_indicies = np.round(np.linspace(0,frames,stages + 1)).astype(int).tolist()
                    for index in frame_indicies:
                        keyframes[index] = {
                            'position': random_float([0,position_range], 3),
                            'rotation': random_float([0,rotation_range], 3)
                        }
                elif mode == "keyframe":
                    keyframesDict = self.set_condition_value(('animate','model','keyframes'))
                    for key in keyframesDict.keys():
                        keyframes[int(key)] = keyframesDict[key]
                self.set_model_keyframes(keyframes)
            if lights:
                # TODO make lights animateable
                raise NotImplementedError

    def set_model_keyframes(self,keyframes):
        for frame_num in keyframes:
            pos = keyframes[frame_num]['position']
            rot = keyframes[frame_num]['rotation']
            self.blender.animate_model(pos,rot,frame_num)

    def render(self, condition='', bool_ch = False):
        output_path = self.parameters['output_path']
        self.output_pathh = output_path
        gpu_index = self.parameters['gpu_index']
        output_parameters = self.parameters['output']
        file_types = output_parameters['file_types']
        filename_params = output_parameters.get('output_filename')
        animate = bool(self.parameters.get('animate'))
        # if animate:
            # self.blender.set_animation_parameters(self.parameters.get('animate'))
        timestamp = time.time()
        self.render_condition['time'] = timestamp
        output_filename = self.get_filename(filename_params, timestamp, condition, animate)
        self.render_condition['output_filename'] = output_filename
        output_file = os.path.join(output_path, output_filename)
        self.output_filee = output_file
        self.render_condition['output_file'] = output_file
        passes = output_parameters['passes']
        res_x = output_parameters['resolution']['x']
        res_y = output_parameters['resolution']['y']
        samples = output_parameters.get('samples', None)
        denoise = output_parameters.get('denoise', True)
        stereo = self.render_condition['output'].get('stereo', False)
        self.render_condition['output']['stereo'] = stereo  # redundant but if no camera specified necessary

        activated_gpus = self.blender.setup_render(res_x, res_y, passes, gpu_index, samples, denoise)
        announce('Render activated_gpus: {0}'.format(activated_gpus))
        self.render_condition['needs_pass_work'] = True
        if 'blend' in file_types:
            blend_file = output_file + '.blend'
            self.blender.save_blend_file(blend_file)
            if len(file_types) == 1:  # only file wanted is blend file
                return
        if 'avi_raw' in file_types:
            avi_raw_file = output_file + '.avi'
            announce('Render filename: {0}'.format(output_filename))
            self.blender.render(avi_raw_file,stereo,animate)
            if len(file_types) == 1:
                self.render_condition['needs_pass_work'] = False
                return
        if 'png' in file_types or 'color' in passes:
            png_file = output_file + '.png'
            announce('Render filename: {0}'.format(output_filename))
            self.blender.render(png_file, stereo, animate, bool_ch)
            if set(file_types).issubset({'blend', 'png'}) and 'png_passes' not in output_parameters:
                self.render_condition['needs_pass_work'] = False
                return
        if self.render_condition['needs_pass_work']:
            exr_file = output_file + '.exr'
            self.blender.render(exr_file, False, animate)

    def get_filename(self, filename_params, timestamp, add_suffix='', animate=False):
        node_name = os.uname()[1]
        pid = os.getpid()
        if animate:
            frame = '.frame.####'
        else:
            frame = ''
        if filename_params:
            marker = '.'
            output_parts = []
            for keys in filename_params:
                if isinstance(keys, string_types):
                    output_value = keys
                else:
                    output_value = get_from_nested_dict(self.render_condition, keys)
                    try:
                        output_value = output_value.replace('/', '')
                    except AttributeError:
                        pass
                    if keys == ['index']:
                        max_digits = len(str(max(self.parameters['index']['total'], self.parameters['index']['max'])))
                        output_value = '{1:0{0}d}'.format(max_digits, output_value)
                output_parts.append(str(output_value))
            if add_suffix!= '':
                output_parts = output_parts+ [add_suffix]
            output_filename = marker.join(output_parts)
        else:
            output_filename = 'time.{0}.pid.{1}.node.{2}{3}'.format(timestamp, pid, node_name, frame)
        return output_filename
