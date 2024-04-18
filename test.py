import json
import rawpy
import imageio
import numpy as np

from channel_transform import channel_transform
from params import Params

filepath = "/Users/moishe/Pictures/2024/2024-04-15/DSCF4762.RAF"
with rawpy.imread(filepath) as raw:
    rgb = raw.postprocess()

    fs_rgb = channel_transform(rgb, Params())
    fs_rgb = fs_rgb / fs_rgb.max() * 255.0
    fs_rgb = fs_rgb.astype(np.uint8)
    imageio.imsave('output.jpg', fs_rgb)
