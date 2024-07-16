import numbers
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt

def normalize_alpha(alpha):
    """Normalize a raw attention weight or 
    class activation map.
    Args:
        alpha: numpy.ndarray, raw attn or cam.
    Returns:
        alpha: numpy.ndarray, normalized attn or cam.
    """
    ma, mi = alpha.max(), alpha.min()
    alpha = (alpha - mi) / (ma - mi)
    return alpha

def upsample_alpha(alpha, 
                   image_shape):
    """Upsample the raw attention weight or 
    class activation map, to be ready for visualization.
    Args:
        alpha: numpy.ndarray, raw attn or cam.
        image_shape: (w, h).
    Returns:
        alpha: numpy.ndarray, resized, unnormalized attn or cam.
    """
    # Resize to image shape 1st
    alpha = cv2.resize(alpha, image_shape)

    return alpha

def heatmap_overlay(img, 
                    alpha,
                    colormap=cv2.COLORMAP_JET,
                    ratio=0.5):
    """Overlay an attention weight or a
    class activation map onto an image.
    Args:
        img: image to overlay heatmap onto.
        alpha: numpy.ndarray, raw attn or cam.
        ratio: how transparent overlayed CAM looks over the image.
    Returns:
        vis: Overlayed image with colored attn or cam.
    """
    # Upsample 1st
    h, w = img.shape[:2]
    alpha = upsample_alpha(alpha, (w, h))

    # Normalization
    alpha = normalize_alpha(alpha)

    # Get binary mask and heatmap
    mask = np.uint8(255 * alpha)
    heatmap = cv2.applyColorMap(mask, colormap)

    # Overlay
    vis = ratio * np.float32(heatmap) + np.float32(img)
    vis = vis / np.max(vis)

    # Scale it back nicely
    vis = np.uint8(255 * vis)

    return vis

def gaussian(x: float, 
             y: float,
             resolution: Tuple[int, int],
             sigma: float = 3):
    """Generate a gaussian bumpy centered around specified (x, y).
    Sigma controls the magnitude of the gaussian bump.
    """
    # Sigma
    if isinstance(sigma, numbers.Number):
        sx, sy = (int(sigma), int(sigma))
    elif isinstance(sigma, (tuple, list)) and len(sigma) == 1:
        sx, sy = (sigma[0], sigma[0])
    elif isinstance(sigma, (tuple, list)) and len(sigma) == 2:
        sx, sy = (sigma[0], sigma[1])

    elif len(sigma) != 2:
        raise ValueError("Please provide only two dimensions (h, w) for size.")

    # Scale the gaze coordinates by image resolution 
    xo = int(x * resolution[1])
    yo = int(y * resolution[0])

    # Gaussian bump
    #M = np.zeros((resolution[0], resolution[1]), dtype=float)
    #for yi in range(resolution[0]):
    #    for xi in range(resolution[1]):
    #        M[yi, xi] = np.exp(-1.0 * ( ((xi - xo) ** 2 / (2 * sx*sx)) + ((yi - yo) ** 2 / (2 * sy*sy)) ) )

    # Vectorized gaussian bump
    # Create an index meshgrid
    Y, X = np.indices((resolution[0], resolution[1]))
    M = np.exp(-1.0 * ( ((X - xo) ** 2 / (2 * sx*sx)) + ((Y - yo) ** 2 / (2 * sy*sy)) ) )

    return M

if __name__ == "__main__":
    img = cv2.imread("desktop.png")
    x, y = (350, 800) # x, y
    h, w = img.shape[:2]

    # Give normalized coordinates
    x /= w
    y /= h

    # Can give a lower resolution gaze map and upsample it later
    resolution = (120, 120)
    M = gaussian(x, y, resolution=resolution, sigma=8)
    vis = heatmap_overlay(img, M)
    vis = cv2.cvtColor(vis, cv2.COLOR_BGR2RGB)
    plt.imshow(vis)
    plt.show()