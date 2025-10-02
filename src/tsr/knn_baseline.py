"""Train/evaluate a kNN baseline for traffic sign recognition.

Usage:
    python -m tsr.knn_baseline --data data/train --k 5 --save models/knn.joblib
"""
import argparse
import numpy as np
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import joblib

from .dataset import list_image_paths
from .features import image_paths_to_feature_matrix

def exactitude(cm: np.ndarray) -> float:
    return np.trace(cm) / cm.sum() if cm.sum() else 0.0

def precision_per_class(cm: np.ndarray) -> list:
    denom = cm.sum(axis=0)
    return [ (cm[i,i] / denom[i]) if denom[i] else None for i in range(cm.shape[0]) ]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/train", help="dataset root with class subfolders")
    ap.add_argument("--k", type=int, default=5, help="k for kNN")
    ap.add_argument("--save", default="", help="optional path to save fitted model (joblib)")
    args = ap.parse_args()

    paths, labels = list_image_paths(args.data)
    if not paths:
        raise SystemExit(f"No images found in {args.data}. Expected structure: data/train/<class>/*.png")

    # Build features as in original code: raw RGB flatten
    X = np.array(image_paths_to_feature_matrix(paths), dtype=float)
    classes = sorted(sorted(set(labels)))
    y = np.array([classes.index(lbl) for lbl in labels], dtype=int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.25)

    clf = KNeighborsClassifier(n_neighbors=args.k)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_pred, labels=list(range(len(classes))))
    print("Classes:", classes)
    print("Confusion matrix:\n", cm)
    print("Accuracy (Exactitude):", exactitude(cm))
    print("Precision per class:", precision_per_class(cm))

    if args.save:
        joblib.dump({"model": clf, "classes": classes}, args.save)
        print("Saved model to", args.save)

if __name__ == "__main__":
    main()