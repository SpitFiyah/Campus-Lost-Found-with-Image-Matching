from pathlib import Path

import numpy as np

from backend.extensions import db
from backend.matching.embedding import save_embedding
from backend.matching.scoring import metadata_scores, weighted_score
from backend.matching.similarity import cosine_similarity
from backend.models.item import Item
from backend.models.match import Match
from backend.services.notification_service import create_notification


def process_item_matches(item, upload_folder):
    if not item.images:
        return []
    source_path = Path(upload_folder) / item.images[0].image_path
    source_embedding_path = source_path.with_suffix(".npy")
    source_vector = save_embedding(source_path, source_embedding_path)
    source_vector = np.load(source_vector)
    opposite_type = "FOUND" if item.type == "LOST" else "LOST"
    candidates = db.session.scalars(db.select(Item).where(Item.type == opposite_type, Item.status == "ACTIVE", Item.category == item.category, Item.location == item.location, Item.id != item.id)).all()
    matches = []
    for candidate in candidates:
        if not candidate.images:
            continue
        candidate_path = Path(upload_folder) / candidate.images[0].image_path
        candidate_embedding_path = candidate_path.with_suffix(".npy")
        candidate_vector = np.load(save_embedding(candidate_path, candidate_embedding_path))
        image_score = (cosine_similarity(source_vector, candidate_vector) + 1) * 50
        scores = metadata_scores(item, candidate) if item.type == "LOST" else metadata_scores(candidate, item)
        lost, found = (item, candidate) if item.type == "LOST" else (candidate, item)
        match = Match.query.filter_by(lost_item_id=lost.id, found_item_id=found.id).first()
        if not match:
            match = Match(lost_item_id=lost.id, found_item_id=found.id, image_similarity=round(image_score, 2), final_score=weighted_score(image_score, scores), **scores)
            db.session.add(match)
            db.session.flush()
            create_notification(lost.user_id, "Possible match found", f"A potential match was found for {lost.name}.", "MATCH_FOUND", lost.id, match.id)
            create_notification(found.user_id, "Possible match found", f"A potential match was found for {found.name}.", "MATCH_FOUND", found.id, match.id)
            matches.append(match)
    db.session.commit()
    return matches
