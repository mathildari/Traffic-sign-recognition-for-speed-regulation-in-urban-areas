from typing import List
import numpy as np
import matplotlib.pyplot as plt

def read_image_to_array(path: str) -> np.ndarray:
    """Read an image with matplotlib (keeps compatibility with the original code)."""
    return plt.imread(path)

def image_array_to_rgb_list(img: np.ndarray) -> list:
    """Flatten HxWx3 into [R,G,B,...] list as in original scripts."""
    h, w = img.shape[0:2]
    out = []
    for l in range(h):
        for c in range(w):
            r,g,b = img[l][c][:3]
            out += [float(r), float(g), float(b)]
    return out

def image_paths_to_feature_matrix(paths: List[str]) -> list:
    return [image_array_to_rgb_list(read_image_to_array(p)) for p in paths]