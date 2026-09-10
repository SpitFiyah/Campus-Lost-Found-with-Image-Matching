# Image Matching Design

The matching service will use an interchangeable embedding provider. The initial provider will preprocess an uploaded image, generate a vector with a locally runnable pretrained model, and save that vector beside the image. Cosine similarity compares vectors because it measures their direction while reducing sensitivity to overall image scale.

Candidate retrieval happens before image comparison: only active reports of the opposite type with compatible category and campus location are considered. A later vector index can replace this first database-backed candidate filter without changing the route or scoring contract.

Every component is normalized to 0-100. The initial score is:

```text
final = image * 0.60 + location * 0.15 + category * 0.10
      + color * 0.10 + date * 0.05
```

The output is a potential match, never proof of ownership. Ownership still requires private verification and human confirmation. Evaluation will compare known similar and unrelated image pairs and track false positives before the threshold is tuned.
