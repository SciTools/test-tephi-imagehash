#!/usr/bin/env python

import os
from glob import glob


BASE = os.path.dirname(os.path.abspath(__file__))
DIR_IMAGES = os.path.join(BASE, "images")
FNAME_MANIFEST = os.path.join(BASE, "image_manifest.txt")


def image_fnames():
    fglob = glob(os.path.join(DIR_IMAGES, "*.png"))
    return sorted([os.path.basename(fname) for fname in fglob])


def manifest_fnames():
    result = []

    if os.path.isfile(FNAME_MANIFEST):
        with open(FNAME_MANIFEST, "r") as fi:
            result = [line.strip() for line in fi.readlines()] 

    return result


def create_image_manifest():
    with open(FNAME_MANIFEST, "w") as fo:
        [fo.write(f"{fname}\n") for fname in image_fnames()]


if __name__ == "__main__":
    create_image_manifest()
