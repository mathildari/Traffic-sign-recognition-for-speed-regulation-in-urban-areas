import os
from pathlib import Path
from typing import List, Tuple

def list_image_paths(dataset_dir: str, extensions={'.png','.jpg','.jpeg','.bmp'}) -> Tuple[list, list]:
    """Return (paths, labels) for images under dataset_dir, where each subfolder is a class label."""
    dataset_dir = Path(dataset_dir)
    paths, labels = [], []
    for cls_dir in sorted([p for p in dataset_dir.iterdir() if p.is_dir()]):
        label = cls_dir.name
        for p in sorted(cls_dir.rglob('*')):
            if p.suffix.lower() in extensions:
                paths.append(str(p))
                labels.append(label)
    return paths, labels

def ensure_dirs(*dirs: str) -> None:
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)