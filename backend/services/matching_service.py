import logging
from pathlib import Path

import numpy as np

from backend.extensions import db
from backend.matching.embedding import save_embedding
from backend.matching.scoring import metadata_scores, weighted_score
from backend.matching.similarity import cosine_similarity
from backend.models.item import Item
from backend.models.match import Match
from backend.services.notification_service import create_notification

logger = logging.getLogger(__name__)


def load_or_generate_embedding(item, upload_folder):
    """Return the primary image's embedding, generating and caching it on first use."""
    image = item.images[0]
    embedding_path = Path(upload_folder) / (image.embedding_path or "")
    if image.embedding_path and embedding_path.exists():
        return np.load(embedding_path)

    source_path = Path(upload_folder) / image.image_path
    destination = source_path.with_suffix(".npy")
    save_embedding(source_path, destination)
    image.embedding_path = destination.name
    return np.load(destination)


def process_item_matches(item, upload_folder):
    if not item.images:
        return []

    try:
        source_vector = load_or_generate_embedding(item, upload_folder)
    except (OSError, ValueError) as error:
        logger.exception("Could not generate embedding for item %s: %s", item.id, error)
        return []

    opposite_type = "FOUND" if item.type == "LOST" else "LOST"
    candidates = db.session.scalars(
        db.select(Item).where(
            Item.type == opposite_type,
            Item.status == "ACTIVE",
            Item.category == item.category,
            Item.location == item.location,
            Item.id != item.id,
        )
    ).all()

    matches = []
    for candidate in candidates:
        if not candidate.images:
            continue
        try:
            candidate_vector = load_or_generate_embedding(candidate, upload_folder)
        except (OSError, ValueError) as error:
            logger.exception("Could not generate embedding for item %s: %s", candidate.id, error)
            continue

        image_score = (cosine_similarity(source_vector, candidate_vector) + 1) * 50
        scores = metadata_scores(item, candidate) if item.type == "LOST" else metadata_scores(candidate, item)
        lost, found = (item, candidate) if item.type == "LOST" else (candidate, item)

        existing = db.session.scalar(
            db.select(Match).where(Match.lost_item_id == lost.id, Match.found_item_id == found.id)
        )
        if existing:
            continue

        match = Match(
            lost_item_id=lost.id,
            found_item_id=found.id,
            image_similarity=round(image_score, 2),
            final_score=weighted_score(image_score, scores),
            **scores,
        )
        db.session.add(match)
        db.session.flush()
        create_notification(lost.user_id, "Possible match found", f"A potential match was found for {lost.name}.", "MATCH_FOUND", lost.id, match.id)
        create_notification(found.user_id, "Possible match found", f"A potential match was found for {found.name}.", "MATCH_FOUND", found.id, match.id)
        matches.append(match)
        logger.info("Match %s created for lost item %s and found item %s (score %.2f)", match.id, lost.id, found.id, match.final_score)

    db.session.commit()
    return matches
