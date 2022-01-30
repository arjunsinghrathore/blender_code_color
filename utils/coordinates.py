import numpy as np
from scipy import array, cos, hstack, cross, arccos, dot, sin, pi, arctan2, sqrt, square
from . import transformations
from .selection import random_float

"""
utils for manipulating and converting between coordinate spaces
"""


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


def generate_random_orientation(max_angle):
    """
    Get rotation matrix for rotation within max_angle of all axis
    """

    a_x = random_float((-max_angle, max_angle))
    a_y = random_float((-max_angle, max_angle))
    a_z = random_float((-max_angle, max_angle))

    rand_rot_x = (cos(a_x / 2.), sin(a_x / 2.), 0, 0)
    rand_rot_y = (cos(a_y / 2.), 0, sin(a_y / 2.), 0)
    rand_rot_z = (cos(a_z / 2.), 0, 0, sin(a_z / 2.))

    rand_rot = transformations.quaternion_multiply(rand_rot_x, rand_rot_y)
    rand_rot = transformations.quaternion_multiply(rand_rot, rand_rot_z)

    return rand_rot


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
