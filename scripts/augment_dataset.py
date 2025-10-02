"""Augment dataset images using transformations inspired by the original 'base de données.py' script.

Usage:
    python scripts/augment_dataset.py --src data/train/90 --dst data/train/90_aug --n 40
"""
import argparse, random
from pathlib import Path
import numpy as np
import cv2
from PIL import Image

def bruit(image_orig):
    h, w, c = image_orig.shape
    n = np.random.randn(h, w, c) * random.randint(5, 30)
    return np.clip(image_orig + n, 0, 255).astype(np.uint8)

def change_gamma(image, alpha=1.0, beta=0.0):
    return np.clip(alpha * image + beta, 0, 255).astype(np.uint8)

def modif_img(img):
    img = img.copy()
    h, w, c = img.shape

    # replace a gray color by random color
    r_color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]
    img = np.where(img == [142, 142, 142], r_color, img).astype(np.uint8)

    if np.random.randint(3):
        k_max = 3
        kernel_blur = np.random.randint(k_max) * 2 + 1
        img = cv2.GaussianBlur(img, (kernel_blur, kernel_blur), 0)

    M = cv2.getRotationMatrix2D((int(w/2), int(h/2)), random.randint(-10, 10), 1)
    img = cv2.warpAffine(img, M, (w, h))

    if np.random.randint(2):
        a = int(max(w, h)/5) + 1
        pts1 = np.float32([[0,0],[w,0],[0,h],[w,h]])
        pts2 = np.float32([
            [0+random.randint(-a,a), 0+random.randint(-a,a)],
            [w-random.randint(-a,a), 0+random.randint(-a,a)],
            [0+random.randint(-a,a), h-random.randint(-a,a)],
            [w-random.randint(-a,a), h-random.randint(-a,a)]
        ])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, M, (w, h))

    if not np.random.randint(4):
        t = np.empty((h, w, c), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                for k in range(c):
                    t[i][j][k] = (i / h)
        M = cv2.getRotationMatrix2D((int(w/2), int(h/2)), np.random.randint(4)*90, 1)
        t = cv2.warpAffine(t, M, (w, h))
        img = (cv2.multiply((img/255).astype(np.float32), t) * 255).astype(np.uint8)

    img = change_gamma(img, random.uniform(0.6, 1.0), -np.random.randint(50))

    if not np.random.randint(4):
        p = (15 + np.random.randint(10)) / 100
        img = (img*p + 50*(1-p)).astype(np.uint8) + np.random.randint(100)

    img = bruit(img)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="source class folder with images")
    ap.add_argument("--dst", required=True, help="destination folder for augmented images")
    ap.add_argument("--n", type=int, default=40, help="number of augmented samples to generate")
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    dst.mkdir(parents=True, exist_ok=True)

    imgs = sorted([p for p in src.iterdir() if p.suffix.lower() in {'.png','.jpg','.jpeg','.bmp'}])
    if not imgs:
        raise SystemExit(f"No images in {src}")

    for i in range(args.n):
        base = cv2.imread(str(random.choice(imgs)))
        if base is None:
            continue
        out = modif_img(base)
        cv2.imwrite(str(dst / f"aug_{i:03d}.png"), out)
    print(f"Saved {args.n} images to {dst}")

if __name__ == "__main__":
    main()