import numpy as np


def channel_transform(rgb, params):
    rgb = rgb.astype(np.float32) / 255.0
    red_channel = rgb[:, :, 0]
    green_channel = rgb[:, :, 1]
    blue_channel = np.zeros_like(red_channel)  # Assume a yellow filter, so no blue channel at all
    ir_channel = rgb[:, :, 2]

    print("params:", params)

    fs_red_channel = (1.0 - (1.0 - red_channel) ** params.gammaRx) * params.fracRx + \
        (1.0 - (1.0 - ir_channel) ** params.gammaRy) * params.fracRy
    fs_green_channel = (1.0 - (1.0 - green_channel) ** params.gammaGx) * params.fracGx + \
        (1.0 - (1.0 - ir_channel) ** params.gammaGy) * params.fracGy
    fs_blue_channel = (1.0 - (1.0 - blue_channel) ** params.gammaBx) * params.fracBx + \
        (1.0 - (1.0 - ir_channel) ** params.gammaBy) * params.fracBy

    ir = 1.0 - (1.0 - fs_blue_channel / params.fracBy) ** (1.0 / params.gammaBy)

    fs_rgb = np.dstack((fs_blue_channel, fs_red_channel, fs_green_channel))
    return fs_rgb
