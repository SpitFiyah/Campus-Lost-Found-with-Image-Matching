# Image Matching Design

## What the embedding actually is

The matching service does **not** use a pretrained neural network. Each image is
resized to 32×32, its RGB channels are each reduced to a 16-bin normalized color
histogram, and the three histograms are concatenated and L2-normalized into a
single 48-dimensional vector (`backend/matching/embedding.py`). This is a classic
color-similarity descriptor, not a learned visual embedding — it captures the
overall color distribution of a photo, not its shape, texture, or the identity of
the object in it.

**Why this instead of a pretrained model:** it has no model download, no GPU
dependency, and no extra runtime library beyond Pillow and numpy already used
elsewhere in the project. It is fully explainable — a professor or reviewer can
compute it by hand — and fast enough to run synchronously inside a request. The
tradeoff is real: two different red backpacks will score highly similar, and the
same backpack photographed under very different lighting can score lower than
expected. That tradeoff is why image similarity is only 60% of the final score,
combined with metadata agreement (see below), and why a match is presented as a
lead, never as proof of ownership.

## Candidate retrieval and scoring

Candidate retrieval happens before image comparison: only active reports of the
opposite type, in the same category and campus location, are considered
(`backend/services/matching_service.py`). This keeps the comparison set small and
means `location_score` and `category_score` are effectively always 100 for any
match that gets created — they exist in the schema as a contract for a future,
looser candidate filter (e.g. same category but any location) without changing
the scoring shape.

Embeddings are cached: the first time an item's image is embedded, the vector is
saved next to the image and the path recorded on `ItemImage.embedding_path`, so
re-running matching against that item (as new opposite-type reports come in)
does not recompute it.

Cosine similarity compares two images' vectors because it measures the angle
between them, which is invariant to overall image brightness/scale — two photos
of the same color under different exposure still point in roughly the same
direction. Every component is normalized to 0-100. The final score is:

```text
final = image * 0.60 + location * 0.15 + category * 0.10
      + color * 0.10 + date * 0.05
```

`date_score` decays 10 points per day of difference between the two reports,
floored at 0. `color_score` is 100 if both reports specify the same color
(case-insensitive) and 40 otherwise (a color mismatch is weak evidence against a
match, not proof against it — colors are self-reported and imprecise).

## Limitations

- **Color, not shape.** Two visually distinct items of the same dominant color
  (a red backpack and a red jacket) can score similarly on the image component.
  This is why category and location must already match before two reports are
  compared at all.
- **Lighting and angle** shift the color histogram and can lower the score for
  genuinely matching photos.
- **Low-quality or heavily cropped photos** reduce histogram signal.
- **Multiple identical products** (e.g. two students losing the same
  mass-produced water bottle) will score highly against each other whether or
  not they're actually the same physical item — this is exactly why private
  verification details and human confirmation remain required before a return.
- A match is a candidate lead. The system never claims to confirm ownership.

## Evaluation

`tests/test_matching.py::test_matching_discriminates_similar_from_unrelated`
embeds three images — two near-identical blue squares and one solid red square —
and asserts the same-color pair scores higher via cosine similarity than either
scores against the unrelated color. This is a minimal same-item-vs-unrelated-item
check in the spirit of the evaluation this project should keep growing: as real
report photos accumulate, replace the synthetic fixtures with a small labeled set
of same/similar/unrelated item photos and track false-positive matches here.
