from PIL import Image, ImageChops
from config import numpy as np
from typing import Tuple
from constants import TRANSPARENT
from math import cos, sin, radians, sqrt
import matplotlib.pyplot as plt
from .tools import get_all_files


def compare_images(im1, im2):
    """
    Calculates the mean square
    error (SME) between two images
    """
    errors = (im1 - im2) / 255
    return np.mean(np.square(errors))


def image_fitness_pixel_by_pixel(image1: np.ndarray, image2: np.ndarray):
    """

    """

    error_matrix = np.abs(image1 - image2)
    total_error_num = error_matrix.shape[0] * error_matrix.shape[1] * error_matrix.shape[2]
    mean_error = np.sum(error_matrix)/total_error_num
    fitness = 255 - mean_error
    return fitness

def get_blank_image(size: Tuple[int, int]) -> Image.Image:
    return Image.new('RGBA', size, TRANSPARENT)


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
    return img.rotate(angle, expand=True, fillcolor=TRANSPARENT)


def get_image(path: str, size=None, toRGBA=True):
    img: Image.Image = Image.open(path)
    if toRGBA:
        img = img.convert('RGBA')

    if size:
        img = img.resize(size)
    
    return img
        
def get_raw_image(path: str, size=None, toRGBA=True):
    img = get_image(path, size, toRGBA)
    return np.array(img, dtype='int')


def set_opacity_inplace(img: Image.Image, opacity: float) -> None:
    img.putalpha(int(255 * opacity))


def affine(img: Image.Image, scale_x, scale_y, shift_x, shift_y, new_size):
    new_size = new_size or img.size
    return img.transform(
        new_size, 
        Image.AFFINE, 
        (1 / scale_x, 0, -shift_x, 0, 1 / scale_y, -shift_y),
        fillcolor=TRANSPARENT,
        )


def low_image(img: Image.Image) -> Image.Image:
    """
    TODO: doc string
    """
    new_size = np.array(img.size) // 8

    return img.resize(tuple(new_size))


def compose_in_gif(images, output_file, delay):
    """
    Creates gif from `images`, save it to `output_file`.
    delay between images in gif is `delay`
    """
    images[0].save(
        output_file, 
        format='GIF', append_images=images[1:], 
        save_all=True, duration=delay, loop=0,
        )


def merge_images(images, axis=0):
    """
    Merge all `images` into one image
    according to `axis`
    """
    assert axis in [0, 1]
    total_len = sum(map(lambda i: i.size[axis], images))
    if axis == 0:
        new_shape = (total_len, images[0].size[1])
        step = images[0].size[0]
    else:
        new_shape = (images[0].size[0], total_len)
        step = images[0].size[1]

    canvas = Image.new('RGB', new_shape)

    for i, image in enumerate(images):
        if axis == 0:
            canvas.paste(image, (i * step, 0))
        else:
            canvas.paste(image, (0, i * step))

    return canvas


def create_animation(directory, target_image, output_file):
    filenames = sorted(get_all_files(directory))
    print(filenames)
    images = map(get_image, filenames)
    merged_images = list(map(lambda i: merge_images([target_image, i]), images))
    
    compose_in_gif(merged_images, output_file, 500)


def show_image(img, name):
    plt.imshow(img)
    plt.title(name)
    plt.show()
