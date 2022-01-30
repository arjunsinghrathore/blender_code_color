import colorsys
import math
import numpy as np

"""
utils for converting between color spaces
"""

RGB_to_XYZ_MATRIX = [[0.4124564, 0.3575761, 0.1804375],
                     [0.2126729, 0.7151522, 0.0721750],
                     [0.0193339, 0.1191920, 0.9503041]]


def HSL_to_RGBA(hue, saturation, lightness):
    """
    Converts HSL color to RGBA
    """
    color = list(colorsys.hls_to_rgb(hue, lightness, saturation))
    color.append(1)
    return color


def HSV_to_RGBA(hue, saturation, value):
    """
    Converts HSV color to RGBA
    """
    color = list(colorsys.hsv_to_rgb(hue, saturation, value))
    color.append(1)
    return color


def apply_color_transform(image, transform):
    """
    applys a 3x3 color transformation matrix to image
    """
    reshaped = image.reshape((image.shape[0] * image.shape[1], image.shape[2]))
    result = np.dot(transform, reshaped.T).T.reshape(image.shape)
    return result


def RGB_to_XYZ(image):
    return apply_color_transform(image, RGB_to_XYZ_MATRIX)


def kelvin_to_RGBA(color_temperature):
    """
    adapted from: https://gist.github.com/petrklus/b1f427accdf7438606a6
    Based on: http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    converts color temperature to RGBA
    """
    # modified to return in range (0,1)
    # range check
    if color_temperature < 1000:
        color_temperature = 1000
    elif color_temperature > 40000:
        color_temperature = 40000

    tmp_internal = color_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red
    red /= 255.0

    # green
    if tmp_internal <= 66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    green /= 255.0

    # blue
    if tmp_internal >= 66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue
    blue /= 255.0

    return [red, green, blue, 1]
