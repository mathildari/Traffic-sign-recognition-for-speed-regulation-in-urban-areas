"""
Fast, pure-numpy kNN using flattened RGB lists (keeps your original approach).
Exposes a simple classify(image_path, db_root, k) function.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def read_img(path: str) -> np.ndarray:
    return plt.imread(path)

def to_rgb_list(img: np.ndarray) -> np.ndarray:
    return img.reshape(-1, 3).astype(float)

def euclid(u: np.ndarray, v: np.ndarray) -> float:
    return np.sqrt(np.sum((u - v) ** 2))

def distances(u: np.ndarray, list_v: list) -> np.ndarray:
    arr = np.zeros((len(list_v), 2))
    for i, v in enumerate(list_v):
        arr[i] = [euclid(u, v), i]
    return arr

def k_nearest(u: np.ndarray, list_v: list, k: int) -> np.ndarray:
    d = distances(u, list_v)
    return d[np.argsort(d[:,0])][:k]

def load_db(db_root: str, folders=(0,1,2), per_folder=40):
    paths, labels = [], []
    db_root = Path(db_root)
    for d in folders:
        for n in range(per_folder):
            p = db_root / str(d) / f"{n}.bmp"
            paths.append(str(p))
            labels.append(d)
    imgs = [to_rgb_list(read_img(p)) for p in paths]
    return imgs, np.array(labels), paths

def majority(arr) -> int:
    uniq, counts = np.unique(arr, return_counts=True)
    return int(uniq[np.argmax(counts)])

def classify(image_path: str, db_root="/home/pi/TIPE/BDD", k=9, folders=(0,1,2), per_folder=40):
    u = to_rgb_list(read_img(image_path))
    imgs, labels, _ = load_db(db_root, folders, per_folder)
    idx = k_nearest(u, imgs, k)[:,1].astype(int)
    voted = majority(labels[idx])
    return voted