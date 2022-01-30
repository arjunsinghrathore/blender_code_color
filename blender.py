#!/usr/bin/env python3
import bpy, bmesh
from mathutils import Vector, Matrix
import os
import numpy as np
import random
from mathutils.geometry import normal
import sys
from mathutils.bvhtree import BVHTree
from operator import add
import math
from numpy import array, cos, hstack, cross, arccos, dot, sin, pi, arctan2, sqrt, square
# from utils.logging import announce

"""
All commands directly to blender
imported into a blender instance using fauxton BlenderModule
"""


# todo maybe remove all bpy.ops and bpy.contexts, everything operate on bpy.data
# todo work out best scene management strategy, (pass around vs. scene = bpy.context.scene)

def setup():
    print ('***************************************')
    """ Setup a new blender scene """
    clear_scene()
    setup_scene()


def clear_scene():
    """ Clears all objects from blender default file """
    # if using blender 2.79 the following line replaces this method
    # bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.wm.read_homefile()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

def only_camera():
    """ Clears all objects from blender default file except Camera"""
    # if using blender 2.79 the following line replaces this method
    # bpy.ops.wm.read_homefile(use_empty=True)
    objs = []
    scene = bpy.context.scene
    for obj in scene.objects:
        objs.append(obj)
    
    bpy.ops.object.select_all(action='DESELECT')
    for b_obj in objs:
        if b_obj.type in ['CAMERA']:
            continue
        b_obj.select = True
        bpy.ops.object.delete()

def only_object():
    """ Clears all objects from blender default file except object"""
    # if using blender 2.79 the following line replaces this method
    # bpy.ops.wm.read_homefile(use_empty=True)
    objs = []
    scene = bpy.context.scene
    for obj in scene.objects:
        if not(obj.name.startswith('object')):
            objs.append(obj)
    # bpy.ops.wm.read_homefile()
    bpy.ops.object.select_all(action='DESELECT')
    for b_obj in objs:
        if b_obj.type in ['CAMERA']:
            continue
        b_obj.select = True
        bpy.ops.object.delete()

    # for material in bpy.data.materials:
    #     # node tree
        
    #     # node_tree = material.node_tree.links
    #     node_tree = material.node_tree
    #     if node_tree is not None:
    #         nodes = node_tree.nodes
    #         # nodes = material.node_tree
    #         # node = nodes.get('Principled BSDF')
    #         for node in nodes:
    #             if node.name == 'Principled BSDF':
    #                 node.inputs[5].default_value = 0
    #                 node.inputs[6].default_value = 0

# def rgb_mask():
#     scene = bpy.context.scene

#     objs = mesh_objects(True)
#     bpy.ops.object.select_all(action='DESELECT')
#     for obj in objs:
#         if obj.type in ['CAMERA', 'LIGHT']:
#             continue
#         scene.objects.active = obj
#         # ** Make your random transforms here ** 
#         RGBMask = bpy.data.materials.new("RGBMask")
#         bpy.context.active_object.data.materials.append(RGBMask)
#         bpy.data.materials["RGBMask"].diffuse_color = 0,0,0
        

#     objs = mesh_objects()
#     bpy.ops.object.select_all(action='DESELECT')
#     for obj in objs:
#         if obj.type in ['CAMERA', 'LIGHT']:
#             continue
#         scene.objects.active = obj
#         # ** Make your random transforms here ** 
#         RGBMask = bpy.data.materials.new("RGBMask")
#         bpy.context.active_object.data.materials.append(RGBMask)
#         bpy.data.materials["RGBMask"].diffuse_color = 1,1,1

# def modify_principled_material_mask():
#     # objects = mesh_indices()
#     # get material
#     for material in bpy.data.materials:
#         # node tree
#         if material.name.startswith('Material'):
#             # node_tree = material.node_tree.links
#             node_tree = material.node_tree
#             if node_tree is not None:
#                 links = node_tree.links
#                 for l in links:
#                     if l.from_node.name == 'Image Texture':
#                         links.remove(l)
#                 nodes = node_tree.nodes
#                 # nodes = material.node_tree
#                 # node = nodes.get('Principled BSDF')
#                 for node in nodes:
#                     try:
#                         node.inputs[0].default_value = [1.0,1.0,1.0,1.0]
#                     except:
#                         pass
        
#         else:
#             # node_tree = material.node_tree.links
#             node_tree = material.node_tree
#             if node_tree is not None:
#                 links = node_tree.links
#                 # for l in links:
#                 #     links.remove(l)
#                 nodes = node_tree.nodes
#                 # nodes = material.node_tree
#                 # node = nodes.get('Principled BSDF')
#                 for node in nodes:
#                     try:
#                         node.inputs[0].default_value = [0,0,0,1.0]
#                     except:
#                         pass


        


# def setup_scene():
#     """ Setup basic scene parameters """
#     scene = bpy.context.scene
#     scene.render.engine = 'CYCLES'
#     scene.world.use_nodes = True
#     scene.cycles.samples = 4000
#     scene.cycles.max_bounces = 500
#     scene.cycles.blur_glossy = 8
#     # scene.cycles.sample_clamp_indirect = 10
#     # scene.cycles.samples = 800
#     scene.cycles.caustics_refractive = False
#     # scene.cycles.use_square_samples = True
#     scene.cycles.progressive = 'BRANCHED_PATH'
#     scene.cycles.aa_samples = 512
#     scene.cycles.diffuse_samples = 12
#     scene.cycles.glossy_samples = 12
#     # scene.cycles.transmission_samples = 2
#     # scene.cycles.ao_samples = 2
#     # scene.cycles.mesh_light_samples = 4
#     # scene.cycles.subsurface_samples = 1
#     # scene.cycles.volume_samples = 1
#     scene.render.resolution_percentage = 100

def setup_scene():
    """ Setup basic scene parameters """
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.world.use_nodes = True
    scene.cycles.samples = 600
    scene.cycles.max_bounces = 20
    scene.cycles.blur_glossy = 8
    # scene.cycles.sample_clamp_indirect = 10
    # scene.cycles.samples = 800
    scene.cycles.caustics_refractive = False
    # scene.cycles.use_square_samples = True
    scene.cycles.progressive = 'BRANCHED_PATH'
    scene.cycles.aa_samples = 512
    scene.cycles.diffuse_samples = 12
    scene.cycles.glossy_samples = 12
    # scene.cycles.transmission_samples = 15
    # scene.cycles.ao_samples = 15
    # scene.cycles.mesh_light_samples = 15
    # scene.cycles.subsurface_samples = 15
    # scene.cycles.volume_samples = 5
    scene.render.resolution_percentage = 100

def setup_scene_mask():
    """ Setup basic scene parameters """
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.world.use_nodes = True
    scene.cycles.samples = 600
    scene.cycles.max_bounces = 20
    scene.cycles.blur_glossy = 8
    # scene.cycles.sample_clamp_indirect = 10
    # scene.cycles.samples = 800
    scene.cycles.caustics_refractive = False
    # scene.cycles.use_square_samples = True
    scene.cycles.progressive = 'BRANCHED_PATH'
    scene.cycles.aa_samples = 512
    scene.cycles.diffuse_samples = 12
    scene.cycles.glossy_samples = 12
    # scene.cycles.transmission_samples = 15
    # scene.cycles.ao_samples = 15
    # scene.cycles.mesh_light_samples = 15
    # scene.cycles.subsurface_samples = 15
    # scene.cycles.volume_samples = 5
    scene.render.resolution_percentage = 100


def env_light(color, strength):
    scene = bpy.context.scene
    scene.world.use_nodes = True
    for n in scene.world.node_tree.nodes:
        if n.name != "World Output" and n.name != "Background":
            scene.world.node_tree.nodes.remove(scene.world.node_tree.nodes[n.name])
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = color
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = strength

def env_white_texture():
    for material in bpy.data.materials:
        # node tree
        # node_tree = material.node_tree.links
        node_tree = material.node_tree
        if node_tree is not None:
            nodes = node_tree.nodes
            # nodes = material.node_tree
            # node = nodes.get('Principled BSDF')
            for node in nodes:
                node.inputs[0].default_value = [1,1,1,1]


def all_items_equal(items):
    """ Are all objects in a list the same """
    return len(set(items)) <= 1


# todo make shape generator functions join dictionary with decorator syntax
def make_shape(shape_name, edge_radius, vertices, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), radius=1):
    """ Add a shape to the blender scene """
    shape_generator = shape_generators[shape_name]
    uniform_proportions = all_items_equal(scale)
    shape_generator(location=location, radius=radius, vertices=vertices,
                    edge_radius=edge_radius, uniform_proportions=uniform_proportions)
    shape = bpy.context.active_object
    shape.select = True
    shape.scale = scale
    shape.name = 'object'
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    shape.rotation_euler = rotation
    shape.select = False


def set_image_material(image_path, roughness, glossiness, object_index):
    material, nodes, links, node_output = setup_baseline_material(object_index)
    node_mix = nodes.new(type='ShaderNodeMixShader')
    node_layer_weight = nodes.new(type='ShaderNodeLayerWeight')
    node_diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    node_gloss = nodes.new(type='ShaderNodeBsdfGlossy')
    node_image = nodes.new(type='ShaderNodeTexImage')
    node_geometry = nodes.new(type='ShaderNodeNewGeometry')

    image_path = os.path.expanduser(image_path)

    node_mix.inputs[0].default_value = glossiness
    node_layer_weight.inputs[0].default_value = glossiness
    node_gloss.inputs[1].default_value = roughness
    node_gloss.inputs[0].default_value = (1, 1, 1, 1)
    node_diffuse.inputs[1].default_value = 0
    node_image.image = bpy.data.images.load(image_path)
    # TODO ask about best projection practice/make parameter?
    node_image.projection = 'SPHERE'
    # node_image.projection = 'TUBE'
    node_image.interpolation = 'Linear'
    node_image.color_space = 'COLOR'
    node_image.extension = 'REPEAT'

    # link nodes
    links.new(node_mix.outputs[0], node_output.inputs[0])
    links.new(node_diffuse.outputs[0], node_mix.inputs[1])
    links.new(node_gloss.outputs[0], node_mix.inputs[2])
    links.new(node_image.outputs[0], node_diffuse.inputs[0])
    links.new(node_geometry.outputs[0], node_image.inputs[0])
    # following link optional: slightly more realistic reflections
    links.new(node_layer_weight.outputs[1], node_mix.inputs[0])


def set_color_material(color, material, roughness, object_name, len_ = 0):
    mat, nodes, links, node_output, len_ = setup_baseline_material(object_name, len_)
    if material == 'matte' or material == 'diffuse':
        node = nodes.new(type='ShaderNodeBsdfDiffuse')
    elif material == 'shiny' or material == 'glossy':
        node = nodes.new(type='ShaderNodeBsdfGlossy')
    elif material == 'glass' or material == 'transparent':
        node = nodes.new(type='ShaderNodeBsdfGlass')
    else:
        raise ValueError('No proper blender material type specified')

    node.inputs[0].default_value = color
    node.inputs[1].default_value = roughness

    # link nodes
    links.new(node.outputs[0], node_output.inputs[0])

#name, 
def set_principled_material(base, color, subsurface, metallic, specular, specular_tint, roughness, anisotropic,
                            anisotropic_rotation, sheen, sheen_tint, clearcoat, clearcoat_roughness, ior, transmission,
                            transmission_roughness, object_index, len_ = 0):
    material, nodes, links, node_output, len_ = setup_baseline_material(object_index, len_)
    # announce('nodes  : {0}'.format(nodes))
    node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    # announce('node_principled  : {0}'.format(node_principled))
    node_principled.distribution = 'GGX'
    if base == 'image':
        node_image = nodes.new(type='ShaderNodeTexImage')
        node_geometry = nodes.new(type='ShaderNodeNewGeometry')
        image_path = os.path.expanduser(color)
        node_image.image = bpy.data.images.load(image_path)
        node_image.projection = 'SPHERE'
        node_image.interpolation = 'Linear'
        node_image.color_space = 'COLOR'
        node_image.extension = 'REPEAT'
        links.new(node_image.outputs[0], node_principled.inputs[0])
        links.new(node_geometry.outputs[0], node_image.inputs[0])
    elif base == 'color':
        node_principled.inputs[0].default_value = color
    # node_principled.inputs[0].default_value = [1.0,1.0,1.0]
    node_principled.inputs[1].default_value = subsurface
    node_principled.inputs[4].default_value = metallic              #0 if metallic < 0.5 else 1
    node_principled.inputs[5].default_value = specular     #0.5 if metallic == 0 else (((ior-1)/(ior+1))**2)/0.08
    node_principled.inputs[6].default_value = specular_tint
    node_principled.inputs[7].default_value = roughness
    node_principled.inputs[8].default_value = anisotropic
    node_principled.inputs[9].default_value = anisotropic_rotation
    node_principled.inputs[10].default_value = sheen
    node_principled.inputs[11].default_value = sheen_tint
    node_principled.inputs[12].default_value = clearcoat
    node_principled.inputs[13].default_value = clearcoat_roughness
    node_principled.inputs[14].default_value = 1.5 if metallic == 0 else ior
    node_principled.inputs[15].default_value = transmission if metallic == 0 else 0
    node_principled.inputs[16].default_value = transmission_roughness if metallic == 0 else 0

    links.new(node_principled.outputs[0], node_output.inputs[0])

    return len_

# def modify_principled_material():
#     # objects = mesh_indices()
#     # get material
#     for material in bpy.data.materials:
#         # node tree
        
#         # node_tree = material.node_tree.links
#         node_tree = material.node_tree
#         if node_tree is not None:
#             links = node_tree.links
#             for l in links:
#                 if l.from_node.name == 'Image Texture':
#                     links.remove(l)
#             nodes = node_tree.nodes
#             # nodes = material.node_tree
#             # node = nodes.get('Principled BSDF')
#             for node in nodes:
#                 if node.name == 'Principled BSDF':
#                     node.inputs[0].default_value = [1.0,1.0,1.0,1.0]


# def modify_principled_material():
#     # objects = mesh_indices()
#     # get material
#     materials = []
#     for material in bpy.data.materials:
#         # node tree
#         materials.append(material.name)
#         if material.name.startswith('Material_ha'):
#             continue
#         # material.diffuse_color = (1,1,1)
#         node_tree = material.node_tree
#         if node_tree is not None:
#             bool_emi = False
#             for n in node_tree.nodes:
#                 if n.type == "EMISSION":
#                     bool_emi = True
#             if not(bool_emi):
#                 links = node_tree.links
#                 for l in links:
#                     # if not(l.from_node.name == 'Image Texture'):
#                         links.remove(l)

    
#     return materials

# def modify_principled_material2():
#     # objects = mesh_indices()
#     # get material
#     materials = []
#     for material in bpy.data.materials:
#         # node tree
#         materials.append(material.name)
#         if material.name.startswith('Material_ha'):
#             continue
#         # material.diffuse_color = (1,1,1)
#         node_tree = material.node_tree
#         if node_tree is not None:
#             bool_emi = False
#             for n in node_tree.nodes:
#                 if n.type == "EMISSION":
#                     bool_emi = True
#                 else:
#                     n.use_custom_color = True
#                     n.color = (1,1,1)
#             # if not(bool_emi):
#             #     links = node_tree.links
#             #     for l in links:
#             #         # if not(l.from_node.name == 'Image Texture'):
#             #             links.remove(l)
#             #     nodes = node_tree.nodes:
                

    
#     return materials

def modify_principled_material():
    objects = mesh_indices2(True)
    # get material
    materials = []
    # for material in bpy.data.materials:
    #     # node tree
    #     materials.append(material.name)
    #     if material.name.startswith('Material_ha'):
    #         continue
    for material in bpy.data.materials:
        bool_remove = True
        if material.name.startswith('Material_ha'):
            bool_remove = False
        node_tree = material.node_tree
        if node_tree is not None:
            for n in node_tree.nodes:
                if n.type == "EMISSION":
                    bool_remove = False
            # links = node_tree.links
            # for l in links:
            #     if not(l.from_node.name == 'Image Texture'):
            #         bool_remove = False
        if bool_remove:
            material.user_clear()
            bpy.data.materials.remove(material)
                

    
    return materials

def modify_principled_material_mask():
    # objects = mesh_indices()
    # get material
    for material in bpy.data.materials:
        # node tree
        if material.name.startswith('Material_ha'):
            node_tree = material.node_tree
            links = node_tree.links
            # for l in links:
            #     links.remove(l)
            for node in node_tree.nodes:
                if node.name == 'Diffuse BSDF':
                    node.inputs[0].default_value = [1,1,1,1]
            
        
        # else:
        #     # node_tree = material.node_tree.links
        #     if material.texture_slots[0]:
        #         for i in range(3):
        #             material.diffuse_color[i] = 1
            
                
        

def setup_baseline_material(object_index, len_):
    obj = bpy.data.objects[object_index]
    obj.select = True
    material = bpy.data.materials.new(name='Material_ha.{0}'.format(object_index))
    # Assign it to object
    if obj.data.materials:
        for i in range(len(obj.data.materials)):
            obj.data.materials[i] = material
    else:
        # no slots
        obj.data.materials.append(material)
    material.use_nodes = True
    # if len_ == -1:
    material.pass_index = len(bpy.data.materials)
    # else:
        # material.pass_index = len_
    nodes = material.node_tree.nodes
    # clear all nodes to start clean
    for node in nodes:
        nodes.remove(node)
    # create nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    links = material.node_tree.links

    return material, nodes, links, node_output, len(bpy.data.materials)


# def add_external_blend_model(blender_file):
#     # loading the materials filename
#     with bpy.data.libraries.load(blender_file) as (data_from, data_to):
#         # all materials available in the file
#         new_objects = data_from.objects
#         num_objects = len(data_from.objects)
#         if num_objects != 1:
#             raise RuntimeError('There should only be one object in file {0}'.format(blender_file))
#
#         # loading all random materials to scene
#         data_to.objects = new_objects
#     scene = bpy.context.scene
#     for index, object in enumerate(data_to.objects):
#         # if doesn't work try this:
#         scene.objects.link(object)

def add_external_materials(material_file):
    for obj in mesh_objects():
        num_object_materials = len(obj.data.materials)

        # loading the materials filename
        with bpy.data.libraries.load(material_file) as (data_from, data_to):
            # all materials available in the file
            num_materials = len(data_from.materials)
            if not num_materials:
                raise RuntimeError('No materials found in material file {0}'.format(material_file))

            new_materials = random.sample(data_from.materials, num_object_materials)

            # loading all random materials to scene
            data_to.materials = new_materials

        for index, material in enumerate(data_to.materials):
            # if doesn't work try this:
            obj.data.materials[index] = material

#show objects that are intersecting
def intersection_check(objects_list, curr_obj):
    #check every object for intersection with every other object
    listt = []
    check = []
    scene =  bpy.context.scene
    for obj_li in objects_list:
            # print()
            # if obj_li == curr_obj:
            #     continue

            #create bmesh objects
            bm1 = bmesh.new()
            bm2 = bmesh.new()

            #fill bmesh data from objects
            bm1.from_mesh(scene.objects[obj_li].data)
            # bm2.from_mesh(scene.objects[curr_obj].data)
            bm2.from_mesh(curr_obj.data)
                   

            #fixed it here:
            bm1.transform(scene.objects[obj_li].matrix_world)
            # bm2.transform(scene.objects[curr_obj].matrix_world) 
            bm2.transform(curr_obj.matrix_world) 

            #make BVH tree from BMesh of objects
            obj_li_BVHtree = BVHTree.FromBMesh(bm1)
            obj_curr_BVHtree = BVHTree.FromBMesh(bm2)           

            #get intersecting pairs
            inter = obj_li_BVHtree.overlap(obj_curr_BVHtree)

            # if obj_li == 'AI48_002_wallsbackground':
            #     check.append(inter)

            #if list is empty, no objects are touching
            if inter != []:
                # print(obj_li + " and " + curr_obj + " are touching!")
                listt.append(obj_li)
                # return obj_li
            # else:
            #     print(obj_li + " and " + curr_obj + " NOT touching!")
            #     # return obj_li
    return listt

def look_at(position, target):
    """
    Taken from the package fauxton written by Mason Mcgill
    Orient the camera towards a point in space.
    """

    def norm(v):
        return sqrt(sum(square(v)))

    def normalize(v):
        return array(v, 'd') / norm(v)

    def rotation(axis, angle):
        w = cos(angle / 2)
        xyz = axis / norm(axis) * sin(angle / 2)
        return hstack([w, xyz])

    def compose(rotation_0, rotation_1):
        w0, x0, y0, z0 = rotation_0
        w1, x1, y1, z1 = rotation_1
        w2 = w0 * w1 - x0 * x1 - y0 * y1 - z0 * z1
        x2 = w0 * x1 + x0 * w1 + y0 * z1 - z0 * y1
        y2 = w0 * y1 + y0 * w1 + z0 * x1 - x0 * z1
        z2 = w0 * z1 + z0 * w1 + x0 * y1 - y0 * x1
        return array([w2, x2, y2, z2])

    target = array(target)
    position = array(position)
    eye = normalize(target - position)
    look_axis = cross((0, 0, -1), eye) if any(eye[:2]) else (1, 0, 0)
    look = rotation(look_axis, arccos(dot((0, 0, -1), eye)))
    pivot = rotation(array((0, 0, -1)), pi / 2 - arctan2(*eye[1::-1]))
    rotation = compose(look, pivot)
    return rotation.tolist()

def AAR_to_XYZ(altitude, azimuth, radius):
    """
    Converts azimuth, altitude and radius to XYZ coordinates
    """
    theta = -altitude + (np.pi / 2)
    return spherical_to_cartesian(radius=radius, theta=theta, phi=azimuth)


def spherical_to_cartesian(radius, theta, phi):
    """
    taken from the program relax http://svn.gna.org/svn/relax/tags/1.3.16/maths_fns/coord_transform.py
    Convert the spherical coordinate vector [r, theta, phi] to the Cartesian vector [x, y, z].
    The parameter r is the radial distance, theta is the polar angle, and phi is the azimuth.
    """
    # Trig alias.
    sin_theta = np.sin(theta)

    cart_vect = np.array([0, 0, 0], dtype='f')
    # The vector.
    cart_vect[0] = radius * np.cos(phi) * sin_theta
    cart_vect[1] = radius * np.sin(phi) * sin_theta
    cart_vect[2] = radius * np.cos(theta)

    return cart_vect.tolist()


def add_light(name, color, intensity, rotation, location=(0, 0, 0), size=1, model_center = 0, radius=0, az_r_l=0, az_r_u=0, al_r_l=0, al_r_u = 0,
                                model_max_dimension = 0, if_counter = 0):
    """ Add a light to the blender scene"""
    bool_checker = True 
    bool_chi = True
    objects_list = mesh_indices(True)
    oniii = mesh_indices2(True)
    counter = 0
    while (bool_checker or bool_chi) and counter<25:
        counter += 1
        scene = bpy.context.scene

        ###########################################################################################################
        ################################Occlude Check##############################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = model_center[0], model_center[1], model_center[2]

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.2, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list != []:
            bool_chi = True
        else:
            bool_chi = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Overlap Check##############################################################
        ###########################################################################################################
        bpy.ops.mesh.primitive_cube_add(location = location, radius = 0.2)
        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name


        inter_list = intersection_check(objects_list, b_obj)

        if inter_list != []:
            bool_checker = True
        else:
            bool_checker = False

        if (bool_checker or bool_chi) and counter != 25:
        
            # bpy.data.objects.remove(lamp_object, do_unlink=True)
            # bpy.data.lamps.remove(lamp_data)

            b_obj.select = True
            bpy.ops.object.delete()
    

            model_cen = [0, 0, 0]

            # location = random_float((1.5,-1.5), 3)
            # location[-1] = abs(location[-1])
            azimuth = random.uniform(az_r_l,az_r_u)
            altitude = random.uniform(al_r_l,al_r_u)
            location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude, radius=radius)
            location = tuple(map(add, location, model_center))

            # squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
            # dist = np.sqrt(squared_dist)

            whole_mdim = min(model_dimensions(True))
            squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
            dist_m = np.sqrt(squared_dist_m)
            # constraint = whole_mdim/2 if whole_mdim/2 < 4 else 4
            constraint_m = model_max_dimension*1.5 #if model_max_dimension*1.5 > 0.75 else 0.75
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

    b_obj.select = True
    bpy.ops.object.delete()
    
    scene = bpy.context.scene

    # Create new lamp datablock
    # lamp_data = bpy.data.lamps.new(name='lamp', type='AREA')
    
    lamp_data = bpy.data.lamps.new(name=name, type='POINT')
    # lamp_data.size = size
    lamp_data.use_nodes = True
    lamp_data.node_tree.nodes['Emission'].inputs[0].default_value = color
    lamp_data.node_tree.nodes['Emission'].inputs[1].default_value = intensity

    lamp_data.cycles.use_multiple_importance_sampling = True

    # Create new object with our lamp datablock
    # lamp_object = bpy.data.objects.new(name='lamp', object_data=lamp_data)
    # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    lamp_object = bpy.data.objects.new(name=name, object_data=lamp_data)
    lamp_object.location = location

    # Link lamp object to the scene so it'll appear in this scene
    scene.objects.link(lamp_object)

    # Place lamp to a specified location
    lamp_object.location = location
    lamp_object.rotation_mode = 'QUATERNION'
    lamp_object.rotation_quaternion = rotation

    # And finally select it make active
    lamp_object.select = True
    scene.objects.active = lamp_object



    return [counter, bool_chi, if_counter, objects_list]


def set_light_properties(name, attribute, value, intensity = 0):
    
    lamp = bpy.data.lamps.get(name)
    if not lamp is None:
        if attribute=='color':
            lamp.node_tree.nodes['Emission'].inputs[0].default_value = value
            # if intensity != 0:
            #     lamp.node_tree.nodes['Emission'].inputs[1].default_value = intensity
            # print(lamp.color)
            # lamp.color = value[:3]
    else:
        print("Lamp does not exist.")
        for mat in bpy.data.materials:
            node_tree = mat.node_tree
            if node_tree:
                for n in node_tree.nodes:
                    if n.type == "EMISSION":
                        for link in n.inputs['Color'].links:
                            print(link)
                            node_tree.links.remove(link)
                        n.inputs['Color'].default_value = value
                        # if intensity != 0:
                        #     for link in n.inputs['Strength'].links:
                        #         print(link)
                        #         node_tree.links.remove(link)
                        #     n.inputs['Strength'].default_value = intensity


def set_hdr_background(hdr_path, hdr_strength, hide_background=False):
    scene = bpy.context.scene
    world = scene.world
    scene.render.engine = 'CYCLES'
    world.use_nodes = True
    nodes = world.node_tree.nodes
    hdr_path = os.path.expanduser(hdr_path)
    # announce('nodes: {0}'.format(nodes))
    env_tex = nodes.new('ShaderNodeTexEnvironment')
    # announce('env_tex: {0}'.format(env_tex))
    env_tex.image = bpy.data.images.load(hdr_path)
    nodes['Background'].inputs[1].default_value = hdr_strength
    world.node_tree.links.new(env_tex.outputs['Color'], nodes['Background'].inputs['Color'])
    if hide_background:
        scene.world.cycles_visibility.camera = False


def set_color_background(color):
    scene = bpy.context.scene
    scene.world.use_nodes = True
    for n in scene.world.node_tree.nodes:
        if n.name != "World Output" and n.name != "Background":
            scene.world.node_tree.nodes.remove(scene.world.node_tree.nodes[n.name])
    scene.world.node_tree.nodes['Background'].inputs[0].default_value = color


def set_scene_background(scene_file, scene_name = "" , light_color=None):
    return add_blend_file(scene_file, scene_name)

def set_scene_background_obj(scene_file, light_color=None):
    bpy.ops.import_scene.obj(filepath=scene_file)
    obj = bpy.context.selected_objects[0]

    obj.name = 'background'
    obj.scale = 2


def override_scene_lights(color, intensity = 0):
    mat_count = 0
    lamp_count = 0
    lamp_types = []
    locations = []
    for mat in bpy.data.materials:
        node_tree = mat.node_tree
        for obj in bpy.data.objects:
            for slot in obj.material_slots:
                if slot.material == mat:
                    location = obj.location
                    location = list(location[:])
        if node_tree:
            for n in node_tree.nodes:
                if n.type == "EMISSION":
                    locations.append(location)
                    for link in n.inputs['Color'].links:
                        print(link)
                        node_tree.links.remove(link)
                    n.inputs['Color'].default_value = color
                    # if True:#intensity != 0:
                    #     mat_count += 1
                    #     for link in n.inputs['Strength'].links:
                    #         print(link)
                    #         node_tree.links.remove(link)
                    #     n.inputs['Strength'].default_value = 30

                    # if n.inputs['Strength'].default_value < 3:
                    #     for link in n.inputs['Strength'].links:
                    #         print(link)
                    #         node_tree.links.remove(link)
                    #     n.inputs['Strength'].default_value = 5
                       

    for lamp in bpy.data.lamps:
        node_tree = lamp.node_tree
        lamp.color = color[0:3]
        for obj in bpy.data.objects:
            if obj.type == 'LAMP':
                if obj.name == lamp.name:
                    location = obj.location
                    location = list(location[:])
        if node_tree:
            for n in node_tree.nodes:
                lamp_types.append(n.type)
                if n.type == "EMISSION":
                    locations.append(location)
                    print(n.inputs['Color'])
                    for link in n.inputs['Color'].links:
                        print(link)
                        node_tree.links.remove(link)
                    n.inputs['Color'].default_value = color
                    # if True:#intensity != 0:
                    #     lamp_count += 1
                    #     for link in n.inputs['Strength'].links:
                    #         print(link)
                    #         node_tree.links.remove(link)
                    #     n.inputs['Strength'].default_value = 30

                    # if n.inputs['Strength'].default_value < 3:
                    #     for link in n.inputs['Strength'].links:
                    #         print(link)
                    #         node_tree.links.remove(link)
                    #     n.inputs['Strength'].default_value = 5

    
    return [mat_count, lamp_count, lamp_types, locations]               
                        


def add_camera(rotation, location, view_angle, stereo=False, radius=1, model_center = 0, az_r_l = 0, az_r_u = 0, al_r_l = 0, al_r_u = 0, \
                if_counter = 0, model_max_dimension = 0):
    # location = [0, 10, 50]
    bool_checker = True 
    bool_chi = True
    bool_chi_z = True
    objects_list = mesh_indices(True)
    counter = 0
    while (bool_checker or bool_chi or bool_chi_z) and counter<25:
        counter += 1
        scene = bpy.context.scene

        ###########################################################################################################
        ################################Out of bounds Check########################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = location[0], location[1], 50

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.05, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list == []:
            bool_chi = True
        else:
            bool_chi = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Out of bounds Check -z########################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = location[0], location[1], -50

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.05, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list == []:
            bool_chi_z = True
        else:
            bool_chi_z = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Occlude Check##############################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = model_center[0], model_center[1], model_center[2]

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.2, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list != []:
            bool_chi = True
        else:
            bool_chi = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Overlap Check##############################################################
        ###########################################################################################################
        bpy.ops.mesh.primitive_cube_add(location = location, radius = 0.2)
        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name
       
        inter_list = intersection_check(objects_list, b_obj)

        if inter_list != []:
            bool_checker = True
        else:
            bool_checker = False

        if (bool_checker or bool_chi or bool_chi_z) and counter < 25:
            # item='CAMERA'
            # bpy.ops.object.select_all(action='DESELECT')
            # bpy.ops.object.select_by_type(type=item)
            # bpy.ops.object.delete()

            b_obj.select = True
            bpy.ops.object.delete()
            
            model_cen = [0, 0, 0]

            azimuth = random.uniform(az_r_l,az_r_u)
            altitude = random.uniform(al_r_l,al_r_u)
            location = AAR_to_XYZ(azimuth=azimuth, altitude=altitude, radius=radius)
            location = tuple(map(add, location, model_center))

            # whole_mdim = min(model_dimensions(True))
            # squared_dist_w = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
            # dist_w = np.sqrt(squared_dist_w)

            squared_dist_m = np.sum((np.array(location)-np.array(model_center))**2, axis=0)
            dist_m = np.sqrt(squared_dist_m)
            # constraint = whole_mdim/2 if whole_mdim/2 < 4 else 4

            multiplier = 1.5

            constraint_m = model_max_dimension*3 #if model_max_dimension*1.5 #> 0.75 else 0.75
            if (dist_m < constraint_m or dist_m > constraint_m*multiplier): # or dist_w > constraint:
                while True:
                    if_counter += 1
                    radius = random.uniform(constraint_m,constraint_m*multiplier)# * model_max_dimension
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
    
    b_obj.select = True
    bpy.ops.object.delete()

    item='CAMERA'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type=item)
    bpy.ops.object.delete()

    if view_angle is None:
        view_angle = np.pi / 4
    scene = bpy.context.scene
    if scene.camera:
        camera = scene.camera
    else:
        bpy.ops.object.camera_add()
        camera = bpy.context.object
    # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    camera.data.clip_start = 0.001
    camera.data.clip_end = 1e+06
    camera.data.lens_unit = 'FOV'
    camera.data.angle = view_angle
    camera.location = location
    camera.rotation_mode = 'QUATERNION'
    camera.rotation_quaternion = rotation
    if stereo:
        camera.data.stereo.convergence_mode = 'TOE'
        camera.data.stereo.convergence_distance = radius
        # TODO convert from blender units to measurable human-like interocular dist/(or not, seems arbitrary)
        camera.data.stereo.interocular_distance = radius / 30.0
        camera.data.stereo.pivot = 'CENTER'

    scene.camera = camera  # defining the active cam for rendering

    return [counter, bool_chi, if_counter, rotation, radius, location]

def track_model():
    scene = bpy.context.scene
    camera = scene.camera
    object = mesh_objects()[0]
    constraint = camera.constraints.new('TRACK_TO')
    constraint.target = object
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

def set_animation_parameters(parameters):
    scene = bpy.context.scene
    scene.frame_start = 0
    scene.frame_end = parameters["frames"]
    scene.render.fps = parameters["fps"]

# def animate_camera(rotation, location, radius_1, radius_2, frame):
#     scene = bpy.context.scene
#     camera = scene.camera
#     target = mesh_objects()[0]
#     scene.frame_start = 0
#     camera.parent = target

#     ######################################################################################
#     ## Add Circle
#     # bpy.ops.curve.primitive_bezier_circle_add(radius=2, location = target.location)
#     # circle = bpy.context.object

#     ## Follow Path Constraint
#     # fp_constraint = camera.constraints.new('FOLLOW_PATH')
#     # fp_constraint.target = circle

#     ######################################################################################
#     # constraint = camera.constraints.new('LIMIT_DISTANCE')
#     # constraint.target = target
#     # constraint.limit_mode = 'LIMITDIST_ONSURFACE'

#     # constraint.distance = radius_1
#     # constraint.keyframe_insert(data_path='distance', frame=0)
#     # constraint.distance = radius_2
#     # constraint.keyframe_insert(data_path='distance', frame=frame)
    
#     ######################################################################################
#     tc = camera.constraints.new(type='TRACK_TO')
#     tc.target = target
#     tc.up_axis = 'UP_Y'
#     tc.track_axis = 'TRACK_NEGATIVE_Z'

#     # camera.keyframe_insert(data_path='location', frame=0)
#     camera.keyframe_insert(data_path='rotation_quaternion', frame=0)
#     # camera.location = location
#     camera.rotation_quaternion = rotation
#     # camera.keyframe_insert(data_path='location', frame=frame)
#     camera.keyframe_insert(data_path='rotation_quaternion', frame=frame)

#     for action in bpy.data.actions:
#         for fcurve in action.fcurves:
#             fcurve.extrapolation = 'LINEAR'
#             for keyframe in fcurve.keyframe_points:
#                 keyframe.interpolation = 'LINEAR'

def animate_camera(rotation, location, radius_1, radius_2, frame):
    scene = bpy.context.scene
    camera = scene.camera
    real_target = mesh_objects()[0]

    bpy.ops.object.empty_add()
    target = bpy.context.active_object
    target.name = 'focus point'
    target.location = real_target.location
    camera.parent = target

    ######################################################################################
    ## Add Circle
    # bpy.ops.curve.primitive_bezier_circle_add(radius=2, location = target.location)
    # circle = bpy.context.object

    ## Follow Path Constraint
    # fp_constraint = camera.constraints.new('FOLLOW_PATH')
    # fp_constraint.target = circle

    ######################################################################################
    # constraint = camera.constraints.new('LIMIT_DISTANCE')
    # constraint.target = target
    # constraint.limit_mode = 'LIMITDIST_ONSURFACE'

    # constraint.distance = radius_1
    # constraint.keyframe_insert(data_path='distance', frame=0)
    # constraint.distance = radius_2
    # constraint.keyframe_insert(data_path='distance', frame=frame)
    
    ######################################################################################
    tc = camera.constraints.new(type='TRACK_TO')
    tc.target = real_target
    tc.up_axis = 'UP_Y'
    tc.track_axis = 'TRACK_NEGATIVE_Z'

    scene.frame_current = 1

    target.rotation_euler = (0,0,0)
    target.keyframe_insert(data_path="rotation_euler")
    scene.frame_current = frame
    target.rotation_euler = (0,0,math.radians(360))
    target.keyframe_insert(data_path="rotation_euler")


    for fc in target.animation_data.action.fcurves:
        fc.extrapolation = 'LINEAR'
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'



def animate_model(position, rotation, frame):
    scene = bpy.context.scene
    anim_target_object = mesh_objects()[0]
    scene.frame_start = 0
    anim_target_object.rotation_mode = 'XYZ'
    anim_target_object.rotation_euler = rotation
    anim_target_object.location = position
    for i in range(0,3):
        anim_target_object.keyframe_insert(data_path='rotation_euler',frame=frame,index=i)
        anim_target_object.keyframe_insert(data_path='location',frame=frame,index=i)


def bezier_step(pt0=Vector(), pt1=Vector(), pt2=Vector(), pt3=Vector(), step=0.0):
    # Return early if step is out of bounds [0, 1].
    if step <= 0.0:
        return pt0.copy()
    if step >= 1.0:
        return pt3.copy()

    # Find coefficients.
    u = 1.0 - step
    tcb = step * step
    ucb = u * u
    tsq3u = tcb * 3.0 * u
    usq3t = ucb * 3.0 * step
    tcb *= step
    ucb *= u

    # Find point and return.
    return pt0 * ucb + pt1 * usq3t + pt2 * tsq3u + pt3 * tcb


def bezier_tangent(pt0=Vector(), pt1=Vector(), pt2=Vector(), pt3=Vector(), step=0.5):
    # Return early if step is out of bounds [0, 1].
    if step <= 0.0:
        return pt1 - pt0
    if step >= 1.0:
        return pt3 - pt2

    # Find coefficients.
    u = 1.0 - step
    ut6 = u * step * 6.0
    tsq3 = step * step * 3.0
    usq3 = u * u * 3.0

    # Find tangent and return.
    return (pt1 - pt0) * usq3 + (pt2 - pt1) * ut6 + (pt3 - pt2) * tsq3



def bezier_multi_seg(knots=[], step=0.0, closed_loop=False):
    knots_len = len(knots)
    if knots_len == 1:
        knot = knots[0]
        coord = knot.co.copy()
        return {'coord': coord, 'tangent': knot.handle_right - coord}

    if closed_loop:
        scaled_t = (step % 1.0) * knots_len
        index = int(scaled_t)
        a = knots[index]
        b = knots[(index + 1) % knots_len]
    else:
        if step <= 0.0:
            knot = knots[0]
            coord = knot.co.copy()
            return {'coord': coord, 'tangent': knot.handle_right - coord}
        if step >= 1.0:
            knot = knots[-1]
            coord = knot.co.copy()
            return {'coord': coord, 'tangent': coord - knot.handle_left}

        scaled_t = step * (knots_len - 1)
        index = int(scaled_t)
        a = knots[index]
        b = knots[index + 1]

    pt0 = a.co
    pt1 = a.handle_right
    pt2 = b.handle_left
    pt3 = b.co
    u = scaled_t - index

    coord = bezier_step(pt0=pt0, pt1=pt1, pt2=pt2, pt3=pt3, step=u)
    tangent = bezier_tangent(pt0=pt0, pt1=pt1, pt2=pt2, pt3=pt3, step=u)
    return {'coord': coord, 'tangent': tangent}

def animate_model_curve(scale):
    # Assumes curve has already been created.
    scene = bpy.context.scene
    curve = scene.objects['random_curve']
    spline = curve.data.splines[0]
    bezier_points = spline.bezier_points
    is_cyclic = spline.use_cyclic_u

    # Create Suzanne monkey head.
    # ops.mesh.primitive_monkey_add()
    suzanne = mesh_objects()[0]
    suzanne.rotation_mode = 'QUATERNION'

    # Create three keyframes for each bezier point.
    key_frame_count = 3.0 * len(bezier_points)
    # scene.frame_start = 0
    # scene.frame_end = frame
    frame_start = scene.frame_start
    frame_end = scene.frame_end
    frame_len = frame_end - frame_start
    frame_skip = int(max(1.0, frame_len / key_frame_count))*2
    frame_range = range(frame_start, frame_end, frame_skip)
    frame_to_percent = 1.0 / frame_len

    for frame in frame_range:
        # Set to current frame.
        scene.frame_set(frame)

        # Calculate coordinates for frame by converting to a percent.
        frame_percent = frame * frame_to_percent
        coord_tangent = bezier_multi_seg(knots=bezier_points,
                                        step=frame_percent,
                                        closed_loop=is_cyclic)

        # Set location.
        coord = coord_tangent['coord']
        suzanne.location = coord
        suzanne.scale = scale
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        suzanne.keyframe_insert(data_path='location')

        # Set rotation based on tangent.
        tangent = coord_tangent['tangent']
        tangent.normalize()
        rotation = tangent.to_track_quat('-Y', 'Z')
        suzanne.rotation_quaternion = rotation
        suzanne.keyframe_insert(data_path='rotation_quaternion')

#This should be abstracted out in some setup script interface as its specific to the projmuticue
def setup_model_grip_points():
    obj = mesh_objects()[0] #Will currently only add grip points to the first mesh
    mesh = obj.data.vertices
    valid_verts = [];
    for vert in mesh:
        if vert.co - bpy.context.scene.camera.location < 0.9*(obj.location - bpy.context.scene.camera.location):
            valid_verts.append(vert.co)
    rand_vert = valid_verts[random.randint(0,len(valid_verts) - 1)]
    to_center = obj.location - rand_vert
    opposite_vert_coors = Vector([0,0,0])
    max_score = 0
    for vert in mesh:
        test_co = vert.co - rand_vert
        score = test_co.dot(to_center)
        if score > max_score:
            max_score = score
            opposite_vert_coors = vert.co
    sphere(location = [0,0,0], radius = 0.2, vertices = 10, edge_radius = 0, uniform_proportions = True)
    grip1 = bpy.context.object
    grip1.parent = obj
    grip1.location = rand_vert
    sphere(location = [0,0,0], radius = 0.2, vertices = 10, edge_radius = 0, uniform_proportions = True)
    grip2 = bpy.context.object
    grip2.parent = obj
    grip2.location = opposite_vert_coors

    mat = bpy.data.materials.new(name="GripMat")

    if grip1.data.materials:
        grip1.data.materials[0] = mat
    else:
        grip1.data.materials.append(mat)
    if grip2.data.materials:
        grip2.data.materials[0] = mat
    else:
        grip2.data.materials.append(mat)

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    # clear all nodes to start clean
    for node in nodes:
        nodes.remove(node)
    # create nodes
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    links = mat.node_tree.links
    node = nodes.new(type='ShaderNodeEmission')

    mat.node_tree.links.new(node_output.inputs['Surface'],node.outputs['Emission'])

    return (grip1.location - grip2.location).magnitude



def save_blend_file(output_file):
    bpy.ops.wm.save_as_mainfile(filepath=output_file)




def setup_render(res_x, res_y, passes, gpu_index=None, samples=None, denoise=True):
    scene = bpy.context.scene
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    if denoise:
        scene.render.layers['RenderLayer'].cycles.use_denoising = True  # TODO make parametrizable
        scene.render.layers['RenderLayer'].cycles.denoising_radius = 2
        scene.render.layers['RenderLayer'].cycles.denoising_feature_strength = 0.6
        scene.render.layers['RenderLayer'].cycles.denoising_strength = 0.6
    if samples:
        scene.cycles.samples = samples
    if gpu_index:
        if res_x >= 256:
            scene.render.tile_x = 256
        else:
            scene.render.tile_x = 128
        if res_y >= 256:
            scene.render.tile_y = 256
        else:
            scene.render.tile_y = 128
    else:
        scene.render.tile_x = 32
        scene.render.tile_y = 32

    # scene.use_nodes = True
    for render_pass in passes:
        if render_pass not in ['color', 'stereo', 'slant', 'tilt']:
            try:
                setattr(scene.render.layers['RenderLayer'], 'use_pass_{0}'.format(render_pass), True)
            except AttributeError:
                print('WARNING: %s is not a proper blender pass.' % render_pass)

    activated_gpus = []

    if gpu_index is not None:
        device_type = "CUDA"
        preferences = bpy.context.user_preferences
        cycles_preferences = preferences.addons["cycles"].preferences
        cuda_devices, opencl_devices = cycles_preferences.get_devices()

        if device_type == "CUDA":
            devices = cuda_devices
        elif device_type == "OPENCL":
            devices = opencl_devices
        else:
            raise RuntimeError("Unsupported device type")

        for device in devices:
            if device.type == "CPU":
                device.use = use_cpus
            else:
                device.use = True
                activated_gpus.append(device.name)

        cycles_preferences.compute_device_type = device_type
        bpy.context.scene.cycles.device = "GPU"

    else:
        context = bpy.context
        preferences = context.user_preferences.addons['cycles'].preferences
        preferences.compute_device_type = 'NONE'
        scene.cycles.device = 'CPU'

    return activated_gpus


def render(output_file, stereo=False, animation=False, bool_ch = False):
    if bool_ch:
        setup_scene_mask()
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links
        # for n in tree.nodes:
        #     tree.nodes.remove(n)
        rl = tree.nodes.new(type="CompositorNodeRLayers")
        # rl = tree.nodes.new(type="CompositorNodeCryptomatte")
        composite = tree.nodes.new(type="CompositorNodeComposite")
        composite.location = 200,0
        scene = bpy.context.scene
        scene.render.filepath = output_file
        # bpy.context.view_layer.cycles.use_pass_crypto_object = True
        # bpy.context.view_layer.cycles.pass_crypto_accurate = True
        # scene.render.layers['RenderLayer'].use_pass_mist = True
        # bpy.context.view_layer.cycles.start = 0
        # bpy.context.view_layer.cycles.pass_crypto_depth = 10
        links.new(rl.outputs['IndexOB'], composite.inputs['Image'])
        # scene.render.image_settings.color_mode = 'BW'
        # scene.view_settings.view_transform = 'Filmic'
        # scene.view_settings.look = 'Filmic - Very High Contrast'
    else:
        setup_scene()
        scene = bpy.context.scene
        # setattr(scene.render.layers['RenderLayer'], 'use_pass_{0}'.format('object_index'), True)
        scene.use_nodes = True
        tree = scene.node_tree
        links = tree.links
        rl = tree.nodes.new(type="CompositorNodeRLayers")
        # rl = tree.nodes.new(type="CompositorNodeCryptomatte")
        composite = tree.nodes.new(type="CompositorNodeComposite")
        composite.location = 200,0
        scene.render.filepath = output_file
        scene.render.image_settings.color_mode = 'RGB'

        ## bpy.types.ColorManagedDisplaySettings.display_device = 'None'
        ## scene.render.image_settings.display_settings = bpy.types.ColorManagedDisplaySettings.display_device
        ## scene.render.image_settings.compression = 100

        # scene.view_settings.view_transform = 'Filmic'

        ## scene.view_settings.look = 'Filmic - Medium Low Contrast'
        ## scene.view_settings.look = 'Filmic - Medium High Contrast'

        # scene.view_settings.look = 'Filmic - Base Contrast'
        scene.view_settings.look = 'None'

        links.new(rl.outputs['Image'], composite.inputs['Image'])

    file_type = output_file.split('.')[-1]
    if animation:
        frame_length = scene.frame_end - scene.frame_start
    if stereo:
        scene.render.use_multiview = True
        scene.render.views["left"].use = True
        scene.render.views["left"].file_suffix = "_L"
        scene.render.views["right"].use = True
        scene.render.views["right"].file_suffix = "_R"
    else:
        scene.render.use_multiview = False
    if file_type == 'exr':
        scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
    elif file_type == 'png':
        scene.render.image_settings.file_format = 'PNG'
    elif file_type == 'avi':
        scene.render.image_settings.file_format = 'FFMPEG'
    bpy.ops.render.render(write_still=True, animation=animation)




def convert_to_meshes():
    """ converts meta objects to meshes """
    scene = bpy.context.scene
    bpy.ops.object.select_all(action='DESELECT')
    for obj in scene.objects:
        if obj.type == 'META':
            mesh = obj.to_mesh(scene, False, 'PREVIEW')

            # add an object
            new_object = bpy.data.objects.new("MBallMesh", mesh)
            scene.objects.link(new_object)
            new_object.matrix_world = obj.matrix_world

            # not keep original
            scene.objects.unlink(obj)
            new_object.select = True
            new_object.name = 'object'
            bpy.ops.object.shade_smooth()
    bpy.ops.object.select_all(action='DESELECT')


def frame_rate():
    return bpy.context.scene.render.fps


def mesh_indices(bool_ch = False):
    """gets the names of the mesh objects in the scene"""
    if bool_ch:
        meshes = []
        scene = bpy.context.scene
        # bpy.ops.object.select_all(action='SELECT')
        for obj in scene.objects:
            if obj.type in ['MESH', 'FONT'] and not(obj.name.startswith('object')):
                meshes.append(obj.name)
    else:
        meshes = []
        scene = bpy.context.scene
        # bpy.ops.object.select_all(action='SELECT')
        for obj in scene.objects:
            if obj.type in ['MESH', 'FONT'] and obj.name.startswith('object'):
                meshes.append(obj.name)
    return meshes

def mesh_indices2(bool_ch = False):
    """gets the names of the mesh objects in the scene"""
    if bool_ch:
        meshes = []
        scene = bpy.context.scene
        # bpy.ops.object.select_all(action='SELECT')
        for obj in scene.objects:
            # if obj.type in ['MESH', 'FONT'] and not(obj.name.startswith('object')):
                meshes.append(obj.name)
    else:
        meshes = []
        scene = bpy.context.scene
        # bpy.ops.object.select_all(action='SELECT')
        for obj in scene.objects:
            if obj.type in ['MESH', 'FONT'] and obj.name.startswith('object'):
                meshes.append(obj.name)
    return meshes


def mesh_objects(bool_ch = False):
    if bool_ch:
        meshes = []
        scene = bpy.context.scene
        for obj in scene.objects:
            if obj.type in ['MESH', 'FONT'] and not(obj.name.startswith('object')):
                meshes.append(obj)
    else:
        meshes = []
        scene = bpy.context.scene
        for obj in scene.objects:
            if obj.type in ['MESH', 'FONT'] and obj.name.startswith('object'):
                meshes.append(obj)
    return meshes



def mesh_count():
    return len(mesh_objects())

def join_models():
    scene = bpy.context.scene
    # bpy.ops.object.select_all(action='SELECT')
    # obj = mesh_objects()[0]
    ctx = bpy.context.copy()

    obs = mesh_objects()

    # one of the objects to join
    ctx['active_object'] = obs[0]

    ctx['selected_objects'] = obs
    # In Blender 2.8x this needs to be the following instead:
    #ctx['selected_editable_objects'] = obs

    # We need the scene bases as well for joining.
    # Remove this line in Blender >= 2.80!
    ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

    bpy.ops.object.join(ctx)


def join_shapes():
    scene = bpy.context.scene
    bpy.ops.object.select_all(action='SELECT')
    obj = mesh_objects()[0]
    obj.name = 'object'
    scene.objects.active = obj
    bpy.ops.object.join()
    bpy.ops.object.select_all(action='DESELECT')


def center_shape():
    for obj in mesh_objects():
        obj.select = True
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        obj.location = (0, 0, 0)
        obj.select = False


def model_bounds(bool_ch = False):
    objects = mesh_objects(bool_ch)
    # objects = mesh_objects(True)
    bounds_list = []
    for obj in objects:
        bounds = [obj.matrix_world * Vector(corner) for corner in obj.bound_box]
        bounds_list.append(np.array([v[:] for v in bounds]))
    all_bounds = np.concatenate(bounds_list, 0)
    return all_bounds.min(0), all_bounds.max(0)

def mesh_objects_box(listt):

    meshes = []
    scene = bpy.context.scene
    for obj in scene.objects:
        if obj.name in listt:
            meshes.append(obj)
    
    return meshes

def model_bounds_box(listt):
    objects = mesh_objects_box(listt)
    max_vol_name = []
    max_vol = -1
    max_vertices = []
    all_volumes = []
    bounding_limits = []
    for obj in objects:
        vertices = [obj.matrix_world * Vector(corner) for corner in obj.bound_box]
        vertices = [v[:] for v in vertices]
        z = abs(vertices[0][2] - vertices[1][2])
        y = abs(vertices[1][1] - vertices[2][1])
        x = abs(vertices[0][0] - vertices[4][0])
        volume = x*y*z
        all_volumes.append(volume)
        if volume > max_vol:# and volume != 0:
            if vertices[0][0]*vertices[4][0]<0.1 and vertices[1][1]*vertices[2][1]<0.1:# and vertices[0][2]*vertices[1][2]<0.1:
                max_vol = volume
                max_vol_name = [obj.name]
                max_vertices = vertices

    bounding_limits = [[max_vertices[0][0], max_vertices[4][0]], [max_vertices[1][1], max_vertices[2][1]], [max_vertices[0][2], max_vertices[1][2]]]
        
    return max_vol_name, max_vertices, bounding_limits


def model_dimensions(bool_ch = False):
    min_bounds, max_bounds = model_bounds(bool_ch)
    dimensions = max_bounds - min_bounds
    dimensions = [float(dim) for dim in dimensions]
    return dimensions


def model_center(bool_ch = False):
    min_bounds, max_bounds = model_bounds(bool_ch)
    coordinates = (max_bounds + min_bounds) / 2
    coordinates = [float(pos) for pos in coordinates]
    return coordinates


def load_blend_file(model_file):
    bpy.ops.wm.open_mainfile(filepath=model_file)


def origin_to_center():
    
    # deselect all of the objects
    bpy.ops.object.select_all(action='DESELECT')


    # loop all scene objects    
    for obj in bpy.context.scene.objects:
        
        # get the meshes
        if obj.type=="MESH":
            
            print(obj)
            
            # select / reset origin / deselect
            obj.select = True
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            obj.select = False
            

# def bound_limitss():
#     scale_max = 30 #np.mean(model_dimensions(True))
#     objects_list = mesh_indices(True)

#     ###########################################################################################################
#     ################################Occlude Check z##############################################################
#     ###########################################################################################################
#     x1, y1, z1 = 0, scale_max, 0
#     x2, y2, z2 = 0, 0, 0

#     dx = x2 - x1
#     dy = y2 - y1
#     dz = z2 - z1    
#     dist = math.sqrt(dx**2 + dy**2 + dz**2)

#     bpy.ops.mesh.primitive_cylinder_add(
#         radius = 0.03, 
#         depth = dist,
#         location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
#     ) 

#     phi = math.atan2(dy, dx) 
#     theta = math.acos(dz/dist) 

#     bpy.context.object.rotation_euler[1] = theta 
#     bpy.context.object.rotation_euler[2] = phi 

#     b_obj_1 = bpy.data.objects[bpy.context.active_object.name]
#     # b_obj.location = location
#     nameee = b_obj_1.name

#     inter_list_1 = intersection_check(objects_list, b_obj_1)

#     b_obj_1.select = True
#     bpy.ops.object.delete()

#     ###########################################################################################################
#     ################################Occlude Check y##############################################################
#     ###########################################################################################################
#     x1, y1, z1 = 0, scale_max, 0
#     x2, y2, z2 = 0, 0, 0

#     dx = x2 - x1
#     dy = y2 - y1
#     dz = z2 - z1    
#     dist = math.sqrt(dx**2 + dy**2 + dz**2)

#     bpy.ops.mesh.primitive_cylinder_add(
#         radius = 0.03, 
#         depth = dist,
#         location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
#     ) 

#     phi = math.atan2(dy, dx) 
#     theta = math.acos(dz/dist) 

#     bpy.context.object.rotation_euler[1] = theta 
#     bpy.context.object.rotation_euler[2] = phi 

#     b_obj_2 = bpy.data.objects[bpy.context.active_object.name]
#     # b_obj.location = location
#     nameee = b_obj_2.name

#     inter_list_2 = intersection_check(objects_list, b_obj_2)

#     b_obj_2.select = True
#     bpy.ops.object.delete()

#     ###########################################################################################################
#     ################################Occlude Check x##############################################################
#     ###########################################################################################################
#     x1, y1, z1 = scale_max, 0, 0
#     x2, y2, z2 = 0, 0, 0

#     dx = x2 - x1
#     dy = y2 - y1
#     dz = z2 - z1    
#     dist = math.sqrt(dx**2 + dy**2 + dz**2)

#     bpy.ops.mesh.primitive_cylinder_add(
#         radius = 0.03, 
#         depth = dist,
#         location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
#     ) 

#     phi = math.atan2(dy, dx) 
#     theta = math.acos(dz/dist) 

#     bpy.context.object.rotation_euler[1] = theta 
#     bpy.context.object.rotation_euler[2] = phi 

#     b_obj_3 = bpy.data.objects[bpy.context.active_object.name]
#     # b_obj.location = location
#     nameee = b_obj_3.name

#     inter_list_3 = intersection_check(objects_list, b_obj_3)

#     b_obj_3.select = True
#     bpy.ops.object.delete()

#     union = Union(inter_list_1, inter_list_2)
#     union = Union(union, inter_list_3)

#     max_vol_name, vertices, bounding_limits = model_bounds_box(union)

#     return [vertices, max_vol_name, bounding_limits, union] #, check_1, check_2, check_3]

def bound_limitss(scene_name = ""):

    objects = mesh_objects(True)

    max_vol_name = []
    max_vol = -1
    max_vol_list = []
    max_vol_name_list = []

    max_vertices = []
    max_vertices_list = []

    vertices_list = []

    all_volumes = []

    bounding_limits = []

    pivot = bpy.context.scene.cursor_location
    pivot = [0, 0, 0] #pivot[:]

    second_bb = ["AI58_006.blend", "AI58_009.blend",  "AI58_004.blend", "AI33_005_280.blend", \
                 "AI33_006_280.blend", "AI33_004_280.blend"]

    manual_names = ["AI043_002_Blender.blend"]
    mesh_names = ["AI43_002_building_wall_001.001background"]

    if scene_name in manual_names:
        man_index = manual_names.index(scene_name)
        obj_man = bpy.data.objects[mesh_names[man_index]]

        vertices = [obj_man.matrix_world * Vector(corner) for corner in obj_man.bound_box]
        vertices = [v[:] for v in vertices]
        vertices_list.append(vertices)
        z = abs(vertices[0][2] - vertices[1][2])
        y = abs(vertices[1][1] - vertices[2][1])
        x = abs(vertices[0][0] - vertices[4][0])
        volume = x*y*z
        all_volumes.append(volume)
        # if volume > max_vol and volume != 0:
        #     if (vertices[0][0]-pivot[0])*(vertices[4][0]-pivot[0]) < 0 and (vertices[1][1]-pivot[1])*(vertices[2][1]-pivot[1]) < 0 : 
        max_vol_list.append(volume)
        max_vol_name_list.append([obj_man.name])
        max_vertices_list.append(vertices)

        max_vol = max_vol_list[0]
        max_vol_name = max_vol_name_list[0]
        max_vertices = max_vertices_list[0]

        bounding_limits = [[max_vertices[0][0], max_vertices[4][0]], [max_vertices[1][1], max_vertices[2][1]], [max_vertices[0][2], max_vertices[1][2]]]

        for i, xyz in enumerate(bounding_limits[:2]):
                if xyz[0] > xyz[1]:
                    bounding_limits[i][0] = bounding_limits[i][0]*0.75
                    bounding_limits[i][1] = bounding_limits[i][1]*1.25
                else:
                    bounding_limits[i][1] = bounding_limits[i][1]*0.75
                    bounding_limits[i][0] = bounding_limits[i][0]*1.25
    else:
        for obj in objects:
            vertices = [obj.matrix_world * Vector(corner) for corner in obj.bound_box]
            vertices = [v[:] for v in vertices]
            vertices_list.append(vertices)
            z = abs(vertices[0][2] - vertices[1][2])
            y = abs(vertices[1][1] - vertices[2][1])
            x = abs(vertices[0][0] - vertices[4][0])
            volume = x*y*z
            all_volumes.append(volume)
            if volume > max_vol and volume != 0:
                if (vertices[0][0]-pivot[0])*(vertices[4][0]-pivot[0]) < 0 and (vertices[1][1]-pivot[1])*(vertices[2][1]-pivot[1]) < 0 : 
                    max_vol_list.append(volume)
                    max_vol_name_list.append([obj.name])
                    max_vertices_list.append(vertices)

        try:
            max_value = max(max_vol_list)
            max_index = max_vol_list.index(max_value)
            # Second bb
            if scene_name in second_bb:
                max_vol_list.remove(max_value)
                max_vol_name_list.remove(max_vol_name_list[max_index])
                max_vertices_list.remove(max_vertices_list[max_index])
                max_value = max(max_vol_list)
                max_index = max_vol_list.index(max_value)
            
            max_vol = max_value
            max_vol_name = max_vol_name_list[max_index]
            max_vertices = max_vertices_list[max_index]
            
            bounding_limits = [[max_vertices[0][0], max_vertices[4][0]], [max_vertices[1][1], max_vertices[2][1]], [max_vertices[0][2], max_vertices[1][2]]]
            
            for i, xyz in enumerate(bounding_limits[:2]):
                if xyz[0] > xyz[1]:
                    bounding_limits[i][0] = bounding_limits[i][0]*0.65 if bounding_limits[i][0] > 0 else bounding_limits[i][0]*1.35
                    bounding_limits[i][1] = bounding_limits[i][1]*1.35 if bounding_limits[i][1] > 0 else bounding_limits[i][1]*0.65
                else:
                    bounding_limits[i][1] = bounding_limits[i][1]*0.65 if bounding_limits[i][1] > 0 else bounding_limits[i][1]*1.35
                    bounding_limits[i][0] = bounding_limits[i][0]*1.35 if bounding_limits[i][0] > 0 else bounding_limits[i][0]*0.65
        except:
            # Default Limits
            bounding_limits = [[-10, 10], [-10, 10], [0, 10]]

    return [max_vertices, max_vol_name, bounding_limits, max_vol_name_list] #, check_1, check_2, check_3]

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def add_blend_file(model_file, scene_name = ""):
    scene = bpy.context.scene

    # with bpy.data.libraries.load(model_file) as (data_from, data_to):
    #     data_to.objects = data_from.objects
    # # link object to current scene
    # for obj in data_to.objects:
    #     # obj.name = 'background_{0}'.format(obj.name)
    #     scene.objects.link(obj)

    # files = []
    # with bpy.data.libraries.load(model_file) as (data_from, data_to):
    #     for name in data_from.objects:
    #         files.append({'name': name})
    # bpy.ops.wm.append(directory=model_file + "/Object/", files=files)

    # with bpy.data.libraries.load(model_file) as (data_from, data_to):
    #     data_to = data_from
    #     for attr in dir(data_to):
    #         setattr(data_to, attr, getattr(data_from, attr))

    with bpy.data.libraries.load(model_file) as (data_from, data_to):
        data_to.objects = data_from.objects

    # link object to current scene
    for obj in data_to.objects:
        obj.name = obj.name + 'background'
        scene.objects.link(obj)
        # x, y, z = obj.scale
        # obj.scale = [x/10, y/10, z/10]
        # bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)

    
    # Scaling based on interior
    limtss = bound_limitss(scene_name)
    # limtss = limtss[0]
    # limtss = [abs(l) for v in limtss for l in v]
    limtss = limtss[2]
    limtss = [abs(l[0]-l[1]) for l in limtss]
    
    scale_mean = max(limtss) #sum(limtss)/len(limtss)

    size_list = ["AI58_003.blend"]

    if scene_name in size_list:
        scalee = scale_mean/15.0  # Bigger the denominator bigger the scale of the scenes
    else:
        scalee = scale_mean/25.0  # Bigger the denominator bigger the scale of the scenes
    
    context = bpy.context
    scale_factor = 1/scalee
    angle = 0

    scene = context.scene
    pivot = scene.cursor_location

    objects = mesh_objects(True)
    
    for ob in objects:
        M = (
            Matrix.Translation(pivot) *
            Matrix.Scale(scale_factor, 4, (0, 1, 0)) *
            Matrix.Scale(scale_factor, 4, (1, 0, 0)) *
            Matrix.Scale(scale_factor, 4, (0, 0, 1)) *
            Matrix.Rotation(angle, 4, (0, 0, 1)) *       
            Matrix.Translation(-pivot)
            )
        ob.matrix_world = M * ob.matrix_world

    return scalee, pivot[:]

def random_float(data_range, dim=1):
    """
    Generate a single random float or a list of them, according to dim
    """
    values = [random.uniform(data_range[0], data_range[1]) for _ in range(dim)]
    if dim == 1:
        values = values[0]
    return values


def add_blend_model(model_file, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), animate = False):
    scene = bpy.context.scene
    with bpy.data.libraries.load(model_file) as (data_from, data_to):
        data_to.objects = data_from.objects
    
    objects_list = mesh_indices(True)
    # bool_checker = True
    counters = []

    # link object to current scene
    for ii, obj_it in enumerate(data_to.objects):
      counter = 0
      bool_checker = True
      bool_anim = False
      while (bool_checker or bool_anim) and counter<25:
        counter += 1
        if obj_it is not None and obj_it.type == 'MESH':
            obj = obj_it.copy()
            obj.data = obj_it.data.copy()
            obj.select = True
            obj.name = 'object'
            scene.objects.link(obj)
            # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            # obj.scale = [max(obj.dimensions)] * 3 #TODO figure out why i did this
            # bpy.ops.object.transform_apply(scale=True)

            ######################################Make Random Curve---> If Animate#############################################
            if animate:
                # # Create bevel control curve.
                # ops.curve.primitive_bezier_circle_add(radius=0.5, enter_editmode=True)
                # ops.curve.subdivide(number_cuts=4)
                # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
                # bevel_control = context.active_object
                # bevel_control.data.name = bevel_control.name = 'Bevel Control'

                # # Set the main curve's bevel control to the bevel control curve.
                # obj_data.bevel_object = bevel_control
                # ops.object.mode_set(mode='OBJECT')

                # # Create taper control curve.
                # ops.curve.primitive_bezier_curve_add(enter_editmode=True)
                # ops.curve.subdivide(number_cuts=3)
                # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
                # taper_control = context.active_object
                # taper_control.data.name = taper_control.name = 'Taper Control'

                # # Set the main curve's taper control to the taper control curve.
                # obj_data.taper_object = taper_control
                # ops.object.mode_set(mode='OBJECT')

                # Create a bezier circle and enter edit mode.
                bpy.ops.curve.primitive_bezier_circle_add(radius=0.07,
                                                    location=location,
                                                    enter_editmode=True)

                # Subdivide the curve by a number of cuts, giving the
                # random vertex function more points to work with.
                bpy.ops.curve.subdivide(number_cuts=16)

                # Randomize the vertices of the bezier circle.
                # offset [-inf .. inf], uniform [0.0 .. 1.0],
                # normal [0.0 .. 1.0], RNG seed [0 .. 10000].
                bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.0, seed=0)

                # Scale the curve while in edit mode.
                bpy.ops.transform.resize(value=(1.0, 1.0, 2.0))

                # Return to object mode.
                bpy.ops.object.mode_set(mode='OBJECT')

                # Store a shortcut to the curve object's data.
                obj_data = bpy.context.active_object
                obj_data.data.name = obj_data.name = 'random_curve'
                animate_model_curve(scale)

                # Convert from a curve to a mesh.
                bpy.ops.object.convert(target='MESH')

                inter_list = intersection_check(objects_list, obj_data)

                if inter_list != []:
                    bool_anim = True
                else:
                    bool_anim = False
            else:
                obj.rotation_euler = rotation
                obj.location = location
                obj.scale = scale
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
            # obj.scale = scale
            # bpy.context.scene.objects.active.scale = scale
            # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            obj.select = False


            ######################################################################################################################

            inter_list = intersection_check(objects_list, obj)

            if inter_list != []:
                bool_checker = True
            else:
                bool_checker = False

            if (bool_checker or bool_anim) and counter != 25:

                location = random_float((1.5,-1.5), 3)
                location[-1] = abs(location[-1])
                model_cen = [0, 0, 0]
                whole_mdim = min(model_dimensions(True))
                squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
                dist = np.sqrt(squared_dist)
                constraint = whole_mdim/2 if whole_mdim/2 > 2 else 2
                if dist > constraint:
                    while True:
                        location = random_float((1.5,-1.5), 3)
                        location[-1] = abs(location[-1])
                        squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
                        dist = np.sqrt(squared_dist)
                        if dist < constraint:
                            break
                # location = tuple(map(add, location, coordinates))
                # rotation = look_at(location, model_center)
            bpy.data.objects.remove(obj, do_unlink=True)
            if animate:
                obj_data.select = True
                bpy.ops.object.delete()
        else:
            break
      counters.append(counter)
      break

    for ii, obj_it in enumerate(data_to.objects):
        if obj_it is not None and obj_it.type == 'MESH':
            obj = obj_it.copy()
            obj.data = obj_it.data.copy()
            obj.select = True
            obj.name = 'object'
            scene.objects.link(obj)
            # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
            # obj.scale = [max(obj.dimensions)] * 3 #TODO figure out why i did this
            # bpy.ops.object.transform_apply(scale=True)
            if animate:
                obj.rotation_euler = rotation
            else:
                obj.rotation_mode = 'QUATERNION'

            if animate:
                # # Create bevel control curve.
                # ops.curve.primitive_bezier_circle_add(radius=0.5, enter_editmode=True)
                # ops.curve.subdivide(number_cuts=4)
                # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
                # bevel_control = context.active_object
                # bevel_control.data.name = bevel_control.name = 'Bevel Control'

                # # Set the main curve's bevel control to the bevel control curve.
                # obj_data.bevel_object = bevel_control
                # ops.object.mode_set(mode='OBJECT')

                # # Create taper control curve.
                # ops.curve.primitive_bezier_curve_add(enter_editmode=True)
                # ops.curve.subdivide(number_cuts=3)
                # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
                # taper_control = context.active_object
                # taper_control.data.name = taper_control.name = 'Taper Control'

                # # Set the main curve's taper control to the taper control curve.
                # obj_data.taper_object = taper_control
                # ops.object.mode_set(mode='OBJECT')

                # Create a bezier circle and enter edit mode.
                bpy.ops.curve.primitive_bezier_circle_add(radius=0.07,
                                                    location=location,
                                                    enter_editmode=True)

                # Subdivide the curve by a number of cuts, giving the
                # random vertex function more points to work with.
                bpy.ops.curve.subdivide(number_cuts=16)

                # Randomize the vertices of the bezier circle.
                # offset [-inf .. inf], uniform [0.0 .. 1.0],
                # normal [0.0 .. 1.0], RNG seed [0 .. 10000].
                bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.0, seed=0)

                # Scale the curve while in edit mode.
                bpy.ops.transform.resize(value=(1.0, 1.0, 2.0))

                # Return to object mode.
                bpy.ops.object.mode_set(mode='OBJECT')

                # Store a shortcut to the curve object's data.
                obj_data = bpy.context.active_object
                obj_data.data.name = obj_data.name = 'random_curve'
                animate_model_curve(scale)
            else:
                obj.rotation_euler = rotation
                obj.location = location
                obj.scale = scale
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            # obj.location = location
            # obj.scale = scale
            # bpy.context.scene.objects.active.scale = scale
            # obj.rotation_euler = rotation
            # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            obj.select = False

        break


    join_models()
    
    return counters
    

def add_obj_model(model_file, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.import_scene.obj(filepath=model_file)
    obj = bpy.context.selected_objects[0]

    # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    obj.name = 'object'
    obj.scale = [max(obj.dimensions)] * 3
    bpy.ops.object.transform_apply(scale=True)
    obj.location = location
    obj.scale = scale
    obj.rotation_euler = rotation
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.select = False

# def select_mod_position():
#         whole_mdim = model_dimensions(True)

#         position = [] 

#         for mdim in whole_mdim:
#             temp = mdim/4
#             if temp < 0.5:
#                 temp = 0.5
#             if temp > 4:
#                 temp = 4
#             position.append(random.uniform(-temp,temp))

#         return position

def select_mod_position(bound_limit):
        whole_mdim = bound_limit[2]

        position = []

        for i in range(3):
            if whole_mdim[i][0] < whole_mdim[i][1]:
                position.append(random.uniform(whole_mdim[i][0],whole_mdim[i][1]))
            else:
                position.append(random.uniform(whole_mdim[i][1],whole_mdim[i][0]))

        return position

def add_stl_model(model_file, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), animate = False, bound_limit = 0, ill_locations = 0):
    # location = [0, 0.5, 0]
    
    objects_list = mesh_indices(True)
    counters = []
    counter = 0
    bool_checker = True
    bool_chi = False
    bool_chi_z = False
    bool_nearby = False
    bool_anim = False

    while (bool_checker or bool_anim or bool_chi or bool_chi_z or bool_nearby) and counter<25:
        counter += 1
        bpy.ops.import_mesh.stl(filepath=model_file)
        obj = bpy.context.selected_objects[0]

        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
        obj.name = 'object'
        

        if animate:
            # # Create bevel control curve.
            # ops.curve.primitive_bezier_circle_add(radius=0.5, enter_editmode=True)
            # ops.curve.subdivide(number_cuts=4)
            # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
            # bevel_control = context.active_object
            # bevel_control.data.name = bevel_control.name = 'Bevel Control'

            # # Set the main curve's bevel control to the bevel control curve.
            # obj_data.bevel_object = bevel_control
            # ops.object.mode_set(mode='OBJECT')

            # # Create taper control curve.
            # ops.curve.primitive_bezier_curve_add(enter_editmode=True)
            # ops.curve.subdivide(number_cuts=3)
            # ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=1.0, seed=0)
            # taper_control = context.active_object
            # taper_control.data.name = taper_control.name = 'Taper Control'

            # # Set the main curve's taper control to the taper control curve.
            # obj_data.taper_object = taper_control
            # ops.object.mode_set(mode='OBJECT')

            # Create a bezier circle and enter edit mode.
            bpy.ops.curve.primitive_bezier_circle_add(radius=0.07,
                                                location=location,
                                                enter_editmode=True)

            # Subdivide the curve by a number of cuts, giving the
            # random vertex function more points to work with.
            bpy.ops.curve.subdivide(number_cuts=16)

            # Randomize the vertices of the bezier circle.
            # offset [-inf .. inf], uniform [0.0 .. 1.0],
            # normal [0.0 .. 1.0], RNG seed [0 .. 10000].
            bpy.ops.transform.vertex_random(offset=1.0, uniform=0.1, normal=0.0, seed=0)

            # Scale the curve while in edit mode.
            bpy.ops.transform.resize(value=(1.0, 1.0, 2.0))

            # Return to object mode.
            bpy.ops.object.mode_set(mode='OBJECT')

            # Store a shortcut to the curve object's data.
            obj_data = bpy.context.active_object
            obj_data.data.name = obj_data.name = 'random_curve'
            animate_model_curve(scale)

            # Convert from a curve to a mesh.
            bpy.ops.object.convert(target='MESH')

            inter_list = intersection_check(objects_list, obj_data)

            if inter_list != []:
                bool_anim = True
            else:
                bool_anim = False
        else:
            # obj.scale = [max(obj.dimensions)] * 3
            bpy.ops.object.shade_smooth()
            bpy.ops.object.transform_apply(scale=True)
            obj.location = location  # [0,0, 7]
            obj.scale = scale
            obj.rotation_euler = rotation
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
        
        obj.select = False

        ###########################################################################################################
        ################################Out of bounds Check +z ####################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = location[0], location[1], 50

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.05, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list == []:
            bool_chi = True
        else:
            bool_chi = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Out of bounds Check -z ####################################################
        ###########################################################################################################
        x1, y1, z1 = location[0], location[1], location[2]
        x2, y2, z2 = location[0], location[1], -50

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1    
        dist = math.sqrt(dx**2 + dy**2 + dz**2)

        bpy.ops.mesh.primitive_cylinder_add(
            radius = 0.05, 
            depth = dist,
            location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
        ) 

        phi = math.atan2(dy, dx) 
        theta = math.acos(dz/dist) 

        bpy.context.object.rotation_euler[1] = theta 
        bpy.context.object.rotation_euler[2] = phi 

        b_obj = bpy.data.objects[bpy.context.active_object.name]
        # b_obj.location = location
        nameee = b_obj.name

        inter_list = intersection_check(objects_list, b_obj)

        if inter_list == []:
            bool_chi_z = True
        else:
            bool_chi_z = False

        b_obj.select = True
        bpy.ops.object.delete()

        ###########################################################################################################
        ################################Distance from other meshes#################################################
        ###########################################################################################################
        dist = []
        # directions = np.array([0, 0, 0])
        
        scene = bpy.context.scene
        for iter_obj in scene.objects:
            if iter_obj.type in ['MESH', 'FONT'] and not(iter_obj.name.startswith('object')):
                dist.append((Vector(location)-iter_obj.location).length)
                # directions += np.array((Vector(location)-iter_obj.location)[:])
        
        dist = sorted(dist)

        for dis in dist[:10]:
            if dis < 7.5:
                bool_nearby = False
            else:
                bool_nearby = True
                break


        ######################################################################################################################

        inter_list = intersection_check(objects_list, obj)

        if inter_list != []:
            bool_checker = True
        else:
            bool_checker = False

        if (bool_checker or bool_anim or bool_chi or bool_chi_z or bool_nearby) and counter != 25:

            bpy.data.objects.remove(obj, do_unlink=True)
            # whole_mdim = min(model_dimensions(True))
            location = select_mod_position(bound_limit)
            # location[-1] = abs(location[-1])

            # model_cen = [0, 0, 0]
            
            # squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
            # dist = np.sqrt(squared_dist)
            # constraint = whole_mdim/4 if whole_mdim/4 < 4 else 4
            # if dist > constraint:
            #     while True:
            #         location = select_mod_position(bound_limit)
            #         # location[-1] = abs(location[-1])
            #         squared_dist = np.sum((np.array(location)-np.array(model_cen))**2, axis=0)
            #         dist = np.sqrt(squared_dist)
            #         if dist < constraint:
            #             break

            # location = tuple(map(add, location, coordinates))
            # rotation = look_at(location, model_center)
        # bpy.data.objects.remove(obj, do_unlink=True)
        # if animate:
        #     obj_data.select = True
        #     bpy.ops.object.delete()

    counters.append(counter)

    return [counters, location, dist]


def add_text_model(body, depth=.1, bevel_depth=0, bevel_resolution=0, font_file=None, location=(0, 0, 0),
                   rotation=(0, 0, 0),
                   scale=(1, 1, 1)):
    scene = bpy.context.scene
    bpy.ops.object.text_add()
    obj = bpy.context.active_object
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'
    obj.data.body = body
    obj.data.extrude = depth  # 0-.5
    obj.data.bevel_depth = bevel_depth  # 0-.04
    obj.data.bevel_resolution = bevel_resolution  # 0-5
    if font_file:
        font_file = os.path.expanduser(font_file)
        obj.data.font = bpy.data.fonts.load(font_file)
    obj.name = 'object'
    obj.location = location
    obj.scale = scale
    rotation_list = list(rotation)
    rotation_list[0] += (3.14159 / 2)
    rotation_list[2] += (3.14159 / 2)
    obj.rotation_euler = rotation_list
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # obj.select = True
    # mesh = obj.to_mesh(scene, False, 'PREVIEW')
    # scene.objects.unlink(obj)
    # new_object = bpy.data.objects.new("textMesh", mesh)
    # scene.objects.link(new_object)
    # new_object.matrix_world = obj.matrix_world
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # obj.select = False
    # new_object.select = True
    # new_object.name = 'object'
    bpy.ops.object.shade_smooth()
    # new_object.location = location
    # new_object.scale = scale
    # rotation_list = list(rotation)
    # rotation_list[0] += (3.14159 / 2)
    # rotation_list[2] += (3.14159 / 2)
    # new_object.rotation_euler = rotation_list
    # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def finish_model():
    for index, obj in enumerate(mesh_objects()):
        if index == 0:
            obj.name = 'object'
        else:
            obj.name = 'object.{0}'.format(index)
        obj.pass_index = 1


def cube(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.mesh.primitive_cube_add(radius=radius, location=location)
    bevel_edges(edge_radius)


def sphere(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.mesh.primitive_uv_sphere_add(size=radius, location=location, segments=vertices, ring_count=vertices)
    bpy.ops.object.shade_smooth()


def cylinder(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, location=location, vertices=vertices)
    bevel_edges(edge_radius)
    bpy.ops.object.shade_smooth()


def torus(location, radius, vertices, edge_radius, uniform_proportions):
    minor_radius = radius / 2 if uniform_proportions else jittered(radius / 2, radius / 6)
    bpy.ops.mesh.primitive_torus_add(major_radius=radius, minor_radius=minor_radius,
                                     location=location, major_segments=vertices, minor_segments=vertices)
    bpy.ops.object.shade_smooth()


def cone(location, radius, vertices, edge_radius, uniform_proportions):
    depth = radius if uniform_proportions else jittered(radius, radius / 3)
    bpy.ops.mesh.primitive_cone_add(radius1=radius, depth=depth, location=location,
                                    vertices=vertices)
    bevel_edges(edge_radius)
    bpy.ops.object.shade_smooth()


def meta_ball(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.object.metaball_add(type='BALL', radius=radius, location=location)
    meta_setup()


def meta_capsule(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.object.metaball_add(type='CAPSULE', radius=radius, location=location)
    meta_setup()


def meta_cube(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.object.metaball_add(type='CUBE', radius=radius, location=location)
    meta_setup()


def meta_ellipsoid(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.object.metaball_add(type='ELLIPSOID', radius=radius, location=location)
    meta_setup()


def meta_plane(location, radius, vertices, edge_radius, uniform_proportions):
    bpy.ops.object.metaball_add(type='PLANE', radius=radius, location=location)
    meta_setup()


shape_generators = {'cube': cube,
                    'sphere': sphere,
                    'cylinder': cylinder,
                    'torus': torus,
                    'cone': cone,
                    'meta_ball': meta_ball,
                    'meta_capsule': meta_capsule,
                    'meta_cube': meta_cube,
                    'meta_ellipsoid': meta_ellipsoid,
                    'meta_plane': meta_plane}


def meta_setup():
    bpy.context.object.data.render_resolution = .05
    bpy.context.object.data.resolution = .05
    # meta objects are slightly larger than normal objects
    # and are scaled down a little extra
    obj = bpy.context.active_object
    obj.scale = (.65, .65, .65)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def bevel_edges(edge_radius):
    if edge_radius > 0:
        obj = bpy.context.active_object
        bevel = obj.modifiers.new(name='bevel', type='BEVEL')
        bevel.limit_method = 'ANGLE'
        bevel.width = edge_radius
        bevel.segments = 20
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier='bevel')
        bpy.ops.object.shade_smooth()


def jittered(mean, maxdiff):
    return np.random.uniform(mean - maxdiff, mean + maxdiff)
