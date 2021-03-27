from PIL import Image, ImageChops
import numpy as np
from typing import Tuple
from constants import WHITE, BLACK
from math import cos, sin, radians, sqrt

def compare_images(im1, im2):
    """
    Calculates the root mean square
    error (RSME) between two images
    """
    errors = np.asarray(ImageChops.difference(im1, im2)) / 255
    return sqrt(np.mean(np.square(errors)))


def get_blank_image(size: Tuple[int, int]) -> Image.Image:
    return Image.new('RGBA', size, WHITE)


def apply_matrix(img: Image.Image, x, y, rotation, scale) -> Image.Image:
    # translate
    T_move = np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]])
    # rotate - opposite angle
    a = radians(rotation)
    T_rotate = np.array([
        [cos(a), -sin(a), 0],
        [sin(a), cos(a), 0],
        [0, 0, 1]])
    
    # scale
    T_scale = np.array([
        [scale, 0, 0],
        [0, scale, 0],
        [0, 0, 1]])

    T = T_move @ T_scale @ T_rotate
    
    T_inv = np.linalg.inv(T)
    return img.transform(img.size, Image.AFFINE, data=T_inv.flatten()[:6], resample=Image.NEAREST)


def alpha_rotate(img: Image.Image, angle: int) -> Image.Image:
    return img.rotate(angle, expand=True, fillcolor=WHITE)


def get_image(path: str, size=(512, 512), toRGBA=True) -> Image.Image:
    img: Image.Image = Image.open(path)
    if toRGBA:
        img = img.convert('RGBA')

    if size:
        return img.resize(size)
    else:
        return img
        

def set_opacity_inplace(img: Image.Image, opacity: float) -> None:
    img.putalpha(int(255 * opacity))


def affine(img: Image.Image, scale_x, scale_y, shift_x, shift_y, new_size):
    new_size = new_size or img.size
    return img.transform(
        new_size, 
        Image.AFFINE, 
        (1 / scale_x, 0, -shift_x, 0, 1 / scale_y, -shift_y),
        fillcolor=WHITE,
        )
