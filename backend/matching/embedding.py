from pathlib import Path

import numpy as np
from PIL import Image


def generate_embedding(image_path):
    image = Image.open(image_path).convert("RGB").resize((32, 32))
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    channel_histograms = [np.histogram(pixels[:, :, channel], bins=16, range=(0, 1), density=True)[0] for channel in range(3)]
    vector = np.concatenate(channel_histograms).astype(np.float32)
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def save_embedding(image_path, embedding_path):
    Path(embedding_path).parent.mkdir(parents=True, exist_ok=True)
    np.save(embedding_path, generate_embedding(image_path))
    return embedding_path
