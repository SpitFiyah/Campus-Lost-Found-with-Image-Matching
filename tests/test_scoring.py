from datetime import date
from types import SimpleNamespace

from backend.matching.scoring import metadata_scores, weighted_score


def item(location="Library", category="Bag", color="Blue", date_lost_found=date(2026, 8, 20)):
    return SimpleNamespace(location=location, category=category, color=color, date_lost_found=date_lost_found)


def test_metadata_scores_reward_exact_agreement():
    scores = metadata_scores(item(), item())
    assert scores == {"location_score": 100.0, "category_score": 100.0, "color_score": 100.0, "date_score": 100.0}


def test_metadata_scores_penalize_location_mismatch():
    scores = metadata_scores(item(location="Library"), item(location="Cafeteria"))
    assert scores["location_score"] == 50.0


def test_metadata_scores_penalize_category_mismatch():
    scores = metadata_scores(item(category="Bag"), item(category="Wallet"))
    assert scores["category_score"] == 0.0


def test_metadata_scores_category_match_is_case_insensitive():
    scores = metadata_scores(item(category="bag"), item(category="BAG"))
    assert scores["category_score"] == 100.0


def test_metadata_scores_penalize_color_mismatch():
    scores = metadata_scores(item(color="Blue"), item(color="Red"))
    assert scores["color_score"] == 40.0


def test_metadata_scores_missing_color_counts_as_mismatch():
    scores = metadata_scores(item(color=None), item(color="Red"))
    assert scores["color_score"] == 40.0


def test_metadata_scores_date_decays_and_floors_at_zero():
    scores = metadata_scores(item(date_lost_found=date(2026, 8, 20)), item(date_lost_found=date(2026, 8, 25)))
    assert scores["date_score"] == 50.0

    scores = metadata_scores(item(date_lost_found=date(2026, 8, 20)), item(date_lost_found=date(2026, 9, 20)))
    assert scores["date_score"] == 0.0


def test_weighted_score_combines_components_with_documented_weights():
    scores = {"location_score": 100.0, "category_score": 100.0, "color_score": 100.0, "date_score": 100.0}
    assert weighted_score(100.0, scores) == 100.0
    assert weighted_score(0.0, scores) == 40.0


def test_weighted_score_clamps_image_score_to_valid_range():
    scores = {"location_score": 0.0, "category_score": 0.0, "color_score": 0.0, "date_score": 0.0}
    assert weighted_score(150.0, scores) == 60.0
    assert weighted_score(-50.0, scores) == 0.0
