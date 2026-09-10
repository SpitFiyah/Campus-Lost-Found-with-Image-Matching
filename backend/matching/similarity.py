import numpy as np


def cosine_similarity(first, second):
    first = np.asarray(first, dtype=np.float32)
    second = np.asarray(second, dtype=np.float32)
    denominator = np.linalg.norm(first) * np.linalg.norm(second)
    if not denominator:
        return 0.0
    return float(np.clip(np.dot(first, second) / denominator, -1, 1))
