from datetime import date

WEIGHTS = {"image_similarity": 0.60, "location_score": 0.15, "category_score": 0.10, "color_score": 0.10, "date_score": 0.05}


def metadata_scores(lost, found):
    days = abs((lost.date_lost_found - found.date_lost_found).days)
    return {"location_score": 100.0 if lost.location == found.location else 50.0, "category_score": 100.0 if lost.category.lower() == found.category.lower() else 0.0, "color_score": 100.0 if lost.color and found.color and lost.color.lower() == found.color.lower() else 40.0, "date_score": max(0.0, 100.0 - days * 10.0)}


def weighted_score(image_score, component_scores):
    values = {"image_similarity": max(0.0, min(100.0, image_score)), **component_scores}
    return round(sum(values[key] * weight for key, weight in WEIGHTS.items()), 2)
