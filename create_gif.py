from tools.image import create_animation
from config import OUTPUT_DIR, SIZE
from tools.image import get_image
import sys
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--images', required=True,
        help='path to directory with images',
    )
    parser.add_argument(
        '-t', '--target', required=True,
        help='path to target image',
    )
    parser.add_argument(
        '-o', '--output',
        help='output file',
    )

    args = parser.parse_args()
    if not args.output:
        target_name = os.path.splitext(os.path.basename(args.target))[0]
        filename = f"{target_name}.gif"
        args.output = os.path.join(OUTPUT_DIR, filename)

    return args

args = parse_arguments()
target_image = get_image(args.target, SIZE)
create_animation(args.images, target_image, args.output)
