import numpy as np
import pytest

from backend.matching.similarity import cosine_similarity


def test_cosine_similarity_identical_vectors_is_one():
    vector = np.array([1.0, 2.0, 3.0])
    assert cosine_similarity(vector, vector) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors_is_zero():
    assert cosine_similarity(np.array([1.0, 0.0]), np.array([0.0, 1.0])) == 0.0


def test_cosine_similarity_opposite_vectors_is_negative_one():
    assert cosine_similarity(np.array([1.0, 0.0]), np.array([-1.0, 0.0])) == -1.0


def test_cosine_similarity_handles_zero_vector_without_dividing_by_zero():
    assert cosine_similarity(np.zeros(3), np.array([1.0, 2.0, 3.0])) == 0.0
    assert cosine_similarity(np.zeros(3), np.zeros(3)) == 0.0
